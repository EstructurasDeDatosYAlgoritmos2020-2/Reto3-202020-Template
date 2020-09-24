"""
 * Copyright 2020, Departamento de sistemas y Computación
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accidentsFile = 'Accidents/us_accidents_small.csv'
#accidentsFile = 'Accidents/US_Accidents_Dec19.csv'


# ___________________________________________________
#  Funciones para imprimir la inforamación de
#  respuesta.  La vista solo interactua con
#  el controlador.
# ___________________________________________________

def printData(cont):
    """
    RETO3 - REQ1
    Imprime la información del catálogo.
    """ 
    print('Accidentes cargados: ' + controller.si)
    print('Promedio votación películas: ' + str(producer['average_rating']))
    print('Total de películas: ' + str(lt.size(producer['movies'])))

        

def dfgsdfsdfsgs():
    """
    RETO3 - REQ1
    Imprime la información del catálogo.
    """
    if producer:
        print('Productora encontrada: ' + producer['name'])
        print('Promedio votación películas: ' + str(producer['average_rating']))
        print('Total de películas: ' + str(lt.size(producer['movies'])))
        iterator = it.newIterator(producer['movies'])
        while it.hasNext(iterator):
            movie = it.next(iterator)
            print('Titulo: ' + movie['title'] + '  Avg. Rating: ' + movie['vote_average'])
    else:
        print('No se encontró la productora.')

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Requerimento : Conocer los accidentes en una fecha.")
    print("4- Requerimento 2: Conocer los accidentes anteriores a una fecha.")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de crimenes ....")
        controller.loadData(cont,accidentsFile)
        printData(cont)

    elif int(inputs[0]) == 3:
        print("\nBuscando crimenes en un rango de fechas: ")


    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 1 del reto 3: ")

    else:
        sys.exit(0)
sys.exit(0)
