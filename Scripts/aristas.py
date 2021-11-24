import pandas as pd
from igraph import *
from math import *
from datetime import *

def distancia_r2(p1,p2): #p1 y p2 son nodos que tiene componente en x y en y donde p2 es mayor a p1
    a = 100000*sqrt(((p2[0]-p1[0])**2)+((p2[1]-p1[1])**2)) #No importa que las long sean negativas
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
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
def get_weight_from_list(G,v1,v2):
    try:
        return G.es[G.get_eid(v1, v2)]["weight"]
    except:
        return float('inf')

def get_get_path(L, pini, pfini, prreds=[]):
    preds.append(L[pfini][1][-1])  #Busco el ultimo predecesor de z
    if pini in preds:
        return preds
    return get_get_path(L, pini, preds[-1], preds) #Para que busque el predecesor del predecesor

def dijkstra(graph,pini,pfin,vertices): #pini es u y pfini es z y recordar que los puntos son de dos componentes x y y
    L = {i: [float('inf'), []] for i in vertices}
    L[pini] = [0,[]] #El segundo componente luego del peso es el vertice predecesor
    S = [] #Lista de los revisados
    while pfin not in S:
        vertices_not_in_S = {i: L[i][0]  for i in vertices if i not in S} #Verts que no estan en S
        v_min_peso_actual = min(vertices_not_in_S, key=vertices_not_in_S.get) #Min peso relacionado a la llave
        S.append(v_min_peso_actual) #Pues nunca va a estar
        vertices_not_in_S.pop(v_min_peso_actual) #Eliminados el agregado
        #Paso 4c
        for i in vertices_not_in_S: #Para todo vertice que no este en S
            c = get_weight_from_list(graph,v_min_peso_actual,i)
            if vertices_not_in_S[i] < c + L[v_min_peso_actual][0]:
                L[i] = [vertices_not_in_S[i],L[i][1]]
            else:
                L[i][1].append(v_min_peso_actual)
                L[i] = [L[v_min_peso_actual][0]+c,L[i][1]]

    shortest_path = get_get_path(L,pini,pfin)
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

def main():
    vertices = []
    t = []
    tp = []
    t,vertices = gen_graph()
    print(t)
    tp = [(str(i[0]),str(i[1]),i[2]) for i in t] #Permite el ploteo y talvez deberia ser el que se vaya para el dijkstra ]
    g = Graph.TupleList(tp, weights=True)
    #Esto devuelve tp a t [(float(i) for i in j.split(',')) for j in g.vs["name"]] pero toca ponerle los pesos
    pini = [-74.0699766, 4.6672853]
    pfin = [-74.0709072, 4.6680027]
    print('---------------------------------------------------------------------------')
    print(vertices)
    a = dijkstra(g,str(pini),str(pfin),[str(i) for i in vertices])
    g.vs["label"] = g.vs["name"]
    g.es["label"] = g.es["weight"]

    layout = g.layout("kk")
    plot(g, layout=layout)
main()
