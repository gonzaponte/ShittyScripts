from General import letters
from RandomNumbers import MersenneTwister
from ROOT import *
from operator import itemgetter
import shelve
import time

t0 = time.time()

letters.append(' ')
R = MersenneTwister()
D = shelve.open('words.shelve',writeback=True)

Nwords = 0#1000000

def word():
    s = ''
    c = R.Choose(letters[:-1])
    while c != ' ':
        s += c
        c = R.Choose(letters)
    return s

for i in range(Nwords):
    w = word()
    D[w] = D.get(w,0) + 1

H = TH1I('a','',20,0,20)
HL = TH1I('b','',25,0,25)
for w,f in D.items():
    n = len(w)
    for i in range(f):
        HL.Fill(n)
for i,(w,f) in enumerate(sorted(D.items(),key=itemgetter(1),reverse=True)[:20]):
    H.SetBinContent(i+1,f)
    H.GetXaxis().SetBinLabel(i+1,w)

H.SetMinimum(0)
HL.SetMinimum(0)
H.Draw()
HL.Draw()

print 'It took {0} s to produce {1} words'.format(time.time() - t0,Nwords)
raw_input()