﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def init_Catalog(): #Comentar
    """ Inicializa el analizador
   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """ 
    #La idea es que guarde dentro de el mapa IATA las keys son el IATA de cada ciudad y los valores los IATA que tienen como destino ese mismo
    try:
        catalog =  {'DirectedConnections':None,
                    'No_DirectedConnections': None,
                    "IATA's_Cities": None}
        catalog['DirectedConnections'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=True,
                                            size=1000,
                                            comparefunction=None)
        catalog['No_DirectedConnections'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=False,
                                            size=1000,
                                            comparefunction=None)
        catalog["IATAs"] = mp.newMap(numelements=1,
                                      maptype='PROBING')
        return catalog
    except Exception as exp:
         error.reraise(exp, 'model:init_Catalog((')

# Funciones para agregar informacion al catalogo
            #Para poder seleccionar que sean digrafos y no dirigidos hay que hacer una función de comparación en donde
            #Hacer dos For in en donde se recorra el mapa[IATA]. El primero recorrerá las llaves, y el segundo la lista que contiene los IATA que tienen como destino
            #el IATA-key.
            # Después de eso un mp.get en el mapa IATA_cities con cada valor de la lista. Si está, hacer un lt.isPresent con la lista de valores  
def addIATAs(catalog, IATA): #Teniendo esto, ya es posible hacer la comparación para definir directed y no directed
    #ADICIÓN A LA HASHTABLE
    Maps_IATA = catalog['IATAs']
    Origin = IATA['Departure']
    Destination = IATA['Destination']
    Origin_Destino = IATA['Departure'] + "-" + IATA['Destination']

    if mp.contains(Maps_IATA, Origin) == False:
        lst_destinations = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(lst_destinations, Destination)
        mp.put(Maps_IATA, Origin, lst_destinations)
    else:
        key_value = mp.get(Maps_IATA, Origin)
        value = me.getValue(key_value) #Esto es una lista
        if lt.isPresent(value, Destination) == False:
            lt.addLast(value, Destination)
    return catalog

def addAirport(catalog, airport):
    IATA = airport['IATA']
    graph_directed = catalog['DirectedConnections']
    graph_Nodirected = catalog['No_DirectedConnections']
    if gr.containsVertex(graph_directed, IATA) == False:
        gr.insertVertex(graph_directed, IATA)
        gr.insertVertex(graph_Nodirected, IATA)

def isDirected_orNot(catalog, IATA):
    Maps_IATAS = catalog['IATAs']
    for origen in lt.iterator(Maps_IATAS['table']):
        origen_key = origen['key']
        origen_value = origen['value'] #A->B
        if origen_key != None:
            for destinations in lt.iterator(origen_value):
                key_value = mp.get(Maps_IATAS, destinations)
                if key_value != None:
                    value = me.getValue(key_value) #B->A sí es cierto, es no dirigido
                    if lt.isPresent(value, origen_key) == True:
                        Origin_Destino = origen_key + "-" + destinations
                        mp.get(value_distance, Origin_Destino)
                        a = "ES NO DIRIGIDO"
                        addConnection_NoDirected()
                    if lt.isPresent(value, origen_key) == False:
                        a = "ES DIRIGIDO"
                        addConnection_Directed()
    pass

def addConnection_Directed(catalog, origin, destination, distance):
    """
    Adiciona un arco entre dos aeropuertos
    """
    edge = gr.getEdge(catalog['DirectedConnections'], origin, destination) #Si no se encuentra el arco entre los vértices en parametro
    if edge is None:
        gr.addEdge(catalog['DirectedConnections'], origin, destination, distance) #Se crea la conexión
    return catalog

def addConnection_NoDirected(catalog, origin, destination, distance):
    """
    Adiciona un arco entre dos aeropuertos
    """
    edge = gr.getEdge(catalog['No_DirectedConnections'], origin, destination) #Si no se encuentra el arco entre los vértices en parametro
    if edge is None:
        gr.addEdge(catalog['No_DirectedConnections'], origin, destination, distance) #Se crea la conexión
    return catalog #De lo contrario, se retorna el cátalogo
#AVANCE PARA HOMONIMAS
        #Para lograr diferenciar las ciudades homonimas, hay que diferenciarlas por "admin_name"
        #Para lograr poder clasificarlas correctamente y que el usuario pueda pedirlas sin ningún problema
        #Es necesario crear un mapa que contenga como llave la ciudad homonima, y dentro de esta llave,
        #que el valor que le corresponda sea lo que las diferencia, en este caso, lo más sencillo de diferenciar es por
        #'admin_name' y que de ahí contenga los datos correspondientes que se necesitan dar como respuesta. 
        #Aún no hemos podido dar con el chiste de lograr diferenciar los dirigidos con los no dirigidos, o sea, hasta el momento sólo ideas que han fracasado.
        #Así que por el momento el avance que podemos presentar es el pseudocódigo de cómo listaremos las ciudades homonimas
        #Nota: Si no ven la adición de datos en los graphs es porque tocó hacerlo nuevamente :)


# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# Funciones de ayuda
#IDEA PARA HACER EL GRAFO NO DIRIGIDO QUE ESTÁ BIEN VERGA
# for Iata_llave in mapa['iata']:
#     iata llave = {'IATA': KAS2, JAD12, etc..-}
#     for iata_2 in iata_llave['values']:
#         lista_valores_iata2 = mp.get(mapa['iata'], iata_2) #esto es una lista creo xd
#         lt.isPresent(lista_valores_iata2,Iata_llave)