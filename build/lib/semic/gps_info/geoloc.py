from geopy.geocoders import Nominatim

def get_city(coord : iter):
    """
    Input: 
        coord: tuple of gps coordinates (longitude, latitude)
    Output:
        dictionnary of the address of the location
    """
    lat = coord[1]
    lon = coord[0]
    nominatim = Nominatim(user_agent = 'my-application')
    r = nominatim.reverse(str(lat) + ',' + str(lon))
    dic = r.raw['address']
    return dic

def select_city_postal(address : dict):
    """
    Input:
        address: dictionnary of the address of a location
    Output:
        name and post code of the location
    """
    if 'village' in address.keys():
        city = 'village'
        if 'postal_code' in address.keys():
            postal = 'postal_code'
        else:
            postal = 'postcode'
    else:
        city = 'city'
        if 'postal_code' in address.keys():
            postal = 'postal_code'
        else:
            postal = 'postcode'
    return address[city], address[postal]