from math import *

# Creo sabe dios cantas particulas (4 millons) entre -50 e +50
v = []
for x in [ -50. + i for i in range(100) ]:
    for y in [ -50. + j for j in range(100) ]:
        for z in [ -50. + k for k in range(100) ]:
            v.append( [x, y, z] )
            v.append( [x, y + 0.5, z + 0.5] )
            v.append( [x + 0.5, y + 0.5, z] )
            v.append( [x + 0.5, y, z + 0.5] )

# Comprobo a distancia ao (0,0,0) porque collo esa particula como referencia
d = [ sqrt(xi*xi+yi*yi+zi*zi) for xi,yi,zi in v ]

# Conxunto de elementos unicos
dists = sorted(list(set(d)))

# Conto cantas veces aparece cada distancia na lista de distancias (solo as 50 primeiras)
for n,di in enumerate(dists[:50]):
    print 'Hai un total de {0} {1}-vecinhos a unha distancia de {2}'.format( d.count(di), n, di )