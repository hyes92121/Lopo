from weather_util import WeatherManager
from sklearn.cluster import KMeans
import numpy as np
from sys import argv
from hmmlearn import hmm

def dft_series(series, coeffnum):
    for idx, c in enumerate(series):
        c = np.fft.fft(c)[:coeffnum]
        c = [coeff.real for coeff in c] + [coeff.imag for coeff in c]
        series[idx] = np.array(c)
    return series

def hmm_series(series):
    model = hmm.GMMHMM(n_components=1, covariance_type="full", n_iter=100)
    print(series[0])
    model.fit([series[0]])
    print(model)
    

def main():
    datadir = argv[1]
    wm = WeatherManager(datadir)
    wm.loadSeries(cities= 
                  ["Philadelphia",
                   "New York",
                   "Montreal",
                   "Boston",
                   "Beersheba",
                   "Tel Aviv District",
                   "Eilat",
                   "Haifa",
                   "Nahariyya",
                   "Jerusalem"],
                    attr="temperature") # date_range=("2017-10-12","2017-11-06"))
    wm.interpolate()
    series = wm.getSeries()
    print(np.argwhere(np.isnan(np.array(series))))

    kmeans = KMeans(n_clusters=2, random_state=0).fit(np.array(series))
    print("Euclidean label", kmeans.labels_)
    
    DFTseries = dft_series(series, 50)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(np.array(DFTseries))
    print("DFT label", kmeans.labels_)

    hmm_series(series)
     

if __name__ == "__main__":
    main()
