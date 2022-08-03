from random import randint, sample,choice
import numpy as np
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
    return round((n * 180)/1000, 0)

def generateTamPopulation(n:int) -> int: # se size não for par, arrendonda para cima até o par mais próximo
    size = round(n ** 0.5)
    if size%2 != 0:
        while(size%2 != 0):
            size+=1
        return size
    return size

def crossoverOperator(inst:list, father:list, mother:list, tam:int, start:int) -> list:
    son = [-1 for _ in range(tam)]
    unvisited = set()

    for i in range(tam):
        unvisited.add(i)

    son[0] = father[start]
    son[1] = father[start+1]
    unvisited.remove(father[start])
    unvisited.remove(father[start+1])
    
    for i in range(2, tam):
        a = (mother.index(son[i-1]) + 1) % tam
        b = (father.index(son[i-1]) + 1) % tam 

        menor = a
        if inst[son[i - 1]][b] < inst[son[i - 1]][menor]:
            menor = b
        
        son[i] = menor
        
        if son[i] not in unvisited:
            a = choice(list(unvisited))
            b = choice(list(unvisited))

            if inst[son[i - 1]][b] < inst[son[i - 1]][menor]:
                son[i] = b
            else:
                son[i] = a

        unvisited.remove(son[i])
 
    return son

def AEX(father:list, mother:list, tam:int) -> list:
  son = [-1 for _ in range(tam)]
  unvisited = set()
  for i in range(tam):
    unvisited.add(i)

  for i in range(2):
    son[i] = father[i]
    unvisited.remove(father[i])

  parents = [father, mother]
  
  for i in range(2, tam):
    son[i] = parents[1][(parents[1].index(son[i-1]) + 1) % tam]
    
    if son[i] not in unvisited:
      son[i] = choice(list(unvisited))

    unvisited.remove(son[i])
    
    parents.reverse()
  return son

def CX(father:list, mother:list, tam:int) -> list:
  son = [-1 for _ in range(tam)]

  for i in range(tam):
    if father[i] not in son:
      son[i] = father[i]
    else:
      break
    if mother[i] not in son:
      son[father.index(mother[i])] = mother[i]
    else:
      break
  
  for i in range(tam):
    if mother[i] not in son:
      son[son.index(-1)] = mother[i]
  
  return son

def swap(array:list, a:int, b:int):
    temp = array[a]
    array[a] = array[b]
    array[b] = temp

def mutation(sons:list, tam:int, ti:int):
    selected = sample(range(tam), round(tam * 0.2))

    for i in selected:
        a = randint(0, ti - 1)
        b = randint(0, ti - 1)
        while b == a:
            b = randint(0, ti - 1)
        swap(sons[i], a, b)

def initPopulation(n:int) ->list:
    population = []
    for _ in range(generateTamPopulation(n)):
        population.append(sample(range(n), n))
    return population

def getCusto(instancia:list, sample:list, tam: int) -> int:
    custo = 0
    for i in range(tam-1):
        custo += instancia[sample[i]][sample[i+1]]
    return custo

def AGHGreX(instancia:list, population:list, tam:int) -> list:
    tp = len(population)
    sons = []
    # selecionando reprodutores
    breeders = sample(range(tp), tp)
    # etapa reprodutiva
    for i in range(int(tp/2)):
        bst1  = randint(0, tam-3)
        sons.append(crossoverOperator(instancia, population[breeders[i]], population[breeders[i+1]], tam, bst1))

        bst2  = randint(0, tam-3)
        while bst2 == bst1:
            bst2  = randint(0, tam-3)
        sons.append(crossoverOperator(instancia, population[breeders[i+2]], population[breeders[i+3]], tam, bst2))
    
    mutation(sons, tp, tam)
    # seleção natural
    tempP = []
    for i in range(tp):
        tempP.append((getCusto(instancia, population[i], tam), i))
    tempP.sort(key=lambda x:x[0])

    for i in range(round(tp * 0.8)):
        tempP.pop()
    
    tempS = []
    for i in range(tp):
        tempS.append((getCusto(instancia, sons[i], tam), i))
    tempS.sort(key=lambda x:x[0])

    for i in range(round(tp * 0.2)):
        tempS.pop()
    
    new_pop = []
    for a in tempP:
        new_pop.append(population[a[1]])
    for b in tempS:
        new_pop.append(sons[b[1]])
    
    return new_pop

instancias = []
files = ["Western Sahara", "Djibouti",  "Qatar"]
li = [29, 38, 194] # tamanho de cada uma das instâncias

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
    print(f"Starting {output[i].name}")
    for max in range(10):
        start = time()
        population = initPopulation(tam)
        while(abs(start - time()) < createInterval(tam)):
            population = AGHGreX(instancias[i], population, tam)
        output[i].time.append(abs(start-time()))
        tempP = []
        for j in range(generateTamPopulation(tam)):
            tempP.append(getCusto(instancias[i], population[j], tam))
        tempP.sort()
        output[i].solutions.append(tempP[0])
# gera a saída no arquivo resultados.csv
dist_to_csv = {
    "instancia": [data.name for data in output],
    "autoria": ["Diogo.Cunha" for _ in range(len(output))],
    "algoritmo": ["AGHGreX" for _ in range(len(output))],
    "q-medio": [int(data.avgQ()) for data in output],
    "q-desvio": [f"{data.dispersionQ():.02f}" for data in output],
    "t-medio": [int(data.avgT()) for data in output]
}
dataframe = pd.DataFrame(dist_to_csv)
dataframe.to_csv('resultados.csv', index=False)