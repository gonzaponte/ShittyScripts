from ROOT import *

fin  = 'calHistSource.root'
fout = 'calib_output_2.root'
tin = fin.Get('selOut/calConst')
fout.cd()
tout = tin.CloneTree()
del tin
fout.Add
