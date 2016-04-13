from ROOT import *
from Math import Factorial
from math import exp, log, floor
from scipy import array
from scipy.optimize import minimize

def Poisson(mean):
    def poisson(k):
        # k = floor(k)
        return mean**k * exp(-mean) / Factorial(k)
    return poisson

def logpoisson(k,mean):
    return k*log(mean) - mean - log( Factorial(k) )

def LLH(M):
    llh = 0.
    for I in range(h.GetNbinsX()):
        llh -= h.GetBinContent(1+I) * logpoisson(I,M)
    return llh


R = TRandom3(0)
h = TH1F('poisson','',10,0,10)

mean = R.Uniform(0,4)
print 'real mean', mean

for i in range(100):
    h.Fill( R.Poisson(mean) )

iguess = array([1.0])
outcome = minimize( LLH, iguess )
print outcome
F = TF1('poissonF',Poisson(outcome.x[0]),0,10)

c = TCanvas()
h.Draw()
F.Draw('same')

raw_input()
