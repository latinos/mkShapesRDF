import ROOT
from mkShapesRDF.processor.framework.module import Module


class FatJetSelMask(Module):
    def __init__(self, jetId=2, minPt=200., maxEta=2.4, lepton_min_pt=10., DeltaRlep=0.8):
        super().__init__("FatJetSelMask")
        self.jetId = jetId
        self.minPt = minPt
        self.maxEta = maxEta
        self.lepton_min_pt = lepton_min_pt
        self.DeltaRlep = DeltaRlep

    def runModule(self, df, values):
        if not hasattr(ROOT, "reduce_cond_any"):
            ROOT.gInterpreter.Declare(r"""
            ROOT::RVecB reduce_cond_any(ROOT::RVecB condition, size_t size1, size_t size2) {
                ROOT::RVecB r;
                for (size_t i = 0; i < size1; i++) {
                    bool c = false;
                    for (size_t j = 0; j < size2; j++) {
                        if (condition[i * size2 + j]) {
                            c = true; break;
                        }
                    }
                    r.push_back(c);
                }
                return r;
            }
            """)

        df = df.Define("LeptonMask_FJC", f"Lepton_pt >= {self.lepton_min_pt}")
        df = df.Define("FatJet_Lepton_comb", "ROOT::VecOps::Combinations(CorrectedFatJet_pt.size(), Lepton_pt[LeptonMask_FJC].size())")

        df = df.Define("FatJet_dR2", """
            ROOT::VecOps::DeltaR2(
                Take(CorrectedFatJet_eta, FatJet_Lepton_comb[0]),
                Take(Lepton_eta[LeptonMask_FJC], FatJet_Lepton_comb[1]),
                Take(CorrectedFatJet_phi, FatJet_Lepton_comb[0]),
                Take(Lepton_phi[LeptonMask_FJC], FatJet_Lepton_comb[1])
            )
        """)

        df = df.Define("CleanFatJet_geometrical", f"!reduce_cond_any(FatJet_dR2 < ({self.DeltaRlep}*{self.DeltaRlep}), CorrectedFatJet_pt.size(), Lepton_pt[LeptonMask_FJC].size())")
        df = df.Define("fatjetIdCut", f"((Take(FatJet_jetId, CorrectedFatJet_jetIdx) & {self.jetId}) == {self.jetId})")
        df = df.Define("CleanFatJetMask", f"(CorrectedFatJet_pt >= {self.minPt} && abs(CorrectedFatJet_eta) <= {self.maxEta} && fatjetIdCut && CleanFatJet_geometrical)")

        values.append([df.Define("_fatjet_before", "int(CorrectedFatJet_pt.size())").Sum("_fatjet_before"), "Original size of CorrectedFatJet"])

        df = df.Define("CleanFatJet_jetIdx", "CorrectedFatJet_jetIdx[CleanFatJetMask]")
        df = df.Define("CleanFatJet_correctedjetIdx", "ROOT::VecOps::Range(CorrectedFatJet_pt.size())[CleanFatJetMask]")

        for prop in ("pt", "eta", "phi", "mass", "msoftdrop"):
            df = df.Define(f"CleanFatJet_{prop}", f"CorrectedFatJet_{prop}[CleanFatJetMask]")

        df = df.Define("nCleanFatJet", "int(CleanFatJet_pt.size())")

        values.append([df.Define("_fatjet_after", "int(CleanFatJet_pt.size())").Sum("_fatjet_after"), "Final size of CleanFatJet"])

        for col in ("LeptonMask_FJC", "FatJet_Lepton_comb", "FatJet_dR2", "CleanFatJet_geometrical", "fatjetIdCut"):
            df = df.DropColumns(col)

        df = df.DropColumns("CleanFatJetMask")

        return df
