#!/usr/bin/env python3
import threading
from pprint import pprint as P
import socket,re

import Utility_FUNC
from configurations import ( socket_PORT,
                            socket_ServerIP,
                            SYNCH_URL)

"""
    It is local host because roboguide is running on PC
    when you connect to robot through ethernet cable then use the IP 
    of original robot 192.168.1.1
"""
JSON_DATA={}

def connect_socket():
    """
    starts socket communication with robot and sends robot's data to DAQ component
    :param SYNCH_URL: ZDMP-DAQ synchronous API
    :return:
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((socket_ServerIP, socket_PORT))

        while True:
            data = s.recv(1024)
            #print(f'[X-SM] {data}')
            #processing RAW data
            if data and ('[X-TCP]' not in data.decode().strip().split()):
                data = data.decode().strip().split()
                # data = re.sub("\s+",
                #     '',
                # data.decode()).split()
                print(f'[X-SM] {data}')

                if len(data)>1:
                    if data[0] not in JSON_DATA:
                        #making python dictionary object
                        JSON_DATA[data[0]] =dict([("XYZ",[float(i) for i in data[1:4] if i.isdigit()]),
                                                ("WPR",[float(i) for i in data[4:7] if i.isdigit()]),
                                                ("CONFIG","NUT000")])
                    else:

                        #updating dictionary values
                        JSON_DATA[data[0]]["XYZ"]=[float(i) for i in data[1:4] ]
                        JSON_DATA[data[0]]["WPR"]=[float(i) for i in data[4:7] ]
                        JSON_DATA[data[0]]["CONFIG"]="NUT000"
                        #
                        # # sending measurements to ZDMP-DAQ using
                        # #custom Fragment endpoint
                        # threading.Timer(0.1, Utility_FUNC.send_Measurements,
                        #                 args=(JSON_DATA,)
                        #                 ).start()
                        #directly to Msg Bus
                        threading.Timer(0.1, Utility_FUNC.pub_POS,
                                        args=(JSON_DATA,)
                                        ).start()


                        #P(list(JSON_DATA.items()))
            else:
                if JSON_DATA.get('[X-TCP14]'):
                    print(f'[X-SM] Removed: {JSON_DATA.pop("[X-TCP14]")}')
                print('[XX-SM] Connection is closed by USER')
                print('[XX-SM] Last Published Data:')
                print('[XX-SM]:')
                #JSON_DATA.pop('[X-TCP14]')
                P(JSON_DATA)
                break
