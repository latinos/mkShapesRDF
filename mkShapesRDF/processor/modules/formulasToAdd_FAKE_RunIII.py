from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.LeptonSel_cfg import *


class formulasToAdd_FAKE_RunIII(Module):
    def __init__(self, era):
        super().__init__("formulasToAdd_FAKE_RunIII")
        self.era = era

    def runModule(self, df, values):

        df = df.Define("METFilter_FAKE", "METFilter_DATA")
        df = df.Define("nCleanJet", "CleanJet_pt.size()")

        muWPlist = [wp for wp in MuonWP[self.era]["TightObjWP"]]
        eleWPlist = [wp for wp in ElectronWP[self.era]["TightObjWP"]]

        for eleWP in eleWPlist:
            for muWP in muWPlist:

                Tag = 'ele_'+eleWP+'_mu_'+muWP

                df = df.Define(
                    "fakeW2l_"+Tag, 
                    'fakeW_'+Tag+'_2l0j*(nCleanJet == 0 || Alt(CleanJet_pt,0,0) < 30)+\
                    fakeW_'+Tag+'_2l1j*((nCleanJet == 1 && Alt(CleanJet_pt,0,0) >= 30) || \
                                       (nCleanJet > 1 && Alt(CleanJet_pt,0,0) >= 30 && Alt(CleanJet_pt,1,0) < 30))+\
                    fakeW_'+Tag+'_2l2j*(nCleanJet > 1 && Alt(CleanJet_pt,1,0) >= 30)'
                )

                df = df.Define(
                    "fake_eq_0_"+Tag,
                    'fakeW2l_'+Tag+' == 0.0'
                )

                df = df.Define(
                    "fakeW2l_"+Tag+"_EleUp",
                    'fake_eq_0_'+Tag+' ? (fakeW_'+Tag+'_2l0jElUp*(nCleanJet == 0 || Alt(CleanJet_pt,0,0) < 30)+\
                      fakeW_'+Tag+'_2l1jElUp*((nCleanJet == 1 && Alt(CleanJet_pt,0,0) >= 30) || \
                                              (nCleanJet > 1 && Alt(CleanJet_pt,0,0) >= 30 && Alt(CleanJet_pt,1,0) < 30)) + \
                      fakeW_'+Tag+'_2l2jElUp*(nCleanJet > 1 && Alt(CleanJet_pt,1,0) >= 30)) \
                      / fakeW2l_'+Tag+' : 0.0'
                )


                df = df.Define(
                    "fakeW2l_"+Tag+"_EleDown",
                    'fake_eq_0_'+Tag+' ? (fakeW_'+Tag+'_2l0jElDown*(nCleanJet == 0 || Alt(CleanJet_pt,0,0) < 30)+ \
                    fakeW_'+Tag+'_2l1jElDown*((nCleanJet == 1 && Alt(CleanJet_pt,0,0) >= 30) || \
                                              (nCleanJet > 1 && Alt(CleanJet_pt,0,0) >= 30 && Alt(CleanJet_pt,1,0) < 30)) + \
                    fakeW_'+Tag+'_2l2jElDown*(nCleanJet > 1 && Alt(CleanJet_pt,1,0) >= 30)) \
                    / fakeW2l_'+Tag+' : 0.0'
                )


                df = df.Define(
                    "fakeW2l_"+Tag+"_MuUp",
                    'fake_eq_0_'+Tag+' ? (fakeW_'+Tag+'_2l0jMuUp*(nCleanJet == 0 || Alt(CleanJet_pt,0,0) < 30)+ \
                    fakeW_'+Tag+'_2l1jMuUp*((nCleanJet == 1 && Alt(CleanJet_pt,0,0) >= 30) || \
                                            (nCleanJet > 1 && Alt(CleanJet_pt,0,0) >= 30 && Alt(CleanJet_pt,1,0) < 30)) + \
                    fakeW_'+Tag+'_2l2jMuUp*(nCleanJet > 1 && Alt(CleanJet_pt,1,0) >= 30)) \
                    / fakeW2l_'+Tag+' : 0.0'
                )
                
                
                
                df = df.Define(
                    "fakeW2l_"+Tag+"_MuDown",
                    'fake_eq_0_'+Tag+' ? (fakeW_'+Tag+'_2l0jMuDown*(nCleanJet == 0 || Alt(CleanJet_pt,0,0) < 30)+ \
                    fakeW_'+Tag+'_2l1jMuDown*((nCleanJet == 1 && Alt(CleanJet_pt,0,0) >= 30) || \
                                              (nCleanJet > 1 && Alt(CleanJet_pt,0,0) >= 30 && Alt(CleanJet_pt,1,0) < 30)) + \
                    fakeW_'+Tag+'_2l2jMuDown*(nCleanJet > 1 && Alt(CleanJet_pt,1,0) >= 30)) \
                    / fakeW2l_'+Tag+' : 0.0'
                )
                
                
                
                df = df.Define(
                    "fakeW2l_"+Tag+"_statEleUp",
                    'fake_eq_0_'+Tag+' ? (fakeW_'+Tag+'_2l0jstatElUp*(nCleanJet == 0 || Alt(CleanJet_pt,0,0) < 30)+ \
                    fakeW_'+Tag+'_2l1jstatElUp*((nCleanJet == 1 && Alt(CleanJet_pt,0,0) >= 30) || \
                                                (nCleanJet > 1 && Alt(CleanJet_pt,0,0) >= 30 && Alt(CleanJet_pt,1,0) < 30)) + \
                    fakeW_'+Tag+'_2l2jstatElUp*(nCleanJet > 1 && Alt(CleanJet_pt,1,0) >= 30)) \
                    / fakeW2l_'+Tag+' : 0.0'
                )
                
                
                df = df.Define(
                    "fakeW2l_"+Tag+"_statEleDown",
                    'fake_eq_0_'+Tag+' ? (fakeW_'+Tag+'_2l0jstatElDown*(nCleanJet == 0 || Alt(CleanJet_pt,0,0) < 30)+ \
                    fakeW_'+Tag+'_2l1jstatElDown*((nCleanJet == 1 && Alt(CleanJet_pt,0,0) >= 30) || \
                                                  (nCleanJet > 1 && Alt(CleanJet_pt,0,0) >= 30 && Alt(CleanJet_pt,1,0) < 30)) + \
                    fakeW_'+Tag+'_2l2jstatElDown*(nCleanJet > 1 && Alt(CleanJet_pt,1,0) >= 30)) \
                    / fakeW2l_'+Tag+' : 0.0'
                )
                
                
                df = df.Define(
                    "fakeW2l_"+Tag+"_statMuUp",
                    'fake_eq_0_'+Tag+' ? (fakeW_'+Tag+'_2l0jstatMuUp*(nCleanJet == 0 || Alt(CleanJet_pt,0,0) < 30)+ \
                    fakeW_'+Tag+'_2l1jstatMuUp*((nCleanJet == 1 && Alt(CleanJet_pt,0,0) >= 30) || \
                                                (nCleanJet > 1 && Alt(CleanJet_pt,0,0) >= 30 && Alt(CleanJet_pt,1,0) < 30)) + \
                    fakeW_'+Tag+'_2l2jstatMuUp*(nCleanJet > 1 && Alt(CleanJet_pt,1,0) >= 30)) \
                    / fakeW2l_'+Tag+' : 0.0'
                )
                
                df = df.Define(
                    "fakeW2l_"+Tag+"_statMuDown",
                    'fake_eq_0_'+Tag+' ? (fakeW_'+Tag+'_2l0jstatMuDown*(nCleanJet == 0 || Alt(CleanJet_pt,0,0) < 30)+ \
                    fakeW_'+Tag+'_2l1jstatMuDown*((nCleanJet == 1 && Alt(CleanJet_pt,0,0) >= 30) || \
                                                  (nCleanJet > 1 && Alt(CleanJet_pt,0,0) >= 30 && Alt(CleanJet_pt,1,0) < 30)) + \
                    fakeW_'+Tag+'_2l2jstatMuDown*(nCleanJet > 1 && Alt(CleanJet_pt,1,0) >= 30)) \
                    / fakeW2l_'+Tag+' : 0.0'
                )

                df = df.DropColumns("fake_eq_0_"+Tag)
        df = df.DropColumns("nCleanJet")

        return df
