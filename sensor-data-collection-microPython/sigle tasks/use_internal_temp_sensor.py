from machine import ADC
import time

adc = machine.ADC(4)

while True:
    adc_voltage = adc.read_u16() * (3.3 / (65535))
    temperature_celsius = 27 - (adc_voltage - 0.706)/0.001721
    print(f"Temperature: {temperature_celsius:.2f} °C")
    time.sleep(2)


