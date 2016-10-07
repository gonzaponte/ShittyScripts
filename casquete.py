from ROOT import *
from math import *

R = TRandom3(0)
Npoints = int(1e5)
Nthetas = 20

G = TGraph()
for j in range(Nthetas):
    theta   = j*pi/Nthetas
    zmin    = cos(theta)
    Ninside = 0.0
    for i in range(Npoints):
        x,y,z = [ R.Gaus(0,1) for i in range(3) ]
        norm  = ( x**2 + y**2 + z**2 )**0.5 / R.Uniform()**(1/3.)
        if z/norm>zmin:
            Ninside += 1
    G.SetPoint(j,theta,Ninside/Npoints * 4*pi/3)

G.SetMarkerStyle(20)
G.Draw('ap')

f = TF1('f','[0]*(cos(x)+2)*(cos(x)-1)^2')
f.SetParameters(5.,1.,0.)
G.Fit(f)
raw_input()