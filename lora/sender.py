###Author: Jennifer Brana
###Last modification: 2/21/2023


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

#for generating message IDs
import random

import time
import busio
import digitalio
import board


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
sensor_data = bytearray(8)

#start_time = time.monotonic()
#elapsed_time = time.monotonic() - start_time

def sendSensorDataLocal():
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi LoRa', 35, 0, 1)

    #create random number for ID
    id = random.randint(0,255)
    id_byte = id.to_bytes(1, byteorder='big') #convert to 1 byte length byte array with big-endian format

    if sensor_data is None:
        display.show()
        display.text('- Waiting for PKT -', 15, 20, 1)
        return
    else:
        #append unique id to byte array. id is appended to the end.
        send_array = sensor_data + id_byte
        send_array = sensor_data.extend(id_byte)

        display.fill(0)
        rfm9x.send(send_array) #actual sending of data
        display.text('try send data', 15, 20, 1)

    display.show()
    time.sleep(1)

    count = 0 #count to track how long the sender has waited after sending the data and not receiving the ack.
    global_count = 0 #count to track how long this packet has been waiting to receive an ack, including time after retries.

    #wait for acknowledgement here
    while True:
        #exit the loop if we've waited 30 minutes for the ack. it's not coming. give up.
        if global_count >= 6:
            display.show()
            display.text('- Ack failure -', 15, 20, 1)
            display.show()
            time.sleep(1)
            return

        #if the lora has waited 5 minutes without an ack, resend the data packet
        if count >= 60:
            global_count += 1
            #append unique id to byte array. id is appended to the end.
            send_array = sensor_data + id_byte
            send_array = sensor_data.extend(id_byte)

            display.fill(0)
            rfm9x.send(send_array) #actual sending of data
            display.text('try send data', 15, 20, 1)
            count = 0 # restart the count value
            time.sleep(5)

        ackpacket = None

        #check for packet rx
        ackpacket = rfm9x.receive()

        if ackpacket is None:
            display.show()
            display.text('- Waiting for Ack -', 15, 20, 1)
        else:
            # Display the packet text and rssi
            display.fill(0)
            prev_packet = ackpacket #received ack packet
            pkt_id = prev_packet[-1] #get the ID of the packet sent

            #check that the packet id matches this one
            if pkt_id == id_byte:
                display.text('success!', 15, 20, 1)
                display.show()
                time.sleep(1)
                return

        count += 1
        global_count += 1
        time.sleep(5) #wait 5 seconds for an ack


    time.sleep(0.1)
    return



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
