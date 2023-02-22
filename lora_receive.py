###Author: Jennifer Brana
###Last modification: 12/06/2022


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

prev_packet = None

# Define the onboard LED
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

# create empty packet for sensor data
packet = bytearray(8)

while True:
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi LoRa', 35, 0, 1)

    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        display.show()
        display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text and rssi
        display.fill(0)
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        display.text('RX: ', 0, 0, 1)
        display.text(packet_text, 25, 0, 1)
        display.show()
        time.sleep(1)
        
        #create ack packet to send ack back to the sender
        pkt_id = prev_packet[-1] #get the packet id, this is the last byte of the byte array
        ack_msg = bytearray(7) #create byte array of all zeros
        send_back = ack_msg + pkt_id #append the packet id of the previous packet to this one 
        
        #send ack back to the sender
        if send_back is not None:
            display.fill(0)
            rfm9x.send(send_array) #actual sending of data
            display.text('send ack', 15, 20, 1)
            
        display.show()
        time.sleep(1)
       

    #test buttons sending
    #if not btnA.value:
        # Send Button A
        #display.fill(0)
        #button_a_data = bytes("Button A!\r\n","utf-8")
        #rfm9x.send(button_a_data)
        #display.text('Sent Button A!', 25, 15, 1)
    #elif not btnB.value:
        # Send Button B
        #display.fill(0)
        #button_b_data = bytes("Button B!\r\n","utf-8")
        #rfm9x.send(button_b_data)
        #display.text('Sent Button B!', 25, 15, 1)
    #elif not btnC.value:
        # Send Button C
        #display.fill(0)
        #button_c_data = bytes("Button C!\r\n","utf-8")
        #rfm9x.send(button_c_data)
        #display.text('Sent Button C!', 25, 15, 1)


    display.show()
    time.sleep(0.1)
