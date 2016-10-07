from ROOT import *
from sys import argv

if len(argv)<2: print 'Usage: python AveragePSF.py [filename]';exit()

F = TFile( argv[1] )

PSFs = [ F.Get( "fit_{0}".format(i) ) for i in range(12) ]

xMin = -220
xMax = +220
yMin = -220
yMax = +220
pMin =    0
pMax = sum(map( lambda ff: ff.Eval(0), PSFs )) * 1.05

V = ( xMax - xMin ) * ( yMax - yMin ) * ( pMax - pMin )

FiducialR = 215.
InFiducial = lambda r: r > FiducialR

R = TRandom3(0)

nIn = 0.0
npoints = int(1e5)
for i in range( npoints ):
    x = R.Uniform(xMin,xMax)
    y = R.Uniform(yMin,yMax)
    r = (x**2 + y**2)**0.5
    if InFiducial(r): continue
    p = R.Uniform(pMin,pMax)
    if p > sum(map( lambda ff: ff.Eval(r), PSFs )): continue
    nIn += 1.0

print 'Integrated PSF = '
