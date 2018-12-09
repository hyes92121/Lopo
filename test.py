import os 
import shutil
import numpy as np 
import matplotlib.pyplot as plt

import wfdb

record = wfdb.rdrecord('b003', smooth_frames=True, 
        sampfrom=300000, sampto=400000)
#wfdb.plot_wfdb(record=record, title='Testing Record')

signals = record.p_signal

print(signals)
print(signals.shape)
