from semic.maps import get_plan
from semic.meteo import get_historique_meteo, get_meteo, get_meteo_monthly, estimate_meteo_year, find_insee
from semic.gps_info import get_elevation_fr, get_elevation, get_city, select_city_postal
from semic.sentinelProcess import search_tile

class Point:
    def __init__(self, coord):
        self.coord = coord
        self.lon = coord[0]
        self.lat = coord[1]

    def elevation(self):
        return get_elevation_fr(self.coord)
    
    def weather(self, year : int, month : int = None, day : int = None):
        if month == None:
            assert day == None, "Parameter month must be filled in"
            return get_historique_meteo(self.coord, year)
        else:
            if day == None:
                return get_historique_meteo(self.coord, year, month)
            else:
                address = get_city(self.coord)
                city, postal_code = select_city_postal(address)
                insee_code = find_insee(city, postal_code)
                date = "{0:0=2d}".format(day) + "-" + "{0:0=2d}".format(month) + str(year)
                return get_meteo(insee_code, date)
    
    def map(self, dist, style = 'plan', width = None, height = None):
        return get_plan(self.coord, dist, style, width, height)
    
    def get_sentinel_im(self, user, pw, date, width, size, l=1, p='./',tile_name=None):
        im = search_tile(user, pw, date, self.coord, width, l, p, tile_name)
        if im != None :
            im = im.resize(size)
            return(im)

class Line:
    def __init__(self, coords):
        self.coords = coords

    def _center_of_line(self):
        length = len(self.coords)
        lon = sum(i[0] for i in self.coords) / length
        lat = sum(i[1] for i in  self.coords) / length
        center = (lon, lat)
        return center

    def weather(self, year : int, month : int = None, day : int = None):
        center = self._center_of_line()

        if month == None:
            assert day == None, "Parameter month must be filled in"
            return get_historique_meteo(center, year)
        else:
            if day == None:
                return get_historique_meteo(center, year, month)
            else:
                address = get_city(center)
                city, postal_code = select_city_postal(address)
                insee_code = find_insee(city, postal_code)
                date = "{0:0=2d}".format(day) + "-" + "{0:0=2d}".format(month) + '-' + str(year)
                return get_meteo(insee_code, date)
    
    def map(self, dist, style = 'plan', width = None, height = None):
        return get_plan(self.coords, dist, style, width, height)
    
    def elevation(self):
        list_elevations = get_elevation_fr(self.coords)
        return list_elevations

    def get_sentinel_im(self, user, pw, date, width, size, l=1, p='./',tile_name=None):
        center = self._center_of_line()
        im = search_tile(user, pw, date, center, width, l, p, tile_name)
        if im != None :
            im = im.resize(size)
            return(im)

# class PolyLine:
#     def __init__(self, coords):
#         self.coords = coords
        
#     def _center_of_polyline(self):
        
#     def meteo(self, year, month = None, day = None):

        