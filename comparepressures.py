from ROOT import *
from math import *

gStyle.SetOptStat('')
gStyle.SetOptTitle(0)

def format(h,name,color):
    h.SetName(name)
    h.SetLineWidth(2)
    h.SetLineColor(color)
    h.GetXaxis().SetRangeUser( 800, 1700 )

def format2(h,name,color):
    h.SetName(name)
    h.RebinX(10)
    h.GetYaxis().SetRangeUser( 1300, 1700 )

def reso(h, color):
    g = TGraph()
    for i in range(1,h.GetNbinsX()+1):
        try:
            p = h.ProjectionY(str(i),i,i)
            p.Fit("gaus")
            f = p.GetFunction("gaus")
            r = h.GetXaxis().GetBinCenter(i)
            R = 235. * f.GetParameter(2) / f.GetParameter(1) * sqrt( 41.5/2458 )
            g.SetPoint( g.GetN(), r, R )
        except:
            continue
    g.SetTitle(";r (mm);Resolution @ Q_{#beta#beta}")
    g.SetMarkerStyle(20)
    g.SetMarkerColor(color)
    return g

F15 = TFile('3/monitoring_5mm.root')
F10 = TFile('10bar/monitoring_5mm.root')
F05 = TFile('5bar/monitoring_5mm.root')

histoname = 'monitoring/hCorr'

H15 = F15.Get(histoname);format(H15,'15 bar',kBlack)
H10 = F10.Get(histoname);format(H10,'10 bar',kRed)
H05 = F05.Get(histoname);format(H05,' 5 bar',kBlue)

LH = TLegend(0.1,0.65,0.3,0.9)
LH.AddEntry(H15,'15 bar','l')
LH.AddEntry(H10,'10 bar','l')
LH.AddEntry(H05,' 5 bar','l')

CH = TCanvas(); CH.SetLogy()
H15.Draw()
H10.Draw('same')
H05.Draw('same')
LH.Draw()

raw_input()

histoname = 'monitoring/hCorr_r'
H15 = F15.Get(histoname);format2(H15,'15 bar',kBlack)
H10 = F10.Get(histoname);format2(H10,'10 bar',kRed)
H05 = F05.Get(histoname);format2(H05,' 5 bar',kBlue)

m = TMultiGraph()
G15 = reso(H15,kBlack);m.Add(G15)
G10 = reso(H10,kRed);m.Add(G10)
G05 = reso(H05,kBlue);m.Add(G05)

CG = TCanvas()
m.Draw('ap')
LH.Draw()
raw_input()





