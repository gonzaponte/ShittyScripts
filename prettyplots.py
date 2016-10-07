from ROOT import *
from NEXT100_maps import PMT_map, corona_map, EL_map

colors = [ kRed, kBlue, kBlack, kViolet ]
F = TFile('output/NEW_S2parametrization.root')
T = F.Get('PMT')

f = TF1()
T.SetBranchAddress('functions',f)

xmax = max(zip(*EL_map.values())[0])
histos = { cor : TProfile(str(cor),';r (mm);Detection Probability',500,0,xmax) for cor in set(corona_map.values())}

c = TCanvas()
n = int(1e4)
dx = xmax / n
for ID,corona in corona_map.items():
    T.GetEntry(ID)
    for i in range(1,n+1):
        r = i*dx
        histos[corona].Fill( r, f.Eval(r) )
    histos[corona].SetMinimum(0)
    histos[corona].SetLineColor(colors[corona])
    histos[corona].Draw( 'same' if ID else '' )
raw_input('press enter to continue...')
