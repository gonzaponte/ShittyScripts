from RandomNumbers import MersenneTwister
from Math import Factorial
from ROOT import *

class Dice:
    RNG = MersenneTwister()
    def Generate(self):
        return self.RNG.Integer(1,7)

outcomes = [ tuple(sorted([i,j,k])) for i in range(1,7) for j in range(1,7) for k in range(1,7)]
unique_outcomes = []
for i in range(1,7):
    for j in range(1,7):
        for k in range(1,7):
            v = tuple(sorted([i,j,k]))
            if v in unique_outcomes: continue
            unique_outcomes.append(v)

outcome_map = { unique : outcomes.count(unique) for unique in unique_outcomes }

#allsame = filter( lambda x: x[0] == x[1] == x[2], unique_outcomes)
#twosame = filter( lambda x: (x[0] == x[1] or x[1] == x[2]) and x[0] != x[2], outcomes)
#alldiff = filter( lambda x: x[0] != x[1] != x[2], unique_outcomes)
#print alldiff
#for w in twosame:
#    print w,sum(w)
#    raw_input()
#print len(allsame), len(twosame), len(alldiff)
#print 6**3,len(outcomes),outcomes
#print 6**3/Factorial(2),len(unique_outcomes),unique_outcomes

Nexperiments = int(1e5)
Ndices = 3
dice = Dice()
H  = TH1I('a','',6*Ndices+1,0,6*Ndices+1)
H2 = TH1I('a','',12,1,13)
Hmap  = TH1I('b','',6,1,7)
Hmap2 = TH1I('c','',12,1,13)

#for i in range(Nexperiments):    
#    diceresult = tuple( sorted( [ dice.Generate() for n in range(Ndices) ] ) )
for diceresult in outcomes:
    #out = -1
    #if diceresult[0] == diceresult[1] == diceresult[2]: out = diceresult[0]
    #elif diceresult[0] != diceresult[1] == diceresult[2]: out = diceresult[0]
    #elif diceresult[0] == diceresult[1] != diceresult[2]: out = diceresult[2]
    #elif diceresult[0] != diceresult[1] != diceresult[2]:
    #    parities = map( lambda x: x%2, diceresult )
    #    if sum(parities) == 0 or sum(parities) == 3: continue
    #    out = diceresult[ parities.index(1 if sum(parities) == 1 else 0) ]
    #        
    dicesum = sum( diceresult )
    #dicesum = out
    H.Fill( dicesum )
    H2.Fill( dicesum - diceresult[0] )
    Hmap.Fill( dicesum % 6 + 1 )
    Hmap2.Fill( 2*(dicesum % 3) + dicesum % 6 )

c = TCanvas()
c.Divide(2,2)
c.cd(1);H.Draw()
c.cd(2);Hmap.Draw()
c.cd(3);H2.Draw()
c.cd(4);Hmap2.Draw()
raw_input()
    
