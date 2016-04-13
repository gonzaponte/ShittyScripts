from ROOT import *

Hnew = None
Hdemo = None
fnew = TFile('pdf_SiPMs_NEW.root')
fdemo = TFile('PDFs.root')

for dice in range(1,29):
    for i in range(64):
        ID = 1000*dice + i
        name = 'SiPM_' + str(ID) + '_norm'
        h = fnew.Get(name)
        if not Hnew:
            Hnew = h.Clone()
            Hnew.Reset()
        Hnew.Add( h )

for dice in range(1,5):
    for i in range(1,65):
        name = 'DB_' + str(dice) + '__SiPM_' + str(i)
        h = fdemo.Get(name)
        if not Hdemo:
            Hdemo = h.Clone()
            Hdemo.Reset()
        Hdemo.Add( h )

Hnew.Scale( 1.0/(28*64) )
Hdemo.Scale( 1.0/(4*64) )

Hnew.SetLineColor(kRed)

Hnew.Draw()
Hdemo.Draw('same')


Nnew = 0.
Ndemo = 0.

Hnew.Scale( 1.0/Hnew.Integral() )
Hdemo.Scale( 1.0/Hdemo.Integral() )

for i in range( 1, Hnew.GetNbinsX() + 1):
    Nnew += Hnew.GetBinContent(i)
    if Nnew > 0.997:
        print 'NEW', Hnew.GetXaxis().GetBinCenter(i)
        break

for i in range( 1, Hdemo.GetNbinsX() + 1):
    Ndemo += Hdemo.GetBinContent(i)
    if Ndemo > 0.997:
        print 'DEMO', Hdemo.GetXaxis().GetBinCenter(i)
        break


raw_input('done')
