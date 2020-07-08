from staticmap import StaticMap, CircleMarker, Line, Polygon

def get_plan(coord, dist, style='plan', width = None, height = None):
    """Documentation
    Parameters:
        coord: tuple of gps coordinates (longitude, latitude)
        dist: distance to see around the gps coordinates
        style: style of the static map in (plan, sat)
        width: width of the image
        height: height of the image
    Out:
        static map arround the gps coordinates
    """
    if style == 'plan':
        # zoom : [1; 20]
        url_temp = 'http://c.tiles.wmflabs.org/osm-no-labels/{z}/{x}/{y}.png'
    elif style == 'sat':
        # zoom : [1; 19]
        # bounds: [[-75, -180], [81, 180]]
        url_temp = 'https://wxs.ign.fr/choisirgeoportail/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE=normal&TILEMATRIXSET=PM&FORMAT=image/jpeg&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}'
    
    if width == None:
        width = dist
    if height == None:
        height = dist
    
    m = StaticMap(width, height, url_template=url_temp, tile_size = 256)
    if any(isinstance(el, (tuple, list)) for el in coord):
        flat_list = [item for sublist in coord for item in sublist]
        line = Line(flat_list, 'red', 2)
        m.add_line(line)
    else:
        marker = CircleMarker(coord, 'red', 5)  # longitude, latitude
        m.add_marker(marker)
    image = m.render()
    return image