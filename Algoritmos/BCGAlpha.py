import numpy as np
from random import choice, randint
from sys import maxsize
from time import time
import pandas as pd
class OutputInstancia: # classe par a organizar os dados de saida
    def __init__(self, name:str):
        self.name = name
        self.solutions = []
        self.time = []
    def avgQ(self): # retorna q-medio
        sum = 0
        tam = len(self.solutions)
        for solution in self.solutions:
            sum += solution
        return round(sum/tam, 0)
    def dispersionQ(self): # retorna q-desvio
        tam = len(self.solutions)
        mean = self.avgQ()
        variacy = 0
        for solution in self.solutions:
            variacy += (solution - mean) ** 2
        return round((variacy/tam) ** 0.5, 2)
    def avgT(self): # retorna t-medio
        tam = len(self.time)
        sum = 0
        for solution in self.time:
            sum += solution
        return round(sum/tam, 0)

def createInterval(n:int) -> int: # retorna por quantos segundos uma instância será executada
    return round((n * 60)/1000, 0)

def exploreNode(instancia:list, nodo:int, unvisited:list, tam:int): # explora um nodo escolhido
    sample = []

    unvisited.sort(key=lambda x:instancia[nodo][x])

    sampleTam = round(tam * 0.3)

    for i in unvisited:
        if(len(sample) == sampleTam):
            break
        sample.append(i)
    
    drawn = choice(sample)

    while (drawn == nodo):
        drawn = choice(sample)

    unvisited.remove(drawn)

    return instancia[nodo][drawn], drawn

def glutonSearch(instancia:list, tam:int): # algoritmo principal da busca gulosa
    unvisited = [i for i in range(tam)] # controla nodos que ainda não foram visitados

    current = randint(0, tam-1)
    unvisited.remove(current)
    best = 0

    while(len(unvisited) > 0):
        custo,current = exploreNode(instancia, current, unvisited, tam)
        best += custo
    
    return best

instancias = []
files = ["Djibouti",  "Qatar",  "Uruguay",  "Zimbabwe", "Western Sahara"]
li = [38, 194, 734, 929, 29] # tamanho de cada uma das instâncias
output = []
for file in files: # carregando a matrix de adjacência
    array = np.fromfile("../Diogo.Cunha/Instâncias/"+file+".bin")
    temp = array.tolist()
    pos = files.index(file)
    graph = [[] for i in range(li[pos])]
    for i in range(len(temp)):
        graph[i%li[pos]].append(temp[i])
    instancias.append(graph)
# main
for i in range(len(files)):
    tam = len(instancias[i])
    output.append(OutputInstancia(files[i]))
    print(f"Starting {output[i].name}")
  
    for max in range(10):
        start = time()
        best = maxsize
        while(abs(start - time()) < createInterval(tam)):
            current = glutonSearch(instancias[i], tam)
            if current < best:
                best = current
        output[i].time.append(abs(start-time()))
        output[i].solutions.append(best)
# gera a saída no arquivo resultados.csv
dist_to_csv = {
    "instancia": [data.name for data in output],
    "autoria": ["Diogo.Cunha" for i in range(len(output))],
    "algoritmo": ["BCGα" for i in range(len(output))],
    "q-medio": [int(data.avgQ()) for data in output],
    "q-desvio": [f"{data.dispersionQ():.02f}" for data in output],
    "t-medio": [int(data.avgT()) for data in output]
}
dataframe = pd.DataFrame(dist_to_csv)
dataframe.to_csv('resultados.csv', index=False)