from ROOT import *


F = TFile( "/Users/Gonzalo/github/elparametrization/PyScripts/ParamBuilder/output/NEXT100_S2SiPMparametrization_plots.root")

M = TMultiGraph()
for ID in range(2):
    f = F.Get("fit_" + str(ID))

    G = TGraph()

    pitch   = 1e-3
    npoints = int(f.GetXmax()/pitch) - 1
    j=0
    for i in range(npoints):
        x0 = i * pitch
        x1 = x0 + pitch * 0.99999
        try:
            G.SetPoint(i-j,x0,abs(1-f.Eval(x1)/f.Eval(x0))+1e-8)
        except:
            j += 1
    M.Add(G)
C = TCanvas()
M.SetTitle("Sampling error with a {0} mm pitch;Distance to center (mm);Relative sampling error".format(pitch))
M.Draw('ap')
C.Modified()
C.SaveAs("sampling_error_{0}.png".format(pitch))