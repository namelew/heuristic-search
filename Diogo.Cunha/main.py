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

def chooseNewNode(pheroTable:list, nodo:int, tam:int) -> int: # seleciona a nova cidade baseada em seu feromônio
    pSum = 0
    for i in range(tam):
        pSum += pheroTable[nodo][i]
    
    pRange = 0
    drawn = randint(0, maxsize) % pSum

    i = 0
    for pV in pheroTable[nodo]:
        if drawn > pRange and drawn < (pRange + pV):
            return i
        pRange += pV
        i += 1
    
    opt = [i for i in range(tam)]
    opt.remove(nodo)

    drawn = choice(opt)

    return drawn
        
def exploreNode(instancia:list, nodo:int, pheroTable:list, tam:int): # explora um nodo escolhido
    i = 0
    for distance in instancia[nodo]:
        if i != nodo:
            if pheroTable[nodo][i] == 0 or pheroTable[i][nodo] == 0: 
                pheroTable[nodo][i] = tam/distance
                pheroTable[i][nodo] = tam/distance
        i += 1
    
    drawn = chooseNewNode(pheroTable, nodo, tam)

    return instancia[nodo][drawn], drawn

def BCCF(instancia:list, pheroTable:list,tam:int): # algoritmo principal da busca por colônia de formigas
    solution = []

    current = randint(0, tam-1)
    solution.append(current)
    best = 0

    while(len(solution) < tam):
        custo,current = exploreNode(instancia, current, pheroTable, tam)
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
files = ["Djibouti",  "Qatar",  "Uruguay",  "Zimbabwe", "Western Sahara"]
li = [38, 194, 734, 929, 29] # tamanho de cada uma das instâncias
output = []
for file in files: # carregando a matrix de adjacência
    array = np.fromfile("Instâncias/"+file+".bin")
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
    pheroTable = [] # tabela de mapeamento de feromônios
    for j in range(tam):
        pheroTable.append([0 for k in range(tam)])
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