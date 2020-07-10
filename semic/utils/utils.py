import numpy as np

def center_of_line(coords):
    lon = np.mean([i[0] for i in coords])
    lat = np.mean([i[1] for i in coords])
    return (lon, lat)