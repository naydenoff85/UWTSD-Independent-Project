from machine import I2C, Pin
from bmp280 import *
import time

# Update these based on your board's I2C pins
scl_pin = 5  # D1 on ESP8266, IO5 on ESP32
sda_pin = 4  # D2 on ESP8266, IO4 on ESP32

# Initialize I2C
# ESP8266: i2c = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100000)
# ESP32: Use id=0 for hardware I2C on default pins, or specify scl and sda
i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=1000000)

def scan_i2c_bus():
    devices = i2c.scan()
    if devices:
        for device in devices:
            print("I2C device found at address: 0x{:02X}".format(device))
    else:
        print("No I2C devices found")

scan_i2c_bus()

try:
    bmp = BMP280(i2c, addr=0x77, use_case=BMP280_CASE_WEATHER)
    print("BMP280 initialization successful")
except OSError as e:
    print(f"Failed to initialize BMP280: {e}")
    
while True:
    pressure=bmp.pressure
    p_bar=pressure/100000
    p_mmHg=pressure/133.3224
    temperature=bmp.temperature
    print("Temperature: {} C".format(temperature))
    print("Pressure: {} Pa, {} bar, {} mmHg".format(pressure,p_bar,p_mmHg))
    time.sleep(5)
    
