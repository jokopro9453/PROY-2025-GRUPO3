import network
import utime
from machine import Pin
led = Pin(22,Pin.OUT)
ssid = 'Interne'
password = '22222222'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        utime.sleep(1)
    print(wlan.ifconfig())
    while(True):
        led.value(1)
        utime.sleep(1)
        led.value(0)
        utime.sleep(1)

connect()