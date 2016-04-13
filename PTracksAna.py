"""
    Analyze PTracks.
"""

from Centella.AAlgo import AAlgo
from Centella.physical_constants import *
from Centella.cerrors import *
from operator import itemgetter

from ROOT import *

failed = gSystem.Load("$GATE_DIR/lib/libGATE")
if failed: raise CImportError("GATE_DIR path not defined!")

class PTracksAna(AAlgo):
    """
        PTracks analyzer.
    """
    def __init__(self,param=False,level = 1,label="",**kargs):
        """
            Initialize members and take input arguments
        """

        self.name = 'PTracksAna'
        AAlgo.__init__(self,param,level,self.name,0,label,kargs)


    def initialize(self):
        self.m.log(1,'+++Starting PTracksAna algorithm.')

        self.rcut     = self.doubles.get("Rcut")
        self.ZcutMin  = self.doubles.get("ZcutMin")
        self.ZcutMax  = self.doubles.get("ZcutMax")
        self.MakeRcut = not (self.rcut is None)
        self.MakeZcut = not (self.ZcutMin is None) and not (self.ZcutMax is None)

        NbinsE   = self.ints   .get("NbinsE"  , 200 )
        NbinsQ   = self.ints   .get("NbinsQ"  , 200 )
        NbinsEh  = self.ints   .get("NbinsEh" , 200 )
        NbinsP   = self.ints   .get("NbinsP"  , 100 )
        NbinsR   = self.ints   .get("NbinsR"  , 100 )
        NbinsXY  = self.ints   .get("NbinsXY" , 100 )
        NbinsZ   = self.ints   .get("NbinsZ"  , 100 )
        NbinsL   = self.ints   .get("NbinsL"  , 100 )
        Nhits    = self.ints   .get("Nhits"   , 25  )
        Ntracks  = self.ints   .get("Ntracks" ,  4  )
        Emin     = self.doubles.get("Emin"    , 0.0 )
        Emax     = self.doubles.get("Emax"    , 1.0 )
        Qmin     = self.doubles.get("Qmin"    , 0.0 )
        Qmax     = self.doubles.get("Qmax"    , 1.0 )
        Erawmin  = self.doubles.get("Erawmin" , 0.0 )
        Erawmax  = self.doubles.get("Erawmax" , 1.0 )
        Ehmin    = self.doubles.get("Ehmin"   , 0.0 )
        Ehmax    = self.doubles.get("Ehmax"   , 1.0 )
        Xmin     = self.doubles.get("Xmin"    , -20.)
        Xmax     = self.doubles.get("Xmax"    , +20.)
        Ymin     = self.doubles.get("Ymin"    , -20.)
        Ymax     = self.doubles.get("Ymax"    , +20.)
        Zmin     = self.doubles.get("Zmin"    , -3. )
        Zmax     = self.doubles.get("Zmax"    , +3. )
        Pmin     = self.doubles.get("Pmin"    ,   0.)
        Pmax     = self.doubles.get("Pmax"    ,  25.)
        Rmin     = self.doubles.get("Rmin"    ,   0.)
        Rmax     = self.doubles.get("Rmax"    ,  35.)
        Lmin     = self.doubles.get("Lmin"    ,   0.)
        Lmax     = self.doubles.get("Lmax"    ,  35.)

        self.hman.h1('hQ'       ,'Event charge;Q (pes);Entries',NbinsQ,Qmin,Qmax)
        self.hman.h1('hEraw'    ,'Event energy;E (pes);Entries',NbinsE,Erawmin,Erawmax)
        self.hman.h1('hEcorr'   ,'Event energy;E (pes);Entries',NbinsE,Emin,Emax)
        self.hman.h2('hEvsE0'   ,'Corrected vs raw energy;E raw (pes);E corrected(pes)',NbinsE,Erawmin,Erawmax,NbinsE,Emin,Emax)
        self.hman.h2('hEvsR'    ,'Corrected energy vs event R;r (mm);E (pes)',200,0,225,NbinsE,Emin,Emax)
        self.hman.h2('hEvsZ'    ,'Corrected energy vs event Z;z (mm);E (pes)',300,-300,300,NbinsE,Emin,Emax)
        self.hman.h1('hEhits'   ,'Hits energy;E (pes);Entries',NbinsEh,Ehmin,Ehmax)
        self.hman.h1('hLength'  ,'Tracks length;l (mm);Entries',NbinsL,Lmin,Lmax)
        self.hman.h1('hdZ'      ,'z deviation;dz (mm);Entries',NbinsZ,Zmin,Zmax)
        self.hman.h2('hdXY'     ,'xy deviation;dx (mm);dy (mm);Entries',NbinsXY,Xmin,Xmax,NbinsXY,Ymin,Ymax)
        self.hman.h2('hpullXY'  ,'xy pull;x pull;y pull;Entries',100,-5,5,100,-5,5)
        self.hman.h1('hdp'      ,'radial deviation;d#rho (mm);Entries',NbinsP,Pmin,Pmax)
        self.hman.h1('hdR'      ,'Full deviation;dr (mm);Entries',NbinsR,Rmin,Rmax)
        self.hman.h1('hNhits'   ,'# hits;# hits;Entries',Nhits,0,Nhits)
        self.hman.h1('hNtracks' ,'# tracks;# tracks;Entries',Ntracks,0,Ntracks)

        self.hman.h2('hdpvsDist','radial deviation vs dist to max SiPM;distance (mm);dr (mm)',100,0.,7.07,NbinsP,Pmin,Pmax)
        self.hman.h2('hQvsDist' ,'event Q vs dist to max SiPM;distance (mm);event Q (pes)',100,0.,7.07,NbinsQ,Qmin,Qmax)

        self.hman.h2('h0tracks' ,'r-z distribution;z (mm);r (mm)',100,-300,300,200,0,225)
        self.hman.h1('hS1charge','S1charge;S1 charge (pes);Entries',40,0,40)

    def GetAveragePosition(self,evt,mc=False):
        X,Y,Z,norm = 0.,0.,0.,0.

        hits = evt.GetMCHits() if mc else [ hit for track in evt.GetTracks() for hit in track.GetHits() ]
        if not hits: return [-1e12]*3
        for hit in hits:
            pos = hit.GetPosition()
            ene = hit.GetAmplitude()
            X += pos.x() * ene
            Y += pos.y() * ene
            Z += pos.z() * ene
            norm += ene
            #print mc, pos.x(),pos.y(),pos.z(),ene
        return X / norm, Y / norm, Z / norm

    def FindOutestHit(self,evt):
        hits = evt.GetMCHits()
        Rmax = 0.
        for i in range( hits.size() ):
            pos = hits[i].GetPosition()
            r2 = pos.x()**2 + pos.y()**2
            Rmax = max( Rmax, r2 )
        return Rmax**0.5

    def ComputeRawSignals( self, event ):
        S2signals  = filter( lambda signal: signal.GetSignalType() == gate.S2, event.GetSignals() )
        E = 0.
        Q = 0.
        for S2signal in S2signals:
            cathode_map = S2signal.GetCatHitMap()
            anode_map   = S2signal.GetAnoHitMap()
            E += sum( sum( cathode_map.GetAmplitudes(i) ) for i in range(len(cathode_map.GetTimeMap())) )
            Q += sum( sum(   anode_map.GetAmplitudes(i) ) for i in range(len(  anode_map.GetTimeMap())) )
        return E/12., Q

    def ComputeS1charge(self, event):
        S1signals = filter( lambda signal: signal.GetSignalType() == gate.S1, event.GetSignals() )
        Q = 0.
        for S1signal in S1signals:
            cathode_map = S1signal.GetCatHitMap()
            Q += sum( sum( cathode_map.GetAmplitudes(i) ) for i in range(len(cathode_map.GetTimeMap())) )
        return Q

    def execute(self,event=None):
        Xt, Yt, Zt = self.GetAveragePosition(event,True)
        Xr, Yr, Zr = self.GetAveragePosition(event,False)
        Rt = (Xt**2 + Yt**2)**0.5
        dx = Xr - Xt
        dy = Yr - Yt
        dz = 274.5 - Zr - Zt
        dp = ( dx**2 + dy**2 )**0.5
        dr = ( dp**2 + dz**2 )**0.5

        x2SiPM = Xt - ( round( Xt + 5., -1 ) - 5. )
        y2SiPM = Yt - ( round( Yt + 5., -1 ) - 5. )
        d2SiPM = ( x2SiPM**2 + y2SiPM**2 )**0.5

        if self.MakeZcut and not (ZcutMin<= Zt <= ZcutMax): return False
        if self.MakeRcut and self.FindOutestHit(event) > self.rcut: return False

        tracks = event.GetTracks()
        self.hman.fill( 'hNtracks', len(tracks) )
        self.hman.fill( 'hdXY', dx, dy)
        self.hman.fill( 'hpullXY', dx, dy)
        self.hman.fill( 'hdZ' , dz )
        self.hman.fill( 'hdp' , dp )
        self.hman.fill( 'hdR' , dr )

        if not len(tracks):
            S1charge = self.ComputeS1charge( event )
            self.hman.fill('h0tracks', Zt, Rt )
            self.hman.fill('hS1charge', S1charge )

        Eraw, Q = self.ComputeRawSignals( event )
        Ecorr = 0.
        for track in tracks:
            length = track.GetLength()
            hits   = track.GetHits()

            self.hman.fill( 'hLength', length )
            self.hman.fill( 'hNhits', len(hits) )

            E = 0.
            for hit in hits:
                E += hit.GetAmplitude()
                self.hman.fill( 'hEhits', hit.GetAmplitude() )

            Ecorr += E

        self.hman.fill( 'hQ'    , Q     )
        self.hman.fill( 'hEraw' , Eraw  )
        self.hman.fill( 'hEcorr', Ecorr )
        self.hman.fill( 'hEvsE0', Eraw, Ecorr )
        self.hman.fill( 'hEvsR' ,   Rt, Ecorr )
        self.hman.fill( 'hEvsZ' ,   Zt, Ecorr )

        if Rt < 150.:
            self.hman.fill( 'hdpvsDist', d2SiPM, dp )
            self.hman.fill( 'hQvsDist' , d2SiPM,  Q )
        return True

    def finalize(self):
        self.m.log(1,'+++Ending PTracksAna algorithm.')

        self.hman['hdX'] = self.hman['hdXY'].ProjectionX('hdX')
        self.hman['hdY'] = self.hman['hdXY'].ProjectionY('hdY')
        self.hman['hpullX'] = self.hman['hpullXY'].ProjectionX('hpullX')
        self.hman['hpullY'] = self.hman['hpullXY'].ProjectionY('hpullY')

        self.hman['hDist'] = self.hman['hdpvsDist'].ProjectionX('hDist')
        hnames = 'hdpvsDist','hQvsDist'

        for hname in hnames:
            h = self.hman[hname].ProfileX(hname+'_profile'); h.SetLineColor(kRed); h.SetLineWidth(2)
            self.hman[hname+'_profile'] = h

        h = self.hman['hdXY'].ProfileX('hdX_profile'); h.SetLineColor(kRed); h.SetLineWidth(2)
        self.hman['hdX_profile'] = h
        h = self.hman['hdXY'].ProfileY('hdY_profile'); h.SetLineColor(kRed); h.SetLineWidth(2)
        self.hman['hdY_profile'] = h

        return
