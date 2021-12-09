"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar puntos de interconexión aérea")
    print("3- Encontrar clústeres de tráfico aéreo")
    print("4- Encontrar la ruta más corta entre ciudades")
    print("5- Utilizar las millas de viajero")
    print("6- Cuantificar el efecto de un aeropuerto cerrado")
    print("7- Comparar con servicio WEB externo")
    print("8- Visualizar gráficamente los requerimientos")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        size= input("Ingrese el tamaño del archivo: ")
        print("Cargando información de los archivos ....")
        catalog = controller.init_Catalog()
        controller.loadCSVs(catalog, size)
        """print('Total aeropuertos en Dirigido: '+str(info[1]))
        print('Total rutas en Dirigido: '+str(info[0]))
        print('Total ciudades: '+str(info[2]))"""
    elif int(inputs[0]) == 2:
        info= controller.inter_points(catalog)
        print("Los aeropuertos mas interconectados son:")
        print(info[0])
        print("La cantidad de aeropuertos interconectados es: ")
        print(info[1])
    elif int(inputs[0]) == 3:
        iata1= input("Ingrese el IATA del primer aeropuerto: ")
        iata2= input("Ingrese el IATA del segundo aeropuerto: ")
        info= controller.clusters(catalog,iata1,iata2)
        print("El total de clusteres en la red es: "+ str(info[0]))
        if info[1] == True:
            print("...y los aeropuertos ingresados sí están en el mismo cluster.")
        else:
            print("...y los aeropuertos ingresados no están en el mismo cluster.")
    elif int(inputs[0]) == 6:
        iata= input("Ingrese el IATA del aeropuerto fuera de servicio: ")
        info= controller.itsclosed(catalog,iata)
        print("El número de aeropuertos afectados es: "+ str(info[0]))
        print("Los primeros tres afectados son: ")
        print(info[1])
        print("Los últimos tres afectados son: ")
        print(info[2])

    else:
        sys.exit(0)
sys.exit(0)
