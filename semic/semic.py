from semic.maps import get_plan
from semic.meteo import get_historique_meteo, get_meteo, get_meteo_monthly, estimate_meteo_year, find_insee, get_historique_meteo_day
from semic.gps_info import get_elevation_fr, get_elevation, get_city, select_city_postal
from semic.sentinelProcess import search_tile
from semic.utils import center_of_line
import json
import datetime

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
    
    
    def set_sentinel_param(self, user, pwd, width, nb_of_tile=1, path_to_sentinel='./', tile_name=None, dl_option='n'):
        self.user = user
        self.pwd = pwd
        self.width = width
        self.path_to_sentinel = path_to_sentinel
        self.nb_tile = nb_of_tile
        self.tile_name = tile_name
        self.dl_option = dl_option
    
    # def datetime_converter(obj):
    #     if isinstance(obj, datetime.datetime):
    #         return obj.__str__()

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
        # if 'Heure du lever du soleil' in dic :
        #     dic['Heure du lever du soleil'] = dic['Heure du lever du soleil'].isoformat()
        # if 'Heure du coucher du soleil' in dic :
        #     dic['Heure du coucher du soleil'] = dic['Heure du coucher du soleil'].isoformat()
        # if 'Durée du jour' in dic :
        #     dic['Durée du jour'] = dic['Durée du jour'].isoformat()

        with open(self.path + dic['Ville'] + '_' + '' + '.json', 'w') as fp:
            json.dump(dic, fp, sort_keys=sort, indent=4, default = str)

    def point(self, coords, year : int, month : int = None, day : int = None, outputs = ['max_temp', 'min_temp', 'avg_temp', 'record_max_temp', 'record_min_temp', 'wind_speed', 'humidity', 'visibility', 'cloud_coverage', 'heat_index', 'dew_point_temp', 'pressure', 'sunrise_time', 'sunset_time', 'day_length', 'rainfall', 'avg_rainfall_per_day', 'record_rainfall_day', 'img_plan', 'img_sat', 'elevation', 'img_sentinel']):
        if day != None:                
            # city, postal = select_city_postal(get_city(coords))
            # insee_code = find_insee(city, postal)
            # date = "{0:0=2d}".format(day) + '-' + "{0:0=2d}".format(month) + '-' + str(year)
            # weather = get_meteo(insee_code, date)
            weather = get_historique_meteo_day(coords, year, month, day)
        else:
            weather = get_historique_meteo(coords, year, month)
        unwanted = set(outputs) - set(weather)
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
            assert (self.user != None) and (self.pwd != None), "Sentinel's user and password must be set to collect sentinel's data (with set_sentinel_param)"
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
                                    self.nb_tile, self.path_to_sentinel, self.tile_name, self.dl_option)
            if img_sentinel != None :
                weather['img_sentinel'] = img_sentinel
        
        return weather
    
    def line(self, coords, year : int, month : int = None, day : int = None):
        center = center_of_line(coords)
        if day != None:
            # city, postal = select_city_postal(get_city(center))
            # insee_code = find_insee(city, postal)
            # date = "{0:0=2d}".format(day) + '-' + "{0:0=2d}".format(month) + '-' + str(year)
            # weather = get_meteo(insee_code, date)
            weather = get_historique_meteo_day(center, year, month, day)
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
                                       self.nb_tile, self.path_to_sentinel, self.tile_name, self.dl_option)
            if img_sentinel != None :
                weather['img_sentinel'] = img_sentinel
        elevation = get_elevation_fr(coords)
        
        
        weather['elevation'] = elevation
        weather['img_sat'] = img_sat
        weather['img_plan'] = img_plan

        return weather

    def polyline(self, coords, dist, year, month = None, day = None):
        list_elevation = []
        for coord in coords:
            list_elevation.append(get_elevation_fr(coord))
        img_plan = get_plan(coords, dist, style = 'plan', width = self.size[0], height = self.size[1], poly = True)
        img_sat = get_plan(coords, dist, style = 'sat', width = self.size[0], height = self.size[1], poly = True)
        
        flat_list = [item for sublist in coords for item in sublist]
        center = center_of_line(flat_list)
        if day != None:
            assert month != None, 'Month parameter must be filled in.'
            weather = get_historique_meteo_day(center, year, month, day)
        else: 
            if month != None:
                weather = get_historique_meteo(center, year, month)
            else:
                weather = get_historique_meteo(center, year)

        weather['img_plan'] = img_plan
        weather['img_sat'] = img_sat
        weather['elevation'] = list_elevation

        return weather     

        
