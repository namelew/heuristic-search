import numpy as np
from random import shuffle
from time import time
import pandas as pd
class OutputInstancia: # classe par a organizar os dados de saida
    def __init__(self, name):
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

def createInterval(n:int): # retorna por quantos segundos uma instância será executada
    return round((n * 60)/1000, 0)
# param(array, preview_value, after_value, new_index)
def shiffElement(array:list, position:int, new:int):
    if array[position] == array[new]:
        return array
    idn = new
    new = array[idn]

    array.pop(idn)

    array.insert(position, new)
# get the custo of current solution
def getCusto(instancia:list, solution:list):
    custo = 0
    tam = len(solution)
    for j in range(tam):
        if j < tam - 1:
            k = j + 1
        else:
            k = tam - j
        custo += instancia[solution[j]][solution[k]]
    return int(custo)
 
def copy(array:list):
    cp = []
    for v in array:
        cp.append(v)
    return cp
 
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
        # generate seed
        seed = [i for i in range(tam)]
        shuffle(seed)
        # get initial custo_min
        custo_min = getCusto(instancias[i], seed)
        start = time()
        isMinLocal = False # check if algorithm is in a min local
        timeout = False # break the second loop
        # gera um caminho ciclico a partir de uma vizinhança gerada por shift
        while (not isMinLocal):
            j = 1
            while(j < tam):
                changeNeibor = False
                for k in range(j, tam):
                    aux = copy(seed)
                    shiffElement(seed, k, j)
                    custo = getCusto(instancias[i], seed)
                    if abs(start - time()) > createInterval(tam):
                        timeout = True
                        break
                    if custo == custo_min:
                        seed = aux
                        continue
                    if custo > custo_min: # check if the got wost then before
                        seed = aux
                        continue
                    custo_min = custo
                    changeNeibor = True
                    j = 1
                    break
                if timeout or isMinLocal:
                    isMinLocal = True
                    break
                if not changeNeibor:
                    j += 1
        output[i].time.append(abs(start-time()))
        output[i].solutions.append(custo_min)
# gera a saída no arquivo resultados.csv
dist_to_csv = {
    "instancia": [data.name for data in output],
    "autoria": ["Diogo.Cunha" for i in range(len(output))],
    "algoritmo": ["BLPMsh" for i in range(len(output))],
    "q-medio": [int(data.avgQ()) for data in output],
    "q-desvio": [f"{data.dispersionQ():.02f}" for data in output],
    "t-medio": [int(data.avgT()) for data in output]
}
dataframe = pd.DataFrame(dist_to_csv)
dataframe.to_csv('resultados.csv', index=False)