import pandas as pd
from igraph import *
#from cython import *
from math import *
from datetime import *
#Lo primero serÃ¡ tener las coordenadas y sacar la distancia entre todos de uno a mucho con distancias en R2

#Eliminar las que tengan distancias mayores a 300 mts pues una cuadra en promedio son 100 mts y las que atraviesen edificios no se como identificarlas para ponerles un numero enorme.
#Tripleta nodo1,nodo2, formula distancia
def distancia_r2(p1,p2): #p1 y p2 son nodos que tiene componente en x y en y donde p2 es mayor a p1
    a = 100000*sqrt(((p2[0]-p1[0])**2)+((p2[1]-p1[1])**2)) #No importa que las long sean negativas pues
    if a <= 150 and a>50: #Limito la distancia a los que deben ser conexos
        print(a)
        return (p1,p2,a) # es una distancia en metros y ni a palo da negativo
    else:
        return (p1,p2,0) # es una distancia en metros
    #el 100000 lo saque a ojo comparando una distancia en maps y con la que encontre la diferencia fue como 10mts entonces todo good

def pond_distance(D,A,alfa): #Donde D es la distancia y A es el num de acidentes entre los puntos A y B
    return (1-alfa)*D + alfa*A #Aun no se como quitar las sobrantes pues en cuanto a distancia no uenta y accidentes pues tampoco ya que si son 0 peta.

def acc_between2nodes(p1,p2,dir_acc_2): #Recibe dos puntos conexos y queremos ver la cantidad de accidentes entre estos
    #dir_acc_2 es la lista de listas de accidentes
    #Para saber cuales son los mayores y los  menores para hacer el intervalo de busqueda
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
    #Para saber cuales son los mayores y los  menores para hacer el intervalo de busqueda
    num_acc = 0
    for i in dir_acc_2:
        if x1<=i[0] and x2>=i[0]:
            if y1<=i[1] and y2>=i[1]: #Es decir esta en el intervalo de los dos puntos cuenta como accidente
                num_acc += 1 # Por cada uno que cumpla agregamos un accidente
    print("Accidentes" + str(num_acc))
    return num_acc

#Toca pedir el alfa al usuario en el input
def gen_graph(alfa = 0.05,name1 = 'Bases_de_datos_utilizadas\coordenadas_test.csv',name2 = 'Bases_de_datos_utilizadas\Accidentes_test.csv'):
    graph_1 = []
    vertices = []
    vertices1 = []
    vertices2 = []
    df1 = pd.read_csv(name1)
    coord = df1.values.tolist() # Lista de listas
    coord2 = coord[1:]
    #df.drop(index=df.index[0],axis=0,inplace=True)
    #df = df.iloc[1: , :] #Mocho la dupla de nombres Esto es por si tiene titulo
    #df.columns = ['0','1']
    #df[0] = df[0].apply(make_positive)
    df2 = pd.read_csv(name2)
    dir_acc = df2.values.tolist() #Lista de listas donde cada lista es de dos elementos la coordenada en x y la de y
    dir_acc = dir_acc[1:]
#-----------------------------------------------------------------------------CYTHON-------------------------------------------------------------------------------------------------------
#    print('CYTHON saving tha day') PENDIENTE PASAR ESTE CODE A cython
    t1 = datetime.now()
    for i in coord2:
        for j in coord2:
            edge = distancia_r2(i,j)
            op_edge = (edge[1],edge[0],edge[2]) #La idea de esto es evitar aristas multiples
            if i!=j and edge not in graph_1 and op_edge not in graph_1 and edge[2] != 0: #El que no este el edge ni el op es para evitar aristas multiples
                graph_1.append(edge)
    t2 = datetime.now()-t1
    print('Time of execution')
    print(t2)
#-----------------------------------------------------------------------------CYTHON-------------------------------------------------------------------------------------------------------
    #graph_1 = [ distancia_r2(i,j) for i in coord for j in coord if i!=j and distancia_r2(i,j) not in graph_1 and distancia_r2(i,j) not in graph_1 and distancia_r2(i,j)[2] != 0]
    print('YASSSSS YA TERMINE EL GRAFO CON PESOS DE DISTANCIA SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
    print(graph_1)
    #Solo ingresan los que tiene una distancia menor o igual a 300mts si es mayor pues se le pone un 0 y no entra al grafo
    #short_distances_graph = [(m[0],m[1],m[2]) for m in graph if m[2]<=300] #Reduzco distancias a solo 300mts como max
    pond_distance_graph = [(h[0],h[1],pond_distance(h[2],acc_between2nodes(h[0],h[1],dir_acc),alfa)) for h in graph_1]#Si se como modificar el peso de cada vvertices me ahorro esta linea
    #Este es el grafo que voy a retornar pues ya tiene las distancias ponderadas y la conexidad, lo unico seria borrar las aristas raras pero pos por ahora meh
    vertices1 = [i[0] for i in pond_distance_graph if i[0] not in vertices1]
    vertices2 = [i[1] for i in pond_distance_graph if i[1] not in vertices2 and i[1] not in vertices] # El and es para evitar duplicados
    vertices = vertices1 + vertices1
    print(vertices)
    return pond_distance_graph,vertices

#----------------Dijkstra--------------------------------------------------------------------------------------------
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
    vertices = []
    t = []
    tp = []
    t,vertices = gen_graph()
    print(t)
    tp = [(str(i[0]),str(i[1]),i[2]) for i in t] #Permite el ploteo y talvez deberia ser el que se vaya para el dijkstra
    #Esto devuelve tp a t [(float(i) for i in j.split(',')) for j in g.vs["name"]] pero toca ponerle los pesos
    pini = [-74.0699766, 4.6672853]
    pfin = [-74.0709072, 4.6680027]
    a = dijkstra(t,pini,pfin,vertices)
    print("El camino mas corto entre los puntos dados es: "+str(a))
    #graph2csv(t) # PARA GUARDARLO Y QUE SEA FACIL DE MOSTRAR EN LA EXPOSICION
    g = Graph.TupleList(tp, weights=True)
    g.vs["label"] = g.vs["name"]
    g.es["label"] = g.es["weight"]

    layout = g.layout("kk")
    plot(g, layout=layout)
main()
