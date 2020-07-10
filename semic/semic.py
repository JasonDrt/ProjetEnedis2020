from semic.maps import get_plan
from semic.meteo import get_historique_meteo, get_meteo, get_meteo_monthly, estimate_meteo_year, find_insee
from semic.gps_info import get_elevation_fr, get_elevation, get_city, select_city_postal
from semic.sentinelProcess import search_tile
from semic.utils import center_of_line
import json

class DataRequest:
    def __init__(self, path_to_folder, size_img):
        self.path = path_to_folder
        self.size = size_img
        self.user = None
        self.pwd = None
    
    def set_sentinel_logs(self, user, pwd):
        self.user = user
        self.pwd = pwd

    def to_json(self, dic, sort = True):
        with open(self.path + dic['Ville'] + '_' + '' + '.json', 'w') as fp:
            json.dump(dic, fp, sort_keys=sort, indent=4)

    def point(self, coords, date, dist):
        img_plan = get_plan(coords, dist, style = 'plan', width = self.size[0], height = self.size[1])
        img_sat = get_plan(coords, dist, style = 'sat', width = self.size[0], height = self.size[1])
        if (self.user != None) and (self.pwd != None):
            img_sentinel = search_tile(self.user, self.pwd, date, coords, dist)
        elevation = get_elevation_fr(coords)
        weather = get_historique_meteo(coords, date)

        weather['elevation'] = elevation
        weather['img_sat'] = img_sat
        weather['img_plan'] = img_plan
        weather['img_sentinel'] = img_sentinel

        return weather
    
    def line(self, coords, date, dist):
        center = center_of_line(coords)
        img_plan = get_plan(center, dist, style = 'plan', width = self.size[0], height = self.size[1])
        img_sat = get_plan(center, dist, style = 'sat', width = self.size[0], height = self.size[1])
        if (self.user != None) and (self.pwd != None):
            img_sentinel = search_tile(self.user, self.pwd, date, center, dist)
        elevation = get_elevation_fr(coords)
        weather = get_historique_meteo(center, date)
        
        weather['elevation'] = elevation
        weather['img_sat'] = img_sat
        weather['img_plan'] = img_plan
        weather['img_sentinel'] = img_sentinel

        return weather

    # def polyline(self, coords, date, dist):
    #     res = {}
    #     list_elevation = []
    #     for coord in coords:
    #         list_elevation.append(get_elevation_fr(coord))
    #     flat_list = [item for sublist in coords for item in sublist]
    #     center = center_of_line(flat_list)

    #     return res           

        