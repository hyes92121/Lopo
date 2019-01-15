# show cities
# show weather attributes
# return a weather attribute time series of multiple cities, given a date range (default all)
import os
import pandas as pd
from sys import argv
from datetime import datetime
import numpy as np


class WeatherManager():
    def __init__(self,datadir):
        self.datasetdir = datadir

    def showCity(self):
        datasetdir = self.datasetdir
        cities = pd.read_csv(os.path.join(datasetdir,"city_attributes.csv"))
        print(cities)

    def showAttr(self):
        print("humidity\npressure\ntemperature\nwind_direction\nwind_speed\nhumidity")

    def loadSeries(self, cities=["Boston","Beersheba","Tel Aviv District","Eilat","Haifa","Nahariyya","Jerusalem"], attr="temperature", date_range=None):
        datasetdir = self.datasetdir
        if date_range is None:
            attr_df = pd.read_csv(os.path.join(datasetdir, attr + ".csv"))

        else:
            try:
                start, end = date_range
                # print(start,end)
                start = datetime.strptime(start, "%Y-%m-%d")
                end = datetime.strptime(end, "%Y-%m-%d")
            except T2ypeError:
                raise TypeError("The format of date_range should be (%Y-%m-%d, %Y-%m-%d")
            if start < datetime(2012,10,1) or start > datetime(2017,11,30) or end < datetime(2012,10,1) or end > datetime(2017,11,30) or start > end:
                raise ValueError("Each datetime must fall between 2012-10-1 and 2017-11-30")
                
            attr_df = pd.read_csv(os.path.join(datasetdir, attr + ".csv"))
            attr_df['datetime'] = pd.to_datetime(attr_df['datetime'])
            attr_df = attr_df[(attr_df["datetime"] >= start) & (attr_df["datetime"] <= end)]
            
        city_series = []
        for city in cities:
            city_series.append(attr_df[city].tolist())
        self.city_series = city_series

    
    def interpolate(self):
        city_series = self.city_series
        for idx, c in enumerate(city_series):
            c = np.array(c)
            nans, x = np.isnan(c), lambda z: z.nonzero()[0]
            c[nans] = np.interp(x(nans), x(~nans), c[~nans])
            city_series[idx] = c
        
        self.city_series = city_series

    def averaged(self, base=24):
        city_series = self.city_series
        for idx, c in enumerate(city_series):
            tmp = []
            for i in range(0, len(c), base):
                tmp.append(np.mean(c[i:i+base]))
            city_series[idx] = np.array(tmp)
        
        self.city_series = city_series 

    def getSeries(self):
        return self.city_series


