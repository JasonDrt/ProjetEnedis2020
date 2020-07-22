import requests
from bs4 import BeautifulSoup
import pandas as pd
from haversine import haversine
import pkgutil
from io import StringIO
import datetime
from collections import defaultdict
import numpy as np
from semic.gps_info import get_city, select_city_postal

def assign_old_state(code):
    """Documentation
    Parameters:
        code: first two digits of a postcode
    Out:
        reg: state for this city in historique_meteo website
    """
    regions = {
        "alsace": ['67', '68'],
        "aquitaine": ['24', '33', '40', '47', '64'],
        "ardeche": ['07'],
        "auvergne": ['03', '15', '43', '63'],
        "bourgogne": ['21', '58', '71', '89'],
        "bretagne": ['22', '29', '35', '56'],
        "centre": ['18', '28', '36', '37', '41', '45'],
        "champagne-ardenne": ['08', '10', '51', '52'],
        "corse": ['20', '2A', '2B'],
        "franche-comte": ['25', '70', '39', '90'],
        "ile-de-re": ['17'],
        "ile-de-france": ['75', '77', '78', '91', '92', '93', '94', '95'],
        "languedoc-roussillon": ['11', '30', '34', '48', '66'],
        "limousin": ['19', '23', '87'],
        "lorraine": ['54', '55', '57', '88'],
        "midi-pyrenees": ['09', '12', '31', '32', '65', '46', '81', '82'],
        "nord-pas-de-calais": ['59', '62'],
        "normandie": ['14', '27', '50', '61', '76'],
        "pays-de-la-loire": ['44', '49', '53', '72', '85'],
        "picardie": ['02', '60', '80'],
        "poitou-charentes": ['16', '79', '86'],
        "provence-alpes-c-te-d-azur": ['04', '05', '06', '13', '83', '84'],
        "rh-ne-alpes": ['01', '26', '38', '42', '69', '73', '74']
    }
    for reg, list_code in regions.items():
        if code in list_code:
            return reg
    print('Code must be between 01 and 95')
    return 0

def check_city(coord, reg, city):
    """Documentation
    Parameters:
        coord: tuple of gps coordinates (longitude, latitude)
        reg: state in historique_meteo website
        city: name of a city
    Out:
        city_url: url of the city in historique_meteo website
        city: name of the city
    """
    lon = coord[0]
    lat = coord[1]
    byt = pkgutil.get_data('semic', 'historique_meteo.csv')
    data = str(byt, 'utf-8')
    df = pd.read_csv(StringIO(data), sep = ',', converters = {'villes': eval, 'villes_url': eval, 'coordinates (lat,lon)': eval})
    # df = pd.read_csv('./historique_meteo.csv', converters = {'villes': eval, 'villes_url': eval, 'coordinates (lat,lon)': eval})
    city = city.lower()
    location = (lat, lon)
    
    if city in df[df['region_url'] == reg]['villes'].values[0]:
        idx = df[df['region_url'] == reg]['villes'].values[0].index(city)
        city_url = df[df['region_url'] == reg]['villes_url'].values[0][idx]
    else:
        dist = []
        for coord in df[df['region_url'] == reg]['coordinates (lat,lon)'].values[0]:
            dist.append(haversine(coord, location, unit = 'm'))
        idx = dist.index(min(dist))
        city_url = df[df['region_url'] == reg]['villes_url'].values[0][idx]
        city = df[df['region_url'] == reg]['villes'].values[0][idx]
    return city_url, city

def check_last_date(region_url, city_url, year, month = None):
    url = 'https://www.historique-meteo.net/france/{0}/{1}/{2}/{3}'
    if month == None:
        month = datetime.datetime.now().month
        month = "{0:02d}".format(month)
    url_test = url.format(region_url, city_url, year, month)
    page = requests.get(url_test)
    code = page.status_code
    while (code != 200) and int(month) > -1:
        month = int(month) - 1
        month = "{0:02d}".format(month)
        url_test = url.format(region_url, city_url, year, month)
        page = requests.get(url_test)
        code = page.status_code
    if month == -1:
        raise Exception("No data available for any month for this year")
    return month

def standardise_keys_hm(dic, day = False):
    if day == False:
        dic['avg_temp'] = dic.pop('Température moyenne (°C)')
        dic['record_max_temp'] = dic.pop('Température maximale record (°C)')
        dic['record_min_temp'] = dic.pop('Température minimale record (°C)')
        dic['avg_rainfall_per_day'] = dic.pop('Précipitations moyennes par jour (mm)')
        dic['rainfall'] = dic.pop('Précipitations totales sur le mois (mm)')
        dic['record_rainfall_day'] = dic.pop('Record de précipitations sur une journée (mm)')
    else:
        dic['rainfall'] = dic.pop('Précipitations (mm)')
    
    dic['max_temp'] = dic.pop('Température maximale (°C)')
    dic['min_temp'] = dic.pop('Température minimale (°C)')
    dic['wind_speed'] = dic.pop('Vitesse du vent (km/h)')
    dic['humidity'] = dic.pop('Humidité (%)')
    dic['visibility'] = dic.pop('Visibilité (km)')
    dic['cloud_coverage'] = dic.pop('Couverture nuageuse (%)')
    dic['heat_index'] = dic.pop('Indice de chaleur')
    dic['dew_point_temp'] = dic.pop('Point de rosée (°C)')
    dic['pressure'] = dic.pop('Pression (hPa)')
    dic['sunrise_time'] = dic.pop('Heure du lever du soleil')
    dic['sunset_time'] = dic.pop('Heure du coucher du soleil')
    dic['day_length'] = dic.pop('Durée du jour')

    return dic

def get_historique_meteo_day(coord, year, month, day):
    address = get_city(coord)
    city, postal = select_city_postal(address)
    region_url = assign_old_state(postal[0:2])
    city_url, city = check_city(coord, region_url, city)

    now = datetime.datetime.now()
    date = datetime.datetime(year = year, month = month, day = day)
    date_l = datetime.datetime(year = 2010, month = 1, day = 1)
    assert (date >= date_l) and (date < now), "The date must be between 01-01-2010 and " + str(now.strftime('%d-%m-%Y'))

    m = '{0:0=2d}'.format(month)
    d = '{0:0=2d}'.format(day)
    url = 'https://www.historique-meteo.net/france/{0}/{1}/{2}/{3}/{4}'
    url = url.format(region_url, city_url, year, m, d)
    res = scrap_historique_meteo(url)

    res = standardise_keys_hm(res, day = True)

    return res

def get_historique_meteo(coord, year, month=None):
    """Documentation
    Parameters:
        coord: tuple of gps coordinates (longitude, latitude)
        year: year for the weather in integer
        month: month for the weather in integer
    Out:
        res: dictionnary of the weather
    """
    address = get_city(coord)
    city, postal = select_city_postal(address)
    region_url = assign_old_state(postal[0:2])
    city_url, city = check_city(coord, region_url, city)

    now = datetime.datetime.now()
    assert (int(year) >= 2009) & (int(year) <=
                                  now.year), "The year must be between 2009 and " + str(now.year)
    year = str(year)

    if month != None:
        month_2d = "{0:0=2d}".format(month)
        month_lim = check_last_date(region_url, city_url, year, month_2d)
        if year == now.year:
            assert (int(month) >= 0) & (
                int(month) <= int(month_lim)), "The month must be between 0 and " + str(month_lim) + " (last month available on the website)"
        else:
            assert (int(month) >= 0) & (int(month) <=
                                        12), "The month must be between 0 and 12"
        url = 'https://www.historique-meteo.net/france/{0}/{1}/{2}/{3}'
        url = url.format(region_url, city_url, year, month_2d)
        res = scrap_historique_meteo(url)

    else:
        if year == now.year:
            month_2d = "{0:0=2d}".format(month)
            month_lim = check_last_date(region_url, city_url, year, month_2d)
            range_month = int(month_lim) + 1
        else:
            range_month = 13

        res = defaultdict(list)

        for month in range(1, range_month):
            month_2d = "{0:0=2d}".format(month)
            url = 'https://www.historique-meteo.net/france/{0}/{1}/{2}/{3}'
            url = url.format(region_url, city_url, year, month_2d)
            dic = scrap_historique_meteo(url)
            for k, v in dic.items():
                res[k].append(v)

        mean_list = ['Température moyenne (°C)', 
                     'Température maximale (°C)',
                     'Température minimale (°C)', 
                     'Vitesse du vent (km/h)', 
                     'Température du vent (°C)', 
                     'Précipitations moyennes par jour (mm)',
                     'Précipitations totales sur le mois (mm)',
                     'Humidité (%)',
                     'Visibilité (km)',
                     'Couverture nuageuse (%)',
                     'Indice de chaleur',
                     'Point de rosée (°C)',
                     'Pression (hPa)']
        max_list = ['Température maximale record (°C)', 'Record de précipitations sur une journée (mm)']
        min_list = ['Température minimale record (°C)']
        mean_time = ['Heure du lever du soleil', 'Heure du coucher du soleil', 'Durée du jour']

        for key in mean_list:
            res[key] = np.mean(res[key])
        for key in max_list:
            res[key] = max(res[key])
        for key in min_list:
            res[key] = min(res[key])
        for key in mean_time:
            m = np.mean(list(map(lambda f: (((f.hour * 60) + f.minute) * 60) + f.second, res[key])))
            res[key] = datetime.datetime.strptime(str(datetime.timedelta(seconds = m)), '%H:%M:%S').time().strftime('%H:%M:%S')
        
    res = standardise_keys_hm(res)

    res['city'] = city
    return dict(res)

def scrap_historique_meteo(url):
    """Documentation
    Parameters:
        url: url for historique_meteo website
    Out:
        dic: dictionnary of the weather
    """
    page = requests.get(url)
    assert page.status_code == 200, "No data available for this date"
    soup = BeautifulSoup(page.content, 'html.parser')
    tableau = soup.find_all('tbody')[0]
    keys = tableau.find_all('td', class_ = None)[:-1]
    values = tableau.find_all('b')
    assert len(keys) == len(values), 'Wrong selection of the data'
    
    dic = {}
    
    for i in range(len(keys)):
        value = values[i].get_text().strip()
        tokeep = ''
        for char in value:
            if char.isdigit() or char == '.' or char == ':':
                tokeep += char
        if ':' in tokeep:
            tokeep = datetime.datetime.strptime(tokeep, '%H:%M:%S').time()
        else:
            tokeep = float(tokeep)
        
        pos = next(i for i,j in list(enumerate(value, 1))[::-1] if j.isdigit())
        unity = value[pos:]
        if unity == '°':
            unity += 'C'
        
        if unity != '':
            key = keys[i].get_text().strip() + ' (' + str(unity) + ')'
        else :
            key = keys[i].get_text().strip()
        
        dic[key] = tokeep
    return dic
            