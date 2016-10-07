from ROOT import *
from Array import *
from math import *
from numpy import loadtxt
from scipy.integrate import quad as integral
from scipy.interpolate import interp1d as interpolate
from Plots import Plot4D


_R = TRandom3(0)

P = 15. # Pressure in bar
T = 20. # Temperature in Celsius

rho = 2.6867774e19 * 131.293 / 6.02214179e23 * P / (T/273.15 + 1)
SPXe_data = loadtxt("xe_stopping_power_NIST.dat")
SPXe_func = interpolate(SPXe_data[:,0],SPXe_data[:,1]*rho, kind="cubic")

E  = lambda p: ( p**2 + 0.511**2 )**0.5
P3 = lambda E: ( E**2 - 0.511**2 )**0.5
sigma = lambda p: 13.6*E(p)/p**2 * 0.01**0.5 * (1+0.038*log(0.01) )


for i in range(1):
    E0    = 2.5 + 0.511
    xyzE  = [Vector4(0.,0.,0.,0.)]
    u     = Vector3(0.,0.,1.)
    while E0>0.511:
        p  = P3(E0)
        dE = min(0.01, E0-0.511); E0 -= dE
        dS = integral( lambda e: 1.0/SPXe_func(e), E0,E0+dE, limit = 1000)[0]
        du = u * dS
        xyzE.append( Vector4(-dE,*(du+xyzE[-1][1]) ) )

        sigmaMS = sigma(p)
        thetaX  = _R.Gaus(0.,sigmaMS)
        thetaY  = _R.Gaus(0.,sigmaMS)
        tanX    = tan(thetaX)
        tanY    = tan(thetaY)

        norm    = sqrt(u[0]**2 + u[1]**2)
        M       = Matrix( Vector(u[1],-u[0],0.)/norm, Vector(-u[0]*u[2],-u[1]*u[2],norm**2)/norm, u ).T() if norm else Identity(3)
        u       = Vector3(* M ** Vector3( tanX, tanY, 1 ).Unit() ).Unit()

    E, xyz = zip(*xyzE); x, y, z = zip(*xyz)
    a = Plot4D(x,y,z,E)
    raw_input()

