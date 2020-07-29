import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import calendar
import pkgutil
from io import StringIO
from semic.utils import URL_METEO_FRANCE

def find_insee(city, postal):
    """
    Inputs:
        city: name of a city
        postal: post code of a city
    Output:
        insee code of this city
    """
    byt = pkgutil.get_data("semic", "code_insee.csv")
    data = str(byt, 'utf-8')
    insee = pd.read_csv(StringIO(data), sep = ',')
    insee = insee[insee['Commune'] == city.upper()]
    assert len(insee) > 0, "Aucune commune ne correspond à cette recherche"
    code = insee['Code INSEE'][insee['Code Postal'].str.contains(str(postal))].values[0]

    return code

def get_meteo(insee, day):
    """
    Inputs:
        insee: insee code of a city
        day: day in format dd-mm-yy
    Output:
        dictionnary of the weather
    """
    lieu_type = 'VILLE_FRANCE'
    
    url = URL_METEO_FRANCE
    url = url.format(insee, lieu_type, day)
    page = requests.get(url)
    assert page.status_code == 200, "Error loading the webpage"
    
    today = datetime.date.today()
    day = datetime.datetime.strptime(day, '%d-%m-%Y').date()
    limite = datetime.datetime.strptime('01-01-1963', '%d-%m-%Y').date()
    assert day < today and day > limite, "Wrong date (Need between 01-01-1963 and " + datetime.date.today().strftime('%d-%m-%Y') + ")"
    
    soup = BeautifulSoup(page.content, 'html.parser')
    liste_info_journee = soup.find_all('ul', class_='grid-half')
#     liste_horaires = soup.find_all('div', class_="grid-half echeances")
    
    if liste_info_journee:
        liste_info_journee = liste_info_journee[0].find_all('li')
#     if liste_horaires:
#         liste_horaires = liste_horaires[0].find_all('dl')
    
    res = liste_info_journee # + liste_horaires
#     for i in res:
#         print(i.get_text().strip())
    dic = {}
    for result in res:
        kv = result.get_text().split(':')
        key = kv[0].strip()
        value = kv[1].strip()
        tokeep = ''
        for i in value:
            if i.isdigit() or i == '.':
                tokeep += i
        dic[key] = float(tokeep)
    
    dic = standardise_keys_mf(dic, day = True)

    return dic

def get_meteo_monthly(insee, month, year):
    """
    Inputs:
        insee: insee code of a city
        month: month in integer
        year: year in integer
    Output:
        dictionnary of the weather for the month
    """
    nb_days = calendar.monthrange(year, month)[1]
    mean_d = {}
    list_min_temp = []
    list_max_temp = []
    list_soleil = []
    list_pluie = []
    for day in range(1, nb_days + 1):
        date = str(day) + '-' + str(month) + '-' + str(year)
        d = get_meteo(insee, date)
        
        list_min_temp.append(d['Température minimale de la journée'])
        list_max_temp.append(d['Température maximale de la journée'])
        list_soleil.append(d["Durée d'ensoleillement de la journée"])
        list_pluie.append(d['Hauteur des précipitations'])
        
    mean_d['Température maximale du mois'] = max(list_max_temp)
    mean_d['Température minimale du mois'] = min(list_min_temp)
    mean_d['Température minimale moyenne'] = sum(list_min_temp) / len(list_min_temp)
    mean_d['Température maximale moyenne'] = sum(list_max_temp) / len(list_max_temp)

    mean_d['Hauteur minimale des précipitations'] = min(list_pluie)
    mean_d['Hauteur maximale des précipitations'] = max(list_pluie)
    mean_d['Hauteur moyenne des précipitations'] = sum(list_pluie) / len(list_pluie)
    
    mean_d["Durée maximale d'ensoleillement"] = max(list_soleil)
    mean_d["Durée minimale d'ensoleillement"] = min(list_soleil)
    mean_d["Durée d'ensoleillement moyenne"] = sum(list_soleil) / len(list_soleil)

    mean_d = standardise_keys_mf(mean_d)

    return mean_d

def estimate_meteo_year(insee, year):
    """
    Inputs:
        insee: insee code of a city
        year: year in integer
    Output:
        dictionnary with the weather for the year
    """
    days = ['01', '06', '11', '16', '21', '26']
    months = ["{0:0=2d}".format(i) for i in range(1, 13)]
    mean_d = {}
    list_min_temp = []
    list_max_temp = []
    list_soleil = []
    list_pluie = []
    for m in months:
        for d in days:
            date = d + '-' + m + '-' + str(year)
            dic = get_meteo(insee, date)
            
            list_min_temp.append(dic['Température minimale de la journée'])
            list_max_temp.append(dic['Température maximale de la journée'])
            list_soleil.append(dic["Durée d'ensoleillement de la journée"])
            list_pluie.append(dic['Hauteur des précipitations'])
    
    mean_d["Température maximale de l'année"] = max(list_max_temp)
    mean_d["Température minimale de l'année"] = min(list_min_temp)
    mean_d["Température minimale moyenne"] = sum(list_min_temp) / len(list_min_temp)
    mean_d["Température maximale moyenne"] = sum(list_max_temp) / len(list_max_temp)

    mean_d['Hauteur minimale des précipitations'] = min(list_pluie)
    mean_d['Hauteur maximale des précipitations'] = max(list_pluie)
    mean_d['Hauteur moyenne des précipitations'] = sum(list_pluie) / len(list_pluie)
    
    mean_d["Durée maximale d'ensoleillement"] = max(list_soleil)
    mean_d["Durée minimale d'ensoleillement"] = min(list_soleil)
    mean_d["Durée d'ensoleillement moyenne"] = sum(list_soleil) / len(list_soleil)

    mean_d = standardise_keys_mf(mean_d)
    
    return mean_d

def standardise_keys_mf(dic, day = False):
    """
    Inputs:
        dic: dict of weather data with keys to standardise
        day: boolean (True if dict contains data for a day, False otherwise)
    Output:
        same dict but with standardized keys
    """
    if day == False:
        dic['max_temp'] = dic.pop("Température maximale de l'année")
        dic['min_temp'] = dic.pop("Température minimale de l'année")
        dic['avg_max_temp'] = dic.pop("Température maximale moyenne")
        dic['avg_min_temp'] = dic.pop("Température minimale moyenne")
        dic['max_rainfall'] = dic.pop("Hauteur maximale des précipitations")
        dic['min_rainfall'] = dic.pop("Hauteur minimale des précipitations")
        dic['avg_rainfall'] = dic.pop("Hauteur moyenne des précipitations")
        dic['max_sunshine'] = dic.pop("Durée maximale d'ensoleillement")
        dic['min_sunshine'] = dic.pop("Durée minimale d'ensoleillement")
        dic['avg_sunshine'] = dic.pop("Durée d'ensoleillement moyenne")
    else :
        dic['min_temp'] = dic.pop('Température minimale de la journée')
        dic['max_temp'] = dic.pop('Température maximale de la journée')
        dic['sunshine'] = dic.pop("Durée d'ensoleillement de la journée")
        dic['rainfall'] = dic.pop('Hauteur des précipitations')
    return dic
