from ROOT import *
from math import *

x = lambda t: 16 * sin(t)**3
y = lambda t: 13 * cos(t) - 5 * cos(2*t) - 3 * cos(3*t) - cos(4*t)

N = 10000
G = TGraph()
for i in range(N):
    t = -pi + i*2*pi/N
    G.SetPoint(i,x(t),y(t))

G.SetLineColor(kRed)
G.SetLineWidth(2)

G.Draw('ac')
raw_input()