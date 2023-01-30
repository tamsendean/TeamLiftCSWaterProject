##Imports for LoRa
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x

#Imports for read_serial
import time
import busio
import digitalio
import board

import serial
import time,threading
from datetime import datetime
import pytz
from csv import DictWriter
import os
max_packet_num = 256



# Delay between sending radio data, in minutes
SENSOR_SEND_DELAY = 1

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create library object using our Bus I2C port
#bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

##Define buttons for testing
# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP


# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

#define radio frequency
RADIO_FREQ_MHZ = 915.0

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

#set transmit power to max
rfm9x.tx_power = 23

#prev_packet = None

# Define the onboard LED
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

# create empty packet for sensor data
#sensor_data = bytearray(8)

def sendSensorData(dataa):
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi LoRa', 35, 0, 1)
   
    if dataa is None:
        display.show()
        display.text('- Waiting for PKT -', 15, 20, 1)
        return
    else:
        display.fill(0)
        rfm9x.send(dataa)
        display.text('sent data', 15, 20, 1)
       
    display.show()
    time.sleep(0.1)
    return



#file_writer = open('agg_data.txt','a')
def UploadThread():
    while True:
        
        os.system("python3 datapusher.py")
        
        os.system("echo -n '' > agg_data.txt")
        os.system("python3 check_connection.py")
        time.sleep(15)

with serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=5) as ard:
    packet = 0
    time.sleep(2) # wait for port to be "ready"
        # unsure as to why this is necessary
        # if sleep is <2 then the first packet is lost
    #background_thread = threading.Thread(target = UploadThread)
    #background_thread.start()
    
    while True:
        print("sending packet", packet)
        ard.write(packet.to_bytes(1, 'big'))
        data = ard.readline()
        print("received", data.decode(), end="")
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
        print("\n timestamped data", data_timestamped)
        
        
        #file_writer.write(data_timestamped.replace('\n',''))
        #file_writer.write('\n')
        os.system("echo '"+data_timestamped+"' >> agg_data.txt")

   
        
        

        
