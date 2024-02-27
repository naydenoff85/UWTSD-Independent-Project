from machine import SoftI2C, Pin
from bmp280 import *
from machine import Pin, I2C
import utime
from time import sleep


i2c=SoftI2C(sda=Pin(4), scl=Pin(5), freq=400000) 
print(i2c.readfrom_mem(0x77, 0xd0, 1)[0])

ERROR = -3 # hPa 

# scan i2c port for available devices
result = SoftI2C.scan(i2c)
print("I2C scan result : ", result) # 118 in decimal is same as 0x76 in hexadecimal
if result != []:
    print("I2C connection successfull")
else:
    print("No devices found !")


# create a BMP 280 object
bmp280_object = BMP280(i2c, addr=0x77, use_case=BMP280_CASE_INDOOR)

# configure the sensor
# These configuration settings give most accurate values in my case
# tweak them according to your own requirements

bmp280_object.power_mode = BMP280_POWER_NORMAL
bmp280_object.oversample = BMP280_OS_HIGH
bmp280_object.temp_os = BMP280_TEMP_OS_8
bmp280_object.press_os = BMP280_TEMP_OS_4
bmp280_object.standby = BMP280_STANDBY_250
bmp280_object.iir = BMP280_IIR_FILTER_2

print("BMP Object created successfully !")
utime.sleep(2) # change it as per requirement
print("\n")

# Function for calculation altitude from pressure and temperature values
# because altitude() method is not present in the Library

def altitude_HYP(hPa , temperature):
    # Hypsometric Equation (Max Altitude < 11 Km above sea level)
    temperature = temperature
    local_pressure = hPa
    sea_level_pressure = 1013.25 # hPa      
    pressure_ratio = sea_level_pressure/local_pressure # sea level pressure = 1013.25 hPa
    h = (((pressure_ratio**(1/5.257)) - 1) * temperature ) / 0.0065
    return h


# altitude from international barometric formula, given in BMP 180 datasheet
def altitude_IBF(pressure):
    local_pressure = pressure    # Unit : hPa
    sea_level_pressure = 1013.25 # Unit : hPa
    pressure_ratio = local_pressure / sea_level_pressure
    altitude = 44330*(1-(pressure_ratio**(1/5.255)))
    return altitude

  
while True:
    # accquire temperature value in celcius
    temperature_c = bmp280_object.temperature # degree celcius
    
    # convert celcius to kelvin
    temperature_k = temperature_c + 273.15
    
    # accquire pressure value
    pressure = bmp280_object.pressure  # pascal
    
    # convert pascal to hectopascal (hPa)
    # 1 hPa = 100 Pa
    # Therefore 1 Pa = 0.01 hPa
    pressure_hPa = ( pressure * 0.01 ) + ERROR # hPa
    
    # accquire altitude values from HYPSOMETRIC formula
    h = altitude_HYP(pressure_hPa, temperature_k)
    
    # accquire altitude values from International Barometric Formula
    altitude = altitude_IBF(pressure_hPa)
    press = "{:.2f}".format(pressure_hPa)
    h_alti = "{:.2f}".format(h)
    i_alti = "{:.2f}".format(altitude)
    print("Temperature : ",temperature_c," Degree Celcius")
    print("Pressure : ",pressure," Pascal (Pa)")
    print("Pressure : ",press," hectopascal (hPa) or millibar (mb)")
    print("Altitude (Hypsometric Formula) : ", h_alti ," meter")
    print("Altitude (International Barometric Formula) : ", i_alti ," meter")
    print("\n")
    sleep(5)
