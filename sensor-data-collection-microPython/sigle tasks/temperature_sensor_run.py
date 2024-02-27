# Imports
import onewire, ds18x20, time
from machine import Pin
from time import sleep

# Set the data pin for the sensor
SensorPin = Pin(27, Pin.IN)

# Tell MicroPython we're using a DS18B20 sensor, and which pin it's on
sensor = ds18x20.DS18X20(onewire.OneWire(SensorPin))

# Look for DS18B20 sensors (each contains a unique rom code)
roms = sensor.scan()
sleep(1)
while True: # Run forever
    
    sensor.convert_temp() # Convert the sensor units to centigrade
    
    time.sleep(2) # Wait 2 seconds (you must wait at least 1 second before taking a reading)
    
    for rom in roms: # For each sensor found (just 1 in this case)
        
        print((sensor.read_temp(rom)), "°C") # Print the temperature reading with °C after it
        
        time.sleep(5) # Wait 5 seconds before starting the loop again