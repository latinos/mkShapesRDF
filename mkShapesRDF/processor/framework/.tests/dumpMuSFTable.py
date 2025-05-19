import ROOT
import numpy as np

import sys

if len(sys.argv) < 3:
    print ("usage: python dumpMuSFTable.py filename.root outfile.txt")

df = ROOT.RDataFrame("Events", sys.argv[1])

cols = df.Define("MuonIdSFProd", "ROOT::VecOps::Product(Lepton_tightMuon_cut_TightID_POG_idSF)")\
         .AsNumpy(["event", "run", "luminosityBlock", "MuonIdSFProd"])

out = np.column_stack((cols['event'], cols['run'], cols['luminosityBlock'], cols['MuonIdSFProd']))
np.savetxt(sys.argv[2], out, delimiter=',', fmt='%i,%i,%i,%1.6f')
