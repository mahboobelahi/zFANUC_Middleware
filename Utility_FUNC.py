import requests,threading,json,urllib.parse,time
from SM_client import connect_socket
from app import mqtt
from FTP_client import download_and_publish_pic
from configurations import (ROBOT_ID,BASE_TOPIC,
                            ORCHESTRATOR_URL,
                            UPDATE_POS_REG,
                            SYNCH_URL)

#Mqtt commands mappings
CMD=dict([
            ("open-socket",200),
            ("send-pic",199),
            ("zRokiPOS",198),
            ("close-socket",197)
        ])

# register robot to ZDMP-DAC Component
def register_device(URL,ID,name):
    # need to set some guard condition to avoid re-registration of device
    # each device registared against a unique external ID
    # Cumulocity credentials are not required anymore within ZDMP network
    req= requests.get(url=f'{URL}/deviceInfo?externalId={ID}')
    if req.status_code == 200:
        
        print('[X-UF] Device is already Registered. Device details are:')
        print(f'[X-HU] ID From DAQ: {req.json().get("id")}')
        #pp(req.json())
    else:
        print('[X-UF] Registering the device....')
        req_R= requests.post(url=f'{URL}/registerDevice?externalId={ID}&name={name}&type=c8y_Serial')
        print(f'[X-UF] Http Status Code: {req_R.status_code}')
        # setting souece ID of device
        print(f'[X-HU] ID From DAQ: {req_R.json().get("id")}')
        print('[X-UF] Device Registered Successfully.\n')
        #pp(req_R.json())
        #ID----'38623848'
        """
         I have a question just for my own knowledge, During the test of the TAU middleware application
         I subscribed to a random topic on message bus using the MQTT box (GUI MQTT client) 
         but this client did not receive any published data through the subscribed device was publishing data continuously.
         Can you please provide some insight into this issue? 
        """
#utility Function(S)

#process commands

def process_CMD(cmd):
    if cmd in CMD:
        payload = {"CMD":CMD.get(cmd)}
        if CMD.get(cmd) == 200:
            # run Socket Messing Server 
            req= requests.get(f'{ORCHESTRATOR_URL}',params=payload)
            
            print(f'[X-UF] Status Code: {req.status_code}, CMD: {CMD.get(cmd)}')
            print(f'[X-UF] {req.text}')
            threading.Thread(target=connect_socket,
                         daemon = True).start()
            return
        elif CMD.get(cmd) == 199:
            # download current Workspace picture and publish to zRoki
            req= requests.get(f'{ORCHESTRATOR_URL}',params=payload)
            print(f'[X-UF] Status Code: {req.status_code}, CMD: {CMD.get(cmd)}')
            print(f'[X-UF] {req.text}')
            threading.Timer(0.5, download_and_publish_pic).start()

        elif CMD.get(cmd) == 197:

            req= requests.get(f'{ORCHESTRATOR_URL}',params=payload)
    else:
        print("[X-UF] CMD not Understand....")

#update robot position
def update_POS(POS):
    #[float(val) for val in json.loads(POS).values()]
    id= 100
    (XX,YY,ZZ,WW,PP,RR) = ([float(val) for val in json.loads(POS).values()])
    payload =dict([ ("id",id),
                    ("XX",XX),("YY",YY),("ZZ",ZZ),
                    ("WW",WW),("PP",PP),("RR",RR)
                    ])
    
    req= requests.get(f'{UPDATE_POS_REG}',params=payload)
    print(f'[X-UH] {req.url}')
    time.sleep(0.1)
    req= requests.get(f'{ORCHESTRATOR_URL}',params={"CMD":198})
    print(f'[X-UH] {req.url}')
    
# ASYNC-Data:

def sub_or_Unsubscribe_DataSource(ASYNCH_URL,ROBOT_ID,subs=False):
    
    if subs:
        req= requests.get(f'{ASYNCH_URL}/unsubscribe',
                params={"externalId":ROBOT_ID,"topicType":'multi' })
        print(f'Subscribing to Data Source: {ROBOT_ID}....')
        req= requests.get(f'{ASYNCH_URL}/subscribe',
                        params={"externalId":ROBOT_ID,"topicType":'multi' })
        if req.status_code ==200:
                print(f'Subscrption Status: {req.status_code} {req.reason}')
        else:
            print(f'Subscrption Status: {req.status_code} {req.reason}')
    else:
        req= requests.get(f'{ASYNCH_URL}/unsubscribe',
                        params={"externalId":ROBOT_ID,"topic":'multi' })

        if req.status_code ==200:
            print(f'Unsubscrption Status: {req.status_code} {req.reason}')
        else:
            print(f'Unsubscrption Status: {req.status_code} {req.reason}')

#SYNCHRONOUSLY sending measurements on custom endpoint
def send_Measurements(JSON_DATA):
    for k, v in JSON_DATA.items():
        # print(k,v)
        # setting query string
        if JSON_DATA.get('[X-TCP14]'):
            print(JSON_DATA.pop('[X-TCP14]'))
        payload = {"externalId": ROBOT_ID,
                   "fragment": f'{BASE_TOPIC}{k}'}
        payload = urllib.parse.urlencode(payload, safe='/')

        req = requests.post(f'{SYNCH_URL}/sendCustomMeasurement',
                            params=payload,
                            json={k: v})
        # print('[X-UF]',req.url)
        print('[X-UF]',req.status_code,req.reason)


#publish positional data to MsgBus
def pub_POS(JSON_Data):
    #frame data
    mqtt.publish('LR-Mate/active-frames/Cam_frame',json.dumps(JSON_Data.get("camera_frame")))
    mqtt.publish('LR-Mate/active-frames/Uframe',json.dumps(JSON_Data.get("uframe_Data")))
    mqtt.publish('LR-Mate/active-frames/Utool',json.dumps(JSON_Data.get("utool_Data")))
    #positional data
    mqtt.publish('LR-Mate/Home-POS',json.dumps(JSON_Data.get("Home_POS")))
    mqtt.publish('LR-Mate/Current_POS',json.dumps(JSON_Data.get("Current_POS")))