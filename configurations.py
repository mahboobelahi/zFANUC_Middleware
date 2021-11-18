

#########################Middleware CONSTS-Global VARS#########################

#related to middleware app only

LocIP = '0.0.0.0'#'192.168.1.2'
LocPort = 3000

#ZDMP DAQ and M&S BUS
ROBOT_ID = 'E122350'
ROBOT_NAME = 'LRMate200iD-4S'+ROBOT_ID
zMSG_PORT = 30204
zMSG_TLS_PORT = 30206
z_MSG_URL = '192.168.100.100'
USER = 'tau'
PASSWORD =  'ZDMP-tau2020!'
TOPIC_TYPE= 'multi'

#Robot-KAREL URLS
ORCHESTRATOR_URL = 'http://192.168.1.1/KAREL/z_Orchstrate'
UPDATE_POS_REG = 'http://192.168.1.1/KAREL/z_getRokiPOS'

#FANUC Socket and FTP  Server
socket_ServerIP = '192.168.1.1'
socket_PORT = 1162      # The port used by the server
FTP_ServerIP = '192.168.1.1'
BASE_TOPIC = 'LR-Mate/'
#DAQ URLs
ADMIN_URL = f'http://192.168.100.100:30025'
ASYNCH_URL =  f'http://192.168.100.100:30026'
SYNCH_URL = f'http://192.168.100.100:30027'

# ZDMP-Cumulocity IoT tenant credentials
domain = "https://zdmp-da.eu-latest.cumulocity.com"
TenantID = "t59849255/mahboob.elahi@tuni.fi"
passward = "mahboobelahi93"

##############################MQTT-Settings###########################################
Conn_ALIVE = 5
MQTT_CLIENT_ID = 'E122350-LRMate200iD-4S'
MQTT_BROKER_URL = z_MSG_URL  # use the free broker from HIVEMQ
MQTT_BROKER_PORT = zMSG_PORT  # default port for non-tls connection
MQTT_USERNAME = USER  # set the username here if you need authentication for the broker
MQTT_PASSWORD = PASSWORD # set the password here if the broker demands authentication
MQTT_KEEPALIVE = Conn_ALIVE  # set the time interval for sending a ping to the broker to 5 seconds
MQTT_TLS_ENABLED = True  # set TLS to disabled for testing purposes
MQTT_TLS_CA_CERTS = './files/ca_certificate.pem'
MQTT_REFRESH_TIME = 1.0  # refresh time in seconds