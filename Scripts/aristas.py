import pandas as pd
import * from igraph
import geopy
import networkx
import * from math
#Lo primero serÃ¡ tener las coordenadas y sacar la distancia entre todos de uno a mucho con distancias en R2

#Eliminar las que tengan distancias mayores a 300 mts pues una cuadra en promedio son 100 mts y las que atraviesen edificios no se como identificarlas para ponerles un numero enorme.
#Tripleta nodo1,nodo2, formula distancia
def distancia_r2(p1,p2): #p1 y p2 son nodos que tiene componente en x y en y
    if 100000*sqrt((p2[0]-p1[0])^2+(p2[1]-p1[1])^2) <= 300: #Limito la distancia a los que deben ser conexos
        return (p1,p2,100000*sqrt((p2[0]-p1[0])^2+(p2[1]-p1[1])^2)) # es una distancia en metros y ni a palo da negativo
    else
        return (p1,p2,0) # es una distancia en metros
    #el 100000 lo saque a ojo comparando una distancia en maps y con la que encontre la diferencia fue como 10mts entonces todo good

def pond_distance(D,A,alfa): #DOnde D es la distancia y A es el num de acidentes entre los puntos A y B
    return (1-alfa)*D + alfa*A #Aun no se como quitar las sobrantes pues en cuanto a distancia no uenta y accidentes pues tampoco ya que si son 0 peta.


def acc_entre2ptos(p1,p2, name = 'siniestralidad_vial_organizado_localidades.xlsx'): #Recibe dos puntos conexos y queremos ver la cantidad de accidentes entre estos
    df = pd.read_csv(name)
    dir_coord = df.values.tolist() #Lista de listas donde cada lista es de dos elementos la coordenada en x y la de y
    #coord = coord[1:] #Mocho la dupla de nombres Esto es por si tiene titulo
    #Para saber cuales son los mayore sy los  menores para hacer el intervalo de busqueda
    if p1[0]>=p2[0]:
        x1 = p2[0]
        x2 = p1[0]
    elif p1[0]<p2[0]:
        x1 = p1[0]
        x2 = p2[0]
    if p1[1]>p2[1]:
        y1 = p2[1]
        y2 = p1[1]
    elif p1[1]<p2[1]:
        y1 = p1[1]
        y2 = p2[1]
    #Para saber cuales son los mayore sy los  menores para hacer el intervalo de busqueda
    num_acc = 0
    for i in dir_coord:
        if x1<=i[0] and x2>=i[0]:
            if y1<=i[1] and y2>=i[1]: #Es decir esta en el intervalo de los dos puntos cuenta como accidente
                num_acc += 1 # Por cada uno que cumpla agregamos un accidente
    return num_acc
#Toca pedir el alfa al usuario en el input
def gen_graph(alfa = 0.05,name = 'C:\Users\USUARIO\Documents\Universidad\UR\Cuarto_Semestre_MACC\Teoría de grafos\Proyecto\BiciSafe\Bases de datos utilizadas\coordenadas.csv'):
    df = pd.read_csv(name)
    coord = df.values.tolist() # Lista de listas
    coord = coord[1:] #Mocho la dupla de nombres
    graph = [ dis(i,j) for i in coord for j in coordenadas if i!=j and dis(i,j) not in graph and dis(j,i) not in graph and dis(i,j)[2] != 0]
    #Solo ingresan los que tiene una distancia menor o igual a 300mts si es mayor pues se le pone un 0 y no entra al grafo
    #short_distances_graph = [(m[0],m[1],m[2]) for m in graph if m[2]<=300] #Reduzco distancias a solo 300mts como max
    pond_distance_graph = [(h[0],h[1],pond_distance(h[2],acc_entre2ptos(h[0],h[1]),alfa)) for h in graph]
    #Este es el grafo que voy a retornar pues ya tiene las distancias ponderadas y la conexidad, lo unico seria borrar las aristas raras pero pos por ahora meh
    return pond_distance_graph

def dijkstra(graph,pini,pfin): #pini es u y pfini es z y recordar que los puntos son de dos componentes x y y
    L = {pini:0} #Diccionario de distancias desde pini
    for i in graph: #Sacando la lista de vertices e inicializando pesos en inf
        if i[0] not in L and i[1] not in L:
            L[i[0]] = float('inf') ## Este truco requiere python 3.5 si no sirve poner un numero enorme y sale
            L[i[1]] = float('inf') ## Este truco requiere python 3.5 si no sirve poner un numero enorme y sale
        elif i[0] not in L:
            L[i[0]] = float('inf') ## Este truco requiere python 3.5 si no sirve poner un numero enorme y sale
        elif i[1] not in L:
            L[i[1]] = float('inf') ## Este truco requiere python 3.5 si no sirve poner un numero enorme y sale
    S = [] #Lista de los revisados
    w = 0
    while pfin not in S:
        S.append(pini)  #Es el unico con 0 y el resto son infinitos
        for i in L:
            if (pfini,i) in graph:
                w = [j[2] for j in graph if (pfini,i) in j or (pfini,i) in j] #Permito el opuesto pues no me importa la direccion solo el peso
            else:
                w = float('inf')
            L[i] = min(L[i],L[pini]+w[0]) #Asi tengo el diccionario con el cost de ir a todas desde v
        
