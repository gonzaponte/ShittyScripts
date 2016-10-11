from ROOT import *
from os import mkdir
from sys import argv

def Usage():
    print '''Usage: python {} [rootfile]'''.format(__file__)
    exit()

if len(argv)<2: Usage()

F = TFile(argv[1],'readonly')

HS = {}
for key in F.GetDirectory("calSi").GetListOfKeys():
    ID = int(''.join( filter( str.isdigit, key.GetName() ) ))
    HS[ID] = key.ReadObj()

Hdummy = HS.values()[0]
S = '#### First ROW is the number of pe corresponding to the center of each bin. Each column is one of those bins. Second ROW onwards contains the number of entries in each bin. Each row corresponds to one SiPM. First column is always the sensor ID.\n'
S += '{}\n'.format(' '.join(map( str, [-10000] + map( Hdummy.GetBinCenter, range(1,Hdummy.GetNbinsX()+1) ) )))

for ID,H in sorted(HS.items()):
    y = map( H.GetBinContent, range(1,H.GetNbinsX()+1) )
    S += '{} {}\n'.format(ID,' '.join(map(str,y)))

open('NoiseSiPM_NEW.dat','w').write(S)


