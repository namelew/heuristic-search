import numpy as np
from random import shuffle
from datetime import datetime
import pandas as pd

class OutputInstancia: # classe par aorganizar os dados de saida
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

def createInterval(n): # retorna por quantos segundos uma instância será executada
    return round((n * 60)/1000, 0)

# param(array, preview_value, after_value, new_index)
def shiffElement(array, preview, after, new):
    idn = new
    new = array[idn]

    array.pop(idn)

    preview = array.index(preview)
    after = array.index(after)

    aux_prev = array[:preview+1]
    aux_after = array[after:]

    aux_after.insert(0, new)
    aux_prev.extend(aux_after)

    return aux_prev

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
    inicio = 0
    tam = len(instancias[i])
    output.append(OutputInstancia(files[i]))
    seed = [i for i in range(tam)]

    for max in range(10):
        custo_min = 0
        # generate seed
        shuffle(seed)
        # get initial custo_min
        for j in range(tam):
            if j < tam - 1:
                k = j + 1
            else:
                k = tam - j
            custo_min += instancias[i][seed[j]][seed[k]]
        start = datetime.now()
        # gera um caminho ciclico aleatório sem repetir vertices
        while abs(start.second - datetime.now().second) < createInterval(tam):
            ...
        output[i].time.append(abs(start.second-datetime.now().second))

# gera a saída no arquivo resultados.csv

# dist_to_csv = {
#     "instancia": [data.name for data in output],
#     "autoria": ["Diogo.Cunha" for i in range(len(output))],
#     "algoritmo": ["BLPMsh" for i in range(len(output))],
#     "q-medio": [int(data.avgQ()) for data in output],
#     "q-desvio": [data.dispersionQ() for data in output],
#     "t-medio": [int(data.avgT()) for data in output]
# }

# dataframe = pd.DataFrame(dist_to_csv)
# dataframe.to_csv('resultados.csv', index=False)