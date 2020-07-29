import numpy as np

def center_of_line(coords):
    """
    Input:
        coords: list of tuples of GPS coordinates
    Output:
        tuple of mean longitudes and latitudes
    """
    lon = np.mean([i[0] for i in coords])
    lat = np.mean([i[1] for i in coords])
    return (lon, lat)