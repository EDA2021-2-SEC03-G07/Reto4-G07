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
 """

from DISClib.ADT.graph import numEdges, numVertices
import config as cf
from App import model
from DISClib.ADT import map as mp
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init_Catalog():
    return model.init_Catalog()

# Funciones para la carga de datos
def loadCSVs(catalog):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.
    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    citiesfile = cf.data_dir + 'worldcities.csv'
    cities_file = csv.DictReader(open(citiesfile, encoding="utf-8"),
                                delimiter=",")
    # for city in cities_file:
    #     model.addCity(catalog, city)
        
    airportsfile = cf.data_dir + 'airports_full.csv'
    airports_file = csv.DictReader(open(airportsfile, encoding="utf-8"),
                                delimiter=",")
    for airport in airports_file:
        model.addAirport(catalog, airport)

    routesfile = cf.data_dir + 'routes_full.csv'
    routes_file = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    for route in routes_file:
        model.addIATAs(catalog, route)
    
    model.isDirected_orNot(catalog)
    return catalog
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo