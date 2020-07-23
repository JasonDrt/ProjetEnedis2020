import requests
from semic.utils import URL_ELEVATION_ALL, URL_ELEVATION_FR

def get_elevation_fr(coord : iter):
    if any(isinstance(el, (tuple, list)) for el in coord):
        lon = [i[0] for i in coord]
        lat = [i[1] for i in coord]
        lon = '|'.join(map(str, lon))
        lat = '|'.join(map(str, lat))
    else:
        lon = coord[0]
        lat = coord[1]
    query = URL_ELEVATION_FR
    q = query.format(lon, lat)
    r = requests.get(q)
    dic = r.json()
    list_elevations = dic['elevations']
    return list_elevations

def get_elevation(coord):
    lon = coord[0]
    lat = coord[1]
    url = URL_ELEVATION_ALL
    url = url.format(lat, lon)
    page = requests.get(url).json()
    if page['status'] == 'OK':
        return page['results'][0]['elevation']
    else:
        print('The request did not work')
        return -10000