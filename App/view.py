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
from DISClib.ADT import orderedmap as om
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


#accidentsFile = 'Accidents/us_accidents_small.csv'
#accidentsFile = 'Accidents/US_Accidents_Dec19.csv'
accidentsFile = 'Accidents/us_accidents_dis_2016.csv'


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

    print('Horas :00 y :30 en las que ocurrieron accidentes cargadas: ' + str(controller.hoursSize(cont)))
    print('Altura del árbol de Horas: ' + str(controller.hourHeight(cont)))

    print('\nFechas en las que ocurrieron accidentes en 2016: ' + str(controller.eachYearSize(cont)[0]))
    print('Altura árbol 2016: ' + str(controller.eachYearHeight(cont)[0]))

    print('\nFechas en las que ocurrieron accidentes en 2017: '+ str(controller.eachYearSize(cont)[1]))
    print('Altura árbol 2017: ' + str(controller.eachYearHeight(cont)[1]))

    print('\nFechas en las que ocurrieron accidentes en 2018: '+ str(controller.eachYearSize(cont)[2]))
    print('Altura árbol 2018: ' + str(controller.eachYearHeight(cont)[2]))

    print('\nFechas en las que ocurrieron accidentes en 2019: '+ str(controller.eachYearSize(cont)[3]))
    print('Altura árbol 2019: ' + str(controller.eachYearHeight(cont)[3]))

    print('\nFechas en las que ocurrieron accidentes en 2020: '+ str(controller.eachYearSize(cont)[4]))
    print('Altura árbol 2020: ' + str(controller.eachYearHeight(cont)[4]))

def printAccidentsByDate(accidents_by_date,search_date):
    """
    RETO3 - REQ1
    Imprime los accidentes dada una fecha
    """
    if accidents_by_date:
        print('En el día: ' + search_date)
        print('Ocurrieron un total de: ' + str((lt.size(accidents_by_date['Accidents_lst']))) + " accidentes.")

        Map_Severity = accidents_by_date['Severities_mp']['table']['elements']
        for severity in Map_Severity:
            severity_lvl = me.getValue(severity)
            if severity_lvl is not None:
                iterator = it.newIterator(severity_lvl['ListBySeverity'])
                
                print('\nAccidentes con Nivel de Gravedad: ' + str(severity_lvl['Severity']) +' (' +str(lt.size(severity_lvl['ListBySeverity'])) + ')')
                while it.hasNext(iterator):
                    acc = it.next(iterator)
                    date_time = datetime.datetime.strptime(acc['Start_Time'], '%Y-%m-%d %H:%M:%S')
                    print('ID: ' +  str(acc['ID']) +  '  Datos Fecha: '+ str(date_time.ctime()) + '    '+ str(acc['Description']))
    else:
        print(accidents_by_date)
        print('No se encontraron accidentes en la fecha ingresada.')

def printAccidentsBeforeDare(return_tuple,search_date):
    """
    RETO3 - REQ2
    Imprime los accidentes anteriores a una fecha.
    """
    if return_tuple is not None:
        print('\nAntes de la fecha ocurrieron: ' +  str(return_tuple[1]) + ' accidentes.')
        print('El día en el que se presentaron más accidentes antes de la fecha ingresada fue: '+ str(return_tuple[0]['key']) + '. Con: '+ str(lt.size(return_tuple[0]['value']['Accidents_lst'])) + ' accidentes.')
    else:
        print('La fecha ingresada no es válida.')

def printAccidentsInRange(return_tuple,initial_date,final_date):
    """
    RETO3 - REQ3
    Imprime los accidentes en un rango de fechas.
    """
    if return_tuple is not None:
        print('\nEntre ' +  str(initial_date) + ','+' y '+ str(final_date)+' ocurrieron: '+ str(return_tuple[3])+ ' accidentes.')  
        print('Se presentaron más accidentes con categoría/severidad de: '+ str(return_tuple[0]) + '. Con un total de: ' + str(return_tuple[1]))
    else:
        print('Una o ambas fechas ingresadas no son válidas.')

def printStateWithMoreAccidentsInRange(return_tuple):
    """
    RETO3 - REQ4
    Imprime el Estado con más accidentes en un rango dado.
    """
    if return_tuple is not None:
        print("\nEl estado con más accidentes es: " + str(return_tuple[0]) + ". Con: " + str(return_tuple[1]) + " accidentes.")
        print("El día en el que se presentaron más accidentes en el rango ingresado fue: " + str((return_tuple[2])['key']) + ". Con: " + str(lt.size((return_tuple[2])['value']['Accidents_lst'])) + " accidentes.")
    else:
        print('Una o ambas fechas ingresadas no son válidas.')

def printAccidentsInHourRange(catalog,accidents_in_range):
    """
    RETO3 - REQ5 
    Imprime los accidentes en un rango de horas.
    """
    severities_dict = {}
    if accidents_in_range is not None:
        
        total_accidents = 0
        iterator1 = it.newIterator(accidents_in_range)
        while it.hasNext(iterator1):       
            h = it.next(iterator1)
         
            numacc = (lt.size(h['Accidents_lst']))
            total_accidents = total_accidents + numacc
            key_set = m.keySet(h['Severities_mp'])
    
            iterator2 = it.newIterator(key_set)
            while it.hasNext(iterator2):    

                sev_num = it.next(iterator2)
                severity_lvl = m.get(h['Severities_mp'],sev_num)['value']

                if severity_lvl is not None:
                        if sev_num not in severities_dict:
                            severities_dict[sev_num] = lt.size(severity_lvl['ListBySeverity'])
                        else:
                            severities_dict[sev_num]  = severities_dict[sev_num]  + lt.size(severity_lvl['ListBySeverity'])

        for sev in severities_dict:
            print('\nHubieron: '+ str(severities_dict[sev] ) + ' accidentes con Nivel de Gravedad: ' + str(sev))
            print('Representan un: ' + str( round(((severities_dict[sev]*100)/total_accidents ),2)) + " % del total de accidentes.")

        print('\nOcurrieron un total de: ' + str(total_accidents) + " accidentes en el rango de horas ingresado.")
    else:
        print('Una o ambas fechas ingresadas no son válidas')

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes.")
    print("3- Requerimento 1: Conocer los accidentes en una fecha.")
    print("4- Requerimento 2: Conocer los accidentes anteriores a una fecha.")
    print("5- Requerimento 3: Conocer los accidentes en un rango de fechas.")
    print("6- Requerimento 4: Conocer el Estado con más accidentes en un rango de fechas.")
    print("7- Requerimento 5: Conocer los accidentes por rango de horas.")
#    print("8- Requerimento 6: Conocer la zona geográfica más accidentada.")
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
        print("\nCargando información de accidentes ...")
        controller.loadData(cont,accidentsFile)
        printData(cont)

    elif int(inputs[0]) == 3:
        print("\nRequerimiento No 1 del reto 3: ")
        search_date = input("\nIngrese la fecha a buscar (YYYY-MM-DD):")
        accidents_by_date = controller.getAccidentsByDate(cont,search_date)
        printAccidentsByDate(accidents_by_date,search_date)

    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 2 del reto 3: ")
        search_date = input("\nIngrese la fecha desde donde se quieren buscar los accidentes anteriores (YYYY-MM-DD):")
        accidents_before = controller.getAccidentsBeforeDate(cont,search_date)
        printAccidentsBeforeDare(accidents_before,search_date)

    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 3 del reto 3: ")
        initial_date = input("\nIngrese el límite inferior del rango de fechas (YYYY-MM-DD):")
        final_date = input("\nIngrese el límite superior del rango de fechas (YYYY-MM-DD):")
        return_tuple = controller.getAccidentsInRange(cont,initial_date,final_date)
        printAccidentsInRange(return_tuple,initial_date,final_date)

    elif int(inputs[0]) == 6:
        print("\nRequerimiento No 4 del reto 3: ")
        initial_date = input("\nIngrese el límite inferior del rango de fechas (YYYY-MM-DD): ")
        final_date = input("\nIngrese el límite superior del rango de fechas (YYYY-MM-DD): ")
        return_tuple = controller.getStateWithMoreAccidents(cont,initial_date,final_date)
        printStateWithMoreAccidentsInRange(return_tuple)
  
    elif int(inputs[0]) == 7:
        print("\nRequerimiento No 5 del reto 3: ")
        initial_hour = str(input("\nIngrese el límite inferior del rango de horas (HH-MM): "))
        final_hour = str(input("\nIngrese el límite superior del rango de horas (HH-MM): "))
        accidents_in_range = controller.getAccidentsInHourRange(cont,initial_hour,final_hour)
        printAccidentsInHourRange(cont,accidents_in_range)

#    elif int(inputs[0]) == 8:
#        print("\nRequerimiento No 6 del reto 3: ")

    else:
        sys.exit(0)
sys.exit(0)
