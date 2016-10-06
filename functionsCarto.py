from cartodb import CartoDBOAuth as CartoDB, CartoDBException, CartoDBAPIKey, FileImport, URLImport
   
def uploadFile(API_KEY, cartodb_user, url, isURL=False):
    cl = CartoDBAPIKey(API_KEY, cartodb_user)
    
    if isURL == False:
    # Import csv file, set privacy as 'link' and create a default viz
        fi = FileImport(url, cl, create_vis='true', privacy='public', content_guessing=True)
        fi.run()    
    else:
        fi = URLImport(url, cl)
        fi.run()
    
    #interval update
    
    #fi = URLImport(MY_URL, cl, interval=3600)
    #fi.run()
    
    #########################################################################################################
    
    #print cl.sql("insert into test (the_geom,foo,bar) values (CDB_LatLng(40.7127,-74.0059),'testing',123)")

