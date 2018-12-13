import sys, getopt
import numpy as np
import pandas as pd
import argparse
from datetime import datetime
from pomegranate import * 


class StockInterface(object):
   def __init__(self):
      self.records = {}
   
   def read_stocks(self, stockcodes, date_range=None):
      # date_range = ("2012-10-20", "2012-10-24")
      if(date_range):
         try:
            start, end = date_range
            print('Date range : ({}, {})'.format(start, end))
            start = datetime.strptime(start, "%Y-%m-%d")
            end = datetime.strptime(end, "%Y-%m-%d")
         
         except TypeError:
            raise TypeError("The format of date_range should be (%Y-%m-%d, %Y-%m-%d")
         
         if start < datetime(2005, 2, 25) or start > datetime(2017, 11, 10) or end < datetime(2005, 2, 25) or end > datetime(2017, 11, 10) or start > end:
            raise ValueError("Date range must fall between 2005-02-25 and 2017-11-10")

      for sc in stockcodes:
         data = pd.read_csv(sc+".us.txt", sep=",", header=0, usecols=["Date", "Close"])
         
         if(date_range):
            data['Date'] = pd.to_datetime(data['Date'])
            data = data[(data["Date"] >= start) & (data["Date"] <= end)]
         
         self.records[sc] = data
         #print(data)
   
   def list_stocks(self):
      print('########################################')
      print('#         Printing all records         #')
      print('########################################\n')
      for k, v in self.records.items():
         print('------------------------------')
         print(f'-     STOCK CODE: {k}       -')
         print('------------------------------\n')
         print(v)
   
   def get_stock(self, stockcode, date=False):
      try:
         stock = self.records[stockcode]
      except KeyError as e:
         print( "KeyError: stock code '{}' does not exist".format(e))

      return np.asarray([stock['Close'].tolist()])

   @property
   def all_stocks(self):
      return self.records
      
   def output_stocks(self, outputfile):
      pass

if __name__ == "__main__":
   pass
   

