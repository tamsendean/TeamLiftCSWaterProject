#How to use LoRa code

Plug code that accepts data from sensors and aggregates into a byte array into the periodic.py.

When this function has completed its aggregation and is ready, call "append_sensordata(dataArray)" where dataArray is the byte array you would like to send. That's it! 
