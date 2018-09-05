#
#reference for init array
#https://tianle.me/2017/02/28/python-array/
#https://stackoverflow.com/questions/48298724/fast-fourier-transform-on-motor-vibration-signal-in-python
#
#https://morvanzhou.github.io/tutorials/data-manipulation/plt/2-5-lagend/
#
#reference for animation
#https://pythonprogramming.net/live-graphs-matplotlib-tutorial/
#
#
#fft
#https://wizardforcel.gitbooks.io/hyry-studio-scipy/content/19.html
#http://bbs.bugcode.cn/t/14340
#https://stackoverflow.com/questions/48298724/fast-fourier-transform-on-motor-vibration-signal-in-python
#http://www.vibrationdata.com/Python.htm
#
#
#https://www.youtube.com/watch?v=aQKX3mrDFoY
#https://stackoverflow.com/questions/48298724/fast-fourier-transform-on-motor-vibration-signal-in-python
#https://www.jianshu.com/p/d5c011776ac0
#https://zhuanlan.zhihu.com/p/27880690
#
#
#cd C:\Users\Niklas Liu\Documents\NRF_test_connection\test-decode-nrf52\test doc
#python central_modify_fft.py -p COM1 -f NRF52 -a EB2533326679
#
#
#
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





noomi_service_base           = BLEUUIDBase(list(reversed([0x75, 0xbf, 0xce, 0x84, 0x18, 0x98, 0x03, 0x9b, 0x6a, 0x4a, 0xb7, 0x26, 0x4c, 0x01, 0x52, 0xe4])))
data_stream                  = BLEUUID(0x1401, noomi_service_base)
command                      = BLEUUID(0x1402, noomi_service_base)


uuids = [noomi_service_base]


array_time = []
for j in range(0, 800):
    array_time.append(j*0.025)



#ACC or Pressure data seperation --------------------------------------------------------------------------------

def seperate_data(data_all):
    data_acc =[]
    data_pressure = []
    if(data_all[0] == 0):
        for i in range(9, len(data_all)):
            data_acc.append(data_all[i])
            ##print(format(data_all[i],'02x')),
        decode_data_acc(data_acc) #select only for acc data
    if (data_all[0] == 2):
        for i in range(9, len(data_all)):
            data_pressure.append(data_all[i])
            ##print(format(data_all[i],'02x')),
        decode_data_pressure(data_pressure) #select only for acc data

#PAUS function for the plot------------------

pause = False
def onClick(event):
    global pause
    pause ^= True
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'),
    print "STOP "
    print pause
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'),

#ACC decoding and plot--------------------------------------------------------------------------------

#for round robin function
array_2d_acc_0 = [([0] * 40) for p in range(3)]  # correct way to initial
array_2d_acc_3 = [([0] * 800) for p in range(3)]
#for display in final
array_2d_acc_4 = [([0] * 800) for p in range(3)]

array_2d_acc_5  = [1]*800
array_2d_acc_6  = [2]*800
array_2d_acc_7  = [3]*800



style.use('fivethirtyeight')
fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
#fig1, ax1 = plt.subplots()
#xt = fig1.text(0.5,0.5,'0')

#fig1.canvas.mpl_connect('key_press_event', on_press)
def animate_acc(i):
    ax1.clear()
    ax1.plot( array_time, array_2d_acc_4[0],'C1', label="X-axis",linewidth=1)
    ax1.plot( array_time, array_2d_acc_4[1],'C2', label="Y-axis",linewidth=1)
    ax1.plot( array_time, array_2d_acc_4[2],'C3', label="Z-axis",linewidth=1)
    plt.legend(loc='best')
    plt.xlabel('Time (second)')
    plt.ylabel('Acceleration (g)')




def decode_data_acc(data_acc):
    print('\nlength is:{}'.format(len(data_acc)))
    print 'Raw:'
    for x in data_acc:
        print(format(x, '02x')),
		
    array_2d_acc_1 = [([''] * 40) for p in range(4)] #correct way to initial
    print('\nlength is:{}'.format(len(array_2d_acc_1[0])))
    print('\n0\n'),
    for i in range(0, len(data_acc)):
        array_2d_acc_1[i%4][i/4]=data_acc[i]
        print(format(array_2d_acc_1[i%4][i/4], '02x')),

    print('\n1\n'), #seperate raw value into arrays
    for i in range(0, 4):
        for j in range(0, 40):
            print(format(array_2d_acc_1[i][j], '02x')),
        print('\n'),



    print('\n2\n'), #seperate value for each axis
    array_2d_acc_2 = [([0] * 40) for p in range(3)]  # correct way to initial
    for i in range(0, 3):
        for j in range(0, 40):
            #array_2d_acc_2[0][j] = (array_2d_acc_1[0][j]%64*16)+(array_2d_acc_1[1][j]/16)   # X-axis 10bits
            array_2d_acc_2[0][j] = (array_2d_acc_1[3-0][j]%64*16)+(array_2d_acc_1[3-1][j]/16)

            #array_2d_acc_2[1][j] = (array_2d_acc_1[1][j]%16*64)+(array_2d_acc_1[2][j]/4)     # Y-axis
            array_2d_acc_2[1][j] = (array_2d_acc_1[3-1][j] % 16 * 64) + (array_2d_acc_1[3-2][j] / 4)

            #array_2d_acc_2[2][j] = (array_2d_acc_1[2][j]%4*256)+(array_2d_acc_1[3][j])     # Z-axis
            array_2d_acc_2[2][j] = (array_2d_acc_1[3-2][j] % 4 * 256) + (array_2d_acc_1[3-3][j])
    print('\n3\n'),
    for i in range(0, 3):
        for j in range(0, 40):
            print(array_2d_acc_2[i][j]),
        print('\n'),

    for i in range(0, 3):
        for j in range(0, 40):
            if(array_2d_acc_2[i][j]/512==1): print('-'),
            print(array_2d_acc_2[i][j]%512),
        print('\n'),

    #decode for each axis
    for i in range(0, 3):
        for j in range(0, 40):
            if(array_2d_acc_2[i][j]/512==1):
                #print('-'),
                array_2d_acc_0[i][j]=-(array_2d_acc_2[i][j]%512*2/512.00000000)
            else:
                array_2d_acc_0[i][j]=(array_2d_acc_2[i][j]%512*2/512.00000000)
            print ('%.6f'%(array_2d_acc_0[i][j])),
        print('\n'),

    print('\n4\n'),

    for i in range(0, 3):
        for j in range(0, 40):
            print("{0:10b}".format(array_2d_acc_2[i][j])),
        print('\n'),
    print('\n5\n'),


    if(pause == False):
         print("\n NOT Update data\n")
         around_robin_acc()
         filling_new_data_acc(array_2d_acc_0)
    else:
         print("\n Update data\n")

    # t = np.linspace(0, 0.5, 500)
    #s = np.sin(40 * 2 * np.pi * t) + 0.5 * np.sin(90 * 2 * np.pi * t)
    #array_time
    '''
    print('\n8\n'),
    s = np.sin(40 * 2 * np.pi * array_time) + 0.5 * np.sin(90 * 2 * np.pi * array_time)
    print('\n9\n'),
    fft = np.fft.fft(s)
    print('\n10\n'),
    T = t[1] - t[0]  # sample rate
    N = s.size
    print('\n11\n'),
    f = np.linspace(0, 1 / T, N)
    print('\n12\n'),
    '''




    '''
    print('\n8\n'),
    s=np.array_2d_acc_4[0]
    print s
    print('\n9\n'),
    fft = np.fft.fft(array_2d_acc_4[0])
    print('\n10\n'),
    t = np.linspace(0, 0.025, 20)
    print('\n11\n'),
    T = t[1] - t[0]  # sample rate
    print('\n12\n'),
    N = s.size
    print "\n\narray_time size is"
    print array_time.size
    print('\n13\n'),
    # 1/T = frequency
    f = np.linspace(0, 1 / T, N)
    print('\n14\n'),
    '''










def around_robin_acc():
    for i in range(0, 3):
        for j in range(0, (800-40)):
            array_2d_acc_3[i][j]=array_2d_acc_4[i][j+40]


def filling_new_data_acc(array_2d_acc_2):
    print('\n06\n'),
    for i in range(0, 3):
        for j in range(0, 40):
            array_2d_acc_3[i][j+800-40]=array_2d_acc_2[i][j]
            print ('%.6f' % (array_2d_acc_0[i][j])),
        print('\n'),
    print('\n07\n'),
    for i in range(0, 3):
        for j in range(0, 800):
            array_2d_acc_4[i][j]=array_2d_acc_3[i][j]
            print ('%.6f' % (array_2d_acc_3[i][j])),
        print('\n'),








#ACC FFT---------------------------------------------------------------------------------------------------
#nor = pd.read_csv('normal.csv', header=1)
#https://plot.ly/matplotlib/fft/

import matplotlib.pyplot as plt
import plotly.plotly as py
import numpy as np


style.use('fivethirtyeight')
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)

def animate_acc_fft(i):

    print('\n08\n'),
    s = []
    print('\n09\n'),
    for j in range(0, 800):
        #array_time.append(j * 0.025)
        s.append(array_2d_acc_4[0][j])

    #t = np.linspace(0, 0.5, 500)
    print('\n10\n'),
    #s = array_2d_acc_4[0]
    print('\n11\n'),
    fft = np.fft.fft(s)
    T = array_time[1] - array_time[0]  # sample rate
    print('\n12\n'),
    N = 800
    print('\n13\n'),

    # 1/T = frequency
    f = np.linspace(0, 1 / T, N)

    ax2.clear()
    #ax2.plot( array_time, array_2d_acc_4[0],'C1', label="X-axis",linewidth=1)
    #ax2.plot( array_time, array_2d_acc_4[1],'C2', label="Y-axis",linewidth=1)
    #ax2.plot( array_time, array_2d_acc_4[2],'C3', label="Z-axis",linewidth=1)
    #ax2.plot(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N)
    ax2.plot(f, np.abs(fft * 1 / N))
    #ax2.plot(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N)
    #plt.bar(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N, width=1.5)  # 1 / N is a normalization factor
    plt.legend(loc='best')
    plt.ylabel("Amplitude")
    plt.xlabel("Frequency [Hz]")




#pressure sensor decoding and plot--------------------------------------------------------------------------------
#for round robin function
'''
array_2d_pressure_0 = ([0] * 40) # correct way to initial
array_2d_pressure_3 = ([0] * 800)
#for display in final
array_2d_pressure_4 = ([0] * 800)

array_2d_pressure_5  = [1]*800
array_2d_pressure_6  = [2]*800
array_2d_pressure_7  = [3]*800


style.use('fivethirtyeight')
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)

def animate_pressure(i):
    ax2.clear()
    ax2.plot( array_time, array_2d_pressure_0[0],'C1', label="X-axis",linewidth=1)
    plt.legend(loc='best')
    plt.xlabel('Time (second)')
    plt.ylabel('Acceleration (g)')



def decode_data_acc(data_acc):





def update_data_pressure(array_2d_pressure_4):
    around_robin()
    filling_new_data(array_2d_pressure_4)
'''






		

		
def init(conn_ic_id):
    global BLEDriver, BLEAdvData, BLEEvtID, BLEAdapter, BLEEnableParams, BLEGapTimeoutSrc, BLEUUID
    config.__conn_ic_id__ = conn_ic_id


class Collector(BLEDriverObserver, BLEAdapterObserver):
    def __init__(self, adapter, uuids, address):
        super(Collector, self).__init__()
        self.adapter    = adapter
        self.conn_q     = Queue.Queue()
        self.adapter.observer_register(self)
        self.adapter.driver.observer_register(self)
        self.uuids = uuids
        self.target_address = address
        self.conn_params = BLEGapConnParams(min_conn_interval_ms = 100,
                                max_conn_interval_ms = 100,
                                conn_sup_timeout_ms  = 4000,
                                slave_latency        = 0)

    def open(self):
        self.adapter.driver.open()

        ble_enable_params = BLEEnableParams(vs_uuid_count      = 2,
                                            service_changed    = False,
                                            periph_conn_count  = 0,
                                            central_conn_count = CONNECTIONS,
                                            central_sec_count  = CONNECTIONS)
        if nrf_sd_ble_api_ver >= 3:
            ble_enable_params.att_mtu = 247
            print("Enabling packet length %d", ble_enable_params.att_mtu)

        self.adapter.driver.ble_enable(ble_enable_params)

        for uuid in self.uuids:
            self.adapter.driver.ble_vs_uuid_add(uuid)


    def close(self):
        self.adapter.driver.close()


    def connect_and_discover(self):
        self.adapter.driver.ble_gap_scan_start()
        new_conn = self.conn_q.get(timeout = 60)

        if nrf_sd_ble_api_ver >= 3:
            att_mtu = self.adapter.att_mtu_exchange(new_conn)

        self.adapter.service_discovery(new_conn)
        self.adapter.enable_notification(new_conn, data_stream)
        return new_conn


    def on_gap_evt_connected(self, ble_driver, conn_handle, peer_addr, role, conn_params):
        print('New connection: {}'.format(conn_handle))
        self.conn_q.put(conn_handle)


    def on_gap_evt_disconnected(self, ble_driver, conn_handle, reason):
        print('Disconnected: {} {}'.format(conn_handle, reason))


    def on_gap_evt_timeout(self, ble_driver, conn_handle, src):
        if src == BLEGapTimeoutSrc.scan:
            ble_driver.ble_gap_scan_start()


    def on_gap_evt_adv_report(self, ble_driver, conn_handle, peer_addr, rssi, adv_type, adv_data):
        dev_name_list = None
        if BLEAdvData.Types.complete_local_name in adv_data.records:
            dev_name_list = adv_data.records[BLEAdvData.Types.complete_local_name]

        elif BLEAdvData.Types.short_local_name in adv_data.records:
            dev_name_list = adv_data.records[BLEAdvData.Types.short_local_name]

        else:
            return

        dev_name        = "".join(chr(e) for e in dev_name_list)
        address_string  = "".join("{0:02X}".format(b) for b in peer_addr.addr)
        print('Received advertisment report, address: 0x{}, device_name: {}'.format(address_string,
                                                                                    dev_name))

        if (dev_name == TARGET_DEV_NAME and address_string == self.target_address):
            self.adapter.connect(peer_addr, conn_params = self.conn_params)


    def on_notification(self, ble_adapter, conn_handle, uuid, data):
        # print ''.join('{:02x}'.format(x) for x in data)
        # storage_data(data)
        #print '\n'
        print''.join('{:02x}'.format(x) for x in data)
        seperate_data(data)


    def on_att_mtu_exchanged(self, ble_driver, conn_handle, att_mtu):
        print('ATT MTU exchanged: conn_handle={} att_mtu={}'.format(conn_handle, att_mtu))


    def on_gattc_evt_exchange_mtu_rsp(self, ble_driver, conn_handle, **kwargs):
        print('ATT MTU exchange response: conn_handle={}'.format(conn_handle))

    def on_gap_evt_conn_param_update_request(self, ble_driver, conn_handle, conn_params):
        print('Connection parameter update request: conn_handle={}, min_conn_int={}, max_conn_int={}'.format(conn_handle,
            conn_params.min_conn_interval, conn_params.max_conn_interval))



def main(serial_port, address):
    print('Serial port used: {}'.format(serial_port))
    driver    = BLEDriver(serial_port=serial_port, auto_flash=True)
    adapter   = BLEAdapter(driver)
    collector = Collector(adapter, uuids, address)
    collector.open()
    for i in xrange(CONNECTIONS):
        conn_handle = collector.connect_and_discover()

    fig1.canvas.mpl_connect('button_press_event', onClick)
    anim1 = animation.FuncAnimation(fig1, animate_acc, blit=False, interval=1000, repeat=True)
    #plt.show()



    anim2 = animation.FuncAnimation(fig2, animate_acc_fft, interval=2000)
    plt.show()

    while(True):
        pass


if __name__ == "__main__":
    print'start to scan'
    serial_port = None
    parser = argparse.ArgumentParser(description='Extract data log from noomi wb')
    parser.add_argument('--port', '-p',
                        type=str,
                        required=True,
                        dest='port',
                        help='COM port the nRF DK is connected to, e.g. COM1')
    parser.add_argument('--family', '-f',
                        type=str,
                        required=True,
                        dest='family',
                        help='NRF51 or NRF52')
    parser.add_argument('--address', '-a',
                        type=str,
                        required=True,
                        dest='address',
                        help='Advertising address of wristband w/o colons, e.g. C29A327DDEFC')

    args = parser.parse_args()
    init(args.family)
    main(args.port, args.address)
    quit()


