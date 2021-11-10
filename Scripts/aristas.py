import pandas as pd
import * from igraph
import geopy
import networkx
import * from math
#Lo primero será tener las coordenadas y sacar la distancia entre todos de uno a mucho con distancias en R2

#Eliminar las que tengan distancias mayores a 300 mts pues una cuadra en promedio son 100 mts y las que atraviesen edificios no se como identificarlas para ponerles un numero enorme.

def distancia_r2(p1,p2)
    return esto = sqrt((p2[0]-p1[0])^2+(p2[1]-p1[1])^2)

def aristas(nodos) # Aqui uso pandas y la funcion de arriba
    l = []
    idk = pd.read_csv
