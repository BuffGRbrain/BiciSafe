import pandas as pd
import * from igraph
import geopy
import networkx
import * from math
#Lo primero serÃ¡ tener las coordenadas y sacar la distancia entre todos de uno a mucho con distancias en R2

#Eliminar las que tengan distancias mayores a 300 mts pues una cuadra en promedio son 100 mts y las que atraviesen edificios no se como identificarlas para ponerles un numero enorme.
#Tripleta nodo1,nodo2, formula distancia
def distancia_r2(p1,p2): #p1 y p2 son nodos que tiene componente en x y en y
    return (p1,p2,100000*sqrt((p2[0]-p1[0])^2+(p2[1]-p1[1])^2)) # es una distancia en metros
    #el 100000 lo saque a ojo comparando una distancia en maps y con la que encontre la diferencia fue como 10mts entonces todo good

def pond_distance(D,A,alfa): #DOnde D es la distancia y A es el num de acidentes entre los puntos A y B
    return (1-alfa)*D + alfa*A #Aun no se como quitar las sobrantes pues en cuanto a distancia no uenta y accidentes pues tampoco ya que si son 0 peta.
    #Se me ocurre que si lo veo en
#
def acc(p1,p2, dir_acci: list):
    accidentes = []
    for i in dir_acci:
        if i[0] == j[0] or i[1] == j[1]: #Es decir comparten direccion o calle o lo que sea que se llame en otras palabras son conexos
            num_acc_j += 1 #Por cada uno

def num_accidentes(name1 = 'adyacencia.csv' , name2='solo_dir_accidentes.csv'): #Falta crear el de dire de accidentes
    #Asumiendo que tengo el punto x,y del accidente en coordenadas
    #Para todo nodo conexo hay al menos un accidente y este lo inventamos, la idea es que los que comparten calle o carrera tienen un accidente esto es para que los accidentes 0 que son atraves de un edificio no joda todo
    df1 = pd.read_csv(name1)
    dir_coord = df1.values.tolist() # Lista de listas
    #coord = coord[1:] #Mocho la dupla de nombres Esto es por si tiene titulo
    df2 = pd.read_csv(name2)
    dir_acci = df2.values.tolist() # Lista de listas




def filter_aristas(name = 'C:\Users\USUARIO\Documents\Universidad\UR\Cuarto_Semestre_MACC\Teoría de grafos\Proyecto\BiciSafe\Bases de datos utilizadas\coordenadas.csv'): # Aqui uso pandas y la funcion de arriba
    l = []
    df = pd.read_csv(name)
    coord = df.values.tolist() # Lista de listas
    coord = coord[1:] #Mocho la dupla de nombres
    #Faltaria eliminar las aristas que tienen mucha distancia o muy poca
    graph = [ dis(i,j) for i in coord for j in coordenadas if i!=j and dis(i,j) not in graph and dis(j,i) not in graph]
    #Puedo ahorrarme esta linea de abajo si pongo de una que la distancia sea menor o igual a 300
    short_distances_graph = [(m[0],m[1],m[2]) for m in graph if m[2]<=300] #Reduzco distancias a solo 300mts como max
    pond_distance_graph = [(h[0],h[1],pond_distance(h[2],num_accidentes(h[0],h[1]),0.05)) for h in short_distances_graph] #Flta poner el alfa como input del usuario
