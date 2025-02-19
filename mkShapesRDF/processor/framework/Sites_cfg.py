import os

Sites = {

    'cern' : {
        "eosTmpWorkDir": "'USEDAS'", ### Optional to redirect the input samples
        "eosDir"       : "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/",
        "rediretor"    : "root://cmsxrootd.fnal.gov/", # xrootd-cms.infn.it. # cmsxrootd.fnal.gov
    },

    'kit' : {
        "eosTmpWorkDir": "'/tmp/'", # + os.getlogin() + "/'", ### Optional to redirect the input samples
        "eosDir"       : "/ceph/ntrevisa/HWWNano/",
        "rediretor"    : "root://cmsxrootd.fnal.gov/", # xrootd-cms.infn.it. # cmsxrootd.fnal.gov
    }
}
