# Reference python module: https://github.com/latinos/LatinoAnalysis/blob/UL_production/NanoGardener/python/modules/l3KinProducer.py

from mkShapesRDF.processor.framework.module import Module
import ROOT


class l3KinProducer(Module):
    def __init__(self):
        super().__init__("l3KinProducer")

    def runModule(self, df, values):
        df = df.Define(
            "Lepton_4DV",
            "ROOT::VecOps::Construct<ROOT::Math::PtEtaPhiMVector>"
            "(Lepton_pt, Lepton_eta, Lepton_phi, "
            "ROOT::RVecF(Lepton_pt.size(), 0))",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            "CleanJet_4DV",
            "ROOT::VecOps::Construct<ROOT::Math::PtEtaPhiMVector>"
            "(CleanJet_pt, CleanJet_eta, CleanJet_phi,"
            # "Take(Jet_mass, CleanJet_jetIdx))",
            # "CleanJet_mass)",
            "ROOT::RVecF(CleanJet_pt.size(), 0))",
            excludeVariations=["MET*"],
        )

        df = df.Define(
            "MET_4DV", "ROOT::Math::PtEtaPhiMVector" "(PuppiMET_pt, 0, PuppiMET_phi, 0)"
        )

        # Variables yet to be implemented:
        ##############################

        # Variables definitions
        prefix = "new_fw_"
        prefix = ""

        ### WH3l variables
        ##################

        df = df.Define(
            "_WH3l_isOk",
            "Lepton_pt[Lepton_pt > 0].size() >= 3 && abs( abs(Lepton_pdgId[0])/Lepton_pdgId[0] + abs(Lepton_pdgId[1])/Lepton_pdgId[1] + abs(Lepton_pdgId[2])/Lepton_pdgId[2] ) <= 1",
            excludeVariations=["JES*", "MET*"],
        )

        ROOT.gInterpreter.Declare(
            """
        float Get_minmllDiffToZ(ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> leptons_vector, ROOT::RVecF leptons_pdgId){
            float minmllDiffToZ = 9999.0;
            if (leptons_vector.size() < 3) return minmllDiffToZ;
            for (uint i = 0; i < 3; i++){
                for (uint j = i+1; j < 3; j++){
                    if ( leptons_pdgId[i] + leptons_pdgId[j] != 0 ) continue;
                    float mllDiffToZ = abs( (leptons_vector[i] + leptons_vector[j]).M() - 91.1876 );
                    if ( mllDiffToZ < minmllDiffToZ ) minmllDiffToZ = mllDiffToZ;
                }
            }
            return minmllDiffToZ;
        }
        """
        )

        df = df.Define(
            prefix + "WH3l_ZVeto",
            "_WH3l_isOk ? Get_minmllDiffToZ(Lepton_4DV, Lepton_pdgId) : 9999.0",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "WH3l_flagOSSF",
            "_WH3l_isOk ? ({}WH3l_ZVeto != 9999.0) : false".format(prefix),
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "WH3l_njet",
            "_WH3l_isOk ? CleanJet_pt[CleanJet_pt > 40 && abs(CleanJet_eta) < 4.7].size() : -9999.0",
            excludeVariations=["MET*"],
        )

        ROOT.gInterpreter.Declare(
            """
        ROOT::RVecF Get_mtlmet(ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> leptons_vector, ROOT::Math::PtEtaPhiMVector met){
            ROOT::RVecF mtlmet_vector;
            if (leptons_vector.size() < 3) return ROOT::RVecF(3, -9999.0);
            for (uint i = 0; i < 3; i++){
                if (leptons_vector[i].Pt() <= 0) break;
                mtlmet_vector.push_back(sqrt( 2 * leptons_vector[i].Pt() * met.Pt() * (1 - cos(abs( DeltaPhi(leptons_vector[i].Phi(),met.Phi() ) ))))) ;
            }
        return mtlmet_vector;
        }
        """
        )
        df = df.Define(
            prefix + "WH3l_mtlmet",
            "_WH3l_isOk ? Get_mtlmet(Lepton_4DV,MET_4DV) : ROOT::RVecF(3, -9999.0)",
        )

        ROOT.gInterpreter.Declare(
            """
        ROOT::RVecF Get_dphilmet(ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> leptons_vector, ROOT::Math::PtEtaPhiMVector met){
            ROOT::RVecF dphilmet_vector;
            if (leptons_vector.size() < 3) return ROOT::RVecF(3, -9999.0);
            for (uint i = 0; i < 3; i++){
                if (leptons_vector[i].Pt() <= 0) break;
                dphilmet_vector.push_back( abs(DeltaPhi(leptons_vector[i].Phi(),met.Phi())) );
            }
        return dphilmet_vector;
        }
        """
        )
        df = df.Define(
            prefix + "WH3l_dphilmet",
            "_WH3l_isOk ? Get_dphilmet(Lepton_4DV,MET_4DV) : ROOT::RVecF(3, -9999.0)",
        )

        ROOT.gInterpreter.Declare(
            """
        ROOT::RVecF Get_mOSll(ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> leptons_vector, ROOT::RVecF leptons_pdgId){
            ROOT::RVecF mOSll_vector;
            if (leptons_vector.size() < 3) return ROOT::RVecF(3, -9999.0);
            for (uint i = 0; i < 3; i++){
                for (uint j = i+1; j < 3; j++){
                    if (leptons_pdgId[i]*leptons_pdgId[j] < 0)
                        mOSll_vector.push_back( (leptons_vector[i]+leptons_vector[j]).M() );
                    else
                        mOSll_vector.push_back(-9999.0);
                }
            }
        return mOSll_vector;
        }
        """
        )
        df = df.Define(
            prefix + "WH3l_mOSll",
            "_WH3l_isOk ? Get_mOSll(Lepton_4DV,Lepton_pdgId) : ROOT::RVecF(3, -9999.0)",
            excludeVariations=["JES*", "MET*"],
        )

        ROOT.gInterpreter.Declare(
            """
        ROOT::RVecF Get_drOSll(ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> leptons_vector, ROOT::RVecF leptons_pdgId){
            ROOT::RVecF drOSll_vector;
            if (leptons_vector.size() < 3) return ROOT::RVecF(3, -9999.0);
            for (uint i = 0; i < 3; i++){
                for (uint j = i+1; j < 3; j++){
                    if (leptons_pdgId[i]*leptons_pdgId[j] < 0)
                        drOSll_vector.push_back( DeltaR(leptons_vector[i].Eta(),leptons_vector[j].Eta(), leptons_vector[i].Phi(),leptons_vector[j].Phi() ) );
                    else
                        drOSll_vector.push_back(-9999.0);
                }
            }
            return drOSll_vector;
        }
        """
        )
        df = df.Define(
            prefix + "WH3l_drOSll",
            "_WH3l_isOk ? Get_drOSll(Lepton_4DV,Lepton_pdgId) : ROOT::RVecF(3, -9999.0)",
            excludeVariations=["JES*", "MET*"],
        )

        ROOT.gInterpreter.Declare(
            """
        ROOT::RVecF Get_ptOSll(ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> leptons_vector, ROOT::RVecF leptons_pdgId){
            ROOT::RVecF ptOSll_vector;
            if (leptons_vector.size() < 3) return ROOT::RVecF(3, -9999.0);
            for (uint i = 0; i < 3; i++){
                for (uint j = i+1; j < 3; j++){
                    if (leptons_pdgId[i]*leptons_pdgId[j] < 0)
                        ptOSll_vector.push_back( (leptons_vector[i]+leptons_vector[j]).Pt() );
                    else
                        ptOSll_vector.push_back(-9999.0);
                }
            }
            return ptOSll_vector;
        }
        """
        )
        df = df.Define(
            prefix + "WH3l_ptOSll",
            "_WH3l_isOk ? Get_ptOSll(Lepton_4DV,Lepton_pdgId) : ROOT::RVecF(3, -9999.0)",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "WH3l_chlll",
            "_WH3l_isOk ? abs(Lepton_pdgId[0])/Lepton_pdgId[0] + abs(Lepton_pdgId[1])/Lepton_pdgId[1] + abs(Lepton_pdgId[2])/Lepton_pdgId[2] : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "WH3l_mlll",
            "_WH3l_isOk ? (Lepton_4DV[0] + Lepton_4DV[1] + Lepton_4DV[2]).M() : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "WH3l_ptlll",
            "_WH3l_isOk ? (Lepton_4DV[0] + Lepton_4DV[1] + Lepton_4DV[2]).Pt() : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "WH3l_ptWWW",
            "_WH3l_isOk ? (Lepton_4DV[0] + Lepton_4DV[1] + Lepton_4DV[2] + MET_4DV).Pt() : -9999.0",
        )

        df = df.Define(
            prefix + "WH3l_dphilllmet",
            "_WH3l_isOk ? abs(DeltaPhi( (Lepton_4DV[0] + Lepton_4DV[1] + Lepton_4DV[2]).Phi(), MET_4DV.Phi() )) : -9999.0",
        )

        df = df.Define(
            prefix + "WH3l_mtWWW",
            "_WH3l_isOk ? sqrt(2*{0}WH3l_ptlll*MET_4DV.Pt()*(1. - cos({0}WH3l_dphilllmet))) : -9999.0".format(
                prefix
            ),
        )

        ROOT.gInterpreter.Declare(
            """
        float Get_ptW(ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> leptons_vector, ROOT::RVecF leptons_pdgId){
            float mindR = 9999.0;
            float ptW = -9999.0;
            ROOT::RVecF ptOSll_vector;
            if (leptons_vector.size() < 3) return -9999.0;
            for (uint i = 0; i < 3; i++){
                for (uint j = 0; j < 3; j++){
                    for (uint k = 0; k < 3; k++){
                        if (i == j || i == k || j == k) continue;
                        if (leptons_pdgId[i]*leptons_pdgId[j] < 0){
                            float dR = DeltaR(leptons_vector[i].Eta(),leptons_vector[j].Eta(), leptons_vector[i].Phi(),leptons_vector[j].Phi());
                            if (dR < mindR) {
                                mindR = dR;
                                ptW = leptons_vector[k].Pt();
                            }
                        }
                    }
                }
            }
            return ptW;
        }
        """
        )
        df = df.Define(
            prefix + "WH3l_ptW",
            "_WH3l_isOk ? Get_ptW(Lepton_4DV, Lepton_pdgId) : -9999.0",
            excludeVariations=["JES*", "MET*"],
        )

        ### ZH3l variables
        ##################

        df = df.Define(
            "ZH3l_CleanJet_4DV",
            "CleanJet_4DV[CleanJet_pt > 30 && abs(CleanJet_eta) < 4.7]",
            excludeVariations=["MET*"],
        )

        # For ZH3l, "l" in these variables *always* refers to the lepton not associated with the Z
        # Once we have the indices of the Z leptons and the X lepton, we can build the ZH3l variables
        ROOT.gInterpreter.Declare(
            """
        ROOT::RVecI Get_ZH3l_Xlepton(ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> leptons_vector, ROOT::RVecF leptons_pdgId){
            ROOT::RVecI ZH3l_LepIdx{-9999,-9999,-9999};
            if (leptons_vector.size() < 3) return ZH3l_LepIdx;
            float minmllDiffToZ = 9999.0;
            for (uint i = 0; i < 3; i++){
                for (uint j = 0; j < 3; j++){
                    for (uint k = 0; k < 3; k++){
                        if (i == j || i == k || j == k) continue;
                        if (leptons_pdgId[i] + leptons_pdgId[j] != 0) continue;
                        float mllDiffToZ = abs( (leptons_vector[i] + leptons_vector[j]).M() - 91.1876 );
                        if (mllDiffToZ < minmllDiffToZ){
                            ZH3l_LepIdx[0] = i;
                            ZH3l_LepIdx[1] = j;
                            ZH3l_LepIdx[2] = k;
                            minmllDiffToZ = mllDiffToZ;
                        }
                    }
                }
            }
            return ZH3l_LepIdx;
        }
        """
        )
        df = df.Define(
            "ZH3l_LepIdx",
            "_WH3l_isOk ? Get_ZH3l_Xlepton(Lepton_4DV, Lepton_pdgId) : ROOT::RVecI{-9999,-9999,-9999}",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            "_ZH3l_isOk",
            "_WH3l_isOk && ZH3l_LepIdx[0] != -9999",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            "ZLepton1",
            "_ZH3l_isOk ? Lepton_4DV[ZH3l_LepIdx[0]] : ROOT::Math::PtEtaPhiMVector(0., 0., 0., 0.)",
            excludeVariations=["JES*", "MET*"],
        )
        df = df.Define(
            "ZLepton2",
            "_ZH3l_isOk ? Lepton_4DV[ZH3l_LepIdx[1]] : ROOT::Math::PtEtaPhiMVector(0., 0., 0., 0.)",
            excludeVariations=["JES*", "MET*"],
        )
        df = df.Define(
            "ZH3l_XLepton",
            "_ZH3l_isOk ? Lepton_4DV[ZH3l_LepIdx[2]] : ROOT::Math::PtEtaPhiMVector(0., 0., 0., 0.)",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "ZH3l_pdgid_l",
            "_ZH3l_isOk ? Lepton_pdgId[ZH3l_LepIdx[2]] : -9999",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "ZH3l_njet", "ZH3l_CleanJet_4DV.size()", excludeVariations=["MET*"]
        )

        df = df.Define(
            prefix + "ZH3l_Z4lveto",
            "_ZH3l_isOk ? abs({0}WH3l_mlll - 91.1876) : -9999.0".format(prefix),
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "ZH3l_dmjjmW",
            "_ZH3l_isOk && {}ZH3l_njet >= 2 ? (ZH3l_CleanJet_4DV[0] + ZH3l_CleanJet_4DV[1]).M() - 80.4 : -9999.0".format(
                prefix
            ),
            excludeVariations=["MET*"],
        )

        df = df.Define(
            prefix + "ZH3l_mTlmet",
            "_ZH3l_isOk ? sqrt(2 * ZH3l_XLepton.Pt() * MET_4DV.Pt() * (1 - cos(abs(DeltaPhi(ZH3l_XLepton.Phi(),MET_4DV.Phi()))))) : -9999.0",
        )

        df = df.Define(
            prefix + "ZH3l_dphilmetjj",
            "_ZH3l_isOk && {}ZH3l_njet >= 2 ? abs( DeltaPhi( (ZH3l_XLepton + MET_4DV).Phi(), (ZH3l_CleanJet_4DV[0] + ZH3l_CleanJet_4DV[1]).Phi()) ) : -9999.0".format(
                prefix
            ),
        )

        df = df.Define(
            prefix + "ZH3l_dphilmetj",
            "_ZH3l_isOk && {}ZH3l_njet >= 1 ? abs( DeltaPhi( (ZH3l_XLepton + MET_4DV).Phi(), ZH3l_CleanJet_4DV[0].Phi()) ) : -9999.0".format(
                prefix
            ),
        )

        df = df.Define(
            prefix + "ZH3l_pTlmetjj",
            "_ZH3l_isOk && {}ZH3l_njet >= 2 ? (ZH3l_XLepton + MET_4DV + ZH3l_CleanJet_4DV[0] + ZH3l_CleanJet_4DV[1]).Pt() : -9999.0".format(
                prefix
            ),
        )

        df = df.Define(
            prefix + "ZH3l_pTlmetj",
            "_ZH3l_isOk && {}ZH3l_njet >= 1 ? (ZH3l_XLepton + MET_4DV + ZH3l_CleanJet_4DV[0]).Pt() : -9999.0".format(
                prefix
            ),
        )

        df = df.Define(
            prefix + "ZH3l_mTlmetj",
            "_ZH3l_isOk && {}ZH3l_njet >= 1 ? sqrt(pow((MET_4DV.Pt() + ZH3l_XLepton.Pt() + ZH3l_CleanJet_4DV[0].Pt()),2) - pow((MET_4DV + ZH3l_XLepton + ZH3l_CleanJet_4DV[0]).Px(),2) - pow((MET_4DV + ZH3l_XLepton + ZH3l_CleanJet_4DV[0]).Py(),2)) : -9999.0".format(
                prefix
            ),
        )

        df = df.Define(
            prefix + "ZH3l_mTlmetjj",
            "_ZH3l_isOk && {}ZH3l_njet >= 2 ? sqrt(pow((MET_4DV.Pt() + ZH3l_XLepton.Pt() + ZH3l_CleanJet_4DV[0].Pt() + ZH3l_CleanJet_4DV[1].Pt()),2) - pow((MET_4DV + ZH3l_XLepton + ZH3l_CleanJet_4DV[0] + ZH3l_CleanJet_4DV[1]).Px(),2) - pow((MET_4DV + ZH3l_XLepton + ZH3l_CleanJet_4DV[0] + ZH3l_CleanJet_4DV[1]).Py(),2)) : -9999.0".format(
                prefix
            ),
        )

        df = df.Define(
            prefix + "ZH3l_pTZ",
            "_ZH3l_isOk ? (ZLepton1+ZLepton2).Pt() : -9999",
            excludeVariations=["JES*", "MET*"],
        )

        df = df.Define(
            prefix + "ZH3l_checkmZ",
            "_ZH3l_isOk ? (ZLepton1+ZLepton2).M() : -9999",
            excludeVariations=["JES*", "MET*"],
        )

        # ### AZH variables
        # #################

        # # Reference: https://github.com/latinos/PlotsConfigurations/blob/master/Configurations/AToZH_Full/scripts/AZH_patch.cc

        # ROOT.gInterpreter.Declare(
        #     """
        # ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> Get_AZH_bJet_4vecId(ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> jets_vector,
        #                                                              ROOT::RVecF jet_btag,
        #                                                              ROOT::RVecF jet_idx
        # ){
        #     ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> AZH_bJet_4vecId;
        #     for (uint i = 0; i < jets_vector.size(); ++i){
        #         if (jets_vector[i].Pt() > 30 && abs(jets_vector[i].Eta()) < 4.7 && jet_btag[jet_idx[i]] > 0.4941){
        #             AZH_bJet_4vecId.push_back(jets_vector[i]);
        #         }
        #     }
        #     return AZH_bJet_4vecId;
        # }
        # """
        # )

        # df = df.Define(
        #     "AZH_bJet_4vecId",
        #     "Get_AZH_bJet_4vecId(CleanJet_4DV, Jet_btagDeepB, CleanJet_jetIdx)",
        #     excludeVariations=["MET*"],
        # )

        # df = df.Define("nbJet", "AZH_bJet_4vecId.size()", excludeVariations=["MET*"])

        # df = df.Define(
        #     "_AZH_isOk", "_ZH3l_isOk && {}ZH3l_njet >= 4 && nbJet >=2".format(prefix)
        # )

        # df = df.Define(
        #     "Zeta",
        #     "_AZH_isOk ? 0.5*pow(80.4, 2) + MET_4DV.Pt() *  ZH3l_XLepton.Pt() * (cos(abs(DeltaPhi(ZH3l_XLepton.Phi(),MET_4DV.Phi() ) ) ) ) : -9999",
        # )

        # df = df.Define(
        #     "A",
        #     "_AZH_isOk ? (pow(Zeta, 2) * pow(ZH3l_XLepton.Pz(), 2)) / pow(ZH3l_XLepton.Pt(), 4) - (pow(MET_4DV.Pt(), 2) * pow(ZH3l_XLepton.E(), 2) - pow(Zeta, 2)) / pow(ZH3l_XLepton.Pt(), 2) > 0 ? \
        #              sqrt((pow(Zeta, 2) * pow(ZH3l_XLepton.Pz(), 2)) / pow(ZH3l_XLepton.Pt(), 4) - (pow(MET_4DV.Pt(), 2) * pow(ZH3l_XLepton.E(), 2) - pow(Zeta, 2)) / pow(ZH3l_XLepton.Pt(), 2)) : \
        #              0 : -9999",
        # )

        # df = df.Define(
        #     "Pznu1",
        #     "_AZH_isOk ? ((Zeta * ZH3l_XLepton.Pz()) / pow(ZH3l_XLepton.Pt(), 2)) + A : -9999",
        # )

        # df = df.Define(
        #     "Pznu2",
        #     "_AZH_isOk ? ((Zeta * ZH3l_XLepton.Pz()) / pow(ZH3l_XLepton.Pt(), 2)) - A : -9999",
        # )

        # df = df.Define(
        #     "Enu1",
        #     "_AZH_isOk ? sqrt(pow(MET_4DV.Pt(), 2) + pow(Pznu1, 2)) : -9999",
        # )

        # df = df.Define(
        #     "Enu2",
        #     "_AZH_isOk ? sqrt(pow(MET_4DV.Pt(), 2) + pow(Pznu2, 2)) : -9999",
        # )

        # df = df.Define(
        #     "AZH_Neutrino1",
        #     "_AZH_isOk ? ROOT::Math::PxPyPzEVector( MET_4DV.Px(), \
        #                                              MET_4DV.Py(), \
        #                                              Pznu1, \
        #                                              Enu1 ) \
        #                                              : ROOT::Math::PxPyPzEVector(0., 0., 0., 0.)",
        # )

        # df = df.Define(
        #     "AZH_Neutrino2",
        #     "_AZH_isOk ? ROOT::Math::PxPyPzEVector( MET_4DV.Px(), \
        #                                              MET_4DV.Py(), \
        #                                              Pznu2, \
        #                                              Enu2 ) \
        #                                              : ROOT::Math::PxPyPzEVector(0., 0., 0., 0.)",
        # )

        # ROOT.gInterpreter.Declare(
        #     """
        # ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> Get_AZH_var_2bjet(ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> jets_vector,
        #                                                                   ROOT::Math::PxPyPzEVector Neutrino1,
        #                                                                   ROOT::Math::PxPyPzEVector Neutrino2,
        #                                                                   ROOT::Math::PtEtaPhiMVector XLepton,
        #                                                                   ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> AZH_bJet_4vecId_
        # ){
        #     float sigmaleptonic = 26.64;
        #     float sigmahadronic = 37.73;
        #     float TopMassLeptonic_true = 168.7;
        #     float TopMassHadronic_true = 163;
        #     ROOT::VecOps::RVec<ROOT::Math::PxPyPzEVector> Neutrinos;
        #     Neutrinos.push_back(Neutrino1);
        #     Neutrinos.push_back(Neutrino2);
        #     ROOT::Math::PtEtaPhiMVector WJet1_best;
        #     ROOT::Math::PtEtaPhiMVector WJet2_best;
        #     ROOT::Math::PtEtaPhiMVector bJetHadronic_best;
        #     ROOT::Math::PtEtaPhiMVector bJetLeptonic_best;
        #     ROOT::Math::PtEtaPhiMVector AZH_Neutrino_best;
        #     float ChisqMin = 9999.0;
        #     for (uint i_neutrino = 0; i_neutrino < 2; ++i_neutrino){
        #         for (uint ibJet1 = 0; ibJet1 < AZH_bJet_4vecId_.size(); ++ibJet1){
        #             for (uint ibJet2 = ibJet1 + 1; ibJet2 < AZH_bJet_4vecId_.size(); ++ibJet2){
        #                 ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> bJetPair;
        #                 bJetPair.push_back(AZH_bJet_4vecId_[ibJet1]);
        #                 bJetPair.push_back(AZH_bJet_4vecId_[ibJet2]);
        #                 ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> WJets;
        #                 for (uint ij = 0; ij < jets_vector.size(); ++ij){
        #                     if ((jets_vector[ij] != bJetPair[0]) && (jets_vector[ij] != bJetPair[1])) {
        #                         WJets.push_back(jets_vector[ij]);
        #                     }
        #                 }
        #                 for (uint k = 0; k < 2; k++){
        #                     for (uint iWJet1 = 0; iWJet1 < WJets.size(); ++iWJet1){
        #                         for (uint iWJet2 = iWJet1 + 1; iWJet2 < WJets.size(); ++iWJet2){
        #                             ROOT::Math::PtEtaPhiMVector WJet1 = WJets[iWJet1];
        #                             ROOT::Math::PtEtaPhiMVector WJet2 = WJets[iWJet2];
        #                             ROOT::Math::PtEtaPhiMVector bJetHadronic = bJetPair[k];
        #                             ROOT::Math::PtEtaPhiMVector bJetLeptonic = bJetPair[1-k];
        #                             float TopMassLeptonic = (XLepton + Neutrinos[i_neutrino] + bJetLeptonic).M();
        #                             float TopMassHadronic = (WJet1 + WJet2 + bJetHadronic).M();
        #                             float Chisq = TMath::Power((TopMassLeptonic-TopMassLeptonic_true)/sigmaleptonic,2) + TMath::Power((TopMassHadronic-TopMassHadronic_true)/sigmahadronic, 2);
        #                             if(Chisq < ChisqMin) {
        #                                 ChisqMin = Chisq;
        #                                 WJet1_best = WJet1;
        #                                 WJet2_best = WJet2;
        #                                 bJetHadronic_best = bJetHadronic;
        #                                 bJetLeptonic_best = bJetLeptonic;
        #                                 AZH_Neutrino_best = Neutrinos[i_neutrino];
        #                             }
        #                         }
        #                     }
        #                 }
        #             }
        #         }
        #     }
        # return {WJet1_best, WJet2_best, bJetHadronic_best, bJetLeptonic_best, AZH_Neutrino_best};
        # }
        # """
        # )
        # df = df.Define(
        #     "WJet1_best",
        #     "_AZH_isOk ? Get_AZH_var_2bjet(ZH3l_CleanJet_4DV, AZH_Neutrino1, AZH_Neutrino2, ZH3l_XLepton, AZH_bJet_4vecId)[0] : ROOT::Math::PtEtaPhiMVector(0.,0.,0.,0.)",
        # )
        # df = df.Define(
        #     "WJet2_best",
        #     "_AZH_isOk ? Get_AZH_var_2bjet(ZH3l_CleanJet_4DV, AZH_Neutrino1, AZH_Neutrino2, ZH3l_XLepton, AZH_bJet_4vecId)[1] : ROOT::Math::PtEtaPhiMVector(0.,0.,0.,0.)",
        # )
        # df = df.Define(
        #     "bJetHadronic_best",
        #     "_AZH_isOk ? Get_AZH_var_2bjet(ZH3l_CleanJet_4DV, AZH_Neutrino1, AZH_Neutrino2, ZH3l_XLepton, AZH_bJet_4vecId)[2] : ROOT::Math::PtEtaPhiMVector(0.,0.,0.,0.)",
        # )
        # df = df.Define(
        #     "bJetLeptonic_best",
        #     "_AZH_isOk ? Get_AZH_var_2bjet(ZH3l_CleanJet_4DV, AZH_Neutrino1, AZH_Neutrino2, ZH3l_XLepton, AZH_bJet_4vecId)[3] : ROOT::Math::PtEtaPhiMVector(0.,0.,0.,0.)",
        # )
        # df = df.Define(
        #     "AZH_Neutrino_best",
        #     "_AZH_isOk ? Get_AZH_var_2bjet(ZH3l_CleanJet_4DV, AZH_Neutrino1, AZH_Neutrino2, ZH3l_XLepton, AZH_bJet_4vecId)[4] : ROOT::Math::PtEtaPhiMVector(0.,0.,0.,0.)",
        # )

        # df = df.Define(
        #     prefix + "AZH_ChiSquare",
        #     "_AZH_isOk ? pow(((ZH3l_XLepton + AZH_Neutrino_best + bJetLeptonic_best).M()-168.7)/26.64,2) + pow(((bJetHadronic_best + WJet1_best + WJet2_best).M()-163.0)/37.73, 2) : -9999.0",
        # )

        # df = df.Define(
        #     prefix + "AZH_mA_minus_mH",
        #     "_AZH_isOk ? (ZH3l_XLepton + AZH_Neutrino_best + bJetLeptonic_best + bJetHadronic_best + WJet1_best + WJet2_best + ZLepton1 + ZLepton2).M() - (ZH3l_XLepton + AZH_Neutrino_best + bJetLeptonic_best + bJetHadronic_best + WJet1_best + WJet2_best).M() : -9999.0",
        # )

        # df = df.Define(
        #     prefix + "AZH_Amass",
        #     "_AZH_isOk ? (ZH3l_XLepton + AZH_Neutrino_best + bJetLeptonic_best + bJetHadronic_best + WJet1_best + WJet2_best + ZLepton1 + ZLepton2).M() : -9999.0",
        # )

        # df = df.Define(
        #     prefix + "AZH_Hmass",
        #     "_AZH_isOk ? (ZH3l_XLepton + AZH_Neutrino_best + bJetLeptonic_best + bJetHadronic_best + WJet1_best + WJet2_best).M() : -9999.0",
        # )

        # df = df.Define(
        #     prefix + "AZH_Tophadronic",
        #     "_AZH_isOk ? (bJetHadronic_best + WJet1_best + WJet2_best).M() : -9999.0",
        # )

        # df = df.Define(
        #     prefix + "AZH_Topleptonic",
        #     "_AZH_isOk ? (ZH3l_XLepton + AZH_Neutrino_best + bJetLeptonic_best).M() : -9999.0",
        # )

        # df = df.Define(
        #     "ZH3l_CleanJet_jetIdx",
        #     "CleanJet_jetIdx[CleanJet_pt > 30 && abs(CleanJet_eta) < 4.7]",
        #     excludeVariations=["MET*"],
        # )

        # ROOT.gInterpreter.Declare(
        #     """
        # ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> Get_AZH_var_1bjet(ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> jets_vector,
        #                                                                   ROOT::RVecF jet_btag,
        #                                                                   ROOT::RVecF jet_idx,
        #                                                                   ROOT::Math::PxPyPzEVector Neutrino1,
        #                                                                   ROOT::Math::PxPyPzEVector Neutrino2,
        #                                                                   ROOT::Math::PtEtaPhiMVector XLepton,
        #                                                                   ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> AZH_bJet_4vecId_
        # ){
        #     float sigmaleptonic = 26.64;
        #     float sigmahadronic = 37.73;
        #     float TopMassLeptonic_true = 168.7;
        #     float TopMassHadronic_true = 163;
        #     ROOT::VecOps::RVec<ROOT::Math::PxPyPzEVector> Neutrinos;
        #     Neutrinos.push_back(Neutrino1);
        #     Neutrinos.push_back(Neutrino2);
        #     ROOT::Math::PtEtaPhiMVector WJet1_best_onebjet;
        #     ROOT::Math::PtEtaPhiMVector WJet2_best_onebjet;
        #     ROOT::Math::PtEtaPhiMVector bJetHadronic_best_onebjet;
        #     ROOT::Math::PtEtaPhiMVector bJetLeptonic_best_onebjet;
        #     ROOT::Math::PtEtaPhiMVector AZH_Neutrino_best_onebjet;
        #     float ChisqMin = 9999.0;
        #     if (AZH_bJet_4vecId_.size() == 1){
        #         for (uint i_neutrino = 0; i_neutrino < 2; ++i_neutrino){
        #             int ibJet2 = 0;
        #             if (jets_vector[ibJet2] == AZH_bJet_4vecId_[0]) ibJet2 = 1;
        #             ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> WJets;
        #             for (uint ij = 0; ij < jets_vector.size(); ++ij){
        #                 if ( (jets_vector[ij] != AZH_bJet_4vecId_[0]) && (jet_btag[jet_idx[ij]] > jet_btag[jet_idx[ibJet2]]) ) {
        #                     ibJet2 = ij;
        #                 }
        #             }
        #             ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector> bJetPair;
        #             bJetPair.push_back(AZH_bJet_4vecId_[0]);
        #             bJetPair.push_back(jets_vector[ibJet2]);
        #             for (int iw =0; iw < jets_vector.size(); ++iw){
        #                 if ( (jets_vector[iw] != AZH_bJet_4vecId_[0]) && (jets_vector[iw] != jets_vector[ibJet2]) ){
        #                     WJets.push_back(jets_vector[iw]);
        #                 }
        #             }
        #             for(int k = 0; k < 2; k++) {
        #                 for (int iWJet1 = 0; iWJet1 < WJets.size(); ++iWJet1){
        #                     for (int iWJet2 = iWJet1 + 1; iWJet2 < WJets.size(); ++iWJet2){
        #                         ROOT::Math::PtEtaPhiMVector WJet1_onebjet = WJets[iWJet1];
        #                         ROOT::Math::PtEtaPhiMVector WJet2_onebjet = WJets[iWJet2];
        #                         ROOT::Math::PtEtaPhiMVector bJetHadronic_onebjet = bJetPair[k];
        #                         ROOT::Math::PtEtaPhiMVector bJetLeptonic_onebjet = bJetPair[1-k];
        #                         float TopMassLeptonic_onebjet = (XLepton + Neutrinos[i_neutrino] + bJetLeptonic_onebjet).M();
        #                         float TopMassHadronic_onebjet = (WJet1_onebjet + WJet2_onebjet + bJetHadronic_onebjet).M();
        #                         float Chisq_onebjet = TMath::Power((TopMassLeptonic_onebjet-TopMassLeptonic_true)/sigmaleptonic,2) + TMath::Power((TopMassHadronic_onebjet-TopMassHadronic_true)/sigmahadronic, 2);
        #                         if(Chisq_onebjet < ChisqMin) {
        #                             ChisqMin = Chisq_onebjet;
        #                             WJet1_best_onebjet = WJet1_onebjet;
        #                             WJet2_best_onebjet = WJet2_onebjet;
        #                             bJetHadronic_best_onebjet = bJetHadronic_onebjet;
        #                             bJetLeptonic_best_onebjet = bJetLeptonic_onebjet;
        #                             AZH_Neutrino_best_onebjet = Neutrinos[i_neutrino];
        #                         }
        #                     }
        #                 }
        #             }
        #         }
        #     }
        #     return {WJet1_best_onebjet, WJet2_best_onebjet, bJetHadronic_best_onebjet, bJetLeptonic_best_onebjet, AZH_Neutrino_best_onebjet};
        # }
        # """
        # )
        # df = df.Define(
        #     "WJet1_best_onebjet",
        #     "_ZH3l_isOk && {}ZH3l_njet >= 4 && nbJet == 1 ? Get_AZH_var_1bjet(ZH3l_CleanJet_4DV, Jet_btagDeepB, ZH3l_CleanJet_jetIdx, AZH_Neutrino1, AZH_Neutrino2, ZH3l_XLepton, AZH_bJet_4vecId)[0] : ROOT::Math::PtEtaPhiMVector(0.,0.,0.,0.)".format(
        #         prefix
        #     ),
        # )
        # df = df.Define(
        #     "WJet2_best_onebjet",
        #     "_ZH3l_isOk && {}ZH3l_njet >= 4 && nbJet == 1 ? Get_AZH_var_1bjet(ZH3l_CleanJet_4DV, Jet_btagDeepB, ZH3l_CleanJet_jetIdx, AZH_Neutrino1, AZH_Neutrino2, ZH3l_XLepton, AZH_bJet_4vecId)[1] : ROOT::Math::PtEtaPhiMVector(0.,0.,0.,0.)".format(
        #         prefix
        #     ),
        # )
        # df = df.Define(
        #     "bJetHadronic_best_onebjet",
        #     "_ZH3l_isOk && {}ZH3l_njet >= 4 && nbJet == 1 ? Get_AZH_var_1bjet(ZH3l_CleanJet_4DV, Jet_btagDeepB, ZH3l_CleanJet_jetIdx, AZH_Neutrino1, AZH_Neutrino2, ZH3l_XLepton, AZH_bJet_4vecId)[2] : ROOT::Math::PtEtaPhiMVector(0.,0.,0.,0.)".format(
        #         prefix
        #     ),
        # )
        # df = df.Define(
        #     "bJetLeptonic_best_onebjet",
        #     "_ZH3l_isOk && {}ZH3l_njet >= 4 && nbJet == 1 ? Get_AZH_var_1bjet(ZH3l_CleanJet_4DV, Jet_btagDeepB, ZH3l_CleanJet_jetIdx, AZH_Neutrino1, AZH_Neutrino2, ZH3l_XLepton, AZH_bJet_4vecId)[3] : ROOT::Math::PtEtaPhiMVector(0.,0.,0.,0.)".format(
        #         prefix
        #     ),
        # )
        # df = df.Define(
        #     "AZH_Neutrino_best_onebjet",
        #     "_ZH3l_isOk && {}ZH3l_njet >= 4 && nbJet == 1 ? Get_AZH_var_1bjet(ZH3l_CleanJet_4DV, Jet_btagDeepB, ZH3l_CleanJet_jetIdx, AZH_Neutrino1, AZH_Neutrino2, ZH3l_XLepton, AZH_bJet_4vecId)[4] : ROOT::Math::PtEtaPhiMVector(0.,0.,0.,0.)".format(
        #         prefix
        #     ),
        # )

        # df = df.Define(
        #     prefix + "AZH_mA_minus_mH_onebjet",
        #     "_ZH3l_isOk && {}ZH3l_njet >= 4 && nbJet == 1 ? (ZH3l_XLepton + AZH_Neutrino_best_onebjet + bJetLeptonic_best_onebjet + bJetHadronic_best_onebjet + WJet1_best_onebjet + WJet2_best_onebjet + ZLepton1 + ZLepton2).M() - (ZH3l_XLepton + AZH_Neutrino_best_onebjet + bJetLeptonic_best_onebjet + bJetHadronic_best_onebjet + WJet1_best_onebjet + WJet2_best_onebjet).M() : -9999.0".format(
        #         prefix
        #     ),
        # )

        df = df.DropColumns("_WH3l_isOk")
        df = df.DropColumns("_ZH3l_isOk")
        # df = df.DropColumns("_AZH_isOk")

        df = df.DropColumns("Lepton_4DV")
        df = df.DropColumns("CleanJet_4DV")
        df = df.DropColumns("MET_4DV")

        df = df.DropColumns("ZH3l_CleanJet_4DV")
        # df = df.DropColumns("ZH3l_CleanJet_jetIdx")
        df = df.DropColumns("ZH3l_LepIdx")
        df = df.DropColumns("ZLepton1")
        df = df.DropColumns("ZLepton2")
        df = df.DropColumns("ZH3l_XLepton")

        # df = df.DropColumns("AZH_bJet_4vecId")
        # df = df.DropColumns("nbJet")
        # df = df.DropColumns("Zeta")
        # df = df.DropColumns("A")
        # df = df.DropColumns("Pznu1")
        # df = df.DropColumns("Pznu2")
        # df = df.DropColumns("Enu1")
        # df = df.DropColumns("Enu2")
        # df = df.DropColumns("AZH_Neutrino1")
        # df = df.DropColumns("AZH_Neutrino2")

        # df = df.DropColumns("AZH_Neutrino_best")
        # df = df.DropColumns("bJetLeptonic_best")
        # df = df.DropColumns("bJetHadronic_best")
        # df = df.DropColumns("WJet1_best")
        # df = df.DropColumns("WJet2_best")

        # df = df.DropColumns("AZH_Neutrino_best_onebjet")
        # df = df.DropColumns("bJetLeptonic_best_onebjet")
        # df = df.DropColumns("bJetHadronic_best_onebjet")
        # df = df.DropColumns("WJet1_best_onebjet")
        # df = df.DropColumns("WJet2_best_onebjet")

        return df
