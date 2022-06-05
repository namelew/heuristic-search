import numpy as np
from random import randint
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
        return round((variacy/tam) ** 1/2, 2)
    def avgT(self): # retorna t-medio
        tam = len(self.time)
        sum = 0
        for solution in self.time:
            sum += solution
        return round(sum/tam, 0)

def createInterval(n): # retorna por quantos segundos uma instância será executada
    return round((n * 60)/1000, 0)

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

    for max in range(10):
        start = datetime.now()
        # gera um caminho ciclico aleatório sem repetir vertices
        while abs(start.second - datetime.now().second) < createInterval(tam):
            solucao = []
            aux = inicio
            custo = 0
            for node in range(tam):
                proximo = randint(0, tam - 1)
                
                if len(solucao) == 28:
                    aresta = (aux, inicio)
                else:
                    aresta = (aux, proximo)
                custo += instancias[i][aresta[0]][aresta[1]]
                solucao.append(aresta)
                
                aux = proximo           
            output[i].solutions.append(custo)
        output[i].time.append(abs(start.second-datetime.now().second))

# gera a saída no arquivo resultados.csv

dist_to_csv = {
    "instancia": [data.name for data in output],
    "autoria": ["Diogo Cunha" for i in range(len(output))],
    "algoritmo": ["BTA" for i in range(len(output))],
    "q-medio": [data.avgQ() for data in output],
    "q-desvio": [data.dispersionQ() for data in output],
    "t-medio": [data.avgT() for data in output]
}

dataframe = pd.DataFrame(dist_to_csv)
dataframe.to_csv('resultados.csv')