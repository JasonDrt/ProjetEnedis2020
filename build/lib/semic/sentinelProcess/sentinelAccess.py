#pip install sentinelsat

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from semic.utils import URL_SENTINEL_API

def connect_api(user,pw,link=URL_SENTINEL_API):
    """Inputs : user : username of your SciHub account
                pw : your password
                link : link to sentinel API
       Output : Api connected"""
    return SentinelAPI(user,pw,link)

def get_products(api, footprint, date, platform='Sentinel-2', prd_type='S2MSI2A', 
                 cloudcover=(0,10), lim=1):
    """Inputs :  api : allows the connection to Sentinel API
                 footprint : Géographical serach of tiles
                 date : tuple of (str or datetime) or str
                     formats : yyyyMMdd ; yyyy-MM-ddThh:mm:ssZ ; NOW-/+<n>DAY(S)
                 platform : Plateform wanted, default = Sentinel-2
                 prd_type : Type of products
                 cloudcover : Percentage of cloud coverage, can be a tuple of int 
                    or a int
                 lim : Limit number of tiles returned by the query, default = None
       Output : Pandas Dataframe containing the query results"""
    
    products = api.query(footprint, date, platformname = platform, limit = lim,
                         cloudcoverpercentage = cloudcover, producttype = prd_type)
    return(api.to_dataframe(products))

def dl_products(api, df_prod,option='n'):
    """Inputs : api : allows the connection to Sentinel API
                df_prod : Pandas Dataframe containing a query results
                option : allows you to choose if you want ('y') or not ('n') to 
                   download a tile. You can choose 'i' so there is an interaction
                   to make your choice
    """
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

