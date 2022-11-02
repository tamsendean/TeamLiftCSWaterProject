import serial
import time,threading
from datetime import datetime
import pytz
from csv import DictWriter
import os
max_packet_num = 256
#file_writer = open('agg_data.txt','a')
def UploadThread():
    while True:
        os.chdir("..")
        os.chdir("data_upload")
        os.system("python3 datapusher.py")
        
        os.chdir("..")
        os.chdir("data_agg")
        os.system("echo -n '' > agg_data.txt")
        time.sleep(60)

with serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=5) as ard:
    packet = 0
    time.sleep(2) # wait for port to be "ready"
        # unsure as to why this is necessary
        # if sleep is <2 then the first packet is lost
    background_thread = threading.Thread(target = UploadThread)
    background_thread.start()
    
    while True:
        print("sending packet", packet)
        ard.write(packet.to_bytes(1, 'big'))
        data = ard.readline()
        print("received", data.decode(), end="")
        packet = (packet + 1) % max_packet_num
        
        oregon_timezone = pytz.timezone("US/Pacific")
        time_now= (datetime.now(oregon_timezone)).strftime("%Y-%m-%d %H:%M:%S")
        data_timestamped = str(data.decode()) + "," + str(time_now)
        print("\n timestamped data", data_timestamped)
        
        
        #file_writer.write(data_timestamped.replace('\n',''))
        #file_writer.write('\n')
        os.system("echo " + "'" + data_timestamped + "' >> agg_data.txt")

   
        
        

        
