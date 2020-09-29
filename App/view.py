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
import datetime
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
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
    print('Accidentes cargados: ' + str(controller.accidentsSize(cont)))
    print('Fechas en las que ocurrieron accidentes cargadas: ' + str(controller.yearsSize(cont)))

    print('\nAccidentes en 2016: ' + str(controller.eachYearSize(cont)[0]))
    print('Altura árbol 2016: ' + str(controller.eachYearSize(cont)[0]))

    print('\nAccidentes en 2017: '+ str(controller.eachYearSize(cont)[1]))
    print('Altura árbol 2017: ' + str(controller.eachYearSize(cont)[1]))

    print('\nAccidentes en 2018: '+ str(controller.eachYearSize(cont)[2]))
    print('Altura árbol 2018: ' + str(controller.eachYearSize(cont)[2]))

    print('\nAccidentes en 2019: '+ str(controller.eachYearSize(cont)[3]))
    print('Altura árbol 2019: ' + str(controller.eachYearSize(cont)[3]))

def printAccidentsByDate(accidents_by_date,search_date):
    """
    RETO3 - REQ1
    Imprime los accidentes dada una fecha
    """
    if accidents_by_date:
        print('En el día: ' + search_date)
        print('Ocurrieron un total de: ' + str((m.size(accidents_by_date['Accidents_lst']))) + " accidentes.")

        Map_Severity = accidents_by_date['Severities_mp']['table']['elements']
        for severity in Map_Severity:
            severity_lvl = me.getValue(severity)

            if severity_lvl is not None:
                iterator = it.newIterator(severity_lvl['ListBySeverity'])

                print('\nAccidentes con Nivel de Gravedad: ' + str(severity_lvl['Severity']))
                while it.hasNext(iterator):
                    acc = it.next(iterator)
                    date_time = datetime.datetime.strptime(acc['Start_Time'], '%Y-%m-%d %H:%M:%S')
                    print('ID: ' +  str(acc['ID']) +  '  Datos Fecha: '+ str(date_time.ctime()) + '    '+ str(acc['Description']))
    
   
    else:
        print(accidents_by_date)
        print('No se encontraron accidentes en la fecha ingresada o la fecha ingresada no se encuentra entre los años 2016-2019.')

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Requerimento 1: Conocer los accidentes en una fecha.")
    print("4- Requerimento 2: Conocer los accidentes anteriores a una fecha.")
#    print("5- Requerimento 3: Conocer los accidentes en un rango de fechas.")
#    print("6- Requerimento 4: Conocer el Estado con más accidentes.")
#    print("7- Requerimento 5: Conocer los accidentes por rango de horas.")
#    print("8- Requerimento 6: Conocer la zona geográfica más accidentada.")
#    print("9- Requerimento 7: ")
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
        print("\nRequerimiento No 1 del reto 3: ")
        search_date = input("Ingrese la fecha a buscar (YYYY-MM-DD):")
        accidents_by_date = controller.getAccidentsByDate(cont,search_date)
        printAccidentsByDate(accidents_by_date,search_date)

    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 2 del reto 3: ")
#    elif int(inputs[0]) == 5:
#        print("\nRequerimiento No 3 del reto 3: ")
#    elif int(inputs[0]) == 6:
#        print("\nRequerimiento No 4 del reto 3: ")
#    elif int(inputs[0]) == 7:
#        print("\nRequerimiento No 5 del reto 3: ")
#    elif int(inputs[0]) == 8:
#        print("\nRequerimiento No 6 del reto 3: ")
#    elif int(inputs[0]) == 9:
#        print("\nRequerimiento No 7 del reto 3: ")

    else:
        sys.exit(0)
sys.exit(0)
