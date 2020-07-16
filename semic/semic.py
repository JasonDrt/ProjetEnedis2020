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
        self.width = None
        self.path_to_sentinel = None
        self.nb_tile = None
        self.tile_name = None
    
    
    def set_sentinel_param(self, user, pwd, width, nb_of_tile=1, path_to_sentinel='./', tile_name=None, dw_option='n'):
        self.user = user
        self.pwd = pwd
        self.width = width
        self.path_to_sentinel = path_to_sentinel
        self.nb_tile = nb_of_tile
        self.tile_name = tile_name
	self.dw_option = dw_option
    
    def to_json(self, dic, sort = True):
        if 'img_plan' in dic:
            img_plan = dic['img_plan']
            img_plan.save(self.path + 'img_plan.jpg', 'JPEG')
            dic['img_plan'] = self.path + 'img_plan.jpg'
        if 'img_sat' in dic:
            img_sat = dic['img_sat']
            img_sat.save(self.path + 'img_sat.jpg', 'JPEG')
            dic['img_sat'] = self.path + 'img_sat.jpg'
        if 'img_sentinel' in dic:
            img_sentinel = dic['img_sentinel']
            img_sentinel.save(self.path + 'img_sentinel.jpg', 'JPEG')
            dic['img_sentinel'] = self.path + 'img_sentinel.jpg'

        with open(self.path + dic['Ville'] + '_' + '' + '.json', 'w') as fp:
            json.dump(dic, fp, sort_keys=sort, indent=4)

    def point(self, coords, year : int, month : int = None, day : int = None):
        if day != None:
            city, postal = select_city_postal(get_city(coords))
            insee_code = find_insee(city, postal)
            date = "{0:0=2d}".format(day) + '-' + "{0:0=2d}".format(month) + '-' + str(year)
            weather = get_meteo(insee_code, date)
        else:
            weather = get_historique_meteo(coords, year, month)
        img_plan = get_plan(coords, self.width, style = 'plan', width = self.size[0], height = self.size[1])
        img_sat = get_plan(coords, self.width, style = 'sat', width = self.size[0], height = self.size[1])
        if (self.user != None) and (self.pwd != None):
            if day != None :
                date = (str(year)+'-'+"{0:0=2d}".format(month)+'-'+"{0:0=2d}".format(day)+'T00:00:00Z-10DAYS', 
                str(year)+'-'+"{0:0=2d}".format(month)+'-'+"{0:0=2d}".format(day)+'T00:00:00Z')
            elif month != None :
                date = date = (str(year)+'-'+"{0:0=2d}".format(month)+'-'+"01"+'T00:00:00Z-10DAYS', 
                str(year)+'-'+"{0:0=2d}".format(month)+'-'+"01"+'T00:00:00Z')
            else :
                date = date = (str(year)+'-'+"01"+'-'+"01"+'T00:00:00Z-10DAYS', 
                str(year)+'-'+"01"+'-'+"01"+'T00:00:00Z')
            img_sentinel = search_tile(self.user, self.pwd, date, coords, self.width, 
                                       self.nb_tile, self.path_to_sentinel, self.tile_name, self.dw_option)
            if img_sentinel != None :
                weather['img_sentinel'] = img_sentinel
        
        elevation = get_elevation_fr(coords)
        

        weather['elevation'] = elevation
        weather['img_sat'] = img_sat
        weather['img_plan'] = img_plan

        return weather
    
    def line(self, coords, year : int, month : int = None, day : int = None):
        center = center_of_line(coords)
        if day != None:
            city, postal = select_city_postal(get_city(center))
            insee_code = find_insee(city, postal)
            date = "{0:0=2d}".format(day) + '-' + "{0:0=2d}".format(month) + '-' + str(year)
            weather = get_meteo(insee_code, date)
        else:
            weather = get_historique_meteo(center, year, month)
        img_plan = get_plan(coords, self.width, style = 'plan', width = self.size[0], height = self.size[1])
        img_sat = get_plan(coords, self.width, style = 'sat', width = self.size[0], height = self.size[1])
        if (self.user != None) and (self.pwd != None):
            if day != None :
                date = (str(year)+'-'+"{0:0=2d}".format(month)+'-'+"{0:0=2d}".format(day)+'T00:00:00Z-10DAYS', 
                str(year)+'-'+"{0:0=2d}".format(month)+'-'+"{0:0=2d}".format(day)+'T00:00:00Z')
            elif month != None :
                date = date = (str(year)+'-'+"{0:0=2d}".format(month)+'-'+"01"+'T00:00:00Z-10DAYS', 
                str(year)+'-'+"{0:0=2d}".format(month)+'-'+"01"+'T00:00:00Z')
            else :
                date = date = (str(year)+'-'+"01"+'-'+"01"+'T00:00:00Z-10DAYS', 
                str(year)+'-'+"01"+'-'+"01"+'T00:00:00Z')
            img_sentinel = search_tile(self.user, self.pwd, date, center, self.width, 
                                       self.nb_tile, self.path_to_sentinel, self.tile_name, self.dw_option)
            if img_sentinel != None :
                weather['img_sentinel'] = img_sentinel
        elevation = get_elevation_fr(coords)
        
        
        weather['elevation'] = elevation
        weather['img_sat'] = img_sat
        weather['img_plan'] = img_plan

        return weather

    def polyline(self, coords, date, dist):
        list_elevation = []
        for coord in coords:
            list_elevation.append(get_elevation_fr(coord))
        img_plan = get_plan(coords, dist, style = 'plan', width = self.size[0], height = self.size[1], poly = True)
        img_sat = get_plan(coords, dist, style = 'sat', width = self.size[0], height = self.size[1], poly = True)
        
        flat_list = [item for sublist in coords for item in sublist]
        center = center_of_line(flat_list)
        weather = get_historique_meteo(center, date)

        weather['img_plan'] = img_plan
        weather['img_sat'] = img_sat
        weather['elevation'] = list_elevation

        return weather     

        
