from ROOT import *
from math import *
from sys import *

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

F = TFile(argv[1])

histoname = 'monitoring/hCorr'

H = F.Get(histoname);format(H,'H',kBlack)

CH = TCanvas(); CH.SetLogy()
H.Draw()
raw_input()

histoname = 'monitoring/hCorr_r'
H = F.Get(histoname);format2(H,'HH',kBlack)

G = reso(H,kBlack)

CG = TCanvas()
G.Draw('ap')
raw_input()





