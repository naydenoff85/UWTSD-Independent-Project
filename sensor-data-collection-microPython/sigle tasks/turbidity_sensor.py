from machine import ADC, Pin
from utime import sleep


turbidity_sensor = ADC(26)
conversion_factor = (3.3 / 65535)
low, high = 1120, 38745


while True:
    raw = turbidity_sensor.read_u16()
    volts = raw * conversion_factor
    percentage = (int(((raw - low) * 100) / (high - low)))
    str_output =  f"Raw: {raw} Voltage {volts:.1f}V  Percentage: {percentage}%"
    print(str_output)
    print(raw)
    sleep(1)