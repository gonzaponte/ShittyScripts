from ROOT import *

R = TRandom3(0)
H = TH1F('h','',250,0,5)
m1 = 12.04
m2 = 11.69

for i in range(int(1e6)):
    s1 = R.Poisson(m1)
    s2 = R.Poisson(m2)
    if s2:
        H.Fill( R.Gaus(s1,s1**0.5)/R.Gaus(s2,s2**0.5) )

H.Draw()
raw_input('ok')
