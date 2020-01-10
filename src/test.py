import pandas as pd 
import geopandas as gpd 
import folium
import numpy as np 
import glob
import matplotlib.pyplot as plt
import matplotlib.dates as md
import os
import shapefile as shp 
import seaborn as sns
import dateutil


#reads file in and calls the cleanit() function 
#returns dictionary with coordinates as keys and an array of measured values as values

def readit():
    path = r'/Users/ramozo_88/Capstone1/data'
    all_files = glob.glob(os.path.join(path, "*.csv"))
    measured_DNI_dict = {}
    clearsky_DNI_dict = {}
    difference_DNI_dict = {}

    for filename in all_files:
        df = pd.read_csv(filename)
        lat, lng, difference_DNI, measured_DNI, clearsky_DNI = cleanit(df)
        measured_DNI_dict.update({(float(lat),float(lng)):measured_DNI.values})
        clearsky_DNI_dict.update({(float(lat),float(lng)):clearsky_DNI.values})
        difference_DNI_dict.update({(float(lat),float(lng)):difference_DNI.values})
    
    return measured_DNI_dict, clearsky_DNI_dict, difference_DNI_dict     

#strips files that have been read in as pandas dataframes
#for information used to plot graphs

def cleanit(df):

    new_df1 = df[['Latitude','Longitude','Time Zone','Elevation','Local Time Zone','Clearsky DHI Units']]
    lat = new_df1['Latitude'][0]
    lng = new_df1['Longitude'][0]
    new_df1 = new_df1.drop([0])
    new_df1.columns = new_df1.iloc[0]
    new_df1 = new_df1.drop([1])
    new_df1 = new_df1.drop(['DHI','Clearsky DHI'], axis=1)
    clearsky_DNI = new_df1['Clearsky DNI'].astype(int)
    measured_DNI = new_df1['DNI'].astype(int)
    difference_DNI = clearsky_DNI - measured_DNI
    return lng, lat, difference_DNI, measured_DNI, clearsky_DNI

#calculate and returns averages of measured values for each coordinate in dictionary and sorts

def get_avgs(dct):
    avg = []
    for key in dct:
        avg.append([key,dct[key].sum()/len(dct)])
    
    avg = sorted(avg, key = lambda x:x[1],reverse=True)
    
    return avg

#returns top 40 averages

def get_top_avgs(dct):
    return get_avgs(dct)[:40]

#calculate and returns least difference averages between measured and clearsky values in dictionary

def get_least_diff_avgs(dict):
    avg = []
    for key in dct:
        avg.append([key,dct[key].sum()/len(dct)])
    
    avg = sorted(avg, key = lambda x:x[1])
    
    return avg

#returns the 40 that have the least difference between measured and clearsky values

def get_bottom_avgs(dct):
    return get_least_diff_avgs(dct)[:40]

#returns coordinates in list

def get_top_coords(lst):
    return [coord[0] for coord in lst]

def geoplot_all_points():
    denver_map1 = folium.Map(location=[39.75,-104.999338],
                        zoom_start=10,
                        tiles="Cartodbpositron")

    for point in measured_DNI_dict.keys():
        folium.Circle(location=[point[0], point[1]], radius=1200, color='yellow', fill_color='yellow').add_to(denver_map1)

def geoplot_top_producers(lst):
    denver_map2 = folium.Map(location=[39.75,-104.999338],
                        zoom_start=10,
                        tiles="Cartodbpositron")

    for point in lst:
        folium.Circle(location=[point[0], point[1]], radius=1200, color='orange', fill_color='orange').add_to(denver_map2)

def geoplot_least_diff_toclearsky(lst):
    denver_map3 = folium.Map(location=[39.75,-104.999338],
                        zoom_start=10,
                        tiles="Cartodbpositron")

    for point in lst:
        folium.Circle(location=[point[0], point[1]], radius=1200, color='purple', fill_color='purple').add_to(denver_map3)



def color_eval():
    pass


if __name__ == "__main__":
    
    measured_DNI_dict, clearsky_DNI_dict, difference_DNI_dict  = readit()
    top_producers = geoplot_top_producers(get_top_coords(get_top_avgs(measured_DNI_dict)))
    least_differentials = geoplot_least_diff_toclearsky(get_top_coords(get_bottom_avgs(difference_DNI_dict)))

