# Anonymous FTP login
from ftplib import FTP
from configurations import FTP_ServerIP
"""
    Currently Image data is directly published on ZDMP service and message bus 
"""

def download_and_publish_pic(mqtt):


    VIS_LOG_BASE_DIR = 'ud1:/vision/logs/'
    with FTP(FTP_ServerIP) as ftp:
        print(f'[X-FTP] Welcome Msg from Robot: {ftp.getwelcome()}')

        # changing to image log dir
        ftp.cwd(VIS_LOG_BASE_DIR)
        print(f'[X-FTP] Current_Dir: {ftp.pwd()}')

        """
            FANUC FTP server supports minimal commands that's why 
            old dir method used for listing all directories
        """
        #List files
        files = []
        ftp.dir(files.append)  # Takes a callback for each file
        VIS_LOG_BASE_DIR=VIS_LOG_BASE_DIR+max(files[-1].split(' '))+'/'
        ftp.cwd(VIS_LOG_BASE_DIR)
        files.clear()
        ftp.dir(files.append)

        #path for latest Log dir
        VIS_LOG_BASE_DIR=VIS_LOG_BASE_DIR+max(files[-1].split(' '))

        print(f'[X-FTP] {VIS_LOG_BASE_DIR}')
        ftp.cwd(VIS_LOG_BASE_DIR)

        # logic for extracting latest image.png file
        img_data = []
        ftp.dir(img_data.append)
        newlist = [x.split()[-1]  for x in img_data if ".png" in x
                if (int((str(x.split()[-1].split('.')[0])[3:]))%2 == 0)]# if ".png" in x x.split()[-1].split('.')[0][3:]
        print('[X-FTP]',newlist,f"RETR {max(newlist)}")

        #downloading file from FTP-Server
        with open(f'{max(newlist)}', 'wb') as local_file:
                    ftp.retrbinary(f'RETR {max(newlist)}', local_file.write)
                    print('[X-FTP] Image downloaded successfully....')

        # reading newly downloaded file as bytes
        with open(f'{max(newlist)}', 'rb') as file:
            pub_data = file.read()
            #publishing image as byte array
            mqtt.publish('LR-Mate/IMG-Data',bytearray(pub_data),qos=1)
            print('[X-FTP] Image published successfully....')

                

