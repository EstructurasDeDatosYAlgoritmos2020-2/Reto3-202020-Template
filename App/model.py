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
    """ Inicializa el catálogo

    Retorna el catálogo inicializado.
    """
    catalog = {'accidents': None,
                '2016': None,
                '2017': None,
                '2018': None,
                '2019': None,
                '2020': None
                }

    catalog['accidents'] = lt.newList('ARRAY_LIST',compareAccidentsID)
#    catalog['years'] = lt.newList('SINGLE_LINKED', )
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
    return catalog

# ==============================
# Funciones para agregar informacion al catalogo
# ==============================

def addAccident(catalog,accident):
    """
    RETO3 - REQ1
    Adiciona un accidente a la lista de accidentes.
    Adiciona el ID de un accidente a su respectivo año de ocurrencia,
    cuya llave es la información del accidente.
    """  
    occurred_start_date = accident['Start_Time']
    if occurred_start_date is not None:

        accident_date = datetime.datetime.strptime(occurred_start_date, '%Y-%m-%d %H:%M:%S')
        ocurred_year = str(accident_date.year)
    
        lt.addLast(catalog['accidents'],accident)
        uptadeAccidentInDate(catalog[ocurred_year],accident) 
    
    return catalog 

def uptadeAccidentInDate(year_map,accident):
    """
    RETO3 - REQ1
    Se toma la fecha del accidente y se busca si ya existe en el arbol
    dicha fecha. Si es asi, se adiciona a su lista de accidentes
    y se añade a una tabla de hash por su severidad.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea.
    """
    ocurred_date = accident['Start_Time']
    acc_date = datetime.datetime.strptime(ocurred_date, '%Y-%m-%d %H:%M:%S')
    entry = om.get(year_map,acc_date.date())

    if entry is None:
        date_entry = newDateEntry()
        
        om.put(year_map,acc_date.date(),date_entry)  
    else:
        date_entry = me.getValue(entry)
    
    addSeverityToDateEntry(date_entry,accident)
    return year_map


def addSeverityToDateEntry(date_entry,accident):
    """
    RETO3 - REQ1
    Actualiza un indice de grado de severidad.  Este indice tiene una lista
    de accidentes y una tabla de hash cuya llave es el grado de severidad del
    accidente y el valor es una lista con los accidentes de dicha severidad
    en la fecha que se está consultando (dada por el nodo del arbol)
    """
    lt.addLast(date_entry['Accidents_lst'],accident)
    severity = accident['Severity']
    entry = m.get(date_entry['Severities_mp'], severity)

    if entry is None:
        severity_entry = newSeverityEntry(accident)
        lt.addLast(severity_entry['ListBySeverity'],accident)
        m.put(date_entry['Severities_mp'] , severity, severity_entry)
    else:
        severity_entry = me.getValue(entry)
        lt.addLast(severity_entry['ListBySeverity'],accident)
    
    return date_entry

def newDateEntry():
    """
    RETO3 - REQ1
    Se crea un nodo dada una fecha con sus respectivas llaves: 
    Lista de accidentes (Lista) y grados de gravedad (Tabla de Hash).
    """
    entry = {'Severities_mp': None, 'Accidents_lst': None}
    entry['Severities_mp'] = m.newMap(numelements=15,
                                     maptype='PROBING',
                                     comparefunction=compareSeverity)
    entry['Accidents_lst'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newSeverityEntry(accident):
    """
    RETO3 - REQ1
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

        return om.values(year_bst,keylow,key_date)
    return None

def getAccidentsInRange(catalog,initial_date,final_date):
    """
    RETO3 - REQ3
    Retorna el número de accidentes ocurridos anteriores a una fecha.
    """ 
    initial_year = str(initial_date.year)
    final_year = str(final_year.year)  
    if initial_date != None and final_date != None:
        
        if initial_year == final_year:

            return 0 , om.values(initial_year,initial_date,final_date)
        else:
            keymax = om.maxKey(catalog[initial_year])
            dates_initial_year = om.values(initial_year,initial_date,keymax)

            keymin = om.minKey(catalog[final_year])
            dates_final_year = om.values(final_year,final_date,keymin)
            return 1 , dates_initial_year , dates_final_year

    return None

    
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
