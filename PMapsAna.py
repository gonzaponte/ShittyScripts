"""
    Analyze PMaps.
"""

from Centella.AAlgo import AAlgo
from Centella.physical_constants import *
from Centella.cerrors import *
from operator import itemgetter

from ROOT import *

failed = gSystem.Load("$GATE_DIR/lib/libGATE")
if failed: raise CImportError("GATE_DIR path not defined!")

class PMapsAna(AAlgo):
    """
        PMaps analyzer.
    """
    def __init__(self,param=False,level = 1,label="",**kargs):
        """
            Initialize members and take input arguments
        """

        self.name = 'PMapsAna'
        AAlgo.__init__(self,param,level,self.name,0,label,kargs)


    def initialize(self):
        self.m.log(1,'+++Starting PMapsAna algorithm.')

        self.rcut     = self.doubles.get("Rcut")
        self.ZcutMin  = self.doubles.get("ZcutMin")
        self.ZcutMax  = self.doubles.get("ZcutMax")
        self.MakeRcut = not (self.rcut is None)
        self.MakeZcut = not (self.ZcutMin is None) and not (self.ZcutMax is None)

        NbinsE   = self.ints   .get("NbinsE"  , 1000 )
        NbinsQ   = self.ints   .get("NbinsQ"  , 1000 )
        NbinsQE  = self.ints   .get("NbinsQE" , 1000 )
        NbinsR   = self.ints   .get("NbinsR"  , 200  )
        NbinsXY  = self.ints   .get("NbinsXY" , 200  )
        NbinsZ   = self.ints   .get("NbinsZ"  , 100  )
        Nslices  = self.ints   .get("Nslices" , 25   )
        Nsignals = self.ints   .get("Nsignals",  4   )
        Nsipms   = self.ints   .get("Nsipms"  ,  20  )
        Qsipms   = self.doubles.get("Qsipms"  ,  20  )
        Emin     = self.doubles.get("Emin"    ,  0.  )
        Emax     = self.doubles.get("Emax"    , 14e5 )
        Qmin     = self.doubles.get("Qmin"    ,  0.  )
        Qmax     = self.doubles.get("Qmax"    , 35e3 )
        QEmin    = self.doubles.get("QEmin"   ,  0.  )
        QEmax    = self.doubles.get("QEmax"   ,  3.  )
        Xmin     = self.doubles.get("Xmin"    , -220.)
        Xmax     = self.doubles.get("Xmax"    , +220.)
        Ymin     = self.doubles.get("Ymin"    , -220.)
        Ymax     = self.doubles.get("Ymax"    , +220.)
        Rmin     = self.doubles.get("Rmin"    ,    0.)
        Rmax     = self.doubles.get("Rmax"    ,  220.)
        Zmin     = self.doubles.get("Zmin"    , -300.)
        Zmax     = self.doubles.get("Zmax"    , +300.)

        self.hman.h1('hE'     ,'Cathode signal;# of photons;Entries',NbinsE,Emin,Emax)
        self.hman.h1('hQ'     ,'Anode signal;# of photons;Entries',NbinsQ,Qmin,Qmax)
        self.hman.h1('hQoverE','Anode/cathode ratio;ratio;Entries',NbinsQE,QEmin,QEmax)
        self.hman.h1('hZ'     ,'Event z;Event z (mm);Entries',NbinsZ,Zmin,Zmax)
        self.hman.h2('hXY'    ,'Event xy;x (mm);y (mm);Entries',NbinsXY,Xmin,Xmax,NbinsXY,Ymin,Ymax)
        self.hman.h1('hR'     ,'Event r;Event r (mm);Entries',NbinsR,Rmin,Rmax)
        self.hman.h1('hNsl'   ,'# slices;Number of slices;Entries',Nslices,0,Nslices)
        self.hman.h1('hNsig'  ,'# S2 signals;# S2 signals;Entries',Nsignals,0,Nsignals)
        self.hman.h1('hNsipms','# SiPMs touched;# SiPMs touched;Entries',Nsipms,0,Nsipms)
        self.hman.h1('hQsipms','SiPMs charge;Q (pes);Entries',Qsipms,0,Qsipms)
        self.hman.h2('hQshape','SiPMs charge ordered;# ;Q (pes);Entries',Nsipms,0,Nsipms,100,0,1.1)

        self.hman.h2('hQvsE'  ,'Anode signal vs cathode signal;# of photons;# of photons',NbinsE,Emin,Emax,NbinsQ,Qmin,Qmax)
        self.hman.h2('hEvsZ'  ,'Cathode signal vs event Z;Average z (mm);# of photons',NbinsZ,Zmin,Zmax,NbinsE,Emin,Emax)
        self.hman.h2('hQvsZ'  ,'Anode signal vs event Z;Average z (mm);# of photons',NbinsZ,Zmin,Zmax,NbinsQ,Qmin,Qmax)
        self.hman.h2('hEvsR'  ,'Cathode signal vs event R;Average r (mm);# of photons',NbinsR,Rmin,Rmax,NbinsE,Emin,Emax)
        self.hman.h2('hQvsR'  ,'Anode signal vs event R;Average r (mm);# of photons',NbinsR,Rmin,Rmax,NbinsQ,Qmin,Qmax)
        self.hman.h2('hNslvsZ','# slices vs z;z (mm);# slices',NbinsZ,Zmin,Zmax,Nslices,0,Nslices)
        self.hman.p1('hShapeE','Event shape;slice - max slice;# of photons',2*Nslices,-Nslices,Nslices,0.,Emax)
        self.hman.p1('hShapeQ','Event shape;slice - max slice;# of photons',2*Nslices,-Nslices,Nslices,0.,Qmax)
        self.hman.h3('hEvsXY' ,'Cathode signal vs XY position;x (mm);y (mm);#photons',NbinsXY,Xmin,Xmax,NbinsXY,Ymin,Ymax,NbinsE,Emin,Emax)
        self.hman.h3('hQvsXY' ,'Anode signal vs XY position;x (mm);y (mm);#photons',NbinsXY,Xmin,Xmax,NbinsXY,Ymin,Ymax,NbinsQ,Qmin,Qmax)
        self.hman.h2('hZeroQ' ,'0Q events;z (mm);r (mm)',NbinsZ,Zmin,Zmax,NbinsR,Rmin,Rmax)

    def GetAveragePosition(self,evt):
        hits = evt.GetMCHits()
        X,Y,Z = 0.,0.,0.
        norm = 0.
        if not hits.size(): return -1e12, -1e12, -1e12
        for i in range( hits.size() ):
            pos = hits[i].GetPosition()
            ene = hits[i].GetAmplitude()
            X += pos.x() * ene
            Y += pos.y() * ene
            Z += pos.z() * ene
            norm += ene
        return X / norm, Y / norm, Z / norm

    def FindOutestHit(self,evt):
        hits = evt.GetMCHits()
        Rmax = 0.
        for i in range( hits.size() ):
            pos = hits[i].GetPosition()
            r2 = pos.x()**2 + pos.y()**2
            Rmax = max( Rmax, r2 )
        return Rmax**0.5

    def execute(self,event=None):
        X0, Y0, Z0 = self.GetAveragePosition(event)
        R0         = ( X0**2 + Y0**2 )**0.5
        S2signals  = filter( lambda signal: signal.GetSignalType() == gate.S2, event.GetSignals() )

        if self.MakeZcut and not (ZcutMin<= Z0 <= ZcutMax): return False
        if self.MakeRcut and self.FindOutestHit(event) > self.rcut: return False

        self.hman.fill( 'hNsig', len(S2signals) )

        if len(S2signals)>1: return False

        self.hman.fill('hXY',X0,Y0)
        self.hman.fill('hZ',Z0)
        self.hman.fill('hR',R0)

        for S2signal in S2signals:
            Q = { 'E':0., 'Q':0. }
            cathode_map = S2signal.GetCatHitMap()
            anode_map   = S2signal.GetAnoHitMap()

            nslices = len(cathode_map.GetTimeMap())

            max_index = sorted( enumerate([ sum( cathode_map.GetAmplitudes(i) ) for i in range(nslices) ]), key = itemgetter(1) )[-1][0]

            for Imap,plane in zip([cathode_map,anode_map],['E','Q']):
                if plane == 'Q':
                    maxq =max( q for q in Imap.GetAmplitudes(max_index) )
                    if maxq:
                        nsipms  = len(Imap.GetAmplitudes(max_index))
                        self.hman.fill('hNsipms',nsipms)
                        for i,q in enumerate(sorted( [q for q in Imap.GetAmplitudes(max_index)], reverse = True )):
                            self.hman.fill('hQshape',i,q/maxq)

                for i in range(nslices):
                    for q in Imap.GetAmplitudes(i):
                        self.hman.fill('hQsipms',q)
                    Qsl = sum( Imap.GetAmplitudes(i) )
                    Q[plane] += Qsl

                    self.hman.fill('hShape'+plane,i-max_index,Qsl)

            E, Q = Q['E'], Q['Q']
            self.hman.fill('hNsl',nslices)

            self.hman.fill('hNslvsZ',Z0,nslices)
            self.hman.fill('hE',E)
            self.hman.fill('hQ',Q)
            self.hman.fill('hQoverE',Q/E)
            self.hman.fill('hQvsE',E,Q)
            self.hman.fill('hEvsZ',Z0,E)
            self.hman.fill('hQvsZ',Z0,Q)
            self.hman.fill('hEvsR',R0,E)
            self.hman.fill('hQvsR',R0,Q)
            self.hman.fill('hEvsXY',X0,Y0,E)
            self.hman.fill('hQvsXY',X0,Y0,Q)

            if E == Q == 0.0:
                self.hman.fill('hZeroQ',Z0,R0)

        return True

    def finalize(self):
        self.m.log(1,'+++Ending PMapsAna algorithm.')

        names = 'hEvsR','hQvsR','hEvsZ','hQvsZ','hQvsE','hNslvsZ'
        for name in names:
            h = self.hman[name].ProfileX(name+'_profile'); h.SetLineColor(kRed); h.SetLineWidth(2)
            self.hman[name+'_profile'] = h
        names = 'hEvsXY','hQvsXY'
        for name in names:
            h = self.hman[name].Project3DProfile('xy_profile'); h.SetLineColor(kRed); h.SetLineWidth(2)
            self.hman[name+'_profile'] = h
        #
        # h = self.hman['hEvsR'].ProfileX('hEvsR_profile'); h.SetLineColor(kRed); h.SetLineWidth(2)
        # h = self.hman['hQvsR'].ProfileX('hQvsR_profile'); h.SetLineColor(kRed); h.SetLineWidth(2)
        # h = self.hman['hEvsZ'].ProfileX('hEvsZ_profile'); h.SetLineColor(kRed); h.SetLineWidth(2)
        # h = self.hman['hQvsZ'].ProfileX('hQvsZ_profile'); h.SetLineColor(kRed); h.SetLineWidth(2)
        # h = self.hman['hQvsE'].ProfileX('hQvsE_profile'); h.SetLineColor(kRed); h.SetLineWidth(2)
        # h = self.hman['hEvsXY'].Project3DProfile('hEvsXY_profile')
        # h = self.hman['hQvsXY'].Project3DProfile('hQvsXY_profile')

        return
