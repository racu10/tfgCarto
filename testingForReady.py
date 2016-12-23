
# coding: utf-8

# In[2]:

#Useful functions @racu10

import pandas as pd
import numpy as np
import overpy
import overpass
import folium
from osmapi import OsmApi
import math
import geopy
import geopy.distance
import time
import unicodedata

MyApi = OsmApi()
apiOverPass = overpass.API()
apiOverPy =  overpy.Overpass()
import functions as fun


# In[4]:

T = fun.getAllBarrisBCNPoligonBox()


# In[6]:

csvData = fun.getDataOfCsv('alldata/sexebarris/opendata_2015_ine-ine01.csv')
for index, row in csvData.iterrows():
    csvData.set_value(index, 'Barris', fun.removeIntInxString(csvData.get_value(index, 'Barris'), '.').lower())


# In[7]:

allData = fun.getDataOfCsv('alldata/sexebarris/opendata_2015_ine-ine01.csv')
allData
state_data = []
for x in T:
    points = []
    for point in T[x]:
        points.append(tuple([point[1], point[0]]))
        state_data.append({x : 3.0})

startLoc = [41.388790,2.158990]
map = folium.Map(location=startLoc)
map.geo_json(geo_path='alldata/barris.geojson', 
             data=csvData,
             columns=['Barris', 'Homes'],
             key_on='feature.neighbourhood',
             fill_color='YlGn', 
             fill_opacity=0.7, 
             line_opacity=0.2,
             legend_name='Poblacio Homes')
map


# In[ ]:



