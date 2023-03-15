/*
  4-20mA T click transmitter code

  This code reads the voltage on pin A0
  and sends the result on 4-20mA current loop

 */

#include <SPI.h>

// Arduino UNO with Mikroe Arduino Uno Click shield
// 4-20mA is placed in socket #2
// CS   is pin 9
// SCK  is pin 13
// MISO is pin 12
// MOSI is pin 11
#define DAC_CS 9

// Calibration data obtained by running the calibration code
const int DAC_4mA  = 796;
const int DAC_20mA = 3982;

// Data min and max range
const int data_min_range = 0;
const int data_max_range = 1023;


// Read from A0 pin
int analog_value;

// Debug mode? (1 - debug, 0 - no debug);
bool debug_mode = 1;

void setup() {

  // Are we in debug mode
  if (debug_mode == 1){
     // Initialize serial
     Serial.begin(9600);
  }

  // Initialize SPI
  pinMode(DAC_CS, OUTPUT);
  digitalWrite(DAC_CS, 1);
  SPI.begin();

}

void loop() {

  // Read the input on analog pin 0:
  analog_value = analogRead(A0);

  // Transmit data
  SendTo420mA(analog_value);

  // Are we in debug mode
  if (debug_mode == 1){
     // Print information
     Serial.print("Transmitted value is: ");
     Serial.println(analog_value);
  }
  
  // Don't update too often, it doesn't make sense
  delay(500);

}

void set_DAC(int set_value){
/*
DAC works on SPI
We must send 16 bits
byte1 is [WR, BUF, /GA, /SHDN, data11, data10, data9, data8]
byte2 is [data7, data6, data5, data4, data3, data2, data1, data0]
Write code
WR    0 - write to DAC register
      1 - Ignore this command
VREF Input Buffer Control bit
BUF   0 - Unbuffered
      1 - Buffered
Output Gain Selection bit
/GA   0 - 1x (VOUT = VREF * D/4096)
      1 - 0 = 2x (VOUT = 2 * VREF * D/4096)
Output Shutdown Control bit
/SHDN 0 - Shutdown the device. Analog output is not available.
      1 - Active mode operation. VOUT is available

WR has to be 0 to write to DAC registers
BUF is set to 0 (unbuffered)
GAIN MUST BE SET TO 1. We can't output more than the Vcc!!!
SHDN also set to 1 to have DAC active.
00110000 = 0x30
*/

  byte first_byte;
  byte second_byte;

  first_byte = (set_value >> 8) & 0x0F;
  first_byte = first_byte | 0x30;
  second_byte = set_value & 0xFF;

  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
  digitalWrite(DAC_CS, 0);
  SPI.transfer(first_byte);
  SPI.transfer(second_byte);
  digitalWrite(DAC_CS, 1);
  SPI.endTransaction();

  // Are we in debug mode
  if (debug_mode == 1){
    // Print information
    Serial.print("DAC is set to: ");
    Serial.println(set_value);
    Serial.println();
  }
}

void SendTo420mA(unsigned int transmitted_Value)
{
  // Map the data to be sent into DAC values
  // that result in a loop current between 4 and 20mA
  int temp = map(transmitted_Value, data_min_range, data_max_range, DAC_4mA, DAC_20mA);
  // update the current loop
  set_DAC(temp);
}