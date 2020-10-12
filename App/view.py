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

def printAccidentsBeforeDare(accidents_before,search,catalog):
    """
    RETO3 - REQ2
    Imprime los accidentes anteriores a una fecha.
    """
    if accidents_before is not None:
 
        num_acc_before_date = 0
        more_accidents = 0
    
        iterator = it.newIterator(accidents_before)
        while it.hasNext(iterator):
            key_acc = it.next(iterator)
            year_bst = str(key_acc.year)
            day = om.get(catalog[year_bst],key_acc)
            
            num_accidents_in_day =  lt.size(day['value']['Accidents_lst'])
            num_acc_before_date = num_acc_before_date + num_accidents_in_day

            if num_accidents_in_day > more_accidents:
                more_accidents = num_accidents_in_day
                winner_day = day
    
        print('\nAntes de la fecha ocurrieron: ' +  str(num_acc_before_date) + ' accidentes.')
        print('El día en el que se presentaron más accidentes antes de la fecha ingresada fue: '+ str(winner_day['key']) + '. Con: '+ str(lt.size(winner_day['value']['Accidents_lst'])) + ' accidentes.')

    else:
        print('La fecha ingresada no es válida.')

def printAccidentsInRange(catalog,initial_date,final_date,accidents_in_range):
    """
    RETO3 - REQ3
    Imprime los accidentes en un rango de fechas.
    """  
    categories_dict = {}
    if accidents_in_range[0] == 0:
        num_acc_in_range = 0 

        iterator = it.newIterator(accidents_in_range[1])
        while it.hasNext(iterator):
            key_acc = it.next(iterator)
            year_bst = str(key_acc.year)
            day = om.get(catalog[year_bst],key_acc)
            acc_lst = day['value']['Accidents_lst']

            num_accidents_in_day =  lt.size(acc_lst)
            num_acc_in_range = num_acc_in_range + num_accidents_in_day
            
            iterator_sev = it.newIterator(acc_lst)
            while it.hasNext(iterator_sev):
                acc = it.next(iterator_sev)
                acc_category = acc['Severity']

                if acc_category not in categories_dict:
                    categories_dict[acc_category] = 1
                else:
                    categories_dict[acc_category] = categories_dict[acc_category] + 1
  
        max_sev = 0
        categories_dict_keys = categories_dict.keys()
        for sev in categories_dict_keys:
            acc_number_sev = categories_dict[sev]
            if acc_number_sev > max_sev:
                max_sev = acc_number_sev
                more_acc_by_category = ( sev , acc_number_sev )
          
        print('\nEntre ' +  str(initial_date) + ','+' y '+ str(final_date)+' ocurrieron: '+ str(num_acc_in_range)+ ' accidentes.')       
        print('Se presentaron más accidentes con categoría/severidad de: '+ str(more_acc_by_category[0]) + '. Con un total de: ' + str(more_acc_by_category[1]))
    
    elif accidents_in_range[0] == 1:
        num_acc_in_range1 = 0 
        num_acc_in_range2 = 0 

        iterator = it.newIterator(accidents_in_range[1])
        while it.hasNext(iterator):

            key_acc = it.next(iterator)
            year_bst = str(key_acc.year)
            day = om.get(catalog[year_bst],key_acc)
            acc_lst = day['value']['Accidents_lst']

            num_accidents_in_day =  lt.size(acc_lst)
            num_acc_in_range1 = num_acc_in_range1 + num_accidents_in_day
                        
            iterator_sev = it.newIterator(acc_lst)
            while it.hasNext(iterator_sev):
                acc = it.next(iterator_sev)
                acc_category = acc['Severity']
                if acc_category not in categories_dict:
                    categories_dict[acc_category] = 1
                else:
                    categories_dict[acc_category] = categories_dict[acc_category] + 1

        iterator2 = it.newIterator(accidents_in_range[2])
        while it.hasNext(iterator2):

            key_acc = it.next(iterator2)
            year_bst = str(key_acc.year)
            day = om.get(catalog[year_bst],key_acc)
            acc_lst = day['value']['Accidents_lst']
    
            num_accidents_in_day =  lt.size(acc_lst)
            num_acc_in_range2 = num_acc_in_range2 + num_accidents_in_day

            iterator_sev = it.newIterator(acc_lst)
            while it.hasNext(iterator_sev):
                acc = it.next(iterator_sev)
                acc_category = acc['Severity']

                if acc_category not in categories_dict:
                    categories_dict[acc_category] = 1
                else:
                    categories_dict[acc_category] = categories_dict[acc_category] + 1

        max_sev = 0
        categories_dict_keys = categories_dict.keys()
       
        for sev in categories_dict_keys:
            acc_number_sev = categories_dict[sev]
            if acc_number_sev > max_sev:
                max_sev = acc_number_sev
                more_acc_by_category = ( sev , acc_number_sev )
         
        print('\nEntre ' +  str(initial_date) + ','+' y '+ str(final_date)+' ocurrieron: '+ str(num_acc_in_range1 + num_acc_in_range2)+ ' accidentes.')       
        print('Se presentaron más accidentes con categoría/severidad de: '+ str(more_acc_by_category[0]) + '. Con un total de: ' + str(more_acc_by_category[1]))

    else:
        print('Una o ambas fechas ingresadas no son válidas.')

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
    print("5- Requerimento 3: Conocer los accidentes en un rango de fechas.")
    print("6- Requerimento 4: Conocer el Estado con más accidentes.")
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
        search_date = input("\nIngrese la fecha a buscar (YYYY-MM-DD):")
        accidents_by_date = controller.getAccidentsByDate(cont,search_date)
        printAccidentsByDate(accidents_by_date,search_date)

    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 2 del reto 3: ")
        search_date = input("\nIngrese la fecha desde donde se quieren buscar los accidentes anteriores (YYYY-MM-DD):")
        accidents_before = controller.getAccidentsBeforeDate(cont,search_date)
        printAccidentsBeforeDare(accidents_before,search_date,cont)

    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 3 del reto 3: ")
        initial_date = input("\nIngrese el límite inferior del rango de fechas (YYYY-MM-DD):")
        final_date = input("\nIngrese el límite superior del rango de fechas (YYYY-MM-DD):")
        accidents_in_range = controller.getAccidentsInRange(cont,initial_date,final_date)
        printAccidentsInRange(cont,initial_date,final_date,accidents_in_range)
    elif int(inputs[0]) == 6:
        print("\nRequerimiento No 4 del reto 3: ")
        state = controller.getStateWithMoreAccidents(cont)
        print("El estado con más accidentes es: ", str(state))
#    elif int(inputs[0]) == 7:
#        print("\nRequerimiento No 5 del reto 3: ")
#    elif int(inputs[0]) == 8:
#        print("\nRequerimiento No 6 del reto 3: ")
#    elif int(inputs[0]) == 9:
#        print("\nRequerimiento No 7 del reto 3: ")

    else:
        sys.exit(0)
sys.exit(0)
