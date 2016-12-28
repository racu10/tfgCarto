
# coding: utf-8

# In[1]:

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


# In[2]:

def getDistance(long1, lat1, long2, lat2):
    """    getDistance(long1, lat1, long2, lat2)

    Get distance betwen 2 coordinates in log/lat.
    
    Parameters
    ----------
    long1 : float
        Longitude 1st coordinate.
    lat1 : float
            Latitude 1st coordinate.
    long2 : float
            Longitude 2nd coordinate.  
    lat2 : float
            Latitude 2nd coordinate.
    Returns
    -------
    float
    Get the value of the distance.
    """
    
    
    r = 6371000 #radio terrestre medio, en metros 
    c = math.pi/180 #constante para transformar grados en radianes
 
    return 2*r*math.asin(math.sqrt(math.sin(c*(lat2-lat1)/2)**2 + math.cos(c*lat1)*math.cos(c*lat2)*math.sin(c*(long2-long1)/2)**2))


# In[3]:

def getDistanceInKm(long1, lat1, long2, lat2):
    """    getDistanceInKm(long1, lat1, long2, lat2)

    Get distance betwen 2 coordinates in log/lat.
    
    Parameters
    ----------
    long1 : float
        Longitude 1st coordinate.
    lat1 : float
            Latitude 1st coordinate.
    long2 : float
            Longitude 2nd coordinate.  
    lat2 : float
            Latitude 2nd coordinate.
    Returns
    -------
    float
    Get the value of the distance.
    """
    
    pt1 = geopy.Point(long1, lat1)
    pt2 = geopy.Point(long2, lat2)
    
    return geopy.distance.distance(pt1, pt2).km
 


# In[4]:

def utmToLatLng(zone, easting, northing, northernHemisphere=True):

    """    utmToLatLng(zone, easting, northing, northernHemisphere=True)

    Tranform UTM location to Lat / Long
    
    Parameters
    ----------
    zone : int
        Value of the zone where are coordinates getted. 
    easting : float
            Falue from easting (X).
    northing : float
            Falue from northing (Y).
    northernHemisphere : bool
            Latitude 2nd coordinate.
    
    Returns
    -------
    tupple (latitude, longitude)
    Get the value of UTM into lat and long.
    
    More info
    ---------
    See http://www.dmap.co.uk/utmworld.htm to locate your zone and the hemisphere.
    
    """
    
    if not northernHemisphere:
        northing = 10000000 - northing

    a = 6378137
    e = 0.081819191
    e1sq = 0.006739497
    k0 = 0.9996

    arc = northing / k0
    mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))

    ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / (1 + math.pow((1 - e * e), (1 / 2.0)))

    ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0

    cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
    cc = 151 * math.pow(ei, 3) / 96
    cd = 1097 * math.pow(ei, 4) / 512
    phi1 = mu + ca * math.sin(2 * mu) + cb * math.sin(4 * mu) + cc * math.sin(6 * mu) + cd * math.sin(8 * mu)

    n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))

    r0 = a * (1 - e * e) / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
    fact1 = n0 * math.tan(phi1) / r0

    _a1 = 500000 - easting
    dd0 = _a1 / (n0 * k0)
    fact2 = dd0 * dd0 / 2

    t0 = math.pow(math.tan(phi1), 2)
    Q0 = e1sq * math.pow(math.cos(phi1), 2)
    fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * math.pow(dd0, 4) / 24

    fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720

    lof1 = _a1 / (n0 * k0)
    lof2 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
    lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 * e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
    _a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
    _a3 = _a2 * 180 / math.pi

    latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi

    if not northernHemisphere:
        latitude = -latitude

    longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - _a3

    return (latitude, longitude)


# In[5]:

def getDataOfCsv(name, sep=';'):
    import pandas as pd
    """    getDataOfCsv(name):

    Load data of csv to pandas.
    
    Parameters
    ----------
    name : String
        Path + file.csv to load.
    sep : String
        Separator of the csv.
    
    Returns
    -------
    Pandas array
    Get the structure of the CSV.
    """
    allData = None
    try:
        allData = pd.read_csv(name, encoding = "utf8", sep=sep)
    except:
        allData = pd.read_csv(name, encoding = "ISO-8859-1", sep=sep)
    return allData


# In[6]:

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


# In[7]:

def getPointOfStreet(streetName, boundingBoxSearch): 
    """    getPointOfStreet(streetName, boundingBoxSearch)

    Get distance betwen 2 coordinates in log/lat.
    
    Parameters
    ----------
    streetName : float
        Name of the street you are looking the points.
    boundingBoxSearch : tuple 
            Bounding box coordinates to limit the map.
    
    Returns
    -------
    OSM structure
    Get all points of the street with the OSM structure with all parameters.
    """
    apiOverPass = overpass.API()
    sql = 'way[name~"'+streetName+'"]'+str(boundingBoxSearch).encode("utf-8")+';'
    
    return apiOverPass.Get(sql)


# In[8]:

def getPointOfStreetPolygon(streetName, polygon): 
    """    getPointOfStreet(streetName, boundingBoxSearch)

    Get distance betwen 2 coordinates in log/lat.
    
    Parameters
    ----------
    streetName : float
        Name of the street you are looking the points.
    boundingBoxSearch : tuple 
            Bounding box coordinates to limit the map.
    
    Returns
    -------
    OSM structure
    Get all points of the street with the OSM structure with all parameters.
    """
    s = polygonArrayToOSMstructure(polygon)
    apiOverPass = overpass.API()
    sql = 'way[name~"'+streetName+'"]'+s+';'
    
    return apiOverPass.Get(sql)


# In[9]:

def getAllStreetPointsLookingForName(allStreetInfoOSM, streetName):
    lstPoints = []
    for street in allStreetInfoOSM:
        if street['type'].strip().lower() == 'linestring':
            if streetName.strip().lower() in street['properties'][u'name'].strip().lower():
                if len(street['geometry']) > 0:
                    for point in street['geometry']:
                        if point not in lstPoints:
                            lstPoints.append(point)   
    return lstPoints


# In[10]:

def fromAllStreetsGetWithStreetNameTheLocationMostNear(allStreetInfoOSM, streetName, xtest, ytest):
    lstPoints = getAllStreetPointsLookingForName(allStreetInfoOSM, streetName)
    
    return fromPointsOfStretGetBestUbicationXY(lstPoints, xtest, ytest)


# In[11]:

def fromPointsOfStretGetBestUbicationXY(pointsOfStreet, xtest, ytest):
    """    fromPointsOfStretGetBestUbicationMinXY(pointsOfStreet, xtest, ytest):

    Localize the point more close to the street given with his points using OSM features.
    
    Parameters
    ----------
    pointsOfStreet : List
           List of points
    xtest : float 
            Actual x coordinate to be remplaced.
    ytest : tuple 
            Actual y coordinate to be remplaced.
            
    Returns
    -------
    tuple x, y
    Get the best location into the street given.
    """
    cx = xtest
    cy = ytest
    minD = float('inf')
    for c in pointsOfStreet:
        y = c[1]
        x = c[0]
        d = getDistance(xtest, ytest, x, y)
        if d < minD:  
            cx = x
            cy = y 
            minD = d
    return cx,cy


# In[12]:

def fromPointsOfStretGetBestUbicationMinXYOSMStructure(pointsOfStreet, xtest, ytest):
    """    fromPointsOfStretGetBestUbicationMinXY(pointsOfStreet, xtest, ytest):

    Localize the point more close to the street given with his points using OSM features.
    
    Parameters
    ----------
    pointsOfStreet : float
        OSM structure with linestring.
    xtest : float 
            Actual x coordinate to be remplaced.
    ytest : tuple 
            Actual y coordinate to be remplaced.
            
    Returns
    -------
    tuple x, y
    Get the best location into the street given.
    """
    
    
    allCorrd = pointsOfStreet['features']
    minD = float('inf')
    cx = xtest
    cy = ytest
    for geo in allCorrd:
        geometry = geo["geometry"]

        if geometry["type"].upper() == "LINESTRING":
            for c in geometry["coordinates"]:
                y = c[0]
                x = c[1]
                #txtHtml = "Coord: "+ str(c) 
                #print(x, ' - ', y)
                #poppin = folium.Popup(html=folium.element.IFrame(html=txtHtml,width=200,height=50))
                #folium.Marker([x,y], icon=folium.Icon(icon='glyphicon-plus', color='pink'),popup = poppin).add_to(markerCluster)
                d = getDistance(xtest, ytest, x, y)
                #print(d, ' --- ', str(c))
                if d < minD:  
                    #print(d, ' --- ', str(c))
                    cx = x
                    cy = y 
                    minD = d
    return cx,cy


# In[13]:

def pandasReadJson(url):
    """    pandasReadJson(url):

    Tranform JSON into pandas Object
    
    Parameters
    ----------
    url : String
        Url of the Json.
            
    Returns
    -------
    pandas structure
    Get all data from JSON URL.
    """
    
    import pandas as pd
    return pd.read_json(url)


# In[14]:

def getNowBikesInBcn():
    """    getNowBikesInBcn():

    From api citybike get json of actual moment of the bikes in barcelona
    
    Parameters
    ----------
            
    Returns
    -------
    pandas structure
    Get all data of citybike barcelona.
    """

    apiBikes = 'http://api.citybik.es/bicing.json'
    df = pandasReadJson(apiBikes)
    return df


# In[15]:

def decodeToUTF8(text):
    try:
        text = unicode(text, 'utf-8')        
    except:
        return text
    return text


# In[16]:

def getAllBarrisBCNPoligonBox(path = 'alldata/barris.geojson', columnName='neighbourhood', orderedXY = False):
    """    getAllBarrisBCNPoligonBox(path)

    From geojson of barris set to dicctionary with his poligon
    
    Parameters
    ----------
    path : String
    Path of the file
    columnName : String
    Name of the column that contains the String info inside properties.
            
    Returns
    -------
    Dictonary
    Dictinary with key is "barri" and data is the poligon.
    """
    dicBarris = dict()
    df = pandasReadJson(path)
    for d in df.iterrows():
        allData = d[1][0]        
        r = dict(allData)
        l = r['properties']
        name = l[columnName].lower()
        #name = name.decode('utf8')
        s = r['geometry']
        coord = []
        if orderedXY == False:
            coord = s['coordinates'][0][0]
        else:
            coord = transformArrYXToXYList(s['coordinates'][0][0])
        dicBarris[name] = coord
    return dicBarris
            


# In[17]:

def polygonArrayToOSMstructure(polygon):
    """    polygonArrayToOSMstructure(polygon)

    With a polygon array gets structure of poly for OSM sql.
    
    Parameters
    ----------
    polygon : Array
    Array that contains the poligon separated [[lat,long], [lat', long'], [lat'', long''], ...] same as [[y,x],[y',x'], [y'',x''], ...] 
    representation of OSM return.
            
    Returns
    -------
    String
    Returns the string asociated for OSM sqls (poly: ...).
    """
    s = '(poly:"'
    for y, x in polygon[:-1]:
        s += str(x)+ ' '+ str(y)+' '
    s += str(polygon[-1][1])+' '+str(polygon[-1][0]) +'")'
    return s


# In[18]:

def getAllNodesIntoPolygon(polygon, timeOut = 30):
    """    getAllNodesIntoPolygon(polygon)

    With a polygon array gets all nodes inside them.
    
    Parameters
    ----------
    polygon : Array
    Array that contains the poligon separated [[lat,long], [lat', long'], [lat'', long''], ...] same as [[y,x],[y',x'], [y'',x''], ...] 
    representation of OSM return.
            
    Returns
    -------
    Dictonary
    Dictinary with key is "barri" and data is the poligon.
    """

    s = polygonArrayToOSMstructure(polygon)
    sql = """node"""+ s + """;out;"""
    allData = []
    try:
        allData = apiOverPass.Get(sql)
    except:
        allData = getAllNodesIntoPolygonErrorTimeOut(sql, timeOut)
    return allData


# In[19]:

def getAllNodesIntoBoundingBox(boundingBoxSearch, timeOut = 30):
    """    getAllNodesIntoPolygon(polygon)

    With a polygon array gets all nodes inside them.
    
    Parameters
    ----------
    polygon : Array
    Array that contains the poligon separated [[lat,long], [lat', long'], [lat'', long''], ...] same as [[y,x],[y',x'], [y'',x''], ...] 
    representation of OSM return.
            
    Returns
    -------
    Dictonary
    Dictinary with key is "barri" and data is the poligon.
    """

    sql = """node"""+ str(boundingBoxSearch).encode("utf-8") + """;out;"""
    allData = []
    try:
        allData = apiOverPass.Get(sql)
    except:
        allData = getAllNodesIntoPolygonErrorTimeOut(sql, timeOut)
    return allData


# In[20]:

def getAllNodesIntoPolygonErrorTimeOut(sql, wait):
    allData = []
    if wait == 0:
        return allData
    time.sleep(wait)
    
    try:
        allData = apiOverPass.Get(sql)
    except:
        allData = []
        print "Time Out"
    return allData


# In[21]:

def getAmenityInfoIntoPolygon(polygon, amenityType='pub', timeOutWaitExcept = 30):
    #http://wiki.openstreetmap.org/wiki/Key:amenity
    
    s = polygonArrayToOSMstructure(polygon)
    sql = "(node[amenity='" + amenityType + "']"+ s +";);out center;"
    allData = []
    try:
        allData = apiOverPass.Get(sql)
    except:
        allData = getAllNodesIntoPolygonErrorTimeOut(sql, timeOutWaitExcept)
    return allData


# In[22]:

def getAmenityInfoIntoBoundingBox(boundingBoxSearch, amenityType='pub', timeOutWaitExcept = 30):
    #http://wiki.openstreetmap.org/wiki/Key:amenity
    sql = "(node[amenity='" + amenityType + "']"+ str(boundingBoxSearch).encode("utf-8") +";);out center;"
    allData = []
    try:
        allData = apiOverPass.Get(sql)
    except:
        allData = getAllNodesIntoPolygonErrorTimeOut(sql, timeOutWaitExcept)
    return allData


# In[23]:

def getNodeInfo(idNode):
    osm = OsmApi()
    T = osm.NodeGet(idNode)
    return T


# In[24]:

def getInfoOfOSMSearch(feature):
    feat = feature["features"]
    lst = []
    if len(feat) > 0:
        for geo in feat:
            T = dict()
            r = geo["geometry"]
            if r["type"].lower() == "point".lower():
                T["geometry"] = tuple([r["coordinates"][1],r["coordinates"][0]])
            else:
                allCoord = []
                for c in r["coordinates"]:
                    allCoord.append(tuple([c[1],c[0]]))
                    T["geometry"] = allCoord
            
            T["type"] = r["type"]
            T["properties"] = geo["properties"]
            lst.append(T)
    return lst
        
        
    


# In[25]:

def coordInsidePolygon(x, y, polygon):
    """    coordInsidePolygon(x, y, polygon)

    With a polygon array try if coord is inside.
    
    Parameters
    ----------
    polygon : Array
    Array that contains the poligon separated [[lat,long], [lat', long'], [lat'', long''], ...] same as [[y,x],[y',x'], [y'',x''], ...] 
    representation of OSM return.
    x : float
    Coord x
    y : float
    Coord y
    
    Returns
    -------
    Bool
    Returns true/false depending if it's inside or not.
    """
    n = len(polygon)
    inside = False    
    if n > 0:
        p1y, p1x = polygon[0]
        for i in range(1, n + 1):
            p2y, p2x = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
    return inside


# In[26]:

def getPerimeterOfDictWithPolygons(dictionary):
    arrPoly = []
    for d in dictionary:
        poly = dictionary[d]
        for x in poly:
            if x not in arrPoly:
                arrPoly.append(x)
    
    tmpArr = []
    cont = 0
    
    
    for x in arrPoly:        
        if coordInsidePolygon(x[0], x[1], tmpArr) == False:
            tmpArr.append(x)
            T = tmpArr[:]
            cont = 0
            for t in tmpArr:
                tmpArr.pop(cont)
                if coordInsidePolygon(t[0], t[1], T) == False:
                    tmpArr.append(t)
                cont += 1
                    
        
    
    print len(arrPoly)
    print len(tmpArr)
    return tmpArr


# In[ ]:




# In[27]:

def transformArrYXToXY(arrYX):
    points = []
    for point in arrYX:
        points.append(tuple([point[1], point[0]]))
    return points

def transformArrYXToXYList(arrYX):
    points = []
    for point in arrYX:
        points.append([point[1], point[0]])
    return points



# In[28]:

def removeIntInxString(txt, sep = '.'):
    s = txt.split(sep)
    rettxt = ''
    if len(s) > 1:
        for t in s[1: len(s) -1]:
            rettxt = rettxt + t.strip() + sep
        rettxt = rettxt + s[-1].strip()
        return rettxt
    else:
        return txt.strip()


# In[29]:

def mapCreation(centerX, centerY):
    map = folium.Map(location=[centerX,centerY])
    return map


# In[30]:

def mapAddMarker(map, coordX, coordY, icn = 'glyphicon-certificate', color = 'blue', popuName = ''):
    folium.Marker([coordX, coordY], popup=popuName,
                   icon = folium.Icon(icon=icn,color = color)).add_to(map)


# In[31]:

def mapAddLine(map, arrPoints, lineColor="#000000",weight=2.5, opacity=1):
    folium.PolyLine(arrPoints, color=lineColor, weight=weight, opacity=opacity).add_to(map)


# In[32]:

def mapWithMarkerCluster(map, name):
    markerCluster = folium.MarkerCluster(name).add_to(map)
    return markerCluster

def mapAddMarkerToCluster(cluster, coordX, coordY, icn = 'glyphicon-certificate', iconcolor = '#0000FF', txtOfPoppup = "", sizeX = 200, sizeY = 50):
    poppin = folium.Popup(html=folium.element.IFrame(html=txtOfPoppup,width=sizeX,height=sizeY))
    folium.Marker([coordX,coordY], icon=folium.Icon(icon=icn, color=iconcolor),popup = poppin).add_to(cluster)


# In[33]:

def mapAddRegularPolygonMarker(map, points, color = '#0000FF', txtOfPoppup = "", sizeX = 200, sizeY = 50):
    poppin = folium.Popup(html=folium.element.IFrame(html=txtOfPoppup,width=sizeX,height=sizeY))
    folium.RegularPolygonMarker(points, weight=2.5, opacity=1, fill_color=color, fill_opacity=1, popup=poppin).add_to(map)


# In[34]:

def saveMap(map, saveFileName = 'map.html'):
    map.save(saveFileName)


# In[35]:

#POLYGON
#POINTS x, y o UTMX UTMY or Ids
#All data or limited Data
#Load From CSV, GEOJSON, Amenity OSM, bikesBCN, Nodes OSM,  


#getDataOfCsv(name, sep=';')
#getNowBikesInBcn()
#getAllBarrisBCNPoligonBox(path = 'alldata/barris.geojson', columnName='neighbourhood')
#pandasReadJson(url)
#getAmenityInfoIntoPolygon(polygon, amenityType='pub', timeOutWaitExcept = 30)
#getAmenityInfoIntoBoundingBox(boundingBoxSearch, amenityType='pub', timeOutWaitExcept = 30)



def transformPandasToStructureInfo(pd, 
                                   type = 'point', 
                                   colPolygonOrX = 0, 
                                   colY = 0, 
                                   ifIsPolygonIsXY = True, 
                                   isUTM = False, 
                                   zoneUTM = 31):
    lst = []    
    for d in pd[:].iterrows():
        if d[1][1] != -1:           
            T = dict()
            tmp = dict()
            tmp = d[1]
            T["type"] = type
            
            if type.strip().lower() == 'point':
                x = tmp[colPolygonOrX]
                y = tmp[colY]
                if is_number(tmp[colPolygonOrX]) == False:                   
                    x = float(tmp[colPolygonOrX].replace(',', '.'))
                if is_number(tmp[colY]) == False:                                   
                    y = float(tmp[colY].replace(',', '.'))
                if isUTM == True:              
                    x = float(x)
                    y = float(y)
                    x, y = utmToLatLng(zoneUTM, x, y)                      
                T["geometry"] = tuple([x,y])
                
            else:
                polyOrX = tmp[colPolygonOrX]
                if ifIsPolygonIsXY == False:
                    polyOrX = transformArrYXToXY(polyOrX) 
                T["geometry"] = polyOrX
            T["properties"] = tmp
            lst.append(T)

    return lst

    
def getDatabase(name, 
                extension, 
                path = "" , 
                sep = "", 
                isPolygon = False, 
                colPolygonOrLong = 0, 
                colLat = 1, columnName = '', 
                ifIsPolygonIsXY = True, 
                isUTM = False, 
                zoneUTM = 31):
    allData = []
    name = name.strip().lower()
    if extension.strip().lower() == 'csv':
        allData = getDataOfCsv(path.strip().lower(), sep)
        if isPolygon == False:
            return [name, transformPandasToStructureInfo(allData, 'point', colPolygonOrLong, colLat, ifIsPolygonIsXY, isUTM,zoneUTM)]
        else:
            return [name, transformPandasToStructureInfo(allData, 'polygon', colPolygonOrLong, colLat, ifIsPolygonIsXY, isUTM,zoneUTM)]
    elif extension.strip().lower() == 'json':
        allData = pandasReadJson(path)
        if isPolygon == False:
            return [name, transformPandasToStructureInfo(allData, 'point', colPolygonOrLong, colLat, ifIsPolygonIsXY, isUTM,zoneUTM)]
        else:
            return [name, transformPandasToStructureInfo(allData, 'polygon', colPolygonOrLong, colLat, ifIsPolygonIsXY, isUTM,zoneUTM)]           
    elif extension.strip().lower() == 'geojson':
        return [name, getAllBarrisBCNPoligonBox(path, columnName, True)]
    elif extension.strip().lower() == 'bcnbikes':        
        return [name, transformPandasToStructureInfo(getNowBikesInBcn(), 'point', 'lng', 'lat', True, True, 31)]
    elif extension.strip().lower() == 'df' or  extension.strip().lower() == 'pandas':
        if isPolygon == False:
            return [name, transformPandasToStructureInfo(path, 'point', colPolygonOrLong, colLat, ifIsPolygonIsXY, isUTM,zoneUTM)]
        else:
            return [name, transformPandasToStructureInfo(path, 'polygon', colPolygonOrLong, colLat, ifIsPolygonIsXY, isUTM,zoneUTM)]

    return allData



# In[36]:

def getDatabaseFromOSM(name, 
                       type = 'amenity|node|way', 
                       searchByPolygon = True, 
                       ifIsPolygonIsXY = True, 
                       boundingBoxOrPolygon = [], 
                       keyWord = '', 
                       timeOutWait = 30):
    
    if searchByPolygon == True and ifIsPolygonIsXY == True:
        boundingBoxOrPolygon = transformArrYXToXYList(boundingBoxOrPolygon)
    
    allData = []
    name = name.strip().lower()
    if type.strip().lower() == 'amenity':
        if searchByPolygon == True:
            return getInfoOfOSMSearch(getAmenityInfoIntoPolygon(boundingBoxOrPolygon, keyWord, timeOutWait))
        else:
            return getInfoOfOSMSearch(getAmenityInfoIntoBoundingBox(boundingBoxOrPolygon, keyWord, timeOutWait))
    elif type.strip().lower() == 'node':
        if searchByPolygon == True:
            return getInfoOfOSMSearch(getAllNodesIntoPolygon(boundingBoxOrPolygon, timeOutWait))
        else:
            return getInfoOfOSMSearch(getAllNodesIntoBoundingBox(boundingBoxOrPolygon, timeOutWait))
    elif type.strip().lower() == 'way':
        if searchByPolygon == True:
            return getInfoOfOSMSearch(getPointOfStreetPolygon(keyWord, boundingBoxOrPolygon))
        else:
            return getInfoOfOSMSearch(getPointOfStreet(keyWord, boundingBoxOrPolygon))
            


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



