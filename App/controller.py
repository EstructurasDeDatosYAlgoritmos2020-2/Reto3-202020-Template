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

import config as cf
from App import model
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(catalog, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    accidentsfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentsfile, encoding="utf-8"),
                                delimiter=",")
    cont = 0
    for accident in input_file:
        model.addAccident(catalog,accident)
        model.addAccidentToState(catalog,accident)
        cont = cont + 1
        if cont == 10:
            break
    
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def getAccidentsByDate(catalog,search_date):
    """
    RETO3 - REQ1
    Llama la función en model que retorna
    el los accidentes ocurridos en una fecha.
    """    
    search_date = datetime.datetime.strptime(search_date, '%Y-%m-%d')
    year_search_date = str(search_date.year)    
    year_bst = catalog[year_search_date]    
    return model.getAccidentsByDate(year_bst,search_date.date())

def getAccidentsBeforeDate(catalog,search_date):
    """
    RETO3 - REQ2
    Llama la función en model que retorna
    el número de accidentes ocurridos anteriores a una fecha.
    """      
    search_date = datetime.datetime.strptime(search_date, '%Y-%m-%d')
    year_search_date = str(search_date.year)
    year_bst = catalog[year_search_date]    
    return model.getAccidentsBeforeDate(year_bst,search_date.date())

def getAccidentsInRange(catalog,initial_date,final_date):
    """
    RETO3 - REQ3
    Llama la función en model que retorna
    los accidentes en un rango de fechas.
    """
    initial_date = datetime.datetime.strptime(initial_date, '%Y-%m-%d')
    final_date = datetime.datetime.strptime(final_date, '%Y-%m-%d')
    return model.getAccidentsInRange(catalog,initial_date.date(),final_date.date())

def getStateWithMoreAccidents(catalog):
    """
    RETO3 - REQ4
    Llama la función en model que retorna
    el Estado con más accidentes reportados.
    """    
    return model.getStateWithMoreAccidents(catalog)

def yearsSize(catalog):
    """
    Llama la función en model que retorna
    el número de fechas en las que ocurrieron accidentes en todos
    los años.
    """    
    return model.yearsSize(catalog)

def accidentsSize(catalog):
    """
    Llama la función en model que retorna
    el número de accidentes.
    """    
    return model.accidentsSize(catalog)

def eachYearSize(catalog):
    """
    Llama la función en model que retorna
    el número de fechas en las que ocurrieron accidentes
    por cada año.
    """    
    return model.eachYearSize(catalog)

def eachYearHeight(catalog):
    """
    Llama la función en model que retorna
    la altura del árbol de cada año.
    """    
    return model.eachYearHeight(catalog)    

def statesSize(catalog):
    """
    RETO3 - REQ4
    Llama la función en model que retorna
    el número de Estados cargados.
    """
    return model.statesSize(catalog)