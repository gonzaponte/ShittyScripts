from ROOT import *

f0 = TFile('rootfiles/aftercalib1e7.root')
f1 = TFile('calib_output.root')
f2 = TFile('monitoring_output.root')

def a():
    # f0.cd('lowEcalib')
    # f0.ls()
    # f1.cd('lowEcalib')
    #f1.ls()

    h0 = f0.Get('lowEcalib/x 0.000000 y 0.000000 PMT 0')
    h1 = f1.Get('lowEcalib/x 0.000000 y 50.000000 PMT 0')
    h2 = f2.Get('monitoring/hRaw')

    c0 = TCanvas()
    h0.Draw()
    c1 = TCanvas()
    h1.Draw()
    c2 = TCanvas()
    h2.Draw()
    # c2.SetLogy()

    raw_input()

def b():
    for x in range(-210,220,10):
        for y in range(-210,220,10):
            for pmt in range(12):
                try:
                    h = f1.Get('lowEcalib/x {0}.000000 y {1}.000000 PMT {2}'.format(x,y,pmt))
                    if h.GetEntries() < 100:
                        print x, y, pmt, h.GetEntries()
                        c = TCanvas()
                        h.Draw()
                        c.Update()
                        raw_input('ok')
                        del c
                except:
                    continue
a()
#b()
