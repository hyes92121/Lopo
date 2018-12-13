import sys, getopt
import numpy as np
from pomegranate import *
from stockinterface import StockInterface

# usage: python3 read_stocks.py -c <stockCodes> -o <outputfile>
# <stockCodes> should be seperated by ','
# e.g. python3 read_stocks.py -c algt,ande,amzn -o cool.csv

# stock sections: https://money.usnews.com/investing/stocks/rankings


class HMM(object):
   def __init__(self, records):
      self.records = records

   def model(self):
      pass

   def get_outlier(self, target):
      prob = dict()
      x = self.to_arr(target)
      model = HiddenMarkovModel.from_samples(NormalDistribution, n_components=10, X=x)
      for k in self.records.keys():
         prob[k] = model.log_probability(self.to_arr(k))
      
      return min(prob, key=prob.get)
   
   def to_arr(self, stockcode):
      return np.asarray([self.records[stockcode]['Close'].tolist()])

def parse(argv):
      stockcodes = list()
      outputfile = ''

      try:
         opts, args = getopt.getopt(argv,"hoc:d:t:", ["ifile=", "ofile=", "daterange=","target="])
      except getopt.GetoptError:
         print('hmm.py -c <stockCodes> -o <outputfile>')
         sys.exit(2)
      for opt, arg in opts:
         if opt == '-h':
            print('hmm.py -c <stockCodes> -o <outputfile>')
            sys.exit()
         elif opt in ("-c", "--ifile"):
            sc = arg.split(",")
            for code in sc:
               stockcodes.append(code)
         
         elif opt in ("-d", "--daterange"):
            dr = arg.split(",")
            date_range = (dr[0], dr[1])

         elif opt in ("-t", "--target"):
            target = arg

         elif opt in ("-o", "--ofile"):
            outputfile = arg + ".csv"

      return stockcodes, date_range, target, outputfile

if __name__ == '__main__':   
   stockcodes, date_range, target, outputfile = parse(sys.argv[1:])

   print('Stock codes:', stockcodes)
   #print ('Output file is ', outputfile)
   
   SI = StockInterface()
   SI.read_stocks(stockcodes, date_range)
   all_stocks = SI.all_stocks

   hmm = HMM(all_stocks)
   print('The outlier is :', hmm.get_outlier(target))
