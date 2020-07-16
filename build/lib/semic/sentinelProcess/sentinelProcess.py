#pip install sentinelsat
#pip install rasterio
#pip install pyproj
#pip install opencv-python
"""!!! Make sure you installed OpenJPEG (https://www.openjpeg.org/) !!!"""

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio import plot
from rasterio.transform import xy
from pyproj import Proj, transform
import os.path
from os import path
import zipfile
from PIL import Image
from semic.sentinelProcess import connect_api, get_products, dl_products
     
def tci_process(path,width,gps_coord):
    #chargement de l'image
    tci = rasterio.open(path, driver='JP2OpenJPEG') #colors
    band1 = tci.read(1)
    band2 = tci.read(2)
    band3 = tci.read(3)
    dim = band1.shape
    x_init,y_init = xy(tci.transform,0,0)
    #conversion coordonnées gps vers référentiel de l'image
    inProj = Proj(init='epsg:4326')
    outProj = Proj(init=tci.crs)
    x_gps,y_gps = gps_coord
    x_im,y_im = transform(inProj,outProj,x_gps,y_gps)
    x_im,y_im = float(round(x_im)),float(round(y_im))
    #recherche du point gps dans l'image
    i,j = 0,0
    while abs(x_init - x_im) > 10 :
        j+=1
        x_init = xy(tci.transform,0,j)[0]
    while abs(y_init - y_im) > 10 :
        i+=1
        y_init = xy(tci.transform,i,0)[1]
    #sélection de la zone voulue
    width = width*100
    if (i-(width/2) >= 0) and (i+(width/2) <= dim[0]) :
        i_t = round(i - width/2)
        i_b = round(i + width/2)
    elif i-(width/2) < 0 :
        #on duplique la 1er ligne
        c1,c2,c3 = band1[0],band2[0],band3[0]
        for k in range(round(i-(width/2))):
            band1 = np.insert(band1,0,c1,axis=0)
            band2 = np.insert(band2,0,c2,axis=0)
            band3 = np.insert(band3,0,c3,axis=0)
        i_t = 0
        i_b = i_t + width
    elif i+(width/2) > dim[0] :
        #on duplique la dernière ligne
        c1,c2,c3 = band1[dim[0]-1],band2[dim[0]-1],band3[dim[0]-1]
        for k in range(round(i+(width/2))-dim[0]):
            band1 = np.insert(band1,dim[0],c1,axis=0)
            band2 = np.insert(band2,dim[0],c2,axis=0)
            band3 = np.insert(band3,dim[0],c3,axis=0)
        i_b = band1.shape[0]
        i_t = i_b - width
    if (j-(width/2) >= 0) and (j+(width/2) <= dim[1]) :
        j_l = round(j - width/2)
        j_r = round(j + width/2)
    elif j-(width/2) < 0 :
        #on duplique la première colonne
        c1,c2,c3 = band1[:,0],band2[:,0],band3[:,0]
        for k in range(round(j-(width/2))):
            band1 = np.insert(band1,0,c1,axis=1)
            band2 = np.insert(band2,0,c2,axis=1)
            band3 = np.insert(band3,0,c3,axis=1)
        j_l = 0
        j_r = j_l + width
    elif j+(width/2) > dim[1] :
        #on duplique la dernière colonne
        c1,c2,c3 = band1[:,dim[1]-1], band2[:,dim[1]-1], band3[:,dim[1]-1]
        for k in range(round(j+(width/2))-dim[1]):
            band1 = np.insert(band1,dim[1],c1,axis=1)
            band2 = np.insert(band2,dim[1],c2,axis=1)
            band3 = np.insert(band3,dim[1],c3,axis=1)
        j_r = band1.shape[1]
        j_l = j_r - width
    band1 = band1[i_t:i_b,j_l:j_r]
    band2 = band2[i_t:i_b,j_l:j_r]
    band3 = band3[i_t:i_b,j_l:j_r]
    return(band1, band2, band3)

def search_tile(user,pw,date,gps_coord,width,l=1,p='./',tile_name=None,option='n'):
    #Connect to Sentinel2 API and search tiles.
    api = connect_api(user, pw)
    if tile_name == None:
        gps_coord_str = str(gps_coord[1])+', '+str(gps_coord[0])
        df_prod = get_products(api, gps_coord_str, date, lim=l)
    else :
        products = api.query(filename=tile_name)
        df_prod = api.to_dataframe(products)
    #Check if the tile has already been downloaded and/or unziped.
    #Image process when it's possible.
    if os.path.exists(p+df_prod['title'][0]+'.SAFE'):
        file_path = p+df_prod['title'][0]+'.SAFE/GRANULE/'
        directories=[]
        for paths, dirs, files in os.walk(file_path):
            for d in dirs:
                directories.append(d)
            for f in files :
                if 'TCI_10m' in f:
                    filename = f
        file_path = file_path+directories[0]+'/IMG_DATA/R10m/'+filename
        band1, band2, band3 = tci_process(file_path,width,gps_coord)
        img = np.zeros((band1.shape[0],band1.shape[1],3),dtype=np.uint8)
        img[:,:,0] = band1
        img[:,:,1] = band2
        img[:,:,2] = band3
        img_pil = Image.fromarray(img)
        return(img_pil)
    
    elif os.path.exists(p+df_prod['title'][0]+'.zip'):
        with zipfile.ZipFile(p+df_prod['title'][0]+'.zip', 'r') as zip_ref:
            zip_ref.extractall(p)
        
        file_path = p+df_prod['title'][0]+'.SAFE/GRANULE/'
        directories=[]
        for paths, dirs, files in os.walk(file_path):
            for d in dirs:
                directories.append(d)
            for f in files :
                if 'TCI_10m' in f:
                    filename = f
        file_path = file_path+directories[0]+'/IMG_DATA/R10m/'+filename
        band1, band2, band3 = tci_process(file_path,width,gps_coord)
        img = np.zeros((band1.shape[0],band1.shape[1],3),dtype=np.uint8)
        img[:,:,0] = band1
        img[:,:,1] = band2
        img[:,:,2] = band3
        img_pil = Image.fromarray(img)
        return(img_pil)
    
    else :
        #Download proposal
        dl_products(api, df_prod,option)
        return(None)
        
def print_img(br,bg,bb,size,name):
    img = np.zeros((br.shape[0],br.shape[1],3))
    img[:,:,0] = br/255
    img[:,:,1] = bg/255
    img[:,:,2] = bb/255
    img = cv2.resize(img,size)
    cv2.imshow(name,img)
    cv2.waitKey()
    cv2.destroyAllWindows()

def _main_(user,pw,gps_coord,date,width,size,p='./',tile_name=None,name='SentinelImage'):
    b1, b2, b3 = search_tile(user,pw,date,gps_coord,width,p=p,tile_name=tile_name)
    print_img(b3,b2,b1,size,name=name)
