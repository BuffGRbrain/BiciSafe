import pandas as pd
from igraph import *
import geopy
import networkx
from math import *
#Lo primero serÃ¡ tener las coordenadas y sacar la distancia entre todos de uno a mucho con distancias en R2

#Eliminar las que tengan distancias mayores a 300 mts pues una cuadra en promedio son 100 mts y las que atraviesen edificios no se como identificarlas para ponerles un numero enorme.
#Tripleta nodo1,nodo2, formula distancia
def distancia_r2(p1,p2): #p1 y p2 son nodos que tiene componente en x y en y
    if 100000*sqrt((p2[0]-p1[0])^2+(p2[1]-p1[1])^2) <= 300: #Limito la distancia a los que deben ser conexos
        return (p1,p2,100000*sqrt((p2[0]-p1[0])^2+(p2[1]-p1[1])^2)) # es una distancia en metros y ni a palo da negativo
    else:
        return (p1,p2,0) # es una distancia en metros
    #el 100000 lo saque a ojo comparando una distancia en maps y con la que encontre la diferencia fue como 10mts entonces todo good

def pond_distance(D,A,alfa): #DOnde D es la distancia y A es el num de acidentes entre los puntos A y B
    return (1-alfa)*D + alfa*A #Aun no se como quitar las sobrantes pues en cuanto a distancia no uenta y accidentes pues tampoco ya que si son 0 peta.


def acc_between2nodes(p1,p2, name = 'Bases_de_datos_utilizadas\Accidentes.csv'): #Recibe dos puntos conexos y queremos ver la cantidad de accidentes entre estos
    df = pd.read_csv(name)
    dir_coord = df.values.tolist() #Lista de listas donde cada lista es de dos elementos la coordenada en x y la de y
    dir_coord = dir_coord[1:] #Mocho la dupla de nombres Esto es por si tiene titulo
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
def gen_graph(alfa = 0.05,name = 'Bases_de_datos_utilizadas\coordenadas.csv'):
    vertices = []
    df = pd.read_csv(name)
    coord = df.values.tolist() # Lista de listas
    coord = coord[1:] #Mocho la dupla de nombres
    graph = [ dis(i,j) for i in coord for j in coordenadas if i!=j and dis(i,j) not in graph and dis(j,i) not in graph and dis(i,j)[2] != 0]
    #Solo ingresan los que tiene una distancia menor o igual a 300mts si es mayor pues se le pone un 0 y no entra al grafo
    #short_distances_graph = [(m[0],m[1],m[2]) for m in graph if m[2]<=300] #Reduzco distancias a solo 300mts como max
    pond_distance_graph = [(h[0],h[1],pond_distance(h[2],acc_between2nodes(h[0],h[1]),alfa)) for h in graph]#Si se como modificar el peso de cada vvertices me ahorro esta linea
    #Este es el grafo que voy a retornar pues ya tiene las distancias ponderadas y la conexidad, lo unico seria borrar las aristas raras pero pos por ahora meh
    vertices1 = [i[0] for i in pond_distance_graph if i[0] not in vertices1]
    vertices.extend(vertices1)
    vertices2 = [i[1] for i in pond_distance_graph if i[1] not in vertices2 and i[1] not in vertices] # El and es para evitar duplicados
    vertices.extend(vertices2)
    return pond_distance_graph,vertices

def get_weight_from_graph(v1,v2,graph):
    vertices_conexos = [(i[0],i[1]) for i in graph if (i[0],i[1]) not in vertices_conexos and (i[1],i[0]) not in vertices_conexos] #Saco las aristas sin peso
    w = float('inf') #Pues la arista entre esos dos no existe
    if (v1,v2) in vertices_conexos:
        w = [j[2] for j in graph if v1 == j[0] and v2 == j[1] ] #Permito el opuesto pues no me importa la direccion solo el peso
    elif (v2,v1) in vertices_conexos:
        w = [j[2] for j in graph if v2 == j[0] and v1 == j[1] ] #Permito el opuesto pues no me importa la direccion solo el peso
    return w

def get_weight_from_list(v,L):
    for i in L:
        if v in i:
            return i[1]

def get_path(L,graph):
    verts_path = [i[0] for i in L]
    vertices_conexos = [(i[0],i[1]) for i in graph if (i[0],i[1]) not in vertices_conexos and (i[1],i[0]) not in vertices_conexos] #Saco las aristas sin peso
    path = [verts_path[0]] #Pongo el inicial que es U
    for v in verts_path[1:]:
        if (path[-1],v) in vertices_conexos: #Es decir existe una aritsta entre estos dos #-1 Para tener siempre el ultimo pues debo seguir la conexidad
            path.append(v)
        elif (v,path[-1]) in vertices_conexos: #Pues tengo que considerar que esten en otro orden
            path.append(v)
    return path


def dijkstra(graph,pini,pfin,vertices): #pini es u y pfini es z y recordar que los puntos son de dos componentes x y y
    L = [(pini,0)] #Menos enredo haciendolo duplas
    lista_costos_iniciales = [(i,float('inf')) for i in vertices if i not in L]
    L.extend(lista_costos_iniciales)
    lista_costos = [i[1] for i in L]
    S = [] #Lista de los revisados
    while pfin not in S:
        #contador = lista_costos.index(min(lista_costos))
        y = L[lista_costos.index(min(lista_costos))][0] #Vertice con el costo min asociado
        if y not in S: #Nunca va a estar en S o eso espero
            x = y #x que no pertenece a S y con L(X) minimo
            S.append(x) #4b
        #Paso 4c
        for i in list(set(vertices)-set(S)): #Para todo vertice que no este en S
            L.append((i,min(get_weight_from_list(i,L),get_weight_from_list(x,L)+get_weight_from_graph(x,i,graph))))
    shortest_path = get_path(L,graph)
    return shortest_path
#-------------------------------------------GRAFO Y CSV------------------------------------------------------
def graph2csv(t) -> None: #Saca el grafo creado en un csv
    df = pd.DataFrame(t)
    df = df.set_axis(['Node A', 'Node B', 'Cost'], axis=1, inplace=False)
    df.to_csv('graph.csv', index=False)


def import_graph(name='graph.csv'):#A partir de un csv crea el grafo falta poner que el usuario meta el nombre con un input
    df = pd.read_csv(name)
    return df.values.tolist()

#-------------------------------------------GRAFO Y CSV------------------------------------------------------

def main(): #estooooo es solo  para pruebas luego hacemos un bien normal y chimbita
    t = gen_graph()
    graph2csv(t) # PARA GUARDARLO Y QUE SEA FACIL DE MOSTRAR EN LA EXPOSICION
    g = Graph.TupleList(t, weights=True)
    g.vs["label"] = g.vs["name"]
    g.es["label"] = g.es["weight"]

    layout = g.layout("kk")
    plot(g, layout=layout)
main()
