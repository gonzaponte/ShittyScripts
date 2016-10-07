from ROOT import *

R = TRandom3(0)

N = 1000
M = 1000
C = 3
H = TH1F('a','',2*N,-N,N)

def question():
    return 1 if R.Integer(C) == R.Integer(C) else -0.5

for i in range(M):
    mark = 0
    for j in range(N):
        mark += question()
    H.Fill(mark)

H.Draw()

raw_input('ok')
