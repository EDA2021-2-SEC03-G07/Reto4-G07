"""
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
assert cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Utils import error as error
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Graphs.dijsktra import Dijkstra
from DISClib.Algorithms.Graphs.bellmanford import BellmanFord
from DISClib.Algorithms.Graphs import scc as strong_c

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def init_Catalog(): #Comentar
    #La idea es que guarde dentro de el mapa IATA las keys son el IATA de cada ciudad y los valores los IATA que tienen como destino ese mismo
    try:
        catalog =  {'DirectedConnections':None,
                    'No_DirectedConnections': None,
                    "IATAs": None,
                    "latitudes": None,
                    "cities": None}

        catalog['DirectedConnections'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=True,
                                            size=10000,
                                            comparefunction=None)
        catalog['No_DirectedConnections'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=False,
                                            size=10,
                                            comparefunction=None)
        catalog["latitudes"] = om.newMap(omaptype='RBT',comparefunction= None)
        catalog["cities"] = mp.newMap(numelements=37500,maptype="PROBING", comparefunction=None)
        catalog["IATAs"] = mp.newMap(maptype='CHAINING',comparefunction=None)

        return catalog
    except Exception as exp:
         error.reraise(exp, 'model:init_Catalog((')

# Funciones para agregar informacion al catalogo
            #Para poder seleccionar que sean digrafos y no dirigidos hay que hacer una función de comparación en donde
            #Hacer dos For in en donde se recorra el mapa[IATA]. El primero recorrerá las llaves, y el segundo la lista que contiene los IATA que tienen como destino
            #el IATA-key.
            # Después de eso un mp.get en el mapa IATA_cities con cada valor de la lista. Si está, hacer un lt.isPresent con la lista de valores  

def addAirport(catalog, airport):
    IATA = airport['IATA']
    graph_directed = catalog['DirectedConnections']
    graph_Nodirected = catalog['No_DirectedConnections']
    if gr.containsVertex(graph_directed, IATA) == False:
        gr.insertVertex(graph_directed, IATA)
    if gr.containsVertex(graph_Nodirected, IATA) == False:
        gr.insertVertex(graph_Nodirected, IATA)


def addIATAs(catalog, IATA): #Teniendo esto, ya es posible hacer la comparación para definir directed y no directed
    Origin = IATA['Departure']
    Destination = IATA['Destination']
    #Origin_Destino = IATA['Departure'] + "-" + IATA['Destination']
    iata_distance = IATA["distance_km"]

    """"if mp.contains(Maps_IATA, Origin) == False:
        lst_destinations = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(lst_destinations, Destination)
        mp.put(Maps_IATA, Origin, lst_destinations)
    else:
        key_value = mp.get(Maps_IATA, Origin)
        value = me.getValue(key_value) #Esto es una lista
        if lt.isPresent(value, Destination) == False:
            lt.addLast(value, Destination)

    if mp.contains(Maps_IATA, Origin_Destino) == False:
        mp.put(catalog["distances"], Origin_Destino, iata_distance)"""

    add_directed(catalog,Origin,Destination,iata_distance)
    return catalog

def add_directed(catalog,origin,destination,distance):
    arco = gr.getEdge(catalog['DirectedConnections'],origin,destination)
    if arco is None:
        gr.addEdge(catalog['DirectedConnections'],origin,destination,distance)

"""def isDirected_orNot(catalog):
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
                        distancia= me.getValue(mp.get(catalog["distances"], Origin_Destino))
                        addConnection_NoDirected(catalog, origen_key, destinations, distancia)
                    if lt.isPresent(value, origen_key) == False:
                        Origin_Destino = origen_key + "-" + destinations
                        distancia= me.getValue(mp.get(catalog["distances"], Origin_Destino))
                        addConnection_Directed(catalog, origen_key, destinations, distancia)
    return catalog"""

""""def addConnection_Directed(catalog, origin, destination, distance):
    edge = gr.getEdge(catalog['DirectedConnections'], origin, destination) #Si no se encuentra el arco entre los vértices en parametro
    if edge is None:
        gr.addEdge(catalog['DirectedConnections'], origin, destination, distance) #Se crea la conexión
    return catalog

def addConnection_NoDirected(catalog, origin, destination, distance):
    edge = gr.getEdge(catalog['No_DirectedConnections'], origin, destination) #Si no se encuentra el arco entre los vértices en parametro
    if edge is None:
        gr.addEdge(catalog['No_DirectedConnections'], origin, destination, distance) #Se crea la conexión
    return catalog #De lo contrario, se retorna el cátalogo"""

def add_nonDirected(catalog):
    list_vertex= gr.vertices(catalog['DirectedConnections'])
    for vertex in lt.iterator(list_vertex):
        adjacents_to_vertex= gr.adjacents(catalog['DirectedConnections'],vertex)
        for adj in lt.iterator(adjacents_to_vertex):
            adjacents_to_adjacent= gr.adjacents(catalog['DirectedConnections'],adj)
            if lt.isPresent(adjacents_to_adjacent,vertex) != 0:
                distance= gr.getEdge(catalog['DirectedConnections'],vertex,adj)["weight"]
                if gr.containsVertex(catalog['No_DirectedConnections'],adj) == False:
                    gr.insertVertex(catalog['No_DirectedConnections'],adj)
                if gr.containsVertex(catalog['No_DirectedConnections'],vertex) == False:
                    gr.insertVertex(catalog['No_DirectedConnections'],vertex)
                if gr.getEdge(catalog['No_DirectedConnections'],vertex,adj) == None:
                    gr.addEdge(catalog['No_DirectedConnections'],vertex,adj,distance)

def inter_points(catalog):
    Airports = lt.newList(datastructure="ARRAY_LIST")
    i_connections = lt.newList(datastructure="ARRAY_LIST")
    routes = catalog['DirectedConnections']
    vertexs = gr.vertices(routes)

    for vertex in lt.iterator(vertexs):
        actualDegree = gr.indegree(routes, vertex) + gr.outdegree(routes, vertex)
        element = {}
        element["key"] = vertex
        element["value"] = actualDegree
        lt.addLast(Airports, element)
    
    ms.sort(Airports, cmpDegree)
    airportsize = lt.size(Airports)
    for i in range(1, 6):
        index= (lt.size(Airports)+1)-i
        IATA= lt.getElement(Airports, index)
        lt.addLast(i_connections, IATA["key"])

    lista_final= lt.subList(Airports,1,5)
    return lista_final, lt.size(i_connections)

def clusters(catalog,iata1,iata2):
    SCC= strong_c.KosarajuSCC(catalog['DirectedConnections'])

    all_SCC= SCC["components"]
    id_SCC= SCC["idscc"]
    same_cluster = "No está fuertemente conectado"
    value1= mp.get(id_SCC, iata1)["value"]
    value2= mp.get(id_SCC, iata2)["value"]
    if value1 == value2 and value1 != None:
        same_cluster= True 
    else:
        same_cluster= False

    return all_SCC, same_cluster

def itsclosed(catalog,iata):
    routes = catalog["DirectedConnections"]
    All_Edges = gr.edges(routes) 
    lst_final = lt.newList(datastructure="ARRAY_LIST")
    for edge in lt.iterator(All_Edges):
        if edge["vertexB"] == iata:
            if not lt.isPresent(lst_final, edge["vertexA"]) == False:
                lt.addLast(lst_final,  edge["vertexA"])

        if edge["vertexA"] == iata:
            if not lt.isPresent(lst_final, edge["vertexB"]) == False:
                lt.addLast(lst_final,  edge["vertexB"])

    """primeros3= lt.subList(lst_final,1,3)
    #ultimos3= lt.subList(lst_final,-2,3)
    ultimos= lt.subList(lst_final,0,lt.size(lst_final)+1)
    Ultimos = lt.newList('ARRAY_LIST')
    j = 0
    while j < 3: #(5)
        last = lt.removeLast(ultimos) #o(1)
        lt.addLast(Ultimos, last) #o(1)
        j += 1"""

    return lt.size(lst_final), lst_final


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


def cmpDegree(degree1, degree2):

    degree1 = int(degree1["value"])
    degree2 = int(degree2["value"])
    return degree1 > degree2