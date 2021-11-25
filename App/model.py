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
    try:
        catalog = {'Aeropuerto': None,
                    'Ciudades': None,
                    'Una_Dirección': None,
                    'Doble_Dirección': None
                    }

        catalog['Aeropuerto'] = mp.newMap(numelements=9000,
                                     maptype='PROBING')

        catalog['Ciudades'] = mp.newMap(numelements=4999,
                                     maptype='PROBING')

        catalog['Una_Dirección'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=10700,
                                              comparefunction=None)
        
        catalog['Doble_Dirección'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=10700,
                                              comparefunction=None)

        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:init()')

# Funciones para agregar informacion al catalogo

def addAirport(catalog, airport):
    Airport_Added = mp.put(catalog['Aeropuerto'], airport['IATA'], airport)
    return Airport_Added
def addCity(catalog, city):
    City_Added = mp.put(catalog['Ciudades'], city['city'], city)
    return City_Added

def addAirportConnection(catalog, Ruta):
        Salida = Ruta["Departure"]
        Destino = Ruta["Destination"]
        Distancia = Ruta["distance_km"]
        addVertexAirport(catalog, Salida)
        addVertexAirport(catalog, Destino)
        addConnection(catalog, Salida, Destino, Distancia)
        return catalog

def addVertexAirport(catalog, IATA):
        if not gr.containsVertex(catalog['Una_Dirección'], IATA):
            gr.insertVertex(catalog['Una_Dirección'], IATA)
        
        if not gr.containsVertex(catalog['Una_Dirección'], IATA):
            gr.insertVertex(catalog['Doble_Dirección'], IATA)
        return catalog

def addConnection(catalog, Salida, Destino, Distancia):
    edge = gr.getEdge(catalog['Una_Dirección'], Salida, Destino)
    if edge is None:
        gr.addEdge(catalog['Una_Dirección'], Salida, Destino, Distancia)
    return catalog


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