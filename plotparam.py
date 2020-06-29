from ROOT import *
from math import *

PMT_map = {
0 : ( 23.9414, 65.7785 ),
1 : ( 44.9951, -53.6231 ),
2 : ( -68.9365, -12.1554 ),
3 : ( 0.0, 185.0 ),
4 : ( 118.916, 141.718 ),
5 : ( 182.189, 32.1249 ),
6 : ( 160.215, -92.5 ),
7 : ( 63.2737, -173.843 ),
8 : ( -63.2737, -173.843 ),
9 : ( -160.215, -92.5 ),
10 : ( -182.189, 32.1249 ),
11 : ( -118.916, 141.718 )
}

PMT_phi_map = { ID : (cos(atan2(y,x)),sin(atan2(y,x))) for ID,(x,y) in PMT_map.items() }

F = TFile("/Users/Gonzalo/github/elparametrization/PyScripts/ParamBuilder/NEW_S2parametrization.root")
F2 = TFile("/Users/Gonzalo/github/elparametrization/PyScripts/ParamBuilder/NEW_S2PMTparametrization_plots.root")

h0 = [F2.Get("PMT {} XY".format(k)) for k in range(12)]
nbinsx, nbinsy = h0[0].GetNbinsX(), h0[0].GetNbinsY()
xmin, xmax = h0[0].GetXaxis().GetBinLowEdge(1), h0[0].GetXaxis().GetBinUpEdge(nbinsx)
ymin, ymax = h0[0].GetYaxis().GetBinLowEdge(1), h0[0].GetYaxis().GetBinUpEdge(nbinsy)

T = F.Get("PMT")
f = TF1()
T.SetBranchAddress("functions", f)

fs = []
for i in range(12):
    T.GetBranch("functions").GetEntry(i)
    fs.append(f.Clone())
del f

f = TF2()
T.SetBranchAddress("angular", f)
T.GetBranch("angular").GetEntry(0)
ang = f.Clone()
del f

rmax = fs[0].GetXmax() - 2.

hs = [TH2F(str(i), "{};x (mm);y (mm)".format(i), nbinsx, xmin, xmax, nbinsy, ymin, ymax) for i in range(12)]
for k in range(3,12):
    print k
    h = hs[k]
    f = fs[k]
    hr = h.Clone()
    for i in range(1, nbinsx+1):
        x = h.GetXaxis().GetBinCenter(i)
        for j in range(1, nbinsy+1):
            y = h.GetYaxis().GetBinCenter(j)
            
            p = h0[k].GetBinContent(i,j)
            r = (x**2+y**2)**0.5
            if r >rmax:
                continue
            w = f(r)
            if k>2:
                c, s = PMT_map[k]
                xs, ys = PMT_map[k]
                dx, dy = x - xs, y - ys
                phi = abs( atan2( -s*dx+c*dy, c*dx + s*dy ) )
                w *= ang(phi, r)
            h.Fill(x, y, w)
            h.Fill(x, y, w/p if p else 1e-20)
    h.Draw("zcol")
    raw_input()


    h.Draw("zcol")
    raw_input()