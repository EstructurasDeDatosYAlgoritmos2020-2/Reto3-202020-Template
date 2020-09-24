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
    catalog = {'years': None,
                'dateIndex': None
                }

    catalog['years'] = lt.newList('SINGLE_LINKED', )
    catalog['2016'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    catalog['2016'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    catalog['2017'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    catalog['2018'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    catalog['2019'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    return catalog


# Funciones para agregar informacion al catalogo


# ==============================
# Funciones de consulta
# ==============================












def yearSize(catalog,year):
    """
    RETO3 - REQ1
    Número de accidentes de un año dado
    """    
    return om.size(catalog[year])

# ==============================
# Funciones de Comparacion
# ==============================

def compareDates(Date1,Date2):
    """
    RETO3 - REQ1
    Compara dos fechas de accidentes en un 
    año dado.
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1