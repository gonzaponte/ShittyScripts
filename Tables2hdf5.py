from __future__ import print_function

import time
import numpy  as np
import tables as tb

from NEW_maps_201607 import   EL_map
from NEW_maps_201607 import  PMT_map
from NEW_maps_201607 import SiPM_map


class ProbDescription(tb.IsDescription):
    grid_xy   = tb.Float32Col(shape=2, pos=1) # Grid xy
    sens_id   = tb.Int32Col  (shape=1, pos=2) # SensorIDs
    sens_prob = tb.Float32Col(shape=1, pos=3) # Probabilities


def FindData(f, ID):
    '''
        Find the lines corresponding to a certain ELpointID.
    '''
    return filter(lambda x: x[1] == ID, f)


def GetCathodeData(cdata):
    '''
        Pick the relevant information.
    '''
    return { int(p[2]) : float(p[3])*20 for p in cdata }


def GetAnodeData(adata):
    '''
        Pick the relevant information.
    '''
    return {int(p[2]) : sum(map(float, p[3:])) for p in adata}


def FillProbabilities(cdata, adata, table, xy0):
    '''
        Return the array corresponding to some row.
    '''
    row  = table.row
    cath = GetCathodeData(cdata)
    anod = GetAnodeData  (adata)
    for probs, sensormap in zip([cath, anod], [PMT_map, SiPM_map]):
        for ID, prob in probs.items():
            row['grid_xy'  ] = np.array(xy0)
            row['sens_id'  ] = ID
            row['sens_prob'] = prob
            row.append()
    table.flush()


def FillSensorTable(table):
    for sensormap in [PMT_map, SiPM_map]:
        for ID, (x, y) in sorted(sensormap.items()):
            sns = np.array([ID, x, y])
            table.append(sns.reshape(1, 3))
    table.flush()


def BuildTable(CathodeFileName, AnodeFileName, outFileName):
    '''
        Build the table and store it in a hdf5 file.
    '''
    fcathode = map(str.split, open(CathodeFileName, 'r').readlines()[1:])
    fanode   = map(str.split, open(AnodeFileName  , 'r').readlines()[1:])
    
    comp = tb.Filters(complib="zlib", complevel=1)
    with tb.open_file(outFileName, "w",
                      filters = comp) as fileOut:
        sens_group = fileOut.create_group(fileOut.root, "Sensors")
        prob_group = fileOut.create_group(fileOut.root, "Probabilities")
        sens_table = fileOut.create_earray(fileOut.root.Sensors, "XY",
                                           atom         = tb.Float32Atom(),
                                           shape        = (0, 3),
                                           expectedrows = len(PMT_map) + len(SiPM_map))
                                           
        FillSensorTable(sens_table)
        prob_table = fileOut.create_table(prob_group,
                                          "data",
                                          ProbDescription,
                                          "probability map",
                                          comp)
        
        t0 = time.time()
        for ELpointID, xy0 in sorted(EL_map.items()):
            if not ELpointID % 10000:
                print(ELpointID, time.time() - t0)
                t0 = time.time()

            strID         = str(ELpointID)
            cathode_data  = FindData(fcathode, strID)
            anode_data    = FindData(fanode  , strID)
            FillProbabilities(cathode_data,
                              anode_data,
                              prob_table,
                              xy0)
    return

if __name__ == '__main__':
    cFileName = '/Users/Gonzalo/Desktop/Tables/ReproducedCathode.txt'
    aFileName = '/Users/Gonzalo/Desktop/Tables/ReproducedAnode.txt'
    oFileName = '/Users/Gonzalo/Desktop/Tablesta/ReproducedFull.h5'
    BuildTable(cFileName, aFileName, oFileName)

