#pip install sentinelsat

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def connect_api(user,pw,link='https://scihub.copernicus.eu/dhus'):
    return SentinelAPI(user,pw,link)

def get_products(api, footprint, date, platform='Sentinel-2', prd_type='S2MSI2A', 
                 cloudcover=(0,10), lim=1):
    
    """Entrées : api
                 footprint : recherche géographique des produits
                 date : tuple de (str ou datetime) ou str
                     formats : yyyyMMdd ; yyyy-MM-ddThh:mm:ssZ ; NOW-/+<n>DAY(S)
                 platform : Plateforme satellite souhaitée, défaut = Sentinel-2
                 prd_type : Type de produits
                 cloudcover : Pourcentage de couverture nuageuse, peut être un tuple de int 
                    désignant un intervalle ou un int
                 lim : Nombre limite de produits chargés, défaut = None
       Sortie : Pandas Dataframe contenant les informations des produits de la requête"""
    
    products = api.query(footprint, date, platformname = platform, limit = lim,
                         cloudcoverpercentage = cloudcover, producttype = prd_type)
    return(api.to_dataframe(products))

def dl_products(api, df_prod,option='n'):
    l = len(df_prod)
    if option == 'i':
        a = input('There is/are '+ str(l) +' file.s to download, you wish to do it? (y/n)')
        if a == 'y' :
            for i in range(l):
                api.download(df_prod.index[i])
        else :
            print('No dowload started')
    elif option == 'y':
        for i in range(l):
                api.download(df_prod.index[i])
    elif option == 'n':
        print('No dowload started')

