from ROOT import *
from sys import argv

if len(argv)<2: print 'Usage: python PrintPSF.py [filename]';exit()

F = TFile( argv[1] )
T = F.Get('PMT')
f = TF1()
T.SetBranchAddress('functions',f)

PSFs = []
for i in range(12):
    T.GetEntry(i)
    PSFs.append( f.Clone() )

G = TGraph()
S = '#r (mm) DE\n'

Rmax    = 215.
npoints = int(1e5)
dr      = Rmax/npoints
for i in range(npoints):
    r = i*dr
    p = sum( psf.Eval(r) for psf in PSFs )
    G.SetPoint( G.GetN(), r, p )
    S += '{0} {1}\n'.format(r,p)

C = TCanvas()
G.SetLineWidth(2)
G.SetTitle('PMTs detection efficiency;r (mm);#varepsilon')
G.Draw('AC')
C.SaveAs('PMTsDetEff.pdf')

open('DetEff.txt','w').write(S)