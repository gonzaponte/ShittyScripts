from sys import argv
from ROOT import *

gStyle.SetOptTitle(0)
gStyle.SetOptStat('')
gStyle.SetOptFit(1111)

F = TFile( argv[1] )

c = TCanvas();c.SetLogy()
h = F.Get('monitoring/hCorr')
n = h.GetMaximum() * 0.1
h.GetXaxis().SetRangeUser(0,3000)
h.Draw()

xmin = h.GetMean() - 5 * h.GetStdDev()
xmax = h.GetMean() + 5 * h.GetStdDev()
h.Fit('gaus','','',xmin,xmax)
f = h.GetFunction('gaus')

s = h.FindObject('stats')
#s.SetX1NDC(3000)

r1 = 235. * f.GetParameter(2) / f.GetParameter(1)
r2 = r1 * (41.5/2458.)**0.5

r1 = round(r1,3)
r2 = round(r2,3)

p1 = TPaveText(200,n,1000,6*n)
p1.AddText(str(r1)+'% @ 41.5 keV')
p1.AddText(str(r2)+'% @ Qbb     ')

p1.Draw('same')

c.Update()
c.Modified()

raw_input()

