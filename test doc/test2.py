import sys
import time
import Queue
import binascii
import argparse
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

import numpy as np


sys.stdout.write('.')
import time
from pc_ble_driver_py.observers     import *

TARGET_DEV_NAME = "Noomi WB"
CONNECTIONS     = 1

from pc_ble_driver_py import config
config.__conn_ic_id__ = "NRF52"

nrf_sd_ble_api_ver = config.sd_api_ver_get()

from pc_ble_driver_py.ble_driver    import BLEDriver, BLEAdvData, BLEEvtID, BLEEnableParams, BLEGapTimeoutSrc, BLEUUID, BLEUUIDBase, BLEGapConnParams
from pc_ble_driver_py.ble_adapter   import BLEAdapter


from scipy.fftpack import fft
import pandas as pd

import scipy.fftpack



def DFT(x):
    N = x.size
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * n / N)
    return np.dot(e, x)






t = np.linspace(0, 0.5, 500)
s = np.sin(40 * 2 * np.pi * t) + 0.5 * np.sin(90 * 2 * np.pi * t)

fft = np.fft.fft(s)
T = t[1] - t[0]  # sample rate
N = s.size

# 1/T = frequency
f = np.linspace(0, 1 / T, N)

plt.ylabel("Amplitude")
plt.xlabel("Frequency [Hz]")
plt.bar(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N, width=1.5)  # 1 / N is a normalization factor
plt.show()

