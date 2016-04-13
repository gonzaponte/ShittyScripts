from ROOT import *
from math import *

def f(x,y):
    z = -17 * int(x) - int(y) % 17
    z = 2 ** z * int( y // 17 )
    return int( 0.5 < int( z % 2 ) )

f = lambda x,y: int( 0.5 < int( ( 2 ** ( -17 * int(x) - int(y) % 17 ) * int(y//17) ) % 2 ) )

k = 5318008


h = TH2F('h',str(k),106,0,106,17,k,k+17)

for x in range(106):
    print x
    for y in range(k):
        h.SetBinContent( h.GetBin(x+1,y+1), f(x,k+y) )

h.Draw('zcol')
raw_input('done')