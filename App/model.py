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
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria
"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newCatalog():
    """ 
    Inicializa el catálogo
    Retorna el catálogo inicializado.
    """
    catalog = {'accidents': None,
                '2016': None,
                '2017': None,
                '2018': None,
                '2019': None,
                '2020': None,
                'Hour_RBT':None
                }

    catalog['accidents'] = lt.newList('ARRAY_LIST',compareAccidentsID)
    catalog['2016'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    catalog['2017'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    catalog['2018'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    catalog['2019'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    catalog['2020'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)   
    catalog['Hour_RBT'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareHours)                              
    return catalog

# ==============================
# Funciones para agregar informacion al catalogo
# ==============================

def addAccident(catalog,accident):
    """
    Adiciona un accidente a la lista de accidentes en el catálogo.
    Adiciona la fecha de un accidente como llave a su respectivo año de ocurrencia (RBT).
    Actualiza el entry en el caso de que la fecha ya exista:
        Se actualiza el mapa de severidades.
        Se actualiza la lista de accidentes en la fecha.
    """  
    occurred_start_date = accident['Start_Time']
    if occurred_start_date is not None:

        accident_date = datetime.datetime.strptime(occurred_start_date, '%Y-%m-%d %H:%M:%S')
        ocurred_year = str(accident_date.year)
        lt.addLast(catalog['accidents'],accident)
        updateAccidentInDate(catalog[ocurred_year],accident) 
        updateAccidentInHour(catalog['Hour_RBT'],accident)

def updateAccidentInDate(year_RBT,accident):
    """
    Adiciona la fecha de un accidente como llave a su respectivo año de ocurrencia (RBT).
    Actualiza el entry en el caso de que la fecha ya exista:
        Se actualiza el mapa de severidades.
        Se actualiza la lista de accidentes en la fecha.
    """
    ocurred_date = accident['Start_Time']
    acc_date = datetime.datetime.strptime(ocurred_date, '%Y-%m-%d %H:%M:%S')
    entry = om.get(year_RBT,acc_date.date())

    if entry is None:
        date_entry = newEntry()
        om.put(year_RBT,acc_date.date(),date_entry)     
    else:
        date_entry = me.getValue(entry)
    addSeverityToEntry(date_entry,accident)

def updateAccidentInHour(hour_RBT,accident):
    """
    RETO3 - REQ5
    Adiciona la hora en la que ocurrió un accidente como llave al RBT.
    Actualiza el entry en el caso de que la hora ya exista:
        Se actualiza el mapa de severidades.
        Se actualiza la lista de accidentes ocurridos en esa hora.
    """
    ocurred_date = accident['Start_Time']
    fifteen_minutes = datetime.timedelta(minutes=15)

    acc_date = datetime.datetime.strptime(ocurred_date, '%Y-%m-%d %H:%M:%S')
    acc_minutes = datetime.timedelta(minutes=acc_date.minute)
   
    if acc_minutes == 00:
        rbt_accident_time = datetime.timedelta(hours=acc_date.hour, minutes = 00)

    elif acc_minutes <= fifteen_minutes:
        rbt_accident_time = datetime.timedelta(hours=acc_date.hour, minutes = 00)

    elif acc_minutes >= fifteen_minutes and acc_minutes <= (fifteen_minutes)*3:
        rbt_accident_time = datetime.timedelta(hours=acc_date.hour, minutes = 30)
    
    elif acc_minutes > (fifteen_minutes)*3:
        rbt_accident_time = datetime.timedelta(hours=(acc_date.hour + 1 ), minutes = 00)

    entry = om.get(hour_RBT,rbt_accident_time)
    if entry is None:
        hour_entry = newEntry()
        om.put(hour_RBT,rbt_accident_time,hour_entry)
    else:
        hour_entry = me.getValue(entry)

    addSeverityToEntry(hour_entry,accident)

def addSeverityToEntry(entryRBT,accident):
    """
    Añade un accidente a la lista de accidentes de la entry (Fecha u Hora, depende del árbol).
    
    Actualiza un entry de grado de severidad. 
    Este indice tiene una lista de accidentes y una tabla de hash:
    (Llave: Grado de severidad del accidente, 
    Valor: Lista con los accidentes de dicha severidad)

    """
    lt.addLast(entryRBT['Accidents_lst'],accident)
    severity = accident['Severity']
    entry_sev_mp = m.get(entryRBT['Severities_mp'], severity)

    if entry_sev_mp is None:
        severity_entry = newSeverityEntry(accident)
        lt.addLast(severity_entry['ListBySeverity'],accident)
        m.put(entryRBT['Severities_mp'] , severity, severity_entry)

    else:
        severity_entry = me.getValue(entry_sev_mp)
        lt.addLast(severity_entry['ListBySeverity'],accident)
    
# ==============================
# Funciones para inicializar las entradas de los RBT o Tablas de Hash.
# ==============================

def newEntry():
    """
    Crea un entry dada una fecha con sus respectivas llaves: 
    Lista de accidentes (Lista) y grados de gravedad (Tabla de Hash).
    """
    entry = {'Severities_mp': None, 'Accidents_lst': None}
    entry['Severities_mp'] = m.newMap(numelements=5,
                                     maptype='PROBING',
                                     comparefunction=compareSeverity)
    entry['Accidents_lst'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newDateEntry():
    """
    Crea un entry dada una fecha con sus respectivas llaves: 
    Lista de accidentes (Lista) y grados de gravedad (Tabla de Hash).
    """
    entry = {'Severities_mp': None, 'Accidents_lst': None}
    entry['Severities_mp'] = m.newMap(numelements=6,
                                     maptype='PROBING',
                                     comparefunction=compareSeverity)
    entry['Accidents_lst'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newHourEntry():
    """
    RETO3 - REQ5
    Crea una entry en el árbol de horas. Con:
    Lista de accidentes (Lista) y grados de gravedad (Tabla de Hash).
    """
    entry = {'Severities_mp': None, 'Accidents_lst': None}
    entry['Severities_mp'] = m.newMap(numelements=6,
                                     maptype='PROBING',
                                     comparefunction=compareSeverity)
    entry['Accidents_lst'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry
    
def newSeverityEntry(accident):
    """
    Se crea un nuevo grado de gravedad con sus respectivas llaves:
    Severity (Grado de gravedad) y Lista de accidentes con esta severidad
    (Single linked lt). 
    """
    severity_entry = {'Severity': None, 'ListBySeverity': None}
    severity_entry['Severity'] = accident['Severity']
    severity_entry['ListBySeverity'] = lt.newList('SINGLE_LINKED', compareSeverity)

    return severity_entry

# ==============================
# Funciones de consulta
# ==============================
 
def getAccidentsByDate(year_bst,search_date):
    """
    RETO3 - REQ1
    Retorna los accidentes ocurridos en una fecha.
    """        
    date_accidents = om.get(year_bst,search_date)
    if date_accidents is not None:
        return me.getValue(date_accidents)
    return None

def auxiliarYearIterator():
    """
    Función Axuiliar de las funciones Auxiliares.
    """

def getBeforeDate(catalog,search_date):
    """
    Función Auxiliar REQ2
    Retorna una tupla con las llaves del RBT del respectivo año.

    """       
    
    year_search_date = search_date.year
    year_bst = catalog[str(year_search_date)]  

    date_accidents = om.get(year_bst,search_date)
    if date_accidents != None:
        
        d_one_year_before = None                                        #Se incian los valores de los años con None, en el caso en el 
        d_two_year_before = None                                        #que el rango no abarque los años desde 2016 a 2020.
        d_three_year_before = None
        d_four_year_before = None
        
        key_date = date_accidents['key']
        keylow = om.minKey(year_bst)
        dates_year = om.keys(year_bst,keylow,key_date)

        yearIterator = int(search_date.year) - 1                        
        search_date = int(search_date.year)                             #Se recorren los años desde el ingresado hasta la primera fecha 
        while yearIterator > 2015:                                      #registrada en 2016                                    

            keymax = om.maxKey(catalog[str(yearIterator)])
            keymin = om.minKey(catalog[str(yearIterator)])

            if yearIterator == search_date - 1:
                d_one_year_before = om.keys(catalog[str(yearIterator)],keymin,keymax)  

            elif yearIterator == search_date - 2:
                d_two_year_before = om.keys(catalog[str(yearIterator)],keymin,keymax) 

            elif yearIterator == search_date - 3:
                d_three_year_before = om.keys(catalog[str(yearIterator)],keymin,keymax) 

            elif yearIterator == search_date - 4:
                d_four_year_before = om.keys(catalog[str(yearIterator)],keylow,keymax)  

            yearIterator = yearIterator - 1
                
        return dates_year , d_one_year_before , d_two_year_before , d_three_year_before , d_four_year_before
    return None

def getInRange(catalog,initial_date,final_date):
    """
    Función Auxiliar REQ3 y REQ4
    Retorna una tupla con las llaves del RBT de accidentes ocurridos en un rango de fechas de un año.

    """ 
    initial_year = str(initial_date.year)
    final_year = str(final_date.year)  
    
    initial_date_accidents = om.contains(catalog[initial_year],initial_date)
    final_date_accidents = om.contains(catalog[final_year],final_date)

    if initial_date_accidents and final_date_accidents:
        print('Checkpoint!')
        dates_second_year = None                                                     
        dates_third_year = None
        dates_fourth_year = None
        dates_fifth_year = None

        keymax = om.maxKey(catalog[initial_year])
        keylow = om.get(catalog[initial_year],initial_date)['key']
        dates_initial_year = om.keys(catalog[initial_year],keylow,keymax)       #Fechas primer año.
            
        keyhigh = om.get(catalog[final_year],final_date)['key']

        initial_year = int(initial_year)
        yearIterator = int(initial_date.year) + 1
        while yearIterator < (int(final_date.year) + 1):                    #Fechas resto de años.
            keymax = om.maxKey(catalog[str(yearIterator)])
            keymin = om.minKey(catalog[str(yearIterator)])
            if yearIterator == initial_year + 1:
                if yearIterator != int(final_year):
                    dates_second_year = om.keys(catalog[str(yearIterator)],keymin,keymax)  
                else:
                    dates_second_year = om.keys(catalog[str(yearIterator)],keymin,keyhigh)  
            elif yearIterator == initial_year + 2:
                if yearIterator != int(final_year):
                    dates_third_year = om.keys(catalog[str(yearIterator)],keymin,keymax) 
                else:
                    dates_third_year = om.keys(catalog[str(yearIterator)],keymin,keyhigh)  
            elif yearIterator == initial_year + 3:
                if yearIterator != int(final_year):
                    dates_fourth_year = om.keys(catalog[str(yearIterator)],keymin,keymax) 
                else:
                    dates_fourth_year = om.keys(catalog[str(yearIterator)],keymin,keyhigh) 
            elif yearIterator == initial_year + 4:
                if yearIterator != int(final_year):
                    dates_fifth_year = om.keys(catalog[str(yearIterator)],keymin,keymax)  
                else:
                    dates_fifth_year = om.keys(catalog[str(yearIterator)],keymin,keyhigh)  

            yearIterator = yearIterator + 1

        return dates_initial_year , dates_second_year , dates_third_year , dates_fourth_year , dates_fifth_year

    return None

def auxiliarPrintFunction(catalog,acc_in_range,criteria):
    """
    Función que ayuda a recorrer e imprimir.
    Función Auxiliar REQ2, REQ3 y REQ4.

    Recibe como parametros:
        *El Catálogo con todos los datos cargados.
        *Tupla del retorno de la función getInRange()
        *Criteria: States, Severities o None

    Retorna una tupla con los siguientes valores:
        *Llave del mayor valor del diccionario segun el criterio ingresado.
        *Mayor valor del diccionario según el criterio ingresado.
        *Día en el que se presentaron más accidentes en el rango.     
        *Número total de accidentes en el rango.

    """
    dictionary = {}
    cont = 0
    condition = 5

    more_accidents = 0
    num_acc_in_range = 0    

    while cont < condition and acc_in_range[cont] is not None:

        iterator = it.newIterator(acc_in_range[cont])
        while it.hasNext(iterator):

            Key_Entry = it.next(iterator)           
            day = om.get(catalog[str(Key_Entry.year)],Key_Entry)
            day_accidents = day['value']['Accidents_lst']

            num_accidents_in_day =  lt.size(day_accidents) 
            num_acc_in_range = num_acc_in_range + num_accidents_in_day          #Se calcula el total de accidentes en el rango de fechas.
                
            if num_accidents_in_day > more_accidents:                           #Se calcula el día en el que ocurrieron más accidentes en el rango de fechas.
                more_accidents = num_accidents_in_day
                more_accidents_day = day

            iterator_acc = it.newIterator(day_accidents)
            while it.hasNext(iterator_acc):
                
                acc = it.next(iterator_acc)
                if criteria is not None:
                    criteria_dictkey = acc[criteria]
                    if criteria_dictkey not in dictionary:
                        dictionary[criteria_dictkey] = 1
                    else:
                        dictionary[criteria_dictkey] = dictionary[criteria_dictkey] + 1

        cont = cont + 1
    
    max_dict_value = 0
    dictionary_keys = dictionary.keys()

    for value in dictionary_keys:                                #Se calcula la llave del diccionario con mayor valor en el rango de fehcas.
        num_value = dictionary[value]
        if num_value > max_dict_value:
            max_dict_value = num_value
            max_value = value

    if criteria is None:
        return more_accidents_day ,  num_acc_in_range  
    return max_value , dictionary[max_value]  , more_accidents_day ,  num_acc_in_range  
    
def getAccidentsBeforeDate(catalog,search_date): 
    """
    RETO3 - REQ2
    Usa la función auxiliar de impresión.
    Retorna los accidentes anteriores a una fecha.
    """
    criteria = None
    acc_before = getBeforeDate(catalog,search_date)
    if acc_before != None:
        print('Checkpoint')
        accidents_before_date = auxiliarPrintFunction(catalog,acc_before,criteria)
        return accidents_before_date
    return None

def getAccidentsInRange(catalog,initial_date,final_date):  
    """
    RETO3 - REQ3
    Usa la función auxiliar de impresión.
    Retorna los accidentes en un rango.
    """
    criteria = 'Severity'
    acc_in_range = getInRange(catalog,initial_date,final_date)
    if acc_in_range != None:
        accidentes_in_range_by_criteria = auxiliarPrintFunction(catalog,acc_in_range,criteria)
        return accidentes_in_range_by_criteria
    return None

def getStateWithMoreAccidents(catalog,initial_date,final_date):
    """
    RETO3 - REQ4
    Usa la función auxiliar de impresión.
    Retorna el Estado con más accidentes registrados en un rango de fechas.
    """ 
    criteria = 'State'
    acc_in_range = getInRange(catalog,initial_date,final_date)
    if acc_in_range != None:
        accidentes_in_range_by_criteria = auxiliarPrintFunction(catalog,acc_in_range,criteria)
        return accidentes_in_range_by_criteria
    return None

def getAccidentsInHourRange(catalog,initial_hour,final_hour):
    """
    RETO3 - REQ5
    Retorna los accidentes dado un rango de horas.
    """ 
    acc_time1 = datetime.timedelta(hours=initial_hour.hour, minutes = initial_hour.minute)
    acc_minutes1 = datetime.timedelta(minutes=initial_hour.minute)
    fifteen_minutes = datetime.timedelta(minutes=15)
    
    if acc_minutes1 == 00:
        rbt_initial_time = acc_time1
    elif acc_minutes1 <= fifteen_minutes:
        rbt_initial_time = datetime.timedelta(hours=initial_hour.hour, minutes = 00)
    elif acc_minutes1 >= fifteen_minutes and acc_minutes1 <= (fifteen_minutes)*3:
        rbt_initial_time = datetime.timedelta(hours=initial_hour.hour, minutes = 30)  
    elif acc_minute1 > (fifteen_minutes)*3:
        rbt_initial_time = datetime.timedelta(hours=(initial_hour.hour + 1 ), minutes = 00)

    acc_time2 = datetime.timedelta(hours=final_hour.hour, minutes = final_hour.minute)
    acc_minutes2 = datetime.timedelta(minutes=final_hour.minute)

    if acc_minutes2 == 00:
        rbt_final_hour = acc_time2
    elif acc_minutes2 <= fifteen_minutes:
        rbt_final_hour = datetime.timedelta(hours=final_hour.hour, minutes = 00)
    elif acc_minutes2 >= fifteen_minutes and acc_minutes2 <= (fifteen_minutes)*3:
        rbt_final_hour = datetime.timedelta(hours=final_hour.hour, minutes = 30)   
    elif acc_minutes2 > (fifteen_minutes)*3:
        rbt_final_hour = datetime.timedelta(hours=(final_hour.hour + 1 ), minutes = 00)

    Hour_RBT = catalog['Hour_RBT']
    keylow = om.get(Hour_RBT,rbt_initial_time)['key']
    keyhigh = om.get(Hour_RBT,rbt_final_hour)['key']

    if initial_hour != None and final_hour != None:
        return om.values(Hour_RBT,keylow,keyhigh)
    return None

# ==============================
# Funciones para consultar tamaño y altura de los árboles/mapas.
# ==============================

def yearsSize(catalog):
    """
    Número de fechas en las que ocurrieron accidentes de todos los años.
    """    
    y1=om.size(catalog['2016'])
    y2=om.size(catalog['2017'])
    y3=om.size(catalog['2018'])
    y4=om.size(catalog['2019'])
    
    return y1 + y2 + y3 +y4
def hoursSize(catalog):
    """
    Número de HH:MM en las que ocurrieron accidentes.
    """
    return om.size(catalog['Hour_RBT'])
def accidentsSize(catalog):
    """
    Número de accidentes.
    """  
    return lt.size(catalog['accidents'])
def eachYearSize(catalog):
    """
    Número de fechas en las que ocurrieron accidentes de
    cada año.
    """    
    y1=om.size(catalog['2016'])
    y2=om.size(catalog['2017'])
    y3=om.size(catalog['2018'])
    y4=om.size(catalog['2019'])
    y5=om.size(catalog['2020'])

    return y1 , y2 , y3 , y4 , y5
def statesSize(catalog):
    """
    RETO3 - REQ4
    Número de estados cargados.
    """
    return m.size(catalog['States'])
def eachYearHeight(catalog):
    """
    Altura del árbol de cada año.
    """       
    y1 = om.height(catalog['2016'])
    y2 = om.height(catalog['2017'])
    y3 = om.height(catalog['2018'])
    y4 = om.height(catalog['2019'])
    y5 = y4=om.height(catalog['2020'])

    return y1, y2, y3, y4 , y5
def hourHeight(catalog):
    """
    Altura del árbol de horas.
    """
    return om.height(catalog['Hour_RBT'])
# ==============================
# Funciones de Comparacion
# ==============================

def compareDates(date1,date2):
    """
    Compara dos fechas de accidentes en un 
    año dado.
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
    
def compareAccidentsID(id1,id2):
    """
    Compara dos IDS de accidentes. 
    """
    if (id1 == id2):
        return 0
    elif (id1 > id2):
        return 1
    else:
        return -1

def compareSeverity(sev_accident1,sev_accident2):
    """
    Compara dos grados de gravedad de accidentes. 
    """
    sev_accident2 = me.getKey(sev_accident2)
    if (sev_accident1 == sev_accident2):
        return 0
    elif (sev_accident1 > sev_accident2):
        return 1
    else:
        return -1

def compareHours(time1,time2):
    """
    Compara dos horas de accidentes.
    """
    if (time1 == time2):
        return 0
    elif (time1 > time2):
        return 1
    else:
        return -1
    