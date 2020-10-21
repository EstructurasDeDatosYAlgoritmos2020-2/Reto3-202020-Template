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
        print("Hola")
        date_entry = newDateEntry()
        om.put(year_RBT,acc_date.date(),date_entry)  
        print(date_entry)
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
    acc_date = datetime.datetime.strptime(ocurred_date, '%Y-%m-%d %H:%M:%S')
    entry = om.get(hour_RBT,acc_date.time())

    if entry is None:
        hour_entry = newHourEntry(acc_date.time())
        om.put(hour_RBT,acc_date.time(),hour_entry)
    else:
        hour_entry = me.getValue(entry)

    addSeverityToEntry(hour_entry,accident)


def addSeverityToEntry(entry,accident):
    """
    Añade un accidente a la lista de accidentes de la entry (Fecha u Hora, depende del árbol).
    
    Actualiza un entry de grado de severidad. 
    Este indice tiene una lista de accidentes y una tabla de hash:
    (Llave: Grado de severidad del accidente, 
    Valor: Lista con los accidentes de dicha severidad)

    """
    lt.addLast(entry['Accidents_lst'],accident)
    severity = accident['Severity']
    entry = m.get(entry['Severities_mp'], severity)

    if entry is None:
        severity_entry = newSeverityEntry(accident)
        lt.addLast(severity_entry['ListBySeverity'],accident)
        print('1',entry['Severities_mp'] )
        print('2',severity)
        print('3', severity_entry)
        m.put(entry['Severities_mp'] , severity, severity_entry)
    else:
        severity_entry = me.getValue(entry)
        lt.addLast(severity_entry['ListBySeverity'],accident)
    

# ==============================
# Funciones para inicializar las entradas de los RBT o Tablas de Hash.
# ==============================


def newDateEntry():
    """
    Crea un entry dada una fecha con sus respectivas llaves: 
    Lista de accidentes (Lista) y grados de gravedad (Tabla de Hash).
    """
    entry = {'Severities_mp': None, 'Accidents_lst': None}
    entry['Severities_mp'] = m.newMap(numelements=15,
                                     maptype='PROBING',
                                     comparefunction=compareSeverity)
    entry['Accidents_lst'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newHouEntry(hour):
    """
    RETO3 - REQ5
    Crea una entry en el árbol de horas. Con:
    Lista de accidentes (Lista) y grados de gravedad (Tabla de Hash).
    """
    entry = {'Hour': None, 'Severities_mp': None, 'Accidents_lst': None}
  
    entry['Severities_mp'] = m.newMap(numelements=15,
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

def getAccidentsBeforeDate(year_bst,search_date):
    """
    RETO3 - REQ2
    Retorna el número de accidentes ocurridos anteriores a una fecha.
    """       
    date_accidents = om.get(year_bst,search_date)
    
    if date_accidents != None:

        key_date = date_accidents['key']
        keylow = om.minKey(year_bst)

        return om.keys(year_bst,keylow,key_date)
    return None

def getAccidentsInRange(catalog,initial_date,final_date):
    """
    RETO3 - REQ3
    Retorna el número de accidentes ocurridos en un rango de fecha.
    """ 
    initial_year = str(initial_date.year)
    final_year = str(final_date.year)  
    
    if initial_date != None and final_date != None:
        
        if initial_year == final_year:          #Primer caso en el que el rango de fechas se encuentra dentro del mismo año
            keylow = om.get(catalog[initial_year],initial_date)['key']
            keyhigh = om.get(catalog[initial_year],final_date)['key']
    
            return 0 , om.keys(catalog[initial_year],keylow,keyhigh)

        else:                                   #Segundo caso en el que el rango de fechas abarca dos años
            keymax = om.maxKey(catalog[initial_year])
            dates_initial_year = om.keys(catalog[initial_year],initial_date,keymax)

            keymin = om.minKey(catalog[final_year])
            dates_final_year = om.keys(catalog[final_year],final_date,keymin)
            return 1 , dates_initial_year , dates_final_year

    return None

def getStateWithMoreAccidents(catalog,initial_date,final_date):
    """
    RETO3 - REQ4
    Retorna el Estado con más accidentes registrados en un rango de fechas.
    """ 
    states_dict = {}
    acc_in_range = getAccidentsInRange(catalog,initial_date,final_date)

    if acc_in_range[0] == 0:
        more_accidents = 0

        iterator = it.newIterator(acc_in_range[1])
        while it.hasNext(iterator):

            key_acc = it.next(iterator)
            year_bst = str(key_acc.year)
            day = om.get(catalog[year_bst],key_acc)
            day_acc = day['value']['Accidents_lst']

            iterator_acc = it.newIterator(day_acc)
            while it.hasNext(iterator_acc):

                acc = it.next(iterator_acc)
                state = acc['State']
                if state not in states_dict:
                    states_dict[state] = 1
                else:
                    states_dict[state] = states_dict[state] + 1

            num_accidents_in_day =  lt.size(day_acc)
            if num_accidents_in_day > more_accidents:
                more_accidents = num_accidents_in_day
                winner_day = day
    
        max_state = 0
        states_dict_keys = states_dict.keys()
        for state in states_dict_keys:
            num_acc_state = states_dict[state]
            if num_acc_state > max_state:
                max_state = num_acc_state
                winner_state = state

    elif acc_in_range[0] == 1:
        more_accidents1 = 0

        iterator = it.newIterator(acc_in_range[1])
        while it.hasNext(iterator):

            key_acc = it.next(iterator)
            year_bst = str(key_acc.year)
            day = om.get(catalog[year_bst],key_acc)
            day_acc = day['value']['Accidents_lst']

            iterator_acc = it.newIterator(day_acc)
            while it.hasNext(iterator_acc):

                acc = it.next(iterator_acc)
                state = acc['State']
                if state not in states_dict:
                    states_dict[state] = 1
                else:
                    states_dict[state] = states_dict[state] + 1
            
            num_accidents_in_day =  lt.size(day_acc)
            if num_accidents_in_day > more_accidents1:
                more_accidents1 = num_accidents_in_day
                winner_day1 = day

        more_accidents2 = 0

        iterator2 = it.newIterator(acc_in_range[2])
        while it.hasNext(iterator2):

            key_acc = it.next(iterator2)
            year_bst = str(key_acc.year)
            day = om.get(catalog[year_bst],key_acc)
            day_acc = day['value']['Accidents_lst']
        
            iterator_acc = it.newIterator(day_acc)
            while it.hasNext(iterator_acc):

                acc = it.next(iterator_acc)
                state = acc['State']
                if state not in states_dict:
                    states_dict[state] = 1
                else:
                    states_dict[state] = states_dict[state] + 1

            num_accidents_in_day =  lt.size(day_acc)
            if num_accidents_in_day > more_accidents2:
                more_accidents2 = num_accidents_in_day
                winner_day2 = day

        if more_accidents1 > more_accidents2:
            winner_day = winner_day1
        else:
            winner_day = winner_day2
    
        max_state = 0
        states_dict_keys = states_dict.keys()
        for state in states_dict_keys:
            num_acc_state = states_dict[state]
            if num_acc_state > max_state:
                max_state = num_acc_state
                winner_state = state

    return winner_state , states_dict[winner_state] , winner_day 

def getAccidentsInHourRange(catalog,initial_hour,final_hour):
    """
    RETO3 - REQ5
    Retorna los accidentes dado un rango de horas.
    """ 
    Hour_RBT = catalog['Hour_RBT']
    if initial_hour != None and final_hour != None:
        return om.values(Hour_RBT,initial_hour,final_hour)
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

def compareStatesNames(keyname,state):
    """
    Compara dos nombres de Estados.
    Compara el nombre del Estado con una entry en 
    el mapa (Hash Table). Requiere obtener la llave del entry.
    """
    state1 = str(keyname)
    state2 = me.getKey(state)
    if (state1 == state2):
        return 0
    elif (state1 > state2):
        return 1
    else:
        return -1

def compareHours(hour1,hour2):
    """
    Compara dos horas de accidentes.
    """
    if (hour1 == hour2):
        return 0
    elif (hour1 > hour2):
        return 1
    else:
        return -1
    