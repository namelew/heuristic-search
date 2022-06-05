from scipy.spatial import distance
import numpy as np
import sys

files = []
for arg in sys.argv:
    if ".py" not in arg:
        files.append(arg)

for file in files:
    name = "../Diogo-Cunha/Instâncias-Origin/"+file+".tsp"
    instancia = open(name)
    conjunto = []
    grafo = []

    for line in instancia.readlines()[7:]:
        node = line.split()
        if node[0].isnumeric():
            conjunto.append((float(node[1]), float(node[2])))
    instancia.close()

    for i in range(len(conjunto)):
        node = []
        for j in range(len(conjunto)):
            dn = distance.euclidean(conjunto[i], conjunto[j])
            node.append(round(dn,0))
        grafo.append(node)
    
    name = "../Diogo-Cunha/Instâncias/"+file+".bin"
    np.array(grafo).tofile(name)