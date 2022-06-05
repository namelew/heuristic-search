from scipy.spatial import distance
from random import randint
import time

# crinado matrix de adjacencia com as cidades do Saara Oeste
instancia = open("../Diogo-Cunha/Instâncias-Origin/'Western Sahara'.tsp")
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

# algoritmo aleatório para resolução do problema do caxeiro viajante
inicio = 0
custo_min = 0
min_path = []

start = int(time.time())

while (start - int(time.time())) * -1 != 30:
    solucao = []
    aux = inicio
    custo = 0
    for node in range(len(grafo[0])):
        proximo = randint(0, len(grafo[0]) - 1)
        
        if len(solucao) == 28:
            aresta = (aux, inicio)
        else:
            aresta = (aux, proximo)
        custo += grafo[aresta[0]][aresta[1]]
        solucao.append(aresta)
        
        aux = proximo
    if custo < custo_min or custo_min == 0:
        custo_min = custo
        min_path = solucao

print(f"Custo minimo:{custo_min}")
print(f"Solução: {min_path}")