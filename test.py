import os 
import shutil
import numpy as np

import matplotlib.pyplot as plt
plt.figure(figsize=(20,20),dpi=100)

import wfdb

from saxpy.alphabet import cuts_for_asize
from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.sax import ts_to_string
from saxpy.sax import sax_via_window

from interface import PhysioInterface


def time_series_to_char(ts):
    ts = ts.flatten()
    ts = znorm(ts)

    return sax_via_window(
            series=ts, 
            win_size=300,
            paa_size=4, 
            alphabet_size=4,
            nr_strategy='none',
            z_threshold=0.1)


def time_series_to_char_1(ts):
    ts = ts.flatten()
    ts = znorm(ts)
    ts = paa(ts, 2000)
    
    rtn = sax_via_window(
            series=ts,
            win_size=100,
            paa_size=4,
            alphabet_size=4,
            nr_strategy='none',
            z_threshold=0.1
            )
    return rtn


def create_mapping():
    import itertools
    seq = (''.join(list(x)) for x in itertools.product('abcd', repeat=4))
    
    return {val:idx for idx, val in enumerate(seq)}



if __name__ == '__main__':
    # load ECG records
    PI = PhysioInterface()
    samp_start  = 300000
    samp_end    = 310000

    PI.load_record('b003', smooth_frames=True, sampfrom=samp_start, sampto=samp_end)
    signal = PI.get_signal('b003')

    # generate SAX representations for each time series
    seq_coll = [time_series_to_char(ts) for ts in np.hsplit(signal, 4)]

    seq2idx = create_mapping()
    total_count = []

    for ts in seq_coll:
        count = [0 for _ in range(256)]
        for k, v in ts.items():
            idx = seq2idx[k]
            count[idx] = len(v)
        total_count.append(count)


    # plot the count for each seq
    time_axis = np.array(range(len(total_count[0])))
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
    
    ax1.plot(time_axis, np.array(total_count[0]))
    ax2.plot(time_axis, np.array(total_count[1]))
    ax3.plot(time_axis, np.array(total_count[2]))
    ax4.plot(time_axis, np.array(total_count[3]))

    plt.savefig('count.png', dpi=400)

    # plot raw signal
    time_axis = np.array(range(samp_end-samp_start))
    ts1, ts2, ts3, ts4 = np.hsplit(signal, 4)
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
    
    ax1.plot(time_axis, np.array(ts1))
    ax2.plot(time_axis, np.array(ts2))
    ax3.plot(time_axis, np.array(ts3))
    ax4.plot(time_axis, np.array(ts4))
    axes = plt.gca()
    axes.set_ylim([-0.25, 1])

    plt.savefig('raw.png', dpi=400)

    # plot normalized signal
    sig_len = samp_end - samp_start

    time_axis = np.array(range(sig_len))
    ts1, ts2, ts3, ts4 = np.hsplit(signal, 4)

    ts1 = znorm(ts1.flatten())
    ts2 = znorm(ts2.flatten())
    ts3 = znorm(ts3.flatten())
    ts4 = znorm(ts4.flatten())

    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')

    ax1.plot(time_axis, np.array(ts1))
    ax1.plot(time_axis, np.array([0.67]*sig_len), linestyle=':')
    ax1.plot(time_axis, np.array([-0.67]*sig_len), linestyle=':')
    ax1.plot(time_axis, np.array([0]*sig_len), linestyle=':')

    ax2.plot(time_axis, np.array(ts2))
    ax2.plot(time_axis, np.array([0.67]*sig_len), linestyle=':')
    ax2.plot(time_axis, np.array([-0.67]*sig_len), linestyle=':')
    ax2.plot(time_axis, np.array([0]*sig_len), linestyle=':')

    ax3.plot(time_axis, np.array(ts3))
    ax3.plot(time_axis, np.array([0.67]*sig_len), linestyle=':')
    ax3.plot(time_axis, np.array([-0.67]*sig_len), linestyle=':')
    ax3.plot(time_axis, np.array([0]*sig_len), linestyle=':')

    ax4.plot(time_axis, np.array(ts4))
    ax4.plot(time_axis, np.array([0.67]*sig_len), linestyle=':')
    ax4.plot(time_axis, np.array([-0.67]*sig_len), linestyle=':')
    ax4.plot(time_axis, np.array([0]*sig_len), linestyle=':')

    plt.savefig('norm.png', dpi=400)



