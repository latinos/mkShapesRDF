from mkShapesRDF.processor.framework.module import Module
import ROOT

class l2KinProducer(Module):
    def __init__(self):
        super().__init__("l2KinProducer")

    def runModule(self, df, values):
        df = df.Define(
            "Lepton_4DV",
            "ROOT::VecOps::Construct<ROOT::Math::PtEtaPhiMVector>"
            "(Lepton_pt, Lepton_eta, Lepton_phi, "
            "ROOT::RVecF(Lepton_pt.size(), 0))",
        )

        df = df.Define(
            "CleanJet_4DV",
            "ROOT::VecOps::Construct<ROOT::Math::PtEtaPhiMVector>"
            "(CleanJet_pt, CleanJet_eta, CleanJet_phi,"
            # "Take(Jet_mass, CleanJet_jetIdx))",
            "CleanJet_mass)",
        )

        df = df.Define(
            "MET_4DV", "ROOT::Math::PtEtaPhiMVector" "(PuppiMET_pt, 0, PuppiMET_phi, 0)"
        )

        df = df.Define(
            "TkMET_4DV", "ROOT::Math::PtEtaPhiMVector" "(TkMET_pt, 0, TkMET_phi, 0)"
        )

        df = df.Define(
            "_isOk",
            "Lepton_pt[Lepton_pt > 0].size() >= 2 && MET_4DV.E()>0",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            "_isOk3l",
            "Lepton_pt[Lepton_pt > 0].size() >= 3 && MET_4DV.E()>0",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define("_lepOk", "Lepton_pt[Lepton_pt > 0].size()")
        df = df.Define("_tkMetOk", "TkMET_4DV.E() > 0")
        df = df.Define("_jetOk", "CleanJet_pt[CleanJet_pt > 0].size()")


        # FIXME complete l2kin module!

        # Variables yet to be implemented:
        ##############################
        # 'mT2',

        # Additional supporting variables
        #################################

        # Needed for mcoll
        df = df.Define(
            "Lepton_enhanced_0",
            "_isOk ? ROOT::Math::PtEtaPhiMVector(Lepton_pt[0] + MET_4DV.Pt() * cos( abs( DeltaPhi( Lepton_4DV[0].Phi(),MET_4DV.Phi() ) ) ), Lepton_eta[0], Lepton_phi[0], 0.) : ROOT::Math::PtEtaPhiMVector(0., 0., 0., 0.)"
        )
        df = df.Define(
            "Lepton_enhanced_1",
            "_isOk ? ROOT::Math::PtEtaPhiMVector(Lepton_pt[1] + MET_4DV.Pt() * cos( abs( DeltaPhi( Lepton_4DV[1].Phi(),MET_4DV.Phi() ) ) ), Lepton_eta[1], Lepton_phi[1], 0.) : ROOT::Math::PtEtaPhiMVector(0., 0., 0., 0.)"
        )

        # Needed for mcollWW
        df = df.Define(
            "Lepton_enhanced_WW_0",
            "_isOk ? ROOT::Math::PtEtaPhiMVector(Lepton_pt[0] + MET_4DV.Pt() * cos( abs( DeltaPhi( Lepton_4DV[0].Phi(),MET_4DV.Phi() ) ) ), Lepton_eta[0], Lepton_phi[0], 80.385) : ROOT::Math::PtEtaPhiMVector(0., 0., 0., 0.)"
        )
        df = df.Define(
            "Lepton_enhanced_WW_1",
            "_isOk ? ROOT::Math::PtEtaPhiMVector(Lepton_pt[1] + MET_4DV.Pt() * cos( abs( DeltaPhi( Lepton_4DV[1].Phi(),MET_4DV.Phi() ) ) ), Lepton_eta[1], Lepton_phi[1], 80.385) : ROOT::Math::PtEtaPhiMVector(0., 0., 0., 0.)"
        )

        # Needed for mTe
        df = df.Define(
            "Lepton_enhanced_mTe_0",
            "_isOk ? ROOT::Math::PtEtaPhiMVector(Lepton_pt[0], Lepton_eta[0], Lepton_phi[0], 80.385) : ROOT::Math::PtEtaPhiMVector(0., 0., 0., 0.)"
        )
        df = df.Define(
            "Lepton_enhanced_mTe_1",
            "_isOk ? ROOT::Math::PtEtaPhiMVector(Lepton_pt[1], Lepton_eta[1], Lepton_phi[1], 80.385) : ROOT::Math::PtEtaPhiMVector(0., 0., 0., 0.)"
        )
        
        # Needed for mllWgSt or drllWgSt
        df = df.Define(
            "mll12",
            "_isOk && (Lepton_pdgId[0] / Lepton_pdgId[1]) == -1 ? (Lepton_4DV[0] + Lepton_4DV[1]).M() : -9999.0"
        )
        df = df.Define(
            "mll13",
            "_isOk3l && (Lepton_pdgId[0] / Lepton_pdgId[2]) == -1 ? (Lepton_4DV[0] + Lepton_4DV[2]).M() : -9999.0"
        )
        df = df.Define(
            "mll23",
            "_isOk3l && (Lepton_pdgId[1] / Lepton_pdgId[2]) == -1 ? (Lepton_4DV[1] + Lepton_4DV[2]).M() : -9999.0"
        )
        
        df = df.Define(
            "drll12",
            "_isOk ? DeltaR(Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1]) : -9999.0",
        )
        df = df.Define(
            "drll13",
            "_isOk3l ? DeltaR(Lepton_eta[0], Lepton_eta[2], Lepton_phi[0], Lepton_phi[2]) : -9999.0",
        )
        df = df.Define(
            "drll23",
            "_isOk3l ? DeltaR(Lepton_eta[1], Lepton_eta[2], Lepton_phi[1], Lepton_phi[2]) : -9999.0",
        )

        # Needed for upara and uperp
        df = df.Define(
            "utv",
            "_isOk ? -MET_4DV- Lepton_4DV[0] - Lepton_4DV[1] : ROOT::Math::PtEtaPhiMVector(0., 0., 0., 0.)",
        )
        

        # Dilepton variables
        prefix = ""

        df = df.Define(
            prefix + "mll", "_isOk ? (Lepton_4DV[0] + Lepton_4DV[1]).M() : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )
        df = df.Define(
            prefix + "dphill",
            "_isOk ? DeltaPhi(Lepton_phi[0], Lepton_phi[1]) : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )
        df = df.Define(
            prefix + "yll",
            "_isOk ? (Lepton_4DV[0] + Lepton_4DV[1]).Rapidity() : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )
        df = df.Define(
            prefix + "ptll", "_isOk ? (Lepton_4DV[0] + Lepton_4DV[1]).Pt() : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )
        df = df.Define(
            prefix + "dphillmet",
            "_isOk ? abs(DeltaPhi((Lepton_4DV[0] + Lepton_4DV[1]).Phi(),MET_4DV.Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "mth",
            "_isOk ? sqrt(2. * {0}ptll * MET_4DV.Pt() * (1. - cos({0}dphillmet))) : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "mTi",
            "_isOk ? (Lepton_4DV[0] + Lepton_4DV[1] + MET_4DV).M() : -9999.0",
        )
        df = df.Define(
            prefix + "mR",
            "_isOk ? sqrt(0.5*({0}mll*{0}mll - MET_4DV.Pt()*{0}ptll*cos({0}dphillmet) + sqrt(({0}mll*{0}mll + {0}ptll*{0}ptll)*({0}mll*{0}mll + MET_4DV.Pt()*MET_4DV.Pt())))) : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "drll",
            "_isOk ? DeltaR(Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1]) : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )
        df = df.Define(
            prefix + "detall", "_isOk ? abs(Lepton_eta[0] - Lepton_eta[1]) : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )
        df = df.Define(
            prefix + "dphilmet",
            "_isOk ? abs(DeltaPhi(Lepton_4DV[0].Phi(), MET_4DV.Phi())) < abs(DeltaPhi(Lepton_4DV[1].Phi(), MET_4DV.Phi())) ? abs(DeltaPhi(Lepton_4DV[0].Phi(), MET_4DV.Phi())) : abs(DeltaPhi(Lepton_4DV[1].Phi(), MET_4DV.Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphilmet1",
            "Lepton_4DV[0].Pt() > 0 && MET_4DV.E() > 0 ? abs(DeltaPhi(Lepton_4DV[0].Phi(), MET_4DV.Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphilmet2",
            "_isOk ? abs(DeltaPhi(Lepton_4DV[1].Phi(), MET_4DV.Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "mtw1",
            "Lepton_4DV[0].Pt() > 0 && MET_4DV.E() > 0 ? sqrt(2. * Lepton_4DV[0].Pt() * MET_4DV.Pt() * (1. - cos({0}dphilmet1))) : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "mtw2",
            "_isOk ? sqrt(2. * Lepton_4DV[1].Pt() * MET_4DV.Pt() * (1. - cos({0}dphilmet2))) : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "projpfmet",
            "_isOk ? {0}dphilmet < 0.5*TMath::Pi() ? sin({0}dphilmet) * MET_4DV.Pt() : MET_4DV.Pt() : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "dphil1tkmet",
            "_isOk && _tkMetOk ? abs(DeltaPhi(Lepton_4DV[0].Phi(), TkMET_4DV.Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphil2tkmet",
            "_isOk && _tkMetOk ? abs(DeltaPhi(Lepton_4DV[1].Phi(), TkMET_4DV.Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphiltkmet",
            "_isOk && _tkMetOk ? min({0}dphil1tkmet, {0}dphil2tkmet) : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "projtkmet",
            "_isOk && _tkMetOk ? {0}dphiltkmet < 0.5*TMath::Pi() ? sin({0}dphiltkmet) * TkMET_4DV.Pt() : TkMET_4DV.Pt() : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "projtkmet",
            "_isOk && _tkMetOk ? min({0}projtkmet, {0}projpfmet) : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "pTWW",
            "_isOk ? (Lepton_4DV[0] + Lepton_4DV[1] + MET_4DV).Pt() : -9999.0",
        )
        df = df.Define(
            prefix + "pTHjj",
            "_isOk && _jetOk>=2 ? (Lepton_4DV[0] + Lepton_4DV[1] + CleanJet_4DV[0] + CleanJet_4DV[1] + MET_4DV).Pt() : -9999.0",
        )
        df = df.Define(
            prefix + "recoil",
            "_isOk ? abs((Lepton_4DV[0] + Lepton_4DV[1] + MET_4DV).Pt()) : -9999.0",
        )
        df = df.Define(
            prefix + "mcoll", "_isOk ? (Lepton_enhanced_0 + Lepton_enhanced_1).M() : -9999.0"
        )
        df = df.Define(
            prefix + "mcollWW", "_isOk ? (Lepton_enhanced_WW_0 + Lepton_enhanced_WW_1).M() : -9999.0"
        )
        df = df.Define(
            prefix + "mTe", "_isOk ? (Lepton_enhanced_mTe_0 + Lepton_enhanced_mTe_1 + MET_4DV).M() : -9999.0"
        )
        df = df.Define(
            prefix + "choiMass", "_isOk ? sqrt( 2*(Lepton_4DV[0].Pt()*Lepton_4DV[0].Pt()) + 2*(Lepton_4DV[1].Pt()*Lepton_4DV[1].Pt()) + 3*(Lepton_4DV[0].Pt()*Lepton_4DV[1].Pt() + (MET_4DV.Pt())*(Lepton_4DV[0].Pt()+Lepton_4DV[1].Pt()) - MET_4DV.Pt()*ptll*cos(dphilmet)) - 2*(Lepton_4DV[1].Pt()*Lepton_4DV[1].Pt()*cos(dphill)) ) : -9999.0"
        )
        df = df.Define(
            prefix + "channel", "_isOk ? (abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11) ? 1 : (abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 13) ? 2 : (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 11) ? 3 : (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13) ? 0 : -9999.0 : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "mllWgSt", "_isOk3l ? mll12 >= 0 && mll13 <  0 && mll23 <  0 ? mll12 :\
                                           mll12 <  0 && mll13 >= 0 && mll23 <  0 ? mll13 : \
                                           mll12 <  0 && mll13 <  0 && mll23 >= 0 ? mll23 : \
                                           mll12 >= 0 && mll13 >= 0 && mll23 <  0 && mll12 <  mll13 ? mll12 : \
                                           mll12 >= 0 && mll13 >= 0 && mll23 <  0 && mll12 >= mll13 ? mll13 : \
                                           mll12 >= 0 && mll13 <  0 && mll23 >= 0 && mll12 <  mll23 ? mll12 : \
                                           mll12 >= 0 && mll13 <  0 && mll23 >= 0 && mll12 >= mll23 ? mll23 : \
                                           mll12 <  0 && mll13 >= 0 && mll23 >= 0 && mll13 <  mll23 ? mll13 : \
                                           mll12 <  0 && mll13 >= 0 && mll23 >= 0 && mll13 >= mll23 ? mll23 : \
                                           mll12 >= 0 && mll13 >= 0 && mll23 >= 0 && mll12 <  mll13 && mll12 <  mll23 ? mll12 : \
                                           mll12 >= 0 && mll13 >= 0 && mll23 >= 0 && mll13 <  mll12 && mll13 <  mll23 ? mll13 : \
                                           mll12 >= 0 && mll13 >= 0 && mll23 >= 0 && mll23 <  mll12 && mll23 <  mll13 ? mll23 : \
                                           -9999.0 : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "drllWgSt", "_isOk3l ? mll12 >= 0 && mll13 <  0 && mll23 <  0 ? drll12 : \
                                            mll12 <  0 && mll13 >= 0 && mll23 <  0 ? drll13 : \
                                            mll12 <  0 && mll13 <  0 && mll23 >= 0 ? drll23 : \
                                            mll12 >= 0 && mll13 >= 0 && mll23 <  0 && mll12 <  mll13 ? drll12 : \
                                            mll12 >= 0 && mll13 >= 0 && mll23 <  0 && mll12 >= mll13 ? drll13 : \
                                            mll12 >= 0 && mll13 <  0 && mll23 >= 0 && mll12 <  mll23 ? drll12 : \
                                            mll12 >= 0 && mll13 <  0 && mll23 >= 0 && mll12 >= mll23 ? drll23 : \
                                            mll12 <  0 && mll13 >= 0 && mll23 >= 0 && mll13 <  mll23 ? drll13 : \
                                            mll12 <  0 && mll13 >= 0 && mll23 >= 0 && mll13 >= mll23 ? drll23 : \
                                            mll12 >= 0 && mll13 >= 0 && mll23 >= 0 && mll12 <  mll13 && mll12 <  mll23 ? drll12 : \
                                            mll12 >= 0 && mll13 >= 0 && mll23 >= 0 && mll13 <  mll12 && mll13 <  mll23 ? drll13 : \
                                            mll12 >= 0 && mll13 >= 0 && mll23 >= 0 && mll23 <  mll12 && mll23 <  mll13 ? drll23 : \
                                            -9999.0 : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "mllThird", "_isOk3l && Lepton_4DV[2].Pt() > 2 ? mll13 >= 0 && mll23 >= 0 && mll23 <  mll13 ? mll23 : \
                                                                      mll13 >= 0 && mll23 >= 0 && mll23 >= mll13 ? mll13 : \
                                                                      mll13 >= 0 && mll23 <  0 ? mll13 : \
                                                                      mll13 <  0 && mll23 >= 0 ? mll23 : \
                                                                      -9999.0: -9999.0",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "mllOneThree", "_isOk3l && Lepton_4DV[2].Pt() > 2 ? mll13 : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )
        df = df.Define(
            prefix + "mllTwoThree", "_isOk3l && Lepton_4DV[2].Pt() > 2 ? mll23 : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )
        df = df.Define(
            prefix + "drllOneThree", "_isOk3l && Lepton_4DV[2].Pt() > 2 ? drll13 : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )
        df = df.Define(
            prefix + "drllTwoThree", "_isOk3l && Lepton_4DV[2].Pt() > 2 ? drll23 : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )
        df = df.Define(
            prefix + "upara", "_isOk ? utv.P() * cos(DeltaPhi(utv.Phi(), (Lepton_4DV[0] + Lepton_4DV[1]).Phi() )) : -9999.0"
        )
        df = df.Define(
            prefix + "uperp", "_isOk ? utv.P() * sin(DeltaPhi(utv.Phi(), (Lepton_4DV[0] + Lepton_4DV[1]).Phi() )) : -9999.0"
        )

        df = df.Define(prefix + "pt1", "Lepton_pt[0] > 0 ? Lepton_pt[0] : -9999.0")
        df = df.Define(prefix + "eta1", "Lepton_pt[0] > 0 ? Lepton_eta[0] : -9999.0")
        df = df.Define(prefix + "phi1", "Lepton_pt[0] > 0 ? Lepton_phi[0] : -9999.0")
        df = df.Define(prefix + "pt2", "_isOk ? Lepton_pt[1] : -9999.0")
        df = df.Define(prefix + "eta2", "_isOk ? Lepton_eta[1] : -9999.0")
        df = df.Define(prefix + "phi2", "_isOk ? Lepton_phi[1] : -9999.0")

        # Lepton(s)-Jet(s) variables
        df = df.Define(
            prefix + "dphilljet",
            "_isOk && _jetOk>=1 ? abs(DeltaPhi((Lepton_4DV[0] + Lepton_4DV[1]).Phi(), CleanJet_4DV[0].Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphilljetjet",
            "_isOk && _jetOk>=2 ? abs(DeltaPhi((Lepton_4DV[0] + Lepton_4DV[1]).Phi(), (CleanJet_4DV[0] + CleanJet_4DV[1]).Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphilljetjet_cut",
            "_isOk && _jetOk>=2 && CleanJet_4DV[0].Pt()>15.0 && CleanJet_4DV[1].Pt()>15.0 ? abs(DeltaPhi((Lepton_4DV[0] + Lepton_4DV[1]).Phi(), (CleanJet_4DV[0] + CleanJet_4DV[1]).Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphijet1met",
            "_isOk && _jetOk>=1 ? abs(DeltaPhi(CleanJet_4DV[0].Phi(), MET_4DV.Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphijet2met",
            "_isOk && _jetOk>=2 ? abs(DeltaPhi(CleanJet_4DV[1].Phi(), MET_4DV.Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphilep1jet1",
            "_isOk && _jetOk>=1 ? abs(DeltaPhi(Lepton_4DV[0].Phi(), CleanJet_4DV[0].Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphilep1jet2",
            "_isOk && _jetOk>=2 ? abs(DeltaPhi(Lepton_4DV[0].Phi(), CleanJet_4DV[1].Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphilep2jet1",
            "_isOk && _jetOk>=1 ? abs(DeltaPhi(Lepton_4DV[1].Phi(), CleanJet_4DV[0].Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphilep2jet2",
            "_isOk && _jetOk>=2 ? abs(DeltaPhi(Lepton_4DV[1].Phi(), CleanJet_4DV[1].Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "detaj1l1",
            "_isOk && _jetOk>=1 ? abs(CleanJet_eta[0] - Lepton_eta[0]) : -9999.0",
        )
        df = df.Define(
            prefix + "detaj1l2",
            "_isOk && _jetOk>=1 ? abs(CleanJet_eta[0] - Lepton_eta[1]) : -9999.0",
        )
        df = df.Define(
            prefix + "detaj2l1",
            "_isOk && _jetOk>=2 ? abs(CleanJet_eta[1] - Lepton_eta[0]) : -9999.0",
        )
        df = df.Define(
            prefix + "detaj2l2",
            "_isOk && _jetOk>=2 ? abs(CleanJet_eta[1] - Lepton_eta[1]) : -9999.0",
        )
        df = df.Define(
            prefix + "mindetajl",
            "_isOk && _jetOk>=2 ? min({0}detaj1l1, min({0}detaj1l2, min({0}detaj2l1, {0}detaj2l2))) : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "dphilep1jj",
            "_isOk && _jetOk>=2 ? abs(DeltaPhi( Lepton_4DV[0].Phi(), (CleanJet_4DV[0] + CleanJet_4DV[1]).Phi() ) ) : -9999.0",
        )
        df = df.Define(
            prefix + "dphilep2jj",
            "_isOk && _jetOk>=2 ? abs(DeltaPhi(Lepton_4DV[1].Phi(), (CleanJet_4DV[0] + CleanJet_4DV[1]).Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "maxdphilepjj",
            "_isOk && _jetOk>=2 ? max({0}dphilep1jj, {0}dphilep2jj) : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "dphilljet_cut",
            "_isOk && _jetOk>=1 && CleanJet_4DV[0].Pt()>15.0 ? abs(DeltaPhi((Lepton_4DV[0] + Lepton_4DV[1]).Phi(), CleanJet_4DV[0].Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphijet1met_cut",
            "_isOk && _jetOk>=1 && CleanJet_4DV[0].Pt()>15.0 ? abs(DeltaPhi(CleanJet_4DV[0].Phi(), MET_4DV.Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphijet2met_cut",
            "_isOk && _jetOk>=2 && CleanJet_4DV[1].Pt()>15.0 ? abs(DeltaPhi(CleanJet_4DV[1].Phi(), MET_4DV.Phi())) : -9999.0",
        )

        df = df.Define(
            prefix + "WlepMt_whss",
            "_isOk ? _jetOk>=2 && {0}dphilep1jj   >  {0}dphilep2jj   ? sqrt( 2 * Lepton_4DV[0].Pt() * MET_4DV.Pt() * (1 - cos({0}dphilmet1) ) ) : \
                     _jetOk>=2 && {0}dphilep1jj   <= {0}dphilep2jj   ? sqrt( 2 * Lepton_4DV[1].Pt() * MET_4DV.Pt() * (1 - cos({0}dphilmet2) ) ) : \
                     _jetOk==1 && {0}dphilep1jet1 >  {0}dphilep2jet1 ? sqrt( 2 * Lepton_4DV[0].Pt() * MET_4DV.Pt() * (1 - cos({0}dphilmet1) ) ) : \
                     _jetOk==1 && {0}dphilep1jet1 <= {0}dphilep2jet1 ? sqrt( 2 * Lepton_4DV[1].Pt() * MET_4DV.Pt() * (1 - cos({0}dphilmet2) ) ) : \
            -9999.0 : -9999.0".format(prefix),
        )


        # dijets variables
        df = df.Define(
            prefix + "njet",
            "CleanJet_pt [CleanJet_pt > 30 && CleanJet_eta < 4.7].size()",
        )
        df = df.Define(
            prefix + "ptjj",
            "_jetOk >=2 ? (CleanJet_4DV[0] + CleanJet_4DV[1]).Pt() : -9999.0",
        )
        df = df.Define(
            prefix + "mjj",
            "_jetOk >=2 ? (CleanJet_4DV[0] + CleanJet_4DV[1]).M() : -9999.0",
        )
        df = df.Define(
            prefix + "dphijj",
            "_jetOk >= 2 ? DeltaPhi(CleanJet_phi[0], CleanJet_phi[1]) : -9999.0",
        )
        df = df.Define(
            prefix + "drjj",
            "_jetOk >= 2 ? DeltaR(CleanJet_eta[0], CleanJet_eta[1], CleanJet_phi[0], CleanJet_phi[1]) : -9999.0",
        )
        df = df.Define(
            prefix + "detajj",
            "_jetOk >=2 ? abs(CleanJet_eta[0] - CleanJet_eta[1]) : -9999.0",
        )
        df = df.Define(
            prefix + "dphijjmet",
            "_isOk && _jetOk>=2 ? abs(DeltaPhi((CleanJet_4DV[0] + CleanJet_4DV[1]).Phi(),MET_4DV.Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "dphijjmet_cut",
            "_isOk && _jetOk>=2 && CleanJet_4DV[0].Pt()>15.0 && CleanJet_4DV[1].Pt()>15.0 ? abs(DeltaPhi((CleanJet_4DV[0] + CleanJet_4DV[1]).Phi(),MET_4DV.Phi())) : -9999.0",
        )
        df = df.Define(
            prefix + "jetpt1_cut",
            "_isOk && _jetOk>=1 && CleanJet_4DV[0].Pt()>15.0 ? CleanJet_4DV[0].Pt() : -9999.0",
        )
        df = df.Define(
            prefix + "jetpt2_cut",
            "_isOk && _jetOk>=2 && CleanJet_4DV[0].Pt()>15.0 && CleanJet_4DV[1].Pt()>15.0 ? CleanJet_4DV[1].Pt() : -9999.0",
        )
        df = df.Define(
            prefix + "m2ljj20",
            "_isOk && _jetOk>=1 && CleanJet_4DV[0].Pt()>30.0 ? CleanJet_4DV[1].Pt()>20.0 ? (Lepton_4DV[0] + Lepton_4DV[1] + CleanJet_4DV[0] + CleanJet_4DV[1]).M() : (Lepton_4DV[0] + Lepton_4DV[1] + CleanJet_4DV[0]).M() : -9999.0",
        )
        df = df.Define(
            prefix + "m2ljj30",
            "_isOk && _jetOk>=1 && CleanJet_4DV[0].Pt()>30.0 ? CleanJet_4DV[1].Pt()>30.0 ? (Lepton_4DV[0] + Lepton_4DV[1] + CleanJet_4DV[0] + CleanJet_4DV[1]).M() : (Lepton_4DV[0] + Lepton_4DV[1] + CleanJet_4DV[0]).M() : -9999.0",
        )
        df = df.Define(
            prefix + "ht",
            "_isOk ? Sum(Lepton_pt[Lepton_pt>0]) + Sum(CleanJet_pt[CleanJet_pt>30]) + MET_4DV.Pt() : -9999.0",
        )
        df = df.Define(
            prefix + "PfMetDivSumMet",
            "_isOk && PuppiMET_sumEt>0.0  ? MET_4DV.Pt() / sqrt(PuppiMET_sumEt) : -9999.0",
        )

        ROOT.gInterpreter.Declare("""
        ROOT::Math::PtEtaPhiMVector Get_vht(ROOT::RVecF lep_pt, ROOT::RVecF lep_eta, ROOT::RVecF lep_phi, ROOT::RVecF jet_pt, ROOT::RVecF jet_eta, ROOT::RVecF jet_phi){
            ROOT::Math::PtEtaPhiMVector vector_sum(0.,0.,0.,0.);
            for (uint i = 0; i < lep_pt.size(); i++){
                if (lep_pt[i] < 10) break;
                ROOT::Math::PtEtaPhiMVector lepp4(lep_pt[i], lep_eta[i], lep_phi[i], 0);
                vector_sum += lepp4;
            }
            for (uint i = 0; i < jet_pt.size(); i++){
                if (jet_pt[i] < 30) break;
                ROOT::Math::PtEtaPhiMVector jetp4(jet_pt[i], jet_eta[i], jet_phi[i], 0);
                vector_sum += jetp4;
            }
        return vector_sum;
        }
        """)

        df = df.Define(
            prefix + "vht_pt",
            "_isOk ? (Get_vht(Lepton_pt, Lepton_eta, Lepton_phi, CleanJet_pt, CleanJet_eta, CleanJet_phi)).Pt() : -9999.0",
        )
        # df = df.Define(
        #     prefix + "vht_phi",
        #     "_isOk ? (Get_vht(Lepton_pt, Lepton_eta, Lepton_phi, CleanJet_pt, CleanJet_eta, CleanJet_phi)).Phi() : -9999.0",
        # )

        # For VBF training
        df = df.Define(
            prefix + "ptTOT_cut",
            "_isOk && _jetOk>=2 && CleanJet_4DV[0].Pt()>15.0 && CleanJet_4DV[1].Pt()>15.0 ? (Lepton_4DV[0] + Lepton_4DV[1] + CleanJet_4DV[0] + CleanJet_4DV[1] + MET_4DV).Pt() : -9999.0",
        )
        df = df.Define(
            prefix + "mTOT_cut",
            "_isOk && _jetOk>=2 && CleanJet_4DV[0].Pt()>15.0 && CleanJet_4DV[1].Pt()>15.0 ? (Lepton_4DV[0] + Lepton_4DV[1] + CleanJet_4DV[0] + CleanJet_4DV[1] + MET_4DV).M() : -9999.0",
        )
        df = df.Define(
            prefix + "OLV1_cut",
            "_isOk && _jetOk>=2 && CleanJet_4DV[0].Pt()>15.0 && CleanJet_4DV[1].Pt()>15.0 ? 2*(Lepton_4DV[0].Eta() - 0.5*((CleanJet_4DV[0] + CleanJet_4DV[1]).Eta())) / ((CleanJet_4DV[0] - CleanJet_4DV[1]).Eta()) : -9999.0",
        )
        df = df.Define(
            prefix + "OLV2_cut",
            "_isOk && _jetOk>=2 && CleanJet_4DV[0].Pt()>15.0 && CleanJet_4DV[1].Pt()>15.0 ? 2*(Lepton_4DV[1].Eta() - 0.5*((CleanJet_4DV[0] + CleanJet_4DV[1]).Eta())) / ((CleanJet_4DV[0] - CleanJet_4DV[1]).Eta()) : -9999.0",
        )
        df = df.Define(
            prefix + "Ceta_cut",
            "_isOk && _jetOk>=2 && CleanJet_4DV[0].Pt()>15.0 && CleanJet_4DV[1].Pt()>15.0 ? {0}OLV1_cut + {0}OLV2_cut : -9999.0".format(
                prefix
            ),
        )

        # WHSS
        df = df.Define( # auxiliary variable
            prefix + "mlljj20_whss_jet2",
            "_isOk && _jetOk>=1 && CleanJet_4DV[0].Pt()>30.0 && CleanJet_4DV[1].Pt()>20.0 ? {0}dphilep1jj <= {0}dphilep2jj ? (Lepton_4DV[0] + Lepton_4DV[0] + CleanJet_4DV[0] + CleanJet_4DV[1]).M() : (Lepton_4DV[1] + Lepton_4DV[1] + CleanJet_4DV[0] + CleanJet_4DV[1]).M() : -9999.0".format(
                prefix
            ),
        )
        df = df.Define( # auxiliary variable
            prefix + "mlljj20_whss_no_jet2",
            "_isOk && _jetOk>=1 && CleanJet_4DV[0].Pt()>30.0 && CleanJet_4DV[1].Pt()<=20.0 ? {0}dphilep1jj <= {0}dphilep2jj ? (Lepton_4DV[0] + Lepton_4DV[0] + CleanJet_4DV[0]).M() : (Lepton_4DV[1] + Lepton_4DV[1] + CleanJet_4DV[0]).M() : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "mlljj20_whss",
            "_isOk && _jetOk>=1 && CleanJet_4DV[0].Pt()>30.0 ? CleanJet_4DV[1].Pt()>20.0 ? {0}mlljj20_whss_jet2 : {0}mlljj20_whss_no_jet2 : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "mlljj30_whss",
            "_isOk && _jetOk>=1 && CleanJet_4DV[0].Pt()>30.0 && CleanJet_4DV[1].Pt()>30.0 ? {0}dphilep1jj <= {0}dphilep2jj ? (Lepton_4DV[0] + Lepton_4DV[0] + CleanJet_4DV[0] + CleanJet_4DV[1]).M() : (Lepton_4DV[1] + Lepton_4DV[1] + CleanJet_4DV[0] + CleanJet_4DV[1]).M() : -9999.0".format(
                prefix
            ),
        )
        df = df.Define( # auxiliary variable
            prefix + "WlepPt_whss_jet2",
            "_isOk && _jetOk>=2 ? {0}dphilep1jj > {0}dphilep2jj ? Lepton_4DV[0].Pt() : Lepton_4DV[1].Pt() : -9999.0".format(
                prefix
            ),
        )
        df = df.Define( # auxiliary variable
            prefix + "WlepPt_whss_no_jet2",
            "_isOk && _jetOk==1 ? {0}detaj1l1 > {0}detaj1l2 ? Lepton_4DV[0].Pt() : Lepton_4DV[1].Pt() : -9999.0".format(
                prefix
            ),
        )
        df = df.Define(
            prefix + "WlepPt_whss",
            "_isOk && _jetOk>=1 ? _jetOk>=2 ? {0}WlepPt_whss_jet2 : {0}WlepPt_whss_no_jet2 : -9999.0".format(
                prefix
            ),
        )

        df = df.DropColumns("Lepton_4DV")
        df = df.DropColumns("CleanJet_4DV")
        df = df.DropColumns("MET_4DV")
        df = df.DropColumns("TkMET_4DV")

        df = df.DropColumns("_isOk")
        df = df.DropColumns("_isOk3l")
        df = df.DropColumns("_lepOk")
        df = df.DropColumns("_tkMetOk")
        df = df.DropColumns("_jetOk")

        df = df.DropColumns("Lepton_enhanced_0")
        df = df.DropColumns("Lepton_enhanced_1")
        df = df.DropColumns("Lepton_enhanced_WW_0")
        df = df.DropColumns("Lepton_enhanced_WW_1")
        df = df.DropColumns("Lepton_enhanced_mTe_0")
        df = df.DropColumns("Lepton_enhanced_mTe_1")
        df = df.DropColumns("utv")

        df = df.DropColumns("mll12")
        df = df.DropColumns("mll13")
        df = df.DropColumns("mll23")
        df = df.DropColumns("drll12")
        df = df.DropColumns("drll13")
        df = df.DropColumns("drll23")


        return df
