from scipy.spatial import distance
import datetime
import sys

class Node:
    def __init__(self, node, before, custo):
        self.node = node
        self.custo = custo
        self.before = before
        self.visited = False

def explore(caminhos):
    mini = sys.maxsize
    new = 0
    for i in range(len(caminhos) - 1):
        if not caminhos[i].visited and caminhos[i].custo < mini:
            new = i
    return new

def dijkstraMinorPath(grafo, inicio):
    nodos = []
    path = []
    
    for i in range(len(grafo[0])):
        nodos.append(Node(i, -1, sys.maxsize))
    nodos.append(Node(inicio, -1, sys.maxsize))
    
    nodos[inicio].custo = 0
    
    for i in range(len(grafo[0])):
        current = explore(nodos)
        nodos[current].visited = True
        
        path.append(current)
        
        for j in range(len(grafo[0])):
            if grafo[current][j] != 0 and not nodos[j].visited and grafo[current][j] < nodos[j].custo:
                nodos[j].custo = grafo[current][j]
                nodos[j].before = current
    nodos[-1].custo = grafo[current][inicio]
    nodos[-1].before = current
    
    path.append(inicio)
    
    return path, nodos

# crinado matrix de adjacencia com as cidades do Saara Oeste
instancia = open('../Diogo-Cunha/Instâncias/argentina.tsp')
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

# brute force - minor path dijkstra

start = datetime.datetime.now()
caminho, solucao = dijkstraMinorPath(grafo, 0)
end = datetime.datetime.now()
custo_min = 0
for nodo in solucao:
  custo_min += nodo.custo
print("Custo minimo",custo_min)
print("Percurso", caminho)
print("Tempo(ms):", int(end.microsecond)-int(start.microsecond))