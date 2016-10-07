from sys import argv
from ROOT import *

if len(argv)<3: print 'Usage: python ExtractEdgeSiPMs.py pitch filename';exit()

def LoadTable():
    D = {}
    for line in open( argv[2], 'r' ):
        if not 'SiPM50' in line: continue
        line = line.split(',')
        ID = line[2]
        x, y = map( float, line[-2:] )
        D[x,y] = ID
    return D

def PlotSiPMs( D ):
    G = TGraph()
    for x,y in D:
        G.SetPoint( G.GetN(), x, y )
    G.SetMarkerStyle(21)
    G.SetMarkerSize(0.1)
    G.SetTitle('SiPMs distribution for pitch = {0} mm;x (mm);y (mm)'.format(pitch))
    C = TCanvas()
    G.Draw('ap')
    C.SaveAs('SiPMs_pitch{0}.pdf'.format(pitch))

def PlotIDs( D ):
    xmax = max(zip(*D.keys())[0]) + 1.5
    ymax = max(zip(*D.keys())[1]) + 1.5
    H = TH2F('IDs',';x (mm);y (mm)',2*int(xmax),-xmax,xmax,2*int(ymax),-ymax,ymax)
    for (x,y),ID in D.items():
        H.SetBinContent(H.FindBin(x,y),int(ID))
    C = TCanvas()
    H.Draw('text')
    raw_input()


Dxy = LoadTable()
pitch = float(argv[1])
outputfilename = 'edgesipms_{0}.txt'.format(pitch)

PlotSiPMs(Dxy)
#PlotIDs(Dxy)

edge = []
for (x,y),ID in Dxy.items():
    if all( Dxy.get((xi,yi)) for xi in [x-pitch,x+pitch] for yi in [y-pitch,y+pitch] ): continue
    edge.append( int(ID) )

open(outputfilename,'w').write('#EdgeSiPMs\n' + '\n'.join(map(str,sorted(edge))) + '\n')







