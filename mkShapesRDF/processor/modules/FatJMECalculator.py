import ROOT
import re

from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.JetMaker_cfg import JetMakerCfg

# CMS JERC/JMAR Run 3 recommendation: https://cms-jme-jmar.docs.cern.ch/recommendations/jet-reconstruction/
#  - AK8PFPuppi JEC/JER correct the ungroomed FatJet pt and mass.
#  - AK4PFPuppi JEC/JER must be applied to both soft-drop SubJets on MC;
#    the corrected groomed mass is their invariant mass (data: JEC only).
#
# FatJetVariationsCalculator.cc does NOT apply JER to the
# individual subjets, and uses the AK8 JES evaluator when shifting subjets.
# Following https://cms-jme-jmar.docs.cern.ch/recommendations/jet-mass/#soft-drop-mass
# This inclusdes an adapter thhat keeps the native AK8 calculator but
# recomputes the soft-drop mass using independent AK4 subjet corrections.

FATJET_SUBJET_JES_CPP = r'''
#ifndef MKSHAPES_FATJET_SUBJET_JES
#define MKSHAPES_FATJET_SUBJET_JES

// Existing CMS jet correction calculator
#include "FatJetVariationsCalculator.h"

#include <Math/GenVector/LorentzVector.h>
#include <Math/GenVector/PtEtaPhiM4D.h>
#include <algorithm>
#include <cmath>
#include <stdexcept>
#include <utility>
#include <cstdint>

class MkShapesFatJetVariationsCalculator : public FatJetVariationsCalculator {

  // Calculates AK4 subjet JER factors
  class SubJetSmearer : public JetMETVariationsCalculatorBase {
  public:
    void configure(const std::string& json, const std::string& tag, const std::string& algorithm, const std::string& smearJson, bool match) {
      auto corrections = correction::CorrectionSet::from_file(json);
      auto smearing = correction::CorrectionSet::from_file(smearJson);
      const auto suffix = "_" + algorithm;
      const auto uncertainty = tag + "_SFUncertainty" + suffix;
      const bool newFormat = hasCorrection(corrections, uncertainty);
      setSmearing(corrections->at(tag + "_PtResolution" + suffix), corrections->at(tag + "_ScaleFactor" + suffix), newFormat ? corrections->at(uncertainty) : nullptr, smearing->at("JERSmear"), false, newFormat, match, 0.2, 3.0);
      checkSmearingArguments();
    }
    
    // Evaluate the JER for one subjet https://cms-jme-jerc.docs.cern.ch/application/jer/#implementation, applyJERSmearing performs matching internally
    std::array<double, 3> factors(double pt, float eta, float phi, int genIdx, const p4compv_t& genpt, const p4compv_t& geneta, const p4compv_t& genphi, int seed, float rho) const {
        auto safePt = genpt;
        auto safeEta = geneta;
        auto safePhi = genphi;
    
        // Protect findGenMatch() from invalid indices.
        if (genIdx < 0 || genIdx >= int(genpt.size())) {
            genIdx = int(genpt.size());
            safePt.push_back(0.f);
            safeEta.push_back(1.e6f);
            safePhi.push_back(0.f);
        }
    
        return applyJERSmearing(m_jetPtRes, m_jerSmear, m_jetEResSF, m_jetEResSFUnc, m_smearDoGenMatch, pt, eta, phi, genIdx,safePt, safeEta, safePhi, seed, rho);
    }
  };

  // AK8 corrections while bypassing native subjet corrections
  class AK8OnlyCalculator : public FatJetVariationsCalculator {
  public:
    explicit AK8OnlyCalculator(FatJetVariationsCalculator base)
        : FatJetVariationsCalculator(std::move(base)) { m_doJECSubjet = false; } // Disable the parent's subjet correction
  };
  enum class Input {Area, Eta, Pt, Rho, Phi, Run};
  struct InputSpec {Input input; correction::Variable::VarType type;};
  using Schema = std::vector<InputSpec>;
  using LorentzVector = ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>>;

  Schema m_subjetJECInputs;
  std::map<std::string, Schema> m_subjetJESInputs;
  AK8OnlyCalculator m_ak8Only;
  SubJetSmearer m_subjetSmearer;
  bool m_smearSubjets = false;

  // Possible inputs from correctionlib json
  static Schema inputSchema(const std::vector<correction::Variable>& inputs) {
    const std::map<std::string, Input> known = {
      {"JetA", Input::Area}, {"JetEta", Input::Eta}, {"JetPt", Input::Pt}, {"Rho", Input::Rho}, {"JetPhi", Input::Phi}, {"run", Input::Run}
    };
    Schema result;
    for (const auto& variable : inputs) {
      const auto found = known.find(variable.name());
      if (found == known.end())
        throw std::invalid_argument("Unsupported SubJet correction input: " + variable.name());
      const auto type = variable.type();
      if (type != correction::Variable::VarType::real &&
          !(found->second == Input::Run && type == correction::Variable::VarType::integer))
        throw std::invalid_argument("Unsupported SubJet correction input type: " + variable.name());
      result.push_back({found->second, type});
    }
    return result;
  }

  // Building input vector
  static std::vector<correction::Variable::Type> inputValues(
      const Schema& schema, double eta, double pt, double phi, double rho, int run) {
    std::vector<correction::Variable::Type> values;
    for (const auto& variable : schema) {
      double value = 0.;
      switch (variable.input) {
        case Input::Area: value = 0.; break;
        case Input::Eta: value = eta; break;
        case Input::Pt: value = pt; break;
        case Input::Rho: value = rho; break;
        case Input::Phi: value = phi; break;
        case Input::Run: value = run; break;
      }
      if (variable.type == correction::Variable::VarType::integer)
        values.emplace_back(run);
      else
        values.emplace_back(value);
    }
    return values;
  }

  // Reconstruct the soft-drop mass. Per: https://cms-jme-jmar.docs.cern.ch/recommendations/jet-mass/#soft-drop-mass, 
  // "In NanoAOD, FatJet_subJetIdx1 and FatJet_subJetIdx2 index the two soft-drop subjets in the event's SubJet collection"
  static ROOT::RVecF groomedMass(const ROOT::RVec<Short_t>& first, const ROOT::RVec<Short_t>& second, const ROOT::RVec<double>& pt, const p4compv_t& eta, const p4compv_t& phi, const ROOT::RVec<double>& mass, const ROOT::RVec<double>& factors) {
    ROOT::RVecF result(first.size(), 0.);
    for (std::size_t jet = 0; jet < first.size(); ++jet) {
      if (first[jet] < 0 || second[jet] < 0 ||
          first[jet] >= int(pt.size()) || second[jet] >= int(pt.size())) continue;
      const auto i = first[jet], j = second[jet];
      // "Build each stored momentum from SubJet_pt, SubJet_eta, SubJet_phi, and SubJet_mass"
      const auto pair =
        LorentzVector(pt[i] * factors[i], eta[i], phi[i], mass[i] * factors[i]) +
        LorentzVector(pt[j] * factors[j], eta[j], phi[j], mass[j] * factors[j]);
      result[jet] = std::abs(pair.M());
    }
    return result;
  }

  static void setSoftDrop(result_t& result, std::size_t index, const ROOT::RVecF& mass) {
    auto pt = result.pt(index);
    auto ungroomed = result.mass(index);
    result.set(index, pt, ungroomed, mass);
  }

public:
  explicit MkShapesFatJetVariationsCalculator(FatJetVariationsCalculator base, const std::string& subjetJson = "", const std::string& subjetJER = "", const std::string& algorithm = "AK4PFPuppi", const std::string& smearJson = "", bool genMatch = true) : FatJetVariationsCalculator(base), m_ak8Only(std::move(base)) {
    if (!m_doJECSubjet) return;
    if (!subjetJER.empty()) {m_subjetSmearer.configure(subjetJson, subjetJER, algorithm, smearJson, genMatch);m_smearSubjets = true;}
    m_subjetJECInputs = std::visit([](const auto& corrector) {
      if (!corrector) throw std::invalid_argument("Missing SubJet JEC corrector");
      return inputSchema(corrector->inputs());
    }, m_jesSFSubjet);
    for (const auto& source : m_jesUncSources) {
      const auto corrector = m_jesUncSourcesSubjet.at(source.first);
      m_subjetJESInputs.emplace(source.first, inputSchema(corrector->inputs()));
    }
  }

  result_t produce(
      const p4compv_t& jet_pt, const p4compv_t& jet_eta, const p4compv_t& jet_phi,
      const p4compv_t& jet_mass, const p4compv_t& jet_rawcorr, const p4compv_t& jet_area,
      const p4compv_t& jet_msoftdrop, const ROOT::RVec<Short_t>& first, const ROOT::RVec<Short_t>& second,
      const p4compv_t& subpt, const p4compv_t& subeta, const p4compv_t& subphi,
      const p4compv_t& submass, const p4compv_t& subraw, const ROOT::RVec<Short_t>& subgenidx,
      const ROOT::RVec<UChar_t>& jet_id, float rho, const ROOT::RVec<Short_t>& genidx,
      int seed, int run, const p4compv_t& genpt, const p4compv_t& geneta,
      const p4compv_t& genphi, const p4compv_t& genmass,
      const p4compv_t& subgenpt = {}, const p4compv_t& subgeneta = {},
      const p4compv_t& subgenphi = {}) const {
      const auto n = subpt.size();
    
    // Just some check on the input lengths
    if (subeta.size() != n || subphi.size() != n || submass.size() != n || subraw.size() != n || (m_smearSubjets && !subgenidx.empty() && subgenidx.size() != n))
      throw std::invalid_argument("Unaligned SubJet inputs");
    
    if (first.size() != jet_pt.size() || second.size() != jet_pt.size())
      throw std::invalid_argument("Unaligned FatJet SubJet indices");
    
    if (subgeneta.size() != subgenpt.size() || subgenphi.size() != subgenpt.size())
      throw std::invalid_argument("Unaligned SubGenJetAK8 inputs");
    
    auto safeGenIdx = genidx;
    auto safeGenPt = genpt, safeGenEta = geneta, safeGenPhi = genphi, safeGenMass = genmass;
    
    if (m_doSmearing) {
      if (geneta.size() != genpt.size() || genphi.size() != genpt.size() ||
          genmass.size() != genpt.size() || genidx.size() != jet_pt.size())
        throw std::invalid_argument("Unaligned GenJetAK8 inputs");
      bool needsSentinel = false;
      for (auto& index : safeGenIdx)
        if (index < 0 || index >= int(genpt.size())) {
          index = int(genpt.size());
          needsSentinel = true;
        }
      if (needsSentinel) {
        safeGenPt.push_back(0.f); safeGenEta.push_back(1.e6f);
        safeGenPhi.push_back(0.f); safeGenMass.push_back(0.f);
      }
    }
    
    auto result = m_ak8Only.produce(
      jet_pt, jet_eta, jet_phi, jet_mass, jet_rawcorr, jet_area, jet_msoftdrop,
      first, second, subpt, subeta, subphi, submass, subraw, jet_id, rho,
      safeGenIdx, seed, run, safeGenPt, safeGenEta, safeGenPhi, safeGenMass);
    if (!m_doJECSubjet) return result;

    ROOT::RVec<double> pt(subpt), mass(submass);
    for (std::size_t i = 0; i < n; ++i) {
      const auto values = inputValues(
        m_subjetJECInputs, subeta[i], subpt[i] * (1. - subraw[i]), subphi[i], rho, run); 
      const double correction = std::visit([&](const auto& corrector) {
        return corrector->evaluate(values);
      }, m_jesSFSubjet);
      if (!std::isfinite(correction))
        throw std::runtime_error("Nonfinite SubJet JEC");
      if (correction > 0.) {
        const double factor = (1. - subraw[i]) * correction;
        pt[i] *= factor;
        mass[i] *= factor;
      }
    }

    // Scale each corrected SubJet four-vector with its own AK4 JER.
    ROOT::RVec<double> jerNom(n, 1.), jerUp(n, 1.), jerDown(n, 1.);
    if (m_smearSubjets) {
      for (std::size_t i = 0; i < n; ++i) {
        const int subjetSeed = seed + i + 1; 
        const int genIdx = i < subgenidx.size() ? int(subgenidx[i]) : -1;
        const auto factors = m_subjetSmearer.factors(
            pt[i], subeta[i], subphi[i], genIdx, subgenpt, subgeneta, subgenphi, subjetSeed, rho);
        for (auto factor : factors)
          if (!std::isfinite(factor) || factor < 0.)
            throw std::runtime_error("Invalid SubJet JER factor");
        jerNom[i] = factors[0]; jerUp[i] = factors[1]; jerDown[i] = factors[2];
      }
    }
    const auto nominal = groomedMass(first, second, pt, subeta, subphi, mass, jerNom);
    const auto labels = available("msoftdrop");
    if (labels.size() != result.size() || labels.size() != result.sizeM())
      throw std::runtime_error("Unsupported FatJet backend result layout");
    std::vector<bool> replaced(labels.size(), false);
    for (std::size_t i = 0; i < labels.size(); ++i)
      if (labels[i] == "nominal") {
        setSoftDrop(result, i, nominal);
        replaced[i] = true;
      } else if (labels[i] == "jerup" || labels[i] == "jerdown") {
        setSoftDrop(result, i, groomedMass(first, second, pt, subeta, subphi,
            mass, labels[i] == "jerup" ? jerUp : jerDown));
        replaced[i] = true;
      }

    for (const auto& source : m_jesUncSourcesSubjet) {
      ROOT::RVec<double> up(jerNom), down(jerNom);
      for (std::size_t i = 0; i < n; ++i) {
        const auto delta = source.second->evaluate(inputValues(
          m_subjetJESInputs.at(source.first), subeta[i], pt[i] * jerNom[i], subphi[i], rho, run));
        up[i] *= 1. + delta;
        down[i] *= 1. - delta;
      }
      for (const auto& direction : {std::string("up"), std::string("down")}) {
        const auto label = "jes" + source.first + direction;
        const auto index = std::find(labels.begin(), labels.end(), label);
        if (index == labels.end()) throw std::runtime_error("Missing FatJet variation: " + label);
        const auto position = std::distance(labels.begin(), index);
        setSoftDrop(result, position, groomedMass(
          first, second, pt, subeta, subphi, mass, direction == "up" ? up : down));
        replaced[position] = true;
      }
    }
    if (std::find(replaced.begin(), replaced.end(), false) != replaced.end())
      throw std::runtime_error("Unsupported FatJet soft-drop variation label");
    return result;
  }
};
#endif
'''

class FatJMECalculator(Module):
    """
    This module calculates the JES/JER for AK8 jets and stores the nominal values and the variations (up/down) in the output tree.
    """
    def __init__(
            self, 
            jet_object="AK8PFPuppi", 
            jes_unc=("Total",), 
            year="", 
            do_JER=True,     
            store_nominal=True, 
            store_variations=True, 
            isMC=True, 
            sampleName="",
            jer_variation_name="jer"
    ):
        """
        FatJMECalculator module

        Parameters:
        ----------
        jet_object : str, default: ``"AK8PFPuppi"``
            Jet collection to correct. 
        jes_unc : tuple, default: ``("Total",)``
            JES uncertainty sources to evaluate
        year : str
            Campaign identifier used to retrieve JEC/JER configurations 
        do_JER : bool, default: ``True``
            Whether to apply JER smearing to FatJets and subjets in MC.
        store_nominal : bool, optional, default: ``True``
            Whether to store the nominal values (corrected or smeared)
        store_variations : bool, optional
            Whether to store the variations (up/down) for JES/JER
        isMC : bool, optional, default: ``True``
            Whether the processed sample is simulation
        sampleName : str,
            Sample name used to resolve DATA JEC 
        jer_variation_name : str, optional, default: ``"jer"``
            Name assigned to the JER systematic variation.
        """
        super().__init__("FatJMECalculator")
        self.jet_object = jet_object
        self.jes_unc = jes_unc
        self.year = year
        self.do_JER = do_JER and isMC # Making sure JER corrections only apply to MC
        self.store_nominal = store_nominal
        self.store_variations = store_variations and isMC
        self.isMC = isMC
        self.sampleName = sampleName
        self.keep_original_order = "TTTo2L2Nu_10k_nano" in sampleName
        self.jer_variation_name = jer_variation_name
        if self.jet_object != "AK8PFPuppi":
            raise ValueError("Run 3 FatJets require AK8PFPuppi")
        self.runPeriods = [k for k in JetMakerCfg[self.year] if str(k).isdigit()] or None

    def runModule(self, df, values):
        from CMSJMECalculators import loadJMESystematicsCalculators
        loadJMESystematicsCalculators()
        ROOT.gInterpreter.Declare(FATJET_SUBJET_JES_CPP)

        periods = self.runPeriods if self.runPeriods else [None]

        for period in periods:
            cfg = JetMakerCfg[self.year][period] if period is not None else JetMakerCfg[self.year]
            ak4 = cfg["jet"]
            fat = cfg["fat_jet"]

            jsonFile       = fat["fatjet_jerc"]
            subjetJson     = ak4["jet_jerc"]
            jetAlgo        = self.jet_object
            subjetAlgo     = fat["subjet_algorithm"]
            jecTag         = cfg["JEC" if self.isMC else "JEC_data"]
            jerTag         = cfg["JER"] if self.do_JER else ""
            subjetJER      = cfg.get("subjet_JER", jerTag) if self.do_JER else ""
            smearJson      = cfg["jer_smear"] if self.do_JER else ""
            smearingTool   = "JERSmear" if self.do_JER else ""
            jecLevel       = "L1L2L3Res"
            year = cfg["year"] if self.runPeriods else (self.year if "FullRunIII" not in self.year else "Full2024v15").split("Full")[1].split("v")[0]
            jesUnc = [source.replace("YEAR", year) for source in self.jes_unc] if self.store_variations else []
            jesUnc_cpp = "std::vector<std::string>{" + ",".join(f'"{x}"' for x in jesUnc) + "}"            

            print(f"AK8 final JEC tag: {jecTag}")

            # DATA JEC tags for 2022EE and 2023 pre-BPix.
            if not self.isMC and isinstance(jecTag, list):
                if len(jecTag) == 3:
                    for i, era in enumerate("EFG"):
                        if f"Run2022{era}" in self.sampleName:
                            jecTag = jecTag[i]
                            break
                elif len(jecTag) == 2:
                    if any(v in self.sampleName for v in ["v1", "v2", "v3"]):
                        jecTag = jecTag[0]
                    elif "v4" in self.sampleName:
                        jecTag = jecTag[1]

            if not isinstance(jecTag, str):
                raise ValueError(f"Unresolved DATA JEC tag for {self.sampleName}")

            subjetTag = cfg.get("subjet_JEC", jecTag)

            # AK8 JEC/JER and AK4 subjet corrections for the soft-drop mass.
            name = f"myFatJetVariationsCalculator_{period}" if period is not None else "myFatJetVariationsCalculator"
            
            ROOT.gInterpreter.Declare(
                f'MkShapesFatJetVariationsCalculator {name} = MkShapesFatJetVariationsCalculator(FatJetVariationsCalculator::create("{jsonFile}", "{jetAlgo}", "{jecTag}", "{jecLevel}", {jesUnc_cpp}, false, "{jerTag}", "{smearJson}", "{smearingTool}", false, true, 0.4, 3.0, "{subjetJson}", "{subjetAlgo}", "{subjetTag}", "{jecLevel}"), "{subjetJson}", "{subjetJER}", "{subjetAlgo}", "{smearJson}", true);'
            )

        # Same source extraction and ordering as JMECalculator.py.
        if self.runPeriods:
            calc = getattr(ROOT, f"myFatJetVariationsCalculator_{self.runPeriods[0]}")
            sources = calc.available()[1:][::2]
            sources = [str(source).removesuffix("up") for source in sources]
            sources = [source.replace(str(JetMakerCfg[self.year][self.runPeriods[0]]["year"]), "YEAR") for source in sources]
        else:
            calc = getattr(ROOT, "myFatJetVariationsCalculator")
            sources = calc.available()[1:][::2]
            sources = [str(source).removesuffix("up") for source in sources]

        print("FatJet JES/JER sources:", sources)

        cols = []
        colsWithType = []

        FatJetColl = "CorrectedFatJet"

        # FatJet collection
        cols.append("FatJet_pt")
        cols.append("FatJet_eta")
        cols.append("FatJet_phi")
        cols.append("FatJet_mass")
        cols.append("FatJet_rawFactor")
        cols.append("FatJet_area")
        cols.append("FatJet_msoftdrop")
        cols.append("FatJet_subJetIdx1")
        cols.append("FatJet_subJetIdx2")

        colsWithType.append("ROOT::RVecF FatJet_pt")
        colsWithType.append("ROOT::RVecF FatJet_eta")
        colsWithType.append("ROOT::RVecF FatJet_phi")
        colsWithType.append("ROOT::RVecF FatJet_mass")
        colsWithType.append("ROOT::RVecF FatJet_rawFactor")
        colsWithType.append("ROOT::RVecF FatJet_area")
        colsWithType.append("ROOT::RVecF FatJet_msoftdrop")
        colsWithType.append("ROOT::RVec<Short_t> FatJet_subJetIdx1")
        colsWithType.append("ROOT::RVec<Short_t> FatJet_subJetIdx2")

        # SubJet collection
        cols.append("SubJet_pt")
        cols.append("SubJet_eta")
        cols.append("SubJet_phi")
        cols.append("SubJet_mass")
        cols.append("SubJet_rawFactor")
        cols.append("SubJet_subGenJetAK8Idx" if self.do_JER and "v15" in self.year else "ROOT::RVec<Short_t>{}")
        cols.append("FatJet_jetId")
        cols.append("Rho_fixedGridRhoFastjetAll")

        colsWithType.append("ROOT::RVecF SubJet_pt")
        colsWithType.append("ROOT::RVecF SubJet_eta")
        colsWithType.append("ROOT::RVecF SubJet_phi")
        colsWithType.append("ROOT::RVecF SubJet_mass")
        colsWithType.append("ROOT::RVecF SubJet_rawFactor")
        colsWithType.append("ROOT::RVec<Short_t> SubJet_subGenJetAK8Idx")
        colsWithType.append("ROOT::RVec<UChar_t> FatJet_jetId")
        colsWithType.append("float Rho_fixedGridRhoFastjetAll")

        if self.do_JER:
            df = df.Define("tmp_fatjet_seed", "int(((ULong64_t(run)<<20) + (ULong64_t(luminosityBlock)<<10) + ULong64_t(event)) & 0x7fffffffULL)")

            cols.append("FatJet_genJetAK8Idx")
            cols.append("tmp_fatjet_seed")
            cols.append("run")
            cols.append("GenJetAK8_pt")
            cols.append("GenJetAK8_eta")
            cols.append("GenJetAK8_phi")
            cols.append("GenJetAK8_mass")
            cols.append("SubGenJetAK8_pt")
            cols.append("SubGenJetAK8_eta")
            cols.append("SubGenJetAK8_phi")
        else:
            cols.append("ROOT::RVec<Short_t>{}") # FatJet_genJetAK8Idx
            cols.append("0")
            cols.append("run")
            cols.append("ROOT::RVecF{}") # GenJetAK8_pt
            cols.append("ROOT::RVecF{}") # GenJetAK8_eta
            cols.append("ROOT::RVecF{}") # GenJetAK8_phi
            cols.append("ROOT::RVecF{}") # GenJetAK8_mass
            cols.append("ROOT::RVecF{}") # SubGenJetAK8_pt
            cols.append("ROOT::RVecF{}") # SubGenJetAK8_eta
            cols.append("ROOT::RVecF{}") # SubGenJetAK8_phi

        colsWithType.append("ROOT::RVec<Short_t> FatJet_genJetAK8Idx")
        colsWithType.append("int seed")
        colsWithType.append("int run")
        colsWithType.append("ROOT::RVecF GenJetAK8_pt")
        colsWithType.append("ROOT::RVecF GenJetAK8_eta")
        colsWithType.append("ROOT::RVecF GenJetAK8_phi")
        colsWithType.append("ROOT::RVecF GenJetAK8_mass")
        colsWithType.append("ROOT::RVecF SubGenJetAK8_pt")
        colsWithType.append("ROOT::RVecF SubGenJetAK8_eta")
        colsWithType.append("ROOT::RVecF SubGenJetAK8_phi")

        # Create a function to handle corrections per run period
        produceCols = [x.rsplit(" ", 1)[-1] for x in colsWithType]

        text_per_run = ""
        if self.runPeriods:
            for runP in self.runPeriods:
                text_per_run += f"""
                    if (runPeriod == {runP}) {{
                        return myFatJetVariationsCalculator_{runP}.produce({", ".join(produceCols)});
                    }}
                """

            ROOT.gInterpreter.Declare(
                """
                MkShapesFatJetVariationsCalculator::result_t getPerRunFatJets(int runPeriod, """ + ", ".join(colsWithType) + """) {
                    """ + text_per_run + """
                    throw std::runtime_error("Unknown FatJet run period");
                }
                """
            )

        if self.runPeriods:
            df = df.Define("fatjetVars", f'getPerRunFatJets(run_period, {", ".join(cols)})', excludeVariations=["*"])
        else:
            df = df.Define("fatjetVars", f'myFatJetVariationsCalculator.produce({", ".join(cols)})', excludeVariations=["*"])

        # Nominal corrected FatJet collections
        nominal_pt = "fatjetVars.pt(0)" if self.store_nominal else "FatJet_pt"

        if self.keep_original_order:
            df = df.Define("CorrectedFatJet_sorting", "ROOT::VecOps::Range(FatJet_pt.size())", excludeVariations=["*"])
        else:
            df = df.Define("CorrectedFatJet_sorting", f"ROOT::VecOps::Reverse(ROOT::VecOps::Argsort({nominal_pt}))", excludeVariations=["*"])

        for prop in ("pt", "eta", "phi", "mass", "msoftdrop"):
            value = f"fatjetVars.{prop}(0)" if self.store_nominal and prop in ("pt", "mass", "msoftdrop") else f"FatJet_{prop}"
            df = df.Define(f"CorrectedFatJet_{prop}", f"Take({value}, CorrectedFatJet_sorting)", excludeVariations=["*"])

        df = df.Define("CorrectedFatJet_jetIdx", "CorrectedFatJet_sorting", excludeVariations=["*"])

        if self.store_variations:
            for i, source in enumerate(sources):
                variation = self.jer_variation_name if source == "jer" else source
                indices = [str(2*i+1+j) for j in range(2)]

                # Sort FatJets according to the varied pt
                orders = []
                for tag, index in zip(("up", "down"), indices):
                    if self.keep_original_order:
                        orders.append("CorrectedFatJet_sorting")
                    else:
                        name = f"fatjet_sort_{source}_{tag}"
                        df = df.Define(name, f"ROOT::VecOps::Reverse(ROOT::VecOps::Argsort(fatjetVars.pt({index})))", excludeVariations=["*"])
                        orders.append(name)

                # Store JES/JER variations
                for prop in ("pt", "mass", "msoftdrop", "eta", "phi", "jetIdx"):
                    varied = []
                    for index, order in zip(indices, orders):
                        if prop in ("pt", "mass", "msoftdrop"):
                            varied.append(f"Take(fatjetVars.{prop}({index}), {order})")
                        elif prop == "jetIdx":
                            varied.append(order) 
                        else:
                            varied.append(f"Take(FatJet_{prop}, {order})")

                    rvec = "std::size_t" if prop == "jetIdx" else "float"
                    df = df.Vary(f"CorrectedFatJet_{prop}", f"ROOT::RVec<ROOT::RVec<{rvec}>>{{{varied[0]}, {varied[1]}}}", ["up", "do"], variation)

        df = df.Define("nCorrectedFatJet", "int(CorrectedFatJet_pt.size())")
        df= df.DropColumns("fatjetVars").DropColumns("fatjet_sort_*").DropColumns("CorrectedFatJet_sorting")

        return df

