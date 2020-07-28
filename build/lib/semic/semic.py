from semic.maps import get_plan
from semic.meteo import get_historique_meteo, get_meteo, get_meteo_monthly, estimate_meteo_year, find_insee, get_historique_meteo_day
from semic.gps_info import get_elevation_fr, get_elevation, get_city, select_city_postal
from semic.sentinelProcess import search_tile
from semic.utils import center_of_line
import json
import datetime
import warnings

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
        self.dl_option = None
	self.cloudcover = None
    
    
    def set_sentinel_param(self, user, pwd, width, nb_of_tile=1, path_to_sentinel='./', tile_name=None, dl_option='n', cc=(0,10)):
        self.user = user
        self.pwd = pwd
        self.width = width
        self.path_to_sentinel = path_to_sentinel
        self.nb_tile = nb_of_tile
        self.tile_name = tile_name
        self.dl_option = dl_option
	self.cloudcover = cc

    def to_json(self, dic, name : str = 'dictionary', sort = True):
        dic_to_save = dic
        if 'img_plan' in dic:
            img_plan = dic['img_plan']
            img_plan.save(self.path + name + '_img_plan.jpg', 'JPEG')
            dic_to_save['img_plan'] = self.path + 'img_plan.jpg'
        if 'img_sat' in dic:
            img_sat = dic['img_sat']
            img_sat.save(self.path + name + '_img_sat.jpg', 'JPEG')
            dic_to_save['img_sat'] = self.path + 'img_sat.jpg'
        if 'img_sentinel' in dic:
            img_sentinel = dic['img_sentinel']
            img_sentinel.save(self.path + name + '_img_sentinel.jpg', 'JPEG')
            dic_to_save['img_sentinel'] = self.path + 'img_sentinel.jpg'

        with open(self.path + name + '.json', 'w') as fp:
            json.dump(dic_to_save, fp, sort_keys=sort, indent=4, default = str)

    def point(self, coords, year : int, month : int = None, day : int = None, outputs = ['max_temp', 'min_temp', 'avg_temp', 'record_max_temp', 'record_min_temp', 'wind_speed', 'humidity', 'visibility', 'cloud_coverage', 'heat_index', 'dew_point_temp', 'pressure', 'sunrise_time', 'sunset_time', 'day_length', 'rainfall', 'avg_rainfall_per_day', 'record_rainfall_day', 'img_plan', 'img_sat', 'elevation', 'img_sentinel', 'city']):
        if day != None:                
            # city, postal = select_city_postal(get_city(coords))
            # insee_code = find_insee(city, postal)
            # date = "{0:0=2d}".format(day) + '-' + "{0:0=2d}".format(month) + '-' + str(year)
            # weather = get_meteo(insee_code, date)
            weather = get_historique_meteo_day(coords, year, month, day)
        else:
            weather = get_historique_meteo(coords, year, month)
        possible_keys = set(['max_temp', 'min_temp', 'avg_temp', 'record_max_temp', 'record_min_temp', 'wind_speed', 'humidity', 'visibility', 'cloud_coverage', 'heat_index', 'dew_point_temp', 'pressure', 'sunrise_time', 'sunset_time', 'day_length', 'rainfall', 'avg_rainfall_per_day', 'record_rainfall_day', 'img_plan', 'img_sat', 'elevation', 'img_sentinel', 'city'])
        if len(set(outputs) - possible_keys) != 0:
            raise Exception("Wrong key(s) : " + str(set(outputs) - possible_keys))
        unwanted = set(weather) - set(outputs)
        for unwanted_key in unwanted:
            del weather[unwanted_key]
        
        if 'img_plan' in outputs:
            img_plan = get_plan(coords, self.width, style = 'plan', width = self.size[0], height = self.size[1])
            weather['img_plan'] = img_plan
        if 'img_sat' in outputs:
            img_sat = get_plan(coords, self.width, style = 'sat', width = self.size[0], height = self.size[1])
            weather['img_sat'] = img_sat
        if 'elevation' in outputs:
            elevation = get_elevation_fr(coords)
            weather['elevation'] = elevation
        if 'img_sentinel' in outputs:
            if (self.user == None) or (self.pwd == None):
                warnings.warn("Sentinel's user and password must be set to collect sentinel's data (with set_sentinel_param)")
                return weather
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
                                    self.nb_tile, self.path_to_sentinel, self.tile_name, self.dl_option, self.cloudcover)
            if img_sentinel != None :
                weather['img_sentinel'] = img_sentinel
        
        return weather
    
    def line(self, coords, year : int, month : int = None, day : int = None, outputs = ['max_temp', 'min_temp', 'avg_temp', 'record_max_temp', 'record_min_temp', 'wind_speed', 'humidity', 'visibility', 'cloud_coverage', 'heat_index', 'dew_point_temp', 'pressure', 'sunrise_time', 'sunset_time', 'day_length', 'rainfall', 'avg_rainfall_per_day', 'record_rainfall_day', 'img_plan', 'img_sat', 'elevation', 'img_sentinel', 'city']):
        center = center_of_line(coords)
        if day != None:
            # city, postal = select_city_postal(get_city(center))
            # insee_code = find_insee(city, postal)
            # date = "{0:0=2d}".format(day) + '-' + "{0:0=2d}".format(month) + '-' + str(year)
            # weather = get_meteo(insee_code, date)
            weather = get_historique_meteo_day(center, year, month, day)
        else:
            weather = get_historique_meteo(center, year, month)
        
        possible_keys = set(['max_temp', 'min_temp', 'avg_temp', 'record_max_temp', 'record_min_temp', 'wind_speed', 'humidity', 'visibility', 'cloud_coverage', 'heat_index', 'dew_point_temp', 'pressure', 'sunrise_time', 'sunset_time', 'day_length', 'rainfall', 'avg_rainfall_per_day', 'record_rainfall_day', 'img_plan', 'img_sat', 'elevation', 'img_sentinel', 'city'])
        if len(set(outputs) - possible_keys) != 0:
            raise Exception("Wrong key(s) : " + str(set(outputs) - possible_keys))
        unwanted = set(weather) - set(outputs)
        for unwanted_key in unwanted:
            del weather[unwanted_key]

        if 'img_plan' in outputs:
            img_plan = get_plan(coords, self.width, style = 'plan', width = self.size[0], height = self.size[1])
            weather['img_plan'] = img_plan
        if 'img_sat' in outputs:
            img_sat = get_plan(coords, self.width, style = 'sat', width = self.size[0], height = self.size[1])
            weather['img_sat'] = img_sat
        if 'elevation' in outputs:
            elevation = get_elevation_fr(coords)
            weather['elevation'] = elevation
        if 'img_sentinel' in outputs:
            if (self.user == None) or (self.pwd == None):
                warnings.warn("Sentinel's user and password must be set to collect sentinel's data (with set_sentinel_param)")
                return weather
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
                                    self.nb_tile, self.path_to_sentinel, self.tile_name, self.dl_option, self.cloudcover)
            if img_sentinel != None :
                weather['img_sentinel'] = img_sentinel
        
        return weather

    def polyline(self, coords, year, month = None, day = None, outputs = ['max_temp', 'min_temp', 'avg_temp', 'record_max_temp', 'record_min_temp', 'wind_speed', 'humidity', 'visibility', 'cloud_coverage', 'heat_index', 'dew_point_temp', 'pressure', 'sunrise_time', 'sunset_time', 'day_length', 'rainfall', 'avg_rainfall_per_day', 'record_rainfall_day', 'img_plan', 'img_sat', 'elevation', 'img_sentinel', 'city']):
        flat_list = [item for sublist in coords for item in sublist]
        center = center_of_line(flat_list)
        if day != None:
            assert month != None, 'Month parameter must be filled in.'
            weather = get_historique_meteo_day(center, year, month, day)
        else: 
            weather = get_historique_meteo(center, year)
        
        possible_keys = set(['max_temp', 'min_temp', 'avg_temp', 'record_max_temp', 'record_min_temp', 'wind_speed', 'humidity', 'visibility', 'cloud_coverage', 'heat_index', 'dew_point_temp', 'pressure', 'sunrise_time', 'sunset_time', 'day_length', 'rainfall', 'avg_rainfall_per_day', 'record_rainfall_day', 'img_plan', 'img_sat', 'elevation', 'img_sentinel', 'city'])
        if len(set(outputs) - possible_keys) != 0:
            raise Exception("Wrong key(s) : " + str(set(outputs) - possible_keys))
        unwanted = set(weather) - set(outputs)
        for unwanted_key in unwanted:
            del weather[unwanted_key]
        
        if 'elevation' in outputs:
            list_elevation = []
            for coord in coords:
                list_elevation.append(get_elevation_fr(coord))
            weather['elevation'] = list_elevation
        if 'img_plan' in outputs:
            img_plan = get_plan(coords, self.width, style = 'plan', width = self.size[0], height = self.size[1], poly = True)
            weather['img_plan'] = img_plan
        if 'img_sat' in outputs:
            img_sat = get_plan(coords, self.width, style = 'sat', width = self.size[0], height = self.size[1], poly = True)        
            weather['img_sat'] = img_sat
        
        if 'img_sentinel' in outputs:
            if (self.user == None) or (self.pwd == None):
                warnings.warn("Sentinel's user and password must be set to collect sentinel's data (with set_sentinel_param)")
                return weather
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
                                    self.nb_tile, self.path_to_sentinel, self.tile_name, self.dl_option, self.cloudcover)
            if img_sentinel != None :
                weather['img_sentinel'] = img_sentinel
        return weather     

        
