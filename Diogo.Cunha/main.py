from random import randint, sample, choice
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

class Subject:
    def __init__(self, path:list, cost:int) -> None:
        self.path = path
        self.cost = cost

TIME_LIMIT = 180

def createInterval(n:int) -> int: # retorna por quantos segundos uma instância será executada
    return round((n * TIME_LIMIT)/1000, 0)

def generateTamPopulation(n:int) -> int: # se size não for par, arrendonda para cima até o par mais próximo
    size = round(n ** 0.5)
    if size%2 != 0:
        while(size%2 != 0):
            size+=1
        return size
    return size

def CX(father:list, mother:list, tam:int) -> Subject:
    son = [-1 for _ in range(tam)]

    for i in range(tam):
        selected = father[i]
        if selected not in son:
            son[i] = selected
        else:
            break
        j = mother.index(selected)
        if father[j] not in son:
            son[j] = father[j]
        else:
            break

    for i in range(tam):
        if mother[i] not in son:
            son[son.index(-1)] = mother[i]
  
    return Subject(son, 0)

def AEX(father: list, mother: list, tam: int) -> Subject:
    son = [-1 for _ in range(tam)]
    unvisited = set()
    for i in range(tam):
        unvisited.add(i)

    for i in range(2):
        son[i] = father[i]
        unvisited.remove(father[i])

    parents = [father, mother]

    for i in range(2, tam):
        son[i] = parents[1][(parents[1].index(son[i - 1]) + 1) % tam]

        if son[i] not in unvisited:
            son[i] = choice(list(unvisited))

        unvisited.remove(son[i])

        parents.reverse()
    return Subject(son, 0)

def swap(array:list, a:int, b:int):
    temp = array[a]
    array[a] = array[b]
    array[b] = temp

def twoOpt(array:list, a:int, b:int) -> list:
    return array[:a] + list(reversed(array[a:b + 1])) + array[b + 1:]

def mutation(sons:list, tam:int, ti:int):
    selected = sample(range(tam), round(tam * 0.2))

    for i in selected:
        a = randint(0, ti - 1)
        b = randint(0, ti - 1)
        while b == a:
            b = randint(0, ti - 1)
        swap(sons[i].path, a, b)

def mutation_sTwoOpt(sons:list, tam:int, ti:int):
    selected = sample(range(tam), round(tam * 0.2))

    for i in selected:
        a = randint(0, ti - 1)
        b = randint(a, ti - 1)
        while b == a:
            b = randint(0, ti - 1)
        if b - a < 5:
            swap(sons[i].path, a, b)
        else:
            sons[i].path = twoOpt(sons[i].path, a, b)

def initPopulation(instancia:list, n:int) ->list:
    population = []
    for _ in range(generateTamPopulation(n)):
        sub = sample(range(n), n)
        population.append(Subject(sub, getCusto(instancia, sub, n)))
    return population

def getCusto(instancia:list, sample:list, tam: int) -> int:
    custo = 0
    for i in range(tam-1):
        custo += instancia[sample[i]][sample[i+1]]
    return custo

def AGCXsw(instancia:list, population:list, tam:int) -> list:
    tp = len(population)
    sons = []
    # selecionando reprodutores
    breeders = sample(range(tp), tp)
    # etapa reprodutiva
    for i in range(int(tp/2)):
        sons.append(CX(population[breeders[i]].path, population[breeders[i+1]].path, tam))
        sons.append(CX(population[breeders[i+1]].path, population[breeders[i]].path, tam))
    
    mutation(sons, tp, tam)
    # seleção natural
    population.sort(key=lambda x:x.cost)

    tss = round(tp * 0.8)

    for _ in range(tss):
        population.pop()
    
    for son in sons:
        son.cost = getCusto(instancia, son.path, tam)
    sons.sort(key=lambda x:x.cost)

    for _ in range(tp - tss):
        sons.pop()
    
    new_pop = []
    for subject in population:
        new_pop.append(subject)
    for son in sons:
        new_pop.append(son)
    
    return new_pop

def AGCXsTwoOpt(instancia:list, population:list, tam:int) -> list:
    tp = len(population)
    sons = []
    # selecionando reprodutores
    breeders = sample(range(tp), tp)
    # etapa reprodutiva
    for i in range(int(tp/2)):
        sons.append(CX(population[breeders[i]].path, population[breeders[i+1]].path, tam))
        sons.append(CX(population[breeders[i+1]].path, population[breeders[i]].path, tam))
    
    mutation_sTwoOpt(sons, tp, tam)
    # seleção natural
    population.sort(key=lambda x:x.cost)

    tss = round(tp * 0.8)

    for _ in range(tss):
        population.pop()
    
    for son in sons:
        son.cost = getCusto(instancia, son.path, tam)
    sons.sort(key=lambda x:x.cost)

    for _ in range(tp - tss):
        sons.pop()
    
    new_pop = []
    for subject in population:
        new_pop.append(subject)
    for son in sons:
        new_pop.append(son)
    
    return new_pop

def AGCAEXsw(instancia:list, population:list, tam:int) -> list:
    tp = len(population)
    sons = []
    # selecionando reprodutores
    breeders = sample(range(tp), tp)
    # etapa reprodutiva
    for i in range(int(tp/2)):
        if tam < 150:
            sons.append(AEX(population[breeders[i]].path, population[breeders[i+1]].path, tam))
            sons.append(AEX(population[breeders[i+1]].path, population[breeders[i]].path, tam))
        else:
            sons.append(AEX(population[breeders[i]].path, population[breeders[i+1]].path, tam))
            sons.append(CX(population[breeders[i+1]].path, population[breeders[i]].path, tam))
    
    mutation(sons, tp, tam)
    # seleção natural
    population.sort(key=lambda x:x.cost)

    tss = round(tp * 0.8)

    for _ in range(tss):
        population.pop()
    
    for son in sons:
        son.cost = getCusto(instancia, son.path, tam)
    sons.sort(key=lambda x:x.cost)

    for _ in range(tp - tss):
        sons.pop()
    
    new_pop = []
    for subject in population:
        new_pop.append(subject)
    for son in sons:
        new_pop.append(son)
    
    return new_pop

instancias = []
files = ["Western Sahara", "Djibouti",  "Qatar",  "Uruguay", "Zimbabwe"]
li = [29, 38, 194, 734, 929] # tamanho de cada uma das instâncias

output = []
for file in files: # carregando a matrix de adjacência
    array = np.fromfile("Instâncias/"+file+".bin")
    temp = array.tolist()
    pos = files.index(file)
    graph = [[] for _ in range(li[pos])]
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
        population = initPopulation(instancias[i], tam)
        while(abs(start - time()) < createInterval(tam)):
            population = AGCAEXsw(instancias[i], population, tam)
        output[i].time.append(abs(start-time()))
        best = population[0].cost
        for j in range(1, generateTamPopulation(tam)):
            current = population[j].cost
            best = current if current < best else best
        print(best)
        output[i].solutions.append(best)
# gera a saída no arquivo resultados.csv
dist_to_csv = {
    "instancia": [data.name for data in output],
    "autoria": ["Diogo.Cunha" for _ in range(len(output))],
    "algoritmo": ["AGCAEXsw" for _ in range(len(output))],
    "q-medio": [int(data.avgQ()) for data in output],
    "q-desvio": [f"{data.dispersionQ():.02f}" for data in output],
    "t-medio": [int(data.avgT()) for data in output]
}
dataframe = pd.DataFrame(dist_to_csv)
dataframe.to_csv('resultados.csv', index=False)