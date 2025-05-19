import ROOT

from mkShapesRDF.processor.data.LeptonSel_cfg import LepFilter_dict, ElectronWP, MuonWP
from mkShapesRDF.processor.framework.module import Module


class LeptonSel(Module):
    def __init__(self, LepFilter, nLF, era, filter=True):
        super().__init__("LeptonSel")
        self.era = era
        self.LepFilter = LepFilter
        self.nLF = nLF
        self.filter = filter

    def runModule(self, df, values):
        Clean_Tag = LepFilter_dict[self.LepFilter]
        Clean_TagWP = LepFilter_dict[Clean_Tag]

        ROOT.gInterpreter.Declare(
            """
        using namespace ROOT;
        using namespace ROOT::VecOps;

        ROOT::RVecB reduce_cond_any(ROOT::RVecB condition, uint size1, uint size2){
            ROOT::RVecB r;
            for (uint i = 0; i < size1; i++){
                bool c = false;
                for (uint j = 0; j < size2; j++){
                    if (condition[i * size2 + j]){
                        c = true;
                        break;
                    }
                }
                r.push_back(c);
            }
            return r;
        }

        RVecB propagateMask(RVecI Lepton_origIdx, RVecB mask, bool defaultValue){
        RVecB r {};

            for (uint i = 0; i < Lepton_origIdx.size(); i++){
                if (Lepton_origIdx[i] < 0){
                    r.push_back(defaultValue);
                } else {
                    r.push_back(mask[Lepton_origIdx[i]]);
                }
            }
            assert (Lepton_origIdx.size() == r.size());
            return r;
        /*
        does not work, why?
        RVecB r(Lepton_origIdx.size(), defaultValue);
        r[Lepton_origIdx >= 0] = Take(mask, Lepton_origIdx[Lepton_origIdx >= 0]);
        return r;
        */
        }
        """
        )
        values.append(
            [
                df.Define("test", "Lepton_pt.size()").Sum("test"),
                "Original size of leptons",
            ]
        )

        columnsToDrop = []
        df = df.Redefine("comb", "ROOT::RVecB(Electron_pt.size(), true)")
        columnsToDrop.append("comb")
        df = df.Define("tmp1", "true")
        columnsToDrop.append("tmp1")
        df = df.Define("tmp2", "true")
        columnsToDrop.append("tmp2")


        ### Electron veto
        for key, cuts in ElectronWP[self.era][Clean_TagWP]["HLTsafe"]["cuts"].items():
            df = df.Redefine("tmp1", key)
            df = df.Redefine("tmp2", "(" + cuts[0] + ")")
            for cut in cuts[1:]:
                df = df.Redefine("tmp2", "tmp2 && (" + cut + ")")
            #df = df.Redefine("comb", "comb && !(tmp1 && !tmp2)")
            df = df.Redefine("comb", "comb && (! tmp1 || tmp2)")
                
        df = df.Define("LeptonMaskHyg_Ele", "propagateMask(Lepton_electronIdx, comb, true)")
        columnsToDrop.append("LeptonMaskHyg_Ele")

        
        ### Muon veto
        df = df.Redefine("comb", "ROOT::RVecB(Muon_pt.size(), true)")

        for key, cuts in MuonWP[self.era][Clean_TagWP]["HLTsafe"]["cuts"].items():
            df = df.Redefine("tmp1", key)
            df = df.Redefine("tmp2", "(" + cuts[0] + ")")
            for cut in cuts[1:]:
                df = df.Redefine("tmp2", "tmp2 && (" + cut + ")")
            #df = df.Redefine("comb", "comb && !(tmp1 && !tmp2)")
            df = df.Redefine("comb", "comb && (! tmp1 || tmp2)")

        df = df.Define("LeptonMaskHyg_Mu", "propagateMask(Lepton_muonIdx, comb, true)")
        columnsToDrop.append("LeptonMaskHyg_Mu")


        if Clean_TagWP=="FakeObjWP":
            df = df.Define("isLoose", "LeptonMaskHyg_Mu || LeptonMaskHyg_Ele")
        else:
            df = df.Redefine("comb", "ROOT::RVecB(Electron_pt.size(), true)")
            for key, cuts in ElectronWP[self.era]["FakeObjWP"]["HLTsafe"]["cuts"].items():
                df = df.Redefine("tmp1", key)
                df = df.Redefine("tmp2", "(" + cuts[0] + ")")
                for cut in cuts[1:]:
                    df = df.Redefine("tmp2", "tmp2 && (" + cut + ")")
                #df = df.Redefine("comb", "comb && !(tmp1 && !tmp2)")
                df = df.Redefine("comb", "comb && (! tmp1 || tmp2)")

            df = df.Define("isLoose_Ele", "propagateMask(Lepton_electronIdx, comb, false)")

            df = df.Redefine("comb", "ROOT::RVecB(Muon_pt.size(), true)")

            for key, cuts in MuonWP[self.era]["FakeObjWP"]["HLTsafe"]["cuts"].items():
                df = df.Redefine("tmp1", key)
                df = df.Redefine("tmp2", "(" + cuts[0] + ")")
                for cut in cuts[1:]:
                    df = df.Redefine("tmp2", "tmp2 && (" + cut + ")")
                #df = df.Redefine("comb", "comb && !(tmp1 && !tmp2)")
                df = df.Redefine("comb", "comb && (! tmp1 || tmp2)")

            df = df.Define("isLoose_Mu", "propagateMask(Lepton_muonIdx, comb, false)")
            df = df.Define("isLoose", "isLoose_Ele || isLoose_Mu")

            columnsToDrop.append("isLoose_Ele")
            columnsToDrop.append("isLoose_Mu")


        ### Electrons
        
        for ids in ElectronWP[self.era]['TightObjWP'].keys():
            
            df = df.Redefine("comb", "ROOT::RVecB(Electron_pt.size(), true)")

            for key, cuts in list(ElectronWP[self.era]['TightObjWP'][ids]['cuts'].items()):
                df = df.Redefine("tmp1", key)
                df = df.Redefine("tmp2", "(" + cuts[0] + ")")
                for cut in cuts[1:]:
                    df = df.Redefine("tmp2", "tmp2 && (" + cut + ")")
                #df = df.Redefine("comb", "comb && !( tmp1 && !tmp2)")
                df = df.Redefine("comb", "comb && (! tmp1 || tmp2)")
                
            df = df.Define("Lepton_isTightElectron_"+ids, "propagateMask(Lepton_electronIdx, comb, false)")
            

        ### Muons

        for ids in MuonWP[self.era]['TightObjWP'].keys():

            df = df.Redefine("comb", "ROOT::RVecB(Muon_pt.size(), true)")
            
            for key, cuts in list(MuonWP[self.era]['TightObjWP'][ids]['cuts'].items()):
                df = df.Redefine("tmp1", key)
                df = df.Redefine("tmp2", "(" + cuts[0] + ")")
                for cut in cuts[1:]:
                    df = df.Redefine("tmp2", "tmp2 && (" + cut + ")")
                #df = df.Redefine("comb", "comb && !( tmp1 && !tmp2)")
                df = df.Redefine("comb", "comb && (! tmp1 || tmp2)")

            df = df.Define("Lepton_isTightMuon_"+ids, "propagateMask(Lepton_muonIdx, comb, false)")



        df = df.Define("LeptonMask_minPt", "Lepton_pt > 8")
        columnsToDrop.append("LeptonMask_minPt")
        df = df.Define(
            "LeptonMask_minPt_pass",
            "LeptonMask_minPt && LeptonMaskHyg_Ele && LeptonMaskHyg_Mu",
        )
        columnsToDrop.append("LeptonMask_minPt_pass")


        # TODO add VetoLeptons and dmZll
        if self.filter:
            df = df.Filter("Lepton_pt[LeptonMask_minPt_pass].size() >= 1")

        values.append(
            [
                df.Define("test", "Lepton_pt[LeptonMask_minPt_pass].size()").Sum(
                    "test"
                ),
                "Size of leptons passing hyg mask and minPt",
            ]
        )

        # this LeptonMask is used for leptons inside Jet cones
        df = df.Define(
            "LeptonMask_JC",
            "LeptonMaskHyg_Ele && LeptonMaskHyg_Mu && (Lepton_pt >= 10)",
        )
        columnsToDrop.append("LeptonMask_JC")

        df = df.Define("CleanJetMask", "CleanJet_eta <= 5.0")
        columnsToDrop.append("CleanJetMask")

        df = df.Define(
            "CleanJet_Lepton_comb",
            "ROOT::VecOps::Combinations(CleanJet_pt[CleanJetMask].size(), Lepton_pt[LeptonMask_JC].size())",
        )
        columnsToDrop.append("CleanJet_Lepton_comb")

        df = df.Define(
            "dR2",
            "ROOT::VecOps::DeltaR2( \
            Take(CleanJet_eta, CleanJet_Lepton_comb[0]), \
            Take(Lepton_eta, CleanJet_Lepton_comb[1]), \
            Take(CleanJet_phi, CleanJet_Lepton_comb[0]), \
            Take(Lepton_phi, CleanJet_Lepton_comb[1]) \
        )",
        )
        columnsToDrop.append("dR2")

        df = df.Define(
            "CleanJet_pass",
            "! reduce_cond_any(dR2<(0.3*0.3), CleanJet_pt[CleanJetMask].size(), Lepton_pt[LeptonMask_JC].size())",
        )
        columnsToDrop.append("CleanJet_pass")

        branches = ["pt", "eta", "phi", "pdgId", "electronIdx", "muonIdx"]
        for prop in branches:
            df = df.Redefine(
                f"Lepton_{prop}",
                f"Lepton_{prop}[LeptonMaskHyg_Ele && LeptonMaskHyg_Mu]",
            )

        branches = ["jetIdx", "pt", "eta", "phi", "mass"]
        for prop in branches:
            df = df.Redefine(
                f"CleanJet_{prop}", f"CleanJet_{prop}[CleanJetMask][CleanJet_pass]"
            )

        for col in columnsToDrop:
            df = df.DropColumns(col)

        return df
