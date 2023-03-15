/*
  4-20mA receiver to display result on 4-20mA bus

  The XTR116 is controlled by the output of an MCP4921 12-bit DAC from Microchip
 */
#include <SPI.h>

#define ADC_CS 9  // change to sensor pin

int loop_current;
int received_data;

// calibration data
const int ADC_4mA  = 784;
const int ADC_20mA = 3954;

const int data_min_range = 0;
const int data_max_range = 1023;


void setup() {
 pinMode (ADC_CS, OUTPUT);
 digitalWrite(ADC_CS, 0);
 delay(100);
 digitalWrite(ADC_CS, 1);

 // initialize serial
 Serial.begin(9600);
 // initialize SPI
 SPI.begin();

}

void loop() {

  // read the loop current
  loop_current = ReadFrom420mA();
  // error checking
  if (loop_current == -1)
    Serial.println("Error: open loop");
  else if (loop_current == -2)
    Serial.println("Error: current loop is in short circuit");
  // remapping to initial data range
  else { 
    received_data = map(loop_current, ADC_4mA, ADC_20mA, data_min_range, data_max_range);
    Serial.print("Received value is: ");
    Serial.println(received_data);
  }
}

unsigned int get_ADC(void){
// extract 12 bits from 16 received
  unsigned int result;
  unsigned int first_byte;
  unsigned int second_byte;

  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE1));
  digitalWrite(ADC_CS, 0);
  first_byte = SPI.transfer(0);
  second_byte = SPI.transfer(0);
  digitalWrite(ADC_CS, 1);
  SPI.endTransaction();

  // call for lower order byte of data to be shifted right by one to remove extra bit
  result = ((first_byte & 0x1F) << 8) | second_byte;
  result = result >> 1;
  return result;
}

int ReadFrom420mA(void)
{
  int result;
  int ADC_result;
  float ADC_avrg = 0;
  for (int i = 0; i < 100; i++){
    ADC_result = get_ADC();
    delay(1);   // measure every 1ms
    ADC_avrg = ADC_avrg + ADC_result;
  }
  result = (int)(ADC_avrg/100);

  // open loop
  if (result < (ADC_4mA - 50)){
    return -1;
  }
  // shortcircuit
  if (result > (ADC_20mA + 50)){
    return -2;
  }
  return result;
}