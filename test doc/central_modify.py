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
array_2d_3 = [([''] * 800) for p in range(4)]
#for display in final
array_2d_4 = [([''] * 800) for p in range(4)]


def decode_data(data_acc):
    print('\nlength is:{}'.format(len(data_acc)))

    print 'Raw:'
    for x in data_acc:
        print(format(x, '02x')),

    #array_2d= np.zeros((2, 1))
    #array_2d_1 = [['']*40]*4 #array 4*160
    array_2d_1 = [([''] * 40) for p in range(4)] #correct way to initial
    print('\nlength is:{}'.format(len(array_2d_1[0])))
    print('\n0\n'),
    for i in range(0, len(data_acc)):
        array_2d_1[i%4][i/4]=data_acc[i]
        print(format(array_2d_1[i%4][i/4], '02x')),

    print('\n1\n'), #seperate raw value into arrays
    for i in range(0, 4):
        for j in range(0, 40):
            print(format(array_2d_1[i][j], '02x')),
        print('\n'),



    print('\n2\n'), #seperate value for each axis
    array_2d_2 = [([0] * 40) for p in range(3)]  # correct way to initial
    for i in range(0, 3):
        for j in range(0, 40):
            #array_2d_2[0][j] = (array_2d_1[0][j]%64*16)+(array_2d_1[1][j]/16)   # X-axis 10bits
            array_2d_2[0][j] = (array_2d_1[3-0][j]%64*16)+(array_2d_1[3-1][j]/16)
            '''
            print((array_2d_1[0][j]%64)),
            print(array_2d_1[1][j]/16),
            print(array_2d_2[0][j]),
            print(','),
            '''
            #array_2d_2[1][j] = (array_2d_1[1][j]%16*64)+(array_2d_1[2][j]/4)     # Y-axis
            array_2d_2[1][j] = (array_2d_1[3-1][j] % 16 * 64) + (array_2d_1[3-2][j] / 4)
            '''
            print((array_2d_1[1][j]%16)),
            print((array_2d_1[2][j]/4)),
            print(array_2d_2[1][j]),
            print(','),
            '''
            #array_2d_2[2][j] = (array_2d_1[2][j]%4*256)+(array_2d_1[3][j])     # Z-axis
            array_2d_2[2][j] = (array_2d_1[3-2][j] % 4 * 256) + (array_2d_1[3-3][j])
            '''
            print((array_2d_1[2][j]%4)),
            print((array_2d_1[3][j])),
            print(array_2d_2[2][j]),
            print(','),
            '''
            #print(array_2d_2[0][j]),
            #print(array_2d_2[1][j]),
            #print(array_2d_2[2][j]),
         #print('\n'),
    print('\n3\n'),
    for i in range(0, 3):
        for j in range(0, 40):
            print(array_2d_2[i][j]),
        print('\n'),

    for i in range(0, 3):
        for j in range(0, 40):
            if(array_2d_2[i][j]/512==1): print('-'),
            print(array_2d_2[i][j]%512),
            #print(format(array_2d_2[i][j]%512, '02f')),
        print('\n'),

    for i in range(0, 3):
        for j in range(0, 40):
            if(array_2d_2[i][j]/512==1): print('-'),
            #print(format((array_2d_2[i][j]%512*2/512.00), '02f')),
            print ('%.2f'%(array_2d_2[i][j]%512*2/512.00)),
            #print(array_2d_2[i][j]%512*2/512),
        print('\n'),

    print('\n4\n'),

    for i in range(0, 3):
        for j in range(0, 40):
            print("{0:10b}".format(array_2d_2[i][j])),
        print('\n'),
    print('\n5\n'),
    animation_data(array_2d_2)


def around_robin():
    for i in range(0, 3):
        for j in range(0, 700):
            array_2d_3[i][j+100]=array_2d_4[i][j]
    return array

#def filling_new_data(data):



def animation_data(array_2d_2):
    around_robin()
    filling_new_data(array_2d_2)





def seperate_data(data_all):
    data_acc =[]
    ##print('\n'),
    if(data_all[0]==0):
        ##print(len(data_all))
        '''
        for i in range(0, len(data_all)):
            print(format(data_all[i], '02x')),
        '''
        for i in range(9, len(data_all)):
            data_acc.append(data_all[i])
            ##print(format(data_all[i],'02x')),
        '''
        print('\n'),
        print('Copy to\n'),
        print(len(data_acc))
        while i < (len(data_acc)):
            print(format(data_acc[i], '02x')),
            i += 1
        print('End \n'),
        '''
        decode_data(data_acc) #select only for acc data
    '''
	   #-----print all 169bytes data-----
	   for x in data1:
		 print(format(x,'02x')),
	   print('\n'),
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
        #print''.join('{:02x}'.format(x) for x in data)
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
