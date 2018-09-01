#reference for init array https://tianle.me/2017/02/28/python-array/
#https://pythonprogramming.net/live-graphs-matplotlib-tutorial/
#python central_modify.py -p COM1 -f NRF52 -a EB2533326679
#cd C:\Users\Niklas Liu\Documents\NRF_test_connection\test-decode-nrf52\test doc
# Copyright (c) 2016 Nordic Semiconductor ASA
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
#   3. Neither the name of Nordic Semiconductor ASA nor the names of other
#   contributors to this software may be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
#   4. This software must only be used in or with a processor manufactured by Nordic
#   Semiconductor ASA, or in or with a processor manufactured by a third party that
#   is used in combination with a processor manufactured by Nordic Semiconductor.
#
#   5. Any software provided in binary or object form under this license must not be
#   reverse engineered, decompiled, modified and/or disassembled.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

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

from pc_ble_driver_py.observers     import *

TARGET_DEV_NAME = "Noomi WB"
CONNECTIONS     = 1

from pc_ble_driver_py import config
config.__conn_ic_id__ = "NRF52"

nrf_sd_ble_api_ver = config.sd_api_ver_get()

from pc_ble_driver_py.ble_driver    import BLEDriver, BLEAdvData, BLEEvtID, BLEEnableParams, BLEGapTimeoutSrc, BLEUUID, BLEUUIDBase, BLEGapConnParams
from pc_ble_driver_py.ble_adapter   import BLEAdapter

noomi_service_base           = BLEUUIDBase(list(reversed([0x75, 0xbf, 0xce, 0x84, 0x18, 0x98, 0x03, 0x9b, 0x6a, 0x4a, 0xb7, 0x26, 0x4c, 0x01, 0x52, 0xe4])))
data_stream                  = BLEUUID(0x1401, noomi_service_base)
command                      = BLEUUID(0x1402, noomi_service_base)


uuids = [noomi_service_base]

#for round robin function
array_2d_3 = [([0] * 800) for p in range(3)]
#for display in final
array_2d_4 = [([0] * 800) for p in range(3)]

array_time = []
#print array_time

for j in range(0, 800):
    array_time.append(j*0.025)
print len(array_time)
print array_time
