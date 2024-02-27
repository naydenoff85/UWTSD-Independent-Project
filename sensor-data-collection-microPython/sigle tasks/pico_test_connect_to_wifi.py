import network
import socket
import machine
from time import sleep


ssid = 'RaspiNET'
password = 'iv4n!sthe3b3st'


status_names = {
    network.STAT_CONNECTING: 'STAT_CONNECTING',   
    network.STAT_CONNECT_FAIL: 'STAT_CONNECT_FAIL',  
    network.STAT_GOT_IP: 'STAT_GOT_IP',       
    network.STAT_IDLE: 'STAT_IDLE',         
    network.STAT_NO_AP_FOUND: 'STAT_NO_AP_FOUND',  
    network.STAT_WRONG_PASSWORD: 'STAT_WRONG_PASSWORD',
    # Catch-all case for unrecognized status codes
    'default': 'UNKNOWN_STATUS'
}


def connect():
    # Configure interface and aasign it to a variable
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    scan_results = wlan.scan()
    # Print the available Networks
    print(str(scan_results))
    
    #Connect to WLAN
    wlan.connect(ssid, password)
    sleep(5)
    print(status_names[wlan.status()])
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        wlan.connect(ssid, password)
        sleep(5)
        # Print the status name
        status_code = wlan.status()
        status_name = status_names.get(status_code, status_names['default'])
        print(status_name)
    cfgArr = wlan.ifconfig()
    ip = cfgArr[0]
    for i in range(len(cfgArr)-1):
        print(cfgArr[i+1])
    print(f'Connected on {ip}') 

connect()



