from ROOT import *
from math import *

hcos = TH1F('cos','',200,-1,1)
hphi = TH1F('phi','',200,0,2*pi)
gdis = TGraph()
gsph = TGraph2D()

Nsipms = 200
factor = 2.0 / Nsipms
twopi  = 2 * pi

gratio = ( sqrt(5) - 1 ) * 0.5
gangle = gratio * twopi

for i in range(Nsipms):
    phi = (gangle * i) % twopi
    theta = acos( 1 - i * factor )
    hcos.Fill( cos(theta) )
    hphi.Fill( phi )
    gsph.SetPoint(i,sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta))

x = gsph.GetX()
y = gsph.GetY()
z = gsph.GetZ()

ii = 0
for i in range(Nsipms):
    x0, y0, z0 = x[i], y[i], z[i]
    drs = sorted( [ (x[j]-x0)**2 + (y[j]-y0)**2 + (z[j]-z0)**2 for j in range(i+1,Nsipms) ] )
    for j,dr in enumerate(drs):
        gdis.SetPoint( ii, j, dr )
        ii += 1

gdis.SetMarkerStyle(20)

c1 = TCanvas();hcos.Draw()
c2 = TCanvas();hphi.Draw()
c3 = TCanvas();gsph.Draw('ATRI')
c4 = TCanvas();gdis.Draw('AP')

raw_input('aaa')
