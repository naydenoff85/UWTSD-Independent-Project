import network
import socket
import machine
from time import sleep


ssid = 'RaspiNET'
password = 'iv4n!sthe3b3st'


def connect():
    # Configure interface and aasign it to a variable
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Scan for available Networks
    scan_results = wlan.scan()
    
    #Connect to WLAN
    wlan.connect(ssid, password)
    sleep(5)
    
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        wlan.connect(ssid, password)
        sleep(5)

    cfgArr = wlan.ifconfig()
    ip = cfgArr[0]
    print(f'Connected on {ip}')
    for i in range(len(cfgArr)-1):
        print(cfgArr[i+1])

connect()