"""
MQTT client that connects to the Adafruit IO MQTT server
and publishes values that represent temperature sensor measurements
"""

import network
from time import sleep
import socket
from umqtt.simple import MQTTClient
import onewire, ds18x20, time
from machine import ADC, Pin

# Fill in your WiFi network name (ssid) and password here:
SSID = 'RaspiNET'
PASSWORD = 'iv4n!sthe3b3st'

# Configure interface and aasign it to a variable
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
    
# Scan for available Networks
scan_results = wlan.scan()

# Connect to WiFi
def wifi_connect():
    
    #Connect to WLAN
    wlan.connect(SSID, PASSWORD)
    sleep(2)
    
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        wlan.connect(SSID, PASSWORD)
        sleep(5)
       


    print(f'Connected on {wlan.ifconfig()[0]}')

# Fill in the Adafruit IO Authentication and Feed MQTT Topic details
mqtt_host = "io.adafruit.com"
mqtt_username = "ivan85"  # The Adafruit IO username
mqtt_password = "aio_uzTi29lq2beejQhPdQU79EVBLKuJ"  # Adafruit IO Key
mqtt_publish_topic = "ivan85/feeds/DS18B20_sensor_data"  # The MQTT topic for the Adafruit IO Feed

mqtt_publish_topic_2 = "ivan85/feeds/turbidity_sensor"  # The MQTT topic for the Adafruit IO Feed

# Enter an ID for this MQTT Client
# It needs to be globally unique across all of Adafruit IO.
mqtt_client_id = "raspi_pi_w_temperature_sensor_DS18B20"
mqtt_client_id_2 = "raspi_pi_w_gravity_turbidity_sensor"

# Initialize MQTTClients and connect them to the MQTT server
mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

mqtt_client_2 = MQTTClient(
        client_id=mqtt_client_id_2,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

wifi_connect()

mqtt_client.connect()
mqtt_client_2.connect()

# Set the data pin for the sensor
SensorPin = Pin(27, Pin.IN)

turbidity_sensor = ADC(28)
conversion_factor = (5.0 / 65535)
low, high = 8866, 65535

# Tell MicroPython we're using a DS18B20 sensor, and which pin it's on
sensor = ds18x20.DS18X20(onewire.OneWire(SensorPin))

# Publish a data point to the Adafruit IO MQTT server every 3 seconds
# Note: Adafruit IO has rate limits in place, every 3 seconds is frequent
# enough to see data in realtime without exceeding the rate limit.

try:
    while True:
        # Read the data drom the DS18B20 temp sensor
        roms = sensor.scan()
        sensor.convert_temp() # Convert the sensor units to centigrade
        sleep(2) # Wait some time (you must wait at least 1 second before taking a reading)
    
        for rom in roms: # For each sensor found (just 1 in this case)
            
            sensor_data = sensor.read_temp(rom)
        
            print((sensor.read_temp(rom)), "°C") # Print the temperature reading with °C after it
            
            # Publish the data to the topic!
            mqtt_client.publish(mqtt_publish_topic, str(sensor_data))
        
        # Delay a bit to avoid hitting the rate limit
        raw = turbidity_sensor.read_u16()
        sleep(1)
        volts = raw * conversion_factor
        percentage = (int(((raw - low) * 100) / (high - low)))
        str_output =  f"Raw: {raw} Voltage {volts:.1f}V  Percentage: {percentage}%"
        turbidity_sensor_data = percentage
        print(str_output)
        mqtt_client_2.publish(mqtt_publish_topic_2, str(percentage))
        sleep(3)
except Exception as e:
    print(f'Failed to publish message: {e}')
finally:
    mqtt_client.disconnect()