
# coding: utf-8

# In[1]:

import functions as fun


# In[2]:

T = fun.getAllBarrisBCNPoligonBox()
print T


# In[3]:

poly = T['les corts'.lower()]
n = fun.getAmenityInfoIntoPolygon(poly, "drinking_water")
print n["features"]


# In[4]:

print poly


# In[5]:

startLoc = [41.388790,2.158990]


# In[6]:

map = fun.mapCreation(startLoc[0], startLoc[1])

for x in T:
    points = []
    for point in T[x]:
        points.append(tuple([point[1], point[0]]))
    #print(points)
    #print x, "\n-----------------------------------------------------------------------\n"
    fun.mapAddLine(map,points, "#0000FF", 2.5, 1)
map


# In[7]:

map = fun.mapCreation(startLoc[0], startLoc[1])

html="add <b>popup</b> here"
#iframe = folium.element.IFrame(html=html,width=100,height=100)
poppin = "add <b>popup</b> here"
#poppin = folium.Popup(html="add <b>popup</b> here")

for x in T:
    points = []
    for point in T[x]:
        points.append(tuple([point[1], point[0]]))
    fun.mapAddRegularPolygonMarker(map, points, '#0000FF', poppin, sizeX = 200, sizeY = 50)
map


# In[8]:

#m = folium.Map(location=[28, -81], zoom_start=6)
#"""
#m.add_children(folium.WmsTileLayer(name="SST",
#                url="http://nowcoast.noaa.gov/wms/com.esri.wms.Esrimap/analyses",
#                format="image/png",
#                layers='NCEP_RAS_ANAL_RTG_SST'))

#m.add_children(folium.WmsTileLayer(name="coastal_labels",
#                url="http://nowcoast.noaa.gov/wms/com.esri.wms.Esrimap/analyses",
#                format="image/png",
#                layers='coastal_labels'))
#
#m.add_children(folium.WmsTileLayer(name="RTMA_PT_WINDVECT_10",
#                url="http://nowcoast.noaa.gov/wms/com.esri.wms.Esrimap/analyses",
#                format="image/png",
#                layers='RTMA_PT_WINDVECT_10'))
#"""
#m.add_children(folium.WmsTileLayer(name="GMRT",
#                url="http://gmrt.marine-geo.org/cgi-bin/mapserv?map=/public/mgg/web/gmrt.marine-geo.org/htdocs/services/map/wms_merc.map",
#                format="image/png",
#                layers='topo'))
#m


# In[9]:

csvData = fun.getDataOfCsv('alldata/sexebarris/opendata_2015_ine-ine01.csv')
for index, row in csvData.iterrows():
    csvData.set_value(index, 'Barris', fun.removeIntInxString(csvData.get_value(index, 'Barris'), '.').lower())
#csvData


# In[ ]:




# In[10]:

pt1 = (48.853, 2.349)
pt2 = (52.516, 13.378)

dist = fun.getDistanceInKm(pt1[0],pt1[1], pt2[0], pt2[1])
print dist
points = []
points.append([pt1, ["asd", "bfc"]])
points.append([pt2, ["asd2", "sldkhjj"]])

[pt for pt in points if fun.getDistanceInKm(pt1[0], pt1[1], pt[0][0], pt[0][1]) > -1.]


# In[11]:

#accidents = fun.getDatabase('ACCIDENTS_GU_BCN_2015', 'cSV', 'ACCIDENTS_GU_BCN_2015.csv' , ';', False, -1,-2, '', True, True, 31)


# In[12]:

#print accidents[:50]


# In[13]:

print fun.getDatabase('BikesBCN', 'bcnbikes')


# In[14]:

barris = fun.getDatabase('Barris', 'geojson', 'alldata/barris.geojson' , '', False, -1,-1, 'neighbourhood')
print barris


# In[15]:

print fun.getDatabaseFromOSM("Restaurants","amenity", True, barris[1]['les corts'], 'restaurant')


# In[16]:

locationAreaBoundingBox = (41.3248770036,2.0520401001,41.4829908452,2.2813796997)
print fun.getDatabaseFromOSM("Restaurants","amenity", False, locationAreaBoundingBox, 'restaurant')


# In[17]:

#print fun.getPerimeterOfDictWithPolygons(barris[1])


# In[18]:

#locationAreaBoundingBox = (41.3248770036,2.0520401001,41.4829908452,2.2813796997)
#print fun.getDatabaseFromOSM("Restaurants","node", False, locationAreaBoundingBox, '')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[19]:

allData = fun.getDataOfCsv('alldata/sexebarris/opendata_2015_ine-ine01.csv')
allData
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

