#!/usr/bin/env python3

import numpy as np
import random
import copy

## CONSTANTES

# Vector de ciudades
CIUDADES = ["Alicante","Barcelona","Bilbao","Cáceres","Cádiz","Córdoba",
"Coruña","Girona","Huelva","León","Madrid","Murcia","Oviedo",
"Pamplona","Donostia","Sevilla","Tarragona","Toledo","Valencia",
"Zaragoza"]
CIUDADES_INDEX = np.arange(len(CIUDADES))

# Matriz de distancias
M = [
[0,515,817,675,688,525,1031,615,703,855,422,75,873,673,766,609,417,411,166,498],
[515,0,620,918,1284,908,1118,100,1140,784,621,590,902,437,529,1046,98,692,349,296],
[817,620,0,605,1058,795,644,720,939,359,395,796,304,159,119,993,555,466,633,324],
[675,918,605,0,369,319,683,1018,323,407,297,654,525,650,679,264,831,264,636,622],
[688,1284,1058,369,0,263,1072,1384,219,796,663,613,914,1070,1132,125,1059,583,808,988],
[525,908,795,319,263,0,995,1008,232,733,400,444,851,807,869,138,796,320,545,725],
[1031,1118,644,683,1072,995,0,1218,1006,334,609,1010,340,738,763,947,1064,675,961,833],
[615,100,720,1018,1384,1008,1218,0,1240,884,721,690,1002,537,629,1146,198,792,449,396],
[703,1140,939,323,219,232,1006,1240,0,730,632,628,821,1039,1101,94,1029,552,791,957],
[855,784,359,407,796,733,334,884,730,0,333,734,118,404,433,671,719,392,685,488],
[422,621,395,297,663,400,609,721,632,333,0,401,451,407,469,538,534,71,352,325],
[75,590,796,654,613,444,1010,690,628,734,401,0,852,714,807,534,492,390,241,539],
[873,902,304,525,914,851,340,1002,821,118,451,852,0,463,423,789,835,510,803,604],
[673,437,159,650,1070,807,738,537,1039,404,407,714,463,0,92,945,372,478,501,175],
[766,529,119,679,1132,869,763,629,1101,433,469,807,423,92,0,1007,464,540,594,268],
[609,1046,993,264,125,138,947,1146,94,671,538,534,789,945,1007,0,949,458,697,863],
[417,98,555,831,1059,796,1064,198,1029,719,534,492,835,372,464,949,0,605,251,231],
[411,692,466,264,583,320,675,792,552,392,71,390,510,478,540,458,605,0,372,396],
[166,349,633,636,808,545,961,449,791,685,352,241,803,501,594,697,251,372,0,326],
[498,296,324,622,988,725,833,396,957,488,325,539,604,175,268,863,231,396,326,0]
]

class Cromosoma:
    def __init__(self, initial_value, value=np.array([])):
        self.value = value
        self.initial_value = initial_value
        self.fitness = None

    # Función fitness para calcular la distancia total de un cromosoma
    def calc_fitness(self):
        total = 0
        for i in range(len(self.value)-1):
            total += distancia_2_ciudades(self.value[i],self.value[i+1])
        # Sumo la distancia desde la ciudad de partida hasta la primera y última
        total += distancia_2_ciudades(self.initial_value,self.value[0])
        total += distancia_2_ciudades(self.value[-1], self.initial_value)
        self.fitness = total

    # Funcion para obtener los nombres de las ciudades de los cromosomas
    def get_ciudades(self):
        ciudades = []
        for i in self.value:
            ciudades.append(CIUDADES[i])
        return ciudades
    
    def to_string(self):
        print(self.value,":",self.fitness)
    
    def empty(self,length):
        self.value = np.full(length, -1)

## FUNCIONES

# Función para generar N cromosomas aleatorios
def gen_cromosomas_aleatorios(N,array,initialIndex): #
    res = []
    for _ in range(N):
        cromosoma = np.copy(array)
        cromosoma = np.delete(cromosoma, initialIndex)
        np.random.shuffle(cromosoma)
        res.append(Cromosoma(initialIndex, cromosoma))
    return res 

# Función para devolver la distancia entre dos ciudades
def distancia_2_ciudades(A,B):
    return M[A][B]

def get_lowest_fitness(k_cromosomas):
    if len(k_cromosomas) == 1:
        return k_cromosomas[0]

    res:Cromosoma = k_cromosomas[0] 
    for i in range(1,len(k_cromosomas)):
        x:Cromosoma = k_cromosomas[i]
        if x.fitness < res.fitness:
            res = x
    return res

def torneo(poblacion, k, get_best_fitness):
    progenitores = []
    while len(progenitores) < len(poblacion):
        contendientes = random.sample(poblacion, k) 
        ganador = get_best_fitness(contendientes)
        progenitores.append(ganador) 
    return progenitores

def search_index_to_insert(array1, array2, val_to_search, start, end):
    for j in range(len(array2)):
        if array2[j] == val_to_search:
            if j not in range(start, end + 1):
                return j
            else:
                val_to_search = array1[j]
                return search_index_to_insert(array1, array2, val_to_search, start, end)

def cruce_parcialmente_mapeado(padre1, padre2):
    hijo = Cromosoma(padre1.initial_value)
    hijo.empty(len(padre1.value))

    # 1- Escogemos dos puntos de cruzamiento al azar y cruzamos el segmento entre ellos de P1 en el primer hijo.
    punto_cruzamiento1 = random.randint(0, len(padre1.value) - 1)
    punto_cruzamiento2 = random.randint(0, len(padre1.value) - 1)
    if punto_cruzamiento1 > punto_cruzamiento2:
        punto_cruzamiento1, punto_cruzamiento2 = punto_cruzamiento2, punto_cruzamiento1
    # Rellenamos el hijo con los valores del padre 1
    for i in range(punto_cruzamiento1, punto_cruzamiento2 + 1):
        hijo.value[i] = padre1.value[i]

    # 2- Buscar elementos en P2 que no hayan sido copiados
    for i in range(punto_cruzamiento1, punto_cruzamiento2 + 1):
        val_to_search = padre1.value[i]
        val_to_insert = padre2.value[i]
        if val_to_insert in hijo.value:
            continue
        index_to_insert = search_index_to_insert(padre1.value, padre2.value, val_to_search, punto_cruzamiento1, punto_cruzamiento2)
        hijo.value[index_to_insert] = val_to_insert
    
    # 3- Copiamos los valores restantes del padre 2
    for i in range(len(hijo.value)):
        if hijo.value[i] == -1:
            hijo.value[i] = padre2.value[i]

    return hijo

def cruzamiento(padre1, padre2):
    hijo1 = cruce_parcialmente_mapeado(padre1, padre2)
    hijo2 = cruce_parcialmente_mapeado(padre2, padre1)
    return hijo1, hijo2

def mutacion_intercambio(cromosoma):
    # Seleccionamos dos genes al azar
    gen1 = random.randint(0,len(cromosoma.value)-1)
    gen2 = random.randint(0,len(cromosoma.value)-1)
    # Intercambiamos los genes
    cromosoma.value[gen1], cromosoma.value[gen2] = cromosoma.value[gen2], cromosoma.value[gen1]

def mutar(cromosoma):
    return mutacion_intercambio(cromosoma)

def algoritmo_genetico(poblacion):
    # Calcular fitness
    for cromosoma in poblacion:
        cromosoma.calc_fitness()

    # Aplicamos el método del torneo
    progenitores = torneo(poblacion,K,get_lowest_fitness)

    # Cruzamos a los progenitores de dos en dos
    hijos = []
    for i in range(0,len(progenitores),2):
        padre1 = progenitores[i]
        padre2 = progenitores[i+1]
        (hijo1,hijo2) = cruzamiento(padre1,padre2)
        hijo1.calc_fitness()
        hijo2.calc_fitness()
        hijos.append(hijo1)
        hijos.append(hijo2)

    # Mutación de los hijos
    for hijo in hijos:
        if random.random() < P_MUTAR:
            mutar(hijo)
        hijo.calc_fitness()
    
    return hijos

## MAIN
N = 30
K = 3
P_MUTAR = 0.1

# Elegir ciudad inicial
ciudad_inicial = "Pamplona"
index_ci = CIUDADES.index(ciudad_inicial)

# Generar N cromosomas aleatorios
poblacion_inicial = gen_cromosomas_aleatorios(N,CIUDADES_INDEX,index_ci)

poblacion = poblacion_inicial
for _ in range(80):
    poblacion = algoritmo_genetico(poblacion)

poblacion_final = poblacion

print("Población inicial")
for i in poblacion_inicial:
    print(i.value, i.fitness)

print("Población final")
for i in poblacion_final:
    print(i.value, i.fitness)

print("Población final nombres")
for i in poblacion_final:
    print(i.get_ciudades(), i.fitness)