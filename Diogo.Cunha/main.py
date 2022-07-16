import numpy as np
from random import choice, randint
from sys import maxsize
from time import time
import pandas as pd
from math import isinf
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

def chooseNewNode(pheroTable:list, unvisited:set, nodo:int, tam:int) -> int: # seleciona a nova cidade baseada em seu feromônio
    samples = []

    for i in range(tam):
        if i in unvisited:
            samples.append(i)

    pSum = 0
    for sample in samples:
        pSum += pheroTable[nodo][sample]
    
    if pSum != 0:
        pRange = 0
        drawn = randint(0, pSum)
        for sample in samples:
            if i in unvisited and pRange <= drawn <= (pRange+pheroTable[nodo][sample]):
                return sample
            pRange += pheroTable[nodo][sample]
    opt = []
    for i in range(tam):
        if i in unvisited:
            opt.append(i)
    drawn = choice(opt)

    return drawn

def exploreNode(instancia:list, nodo:int, pheroTable:list, unvisited:set, tam:int): # explora um nodo escolhido
    i = 0
    for distance in instancia[nodo]:
        if i in unvisited:
            newPhero = pheroTable[nodo][i]/distance
            if not isinf(newPhero * 1000) or newPhero <= 4000:
                aux = round(newPhero * 1000, 2)
                pheroTable[nodo][i] = round(aux)
                pheroTable[i][nodo] = round(aux)
            else:
                pheroTable[nodo][i] = 4000
                pheroTable[i][nodo] = 4000
        i += 1
    
    drawn = chooseNewNode(pheroTable, unvisited, nodo, tam)
    unvisited.remove(drawn)

    return instancia[nodo][drawn], drawn

def BCCF(instancia:list, pheroTable:list,tam:int): # algoritmo principal da busca por colônia de formigas
    solution = []
    unvisited = set()
    
    current = randint(0, tam-1)

    for i in range(tam):
        if i != current:
            unvisited.add(i)
    
    solution.append(current)
    best = 0

    while(len(unvisited) > 0):
        custo,current = exploreNode(instancia, current, pheroTable, unvisited, tam)
        solution.append(current)
        best += custo
    
    return solution,best

def reinforcePhero(pheroTable:list, solution:list, tam:int): # fortalece os feromônios de todos os nodos que aparecem na solução
    for i in range(tam - 1):
        pheroTable[solution[i]][solution[i + 1]] = pheroTable[solution[i]][solution[i + 1]] * 1.2
        pheroTable[solution[i + 1]][solution[i]] = pheroTable[solution[i + 1]][solution[i]] * 1.2
    pheroTable[solution[i]][solution[0]] = pheroTable[solution[i]][solution[0]] * 1.2
    pheroTable[solution[0]][solution[i]] = pheroTable[solution[0]][solution[i]] * 1.2

def diminishPhero(pheroTable:list, solution:list, tam:int): # enfraquece os feromônios
    for i in range(tam - 1):
        pheroTable[solution[i]][solution[i + 1]] = pheroTable[solution[i]][solution[i + 1]] * 0.8
        pheroTable[solution[i + 1]][solution[i]] = pheroTable[solution[i + 1]][solution[i]] * 0.8
    pheroTable[solution[i]][solution[0]] = pheroTable[solution[i]][solution[0]] * 0.8
    pheroTable[solution[0]][solution[i]] = pheroTable[solution[0]][solution[i]] * 0.8

instancias = []
files = ["Western Sahara", "Djibouti",  "Qatar",  "Uruguay", "Zimbabwe"]
li = [29, 38, 194, 734, 929] # tamanho de cada uma das instâncias
output = []
for file in files: # carregando a matrix de adjacência
    array = np.fromfile("Instâncias/"+file+".bin")
    temp = array.tolist()
    pos = files.index(file)
    graph = [[] for i in range(li[pos])]
    for i in range(len(temp)):
        graph[i%li[pos]].append(round(temp[i]))
    instancias.append(graph)
# main
for i in range(len(files)):
    tam = len(instancias[i])
    output.append(OutputInstancia(files[i]))
    pheroTable = [] # tabela de mapeamento de feromônios
    for j in range(tam):
        pheroTable.append([tam if j != k else 0 for k in range(tam)])
    print(f"Starting {output[i].name}")
    for max in range(10):
        start = time()
        best = maxsize
        bestPath = [0]
        while(abs(start - time()) < createInterval(tam)):
            solution,current = BCCF(instancias[i], pheroTable, tam)
            if current < best:
                reinforcePhero(pheroTable, solution, tam)
                best = current
                bestPath = solution
            else:
                diminishPhero(pheroTable, solution, tam)
        output[i].time.append(abs(start-time()))
        output[i].solutions.append(best)
# gera a saída no arquivo resultados.csv
dist_to_csv = {
    "instancia": [data.name for data in output],
    "autoria": ["Diogo.Cunha" for i in range(len(output))],
    "algoritmo": ["BCCF" for i in range(len(output))],
    "q-medio": [int(data.avgQ()) for data in output],
    "q-desvio": [f"{data.dispersionQ():.02f}" for data in output],
    "t-medio": [int(data.avgT()) for data in output]
}
dataframe = pd.DataFrame(dist_to_csv)
dataframe.to_csv('resultados.csv', index=False)