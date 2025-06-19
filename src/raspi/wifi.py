import network
import utime
from machine import Pin
ssid = 'Tu SSID'
password = 'Tu PASS'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        utime.sleep(1)
    print(wlan.ifconfig())

connect()
