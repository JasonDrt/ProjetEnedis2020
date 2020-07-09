from semic.maps import get_plan
from semic.meteo import get_historique_meteo, get_meteo, get_meteo_monthly, estimate_meteo_year, find_insee
from semic.gps_info import get_elevation_fr, get_elevation, get_city, select_city_postal
from semic.sentinelProcess import search_tile

class Point:
    def __init__(self, coord, year:int, month:int = None, day:int = None, user, pw, width, size,dist):
        self.coord = coord
        self.lon = coord[0]
        self.lat = coord[1]
        self.year = year
        self.month = month
        self.day = day
        self.user = user
        self.pw = pw
        self.width = width
        self.size = size
        self.dist = dist
        
    def elevation(self):
        return get_elevation_fr(self.coord)
    
    def weather(self):
        if self.month == None:
            assert self.day == None, "Parameter month must be filled in"
            return get_historique_meteo(self.coord, self.year)
        else:
            if self.day == None:
                return get_historique_meteo(self.coord, self.year, self.month)
            else:
                address = get_city(self.coord)
                city, postal_code = select_city_postal(address)
                insee_code = find_insee(city, postal_code)
                date = "{0:0=2d}".format(self.day) + "-" + "{0:0=2d}".format(self.month) + str(self.year)
                return get_meteo(insee_code, date)
    
    def map(self, style = 'plan', w = None, height = None):
        return get_plan(self.coord, self.dist, style, w, height)
    
    def get_sentinel_im(self, l=1, p='./',tile_name=None):
        date = (str(self.year)+'-'+"{0:0=2d}".format(self.month)+'-'+"{0:0=2d}".format(self.day)+'T00:00:00Z-10DAYS', 
                str(self.year)+'-'+"{0:0=2d}".format(self.month)+'-'+"{0:0=2d}".format(self.day)+'T00:00:00Z')
        im = search_tile(self.user, self.pw, date, self.coord, self.width, l, p, tile_name)
        if im != None :
            im = im.resize(self.size)
            return(im)

class Line:
    def __init__(self, coords, year:int, month:int = None, day:int = None, user, pw, width, size,dist):
        self.coords = coord
        self.year = year
        self.month = month
        self.day = day
        self.user = user
        self.pw = pw
        self.width = width
        self.size = size
        self.dist = dists

    def _center_of_line(self):
        length = len(self.coords)
        lon = sum(i[0] for i in self.coords) / length
        lat = sum(i[1] for i in  self.coords) / length
        center = (lon, lat)
        return center

    def weather(self):
        center = self._center_of_line()

        if self.month == None:
            assert self.day == None, "Parameter 'month' must be filled in"
            return get_historique_meteo(center, self.year)
        else:
            if self.day == None:
                return get_historique_meteo(center, self.year, self.month)
            else:
                address = get_city(center)
                city, postal_code = select_city_postal(address)
                insee_code = find_insee(city, postal_code)
                date = "{0:0=2d}".format(self.day) + "-" + "{0:0=2d}".format(self.month) + '-' + str(self.year)
                return get_meteo(insee_code, date)
    
    def map(self, style = 'plan', w = None, height = None):
        return get_plan(self.coords, self.dist, style, w, height)
    
    def elevation(self):
        list_elevations = get_elevation_fr(self.coords)
        return list_elevations

    def get_sentinel_im(self, l=1, p='./',tile_name=None):
        date = (str(self.year)+'-'+"{0:0=2d}".format(self.month)+'-'+"{0:0=2d}".format(self.day)+'T00:00:00Z-10DAYS', 
                str(self.year)+'-'+"{0:0=2d}".format(self.month)+'-'+"{0:0=2d}".format(self.day)+'T00:00:00Z')
        center = self._center_of_line()
        im = search_tile(self.user, self.pw, date, center, self.width, l, p, tile_name)
        if im != None :
            im = im.resize(self.size)
            return(im)
