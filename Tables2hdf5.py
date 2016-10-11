import tables as tb
import numpy as np
import time
from NEW_maps_201607 import EL_map,PMT_map,SiPM_map

ID2index = { ID : i for i,ID in enumerate(sorted(SiPM_map)) }

def FindData(f,ID):
    '''
        Find the lines corresponding to a certain ELpointID.
    '''
    return filter( lambda x: x[1] == ID, f )

def GetCathodeData(cdata):
    '''
        Pick the relevant information.
    '''
    return np.array([ float(p[3])*20 for p in sorted(cdata,key=lambda x: int(x[2]))])

def GetAnodeData(adata):
    '''
        Pick the relevant information.
    '''
    x = np.zeros(len(SiPM_map))
    for p in sorted(adata,key=lambda x: int(x[2])):
        x[ID2index[int(p[2])]] = sum(map(float,p[3:]))
    return x

def GetProbabilities( cdata, adata ):
    '''
        Return the array corresponding to some row.
    '''
    return np.concatenate((GetCathodeData(cdata),GetAnodeData(adata)))

def BuildTable(CathodeFileName,AnodeFileName,outFileName):
    '''
        Build the table and store it in a hdf5 file.
    '''
    fcathode = map( str.split, open(CathodeFileName,'r').readlines()[1:] )
    fanode   = map( str.split, open(AnodeFileName,'r').readlines()[1:] )
    
    nsensors = len(PMT_map) + len(SiPM_map)
    tablestr = []
    with tb.open_file(outFileName, "w",filters=tb.Filters(complib="zlib", complevel=1)) as fileOut:
        group = fileOut.create_group(fileOut.root,"GridData")
#        xytable = fileOut.create_table(group, "XY", XYdescription,"ELpointID-XY map",tb.Filters(0))
#        probstable = fileOut.create_table(group, "Probs",ProbDescription,"Probabilities",tb.Filters(0))
        xytable = fileOut.create_earray(fileOut.root.GridData, "XY",
                                        atom=tb.Float32Atom(),
                                        shape=(0, 2),
                                        expectedrows=len(EL_map))
                                        
        probstable = fileOut.create_earray(fileOut.root.GridData, "Probabilities",
                                           atom=tb.Float32Atom(),
                                           shape=(0, nsensors),
                                           expectedrows=len(EL_map))
                                           
        t0 = time.time()
        for ELpointID,xy in sorted(EL_map.items()):
            if not ELpointID % 10000: print ELpointID, time.time() - t0;t0 = time.time()
            strID = str(ELpointID)
            cathode_data  = FindData(fcathode,strID)
            anode_data    = FindData(fanode,strID)
            
            xytable.append( np.array(xy).reshape((1,2)) )
            probstable.append( GetProbabilities(cathode_data,anode_data).reshape((1,nsensors)) )
    xytable.flush()
    probstable.flush()
    return

if __name__ == '__main__':
    cFileName = '/Users/Gonzalo/Desktop/Tables/ReproducedCathode.txt'
    aFileName = '/Users/Gonzalo/Desktop/Tables/ReproducedAnode.txt'
    oFileName = '/Users/Gonzalo/Desktop/TableS/ReproducedFull.h5'
    BuildTable( cFileName, aFileName, oFileName )

