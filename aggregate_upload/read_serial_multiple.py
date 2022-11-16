import serial
import time,threading
from datetime import datetime
import pytz
import os
import queue

max_packet_num = 256
#file_writer = open('agg_data.txt','a')
def UploadThread():
    while True:
        
        os.system("python3 datapusher.py")
        
        os.system("echo -n '' > agg_data.txt")
        time.sleep(15)

def readSerial(port, queue):
    with serial.Serial(port=port, baudrate=9600, timeout=5) as ard:
        packet = 0
        time.sleep(2) # wait for port to be "ready"
            # unsure as to why this is necessary
            # if sleep is <2 then the first packet is lost
        #background_thread = threading.Thread(target = UploadThread)
        #background_thread.start()
        
        while True:
            # print("sending packet", packet)
            ard.write(packet.to_bytes(1, 'big'))
            data = ard.readline()
            # print("received", data.decode(), end="")
            packet = (packet + 1) % max_packet_num
            
            oregon_timezone = pytz.timezone("US/Pacific")
            time_now= (datetime.now(oregon_timezone)).strftime("%Y-%m-%d %H:%M:%S")
            
            #past_loop_hr = str(time_now)[10:13] # remembers last hour state
            # if the current hour isn't the same as the last timestamp, then it's time to move data to a new file
            # not tested yet
            #curr_loop_hr = str(time_now)[10:13]
            #if (past_loor_hr != curr_loop_hr):
                #print("\n new hour reached")
                    #with open('agg_data.txt') as f:
                        #os.system("echo " + "'" + f.readlines() + "' >> hourly_data.txt")
            data_timestamped = str(data.decode()) + "," + str(time_now)
            #print("\n timestamped data", data_timestamped)
            
            
            #file_writer.write(data_timestamped.replace('\n',''))
            #file_writer.write('\n')
            #os.system("echo '"+data_timestamped+"' >> agg_data.txt")
            q.put(port + " " + data_timestamped)


q = queue.Queue()

thr1 = threading.Thread(target=readSerial, args=('/dev/ttyACM0',q))
thr2 = threading.Thread(target=readSerial, args=('/dev/ttyACM1',q))

thr1.start()
thr2.start()

while(True):
    data = q.get(block=True)
    print(data)