## CONSTANTS

# historiquemeteo.py
URL_HISTORIQUE_METEO_MONTH = 'https://www.historique-meteo.net/france/{0}/{1}/{2}/{3}'
URL_HISTORIQUE_METEO_DAY = 'https://www.historique-meteo.net/france/{0}/{1}/{2}/{3}/{4}'

# meteofrance.py
URL_METEO_FRANCE = "http://www.meteofrance.com/climat/meteo-date-passee?lieuId={0}0&lieuType={1}&date={2}"

# maps.py
URL_TILE_PLAN = 'http://c.tiles.wmflabs.org/osm-no-labels/{z}/{x}/{y}.png'
URL_TILE_SAT = 'https://wxs.ign.fr/choisirgeoportail/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE=normal&TILEMATRIXSET=PM&FORMAT=image/jpeg&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}'

# elevation.py
URL_ELEVATION_FR = 'http://wxs.ign.fr/choisirgeoportail/alti/rest/elevation.json?lon={0}&lat={1}&zonly=true'
URL_ELEVATION_ALL = "https://api.opentopodata.org/v1/eudem25m?locations={0},{1}"

# sentinelAccess.py + sentinelProcessTest.py
URL_SENTINEL_API = 'https://scihub.copernicus.eu/dhus'