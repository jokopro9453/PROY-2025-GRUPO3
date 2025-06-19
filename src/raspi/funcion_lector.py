from machine import Pin
from mfrc522 import MFRC522
import time

lector = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)

TARJETA = 2014413788
LLAVERO = 805714588

def verificar_rfid():
    lector.init()
    (stat, tag_type) = lector.request(lector.REQIDL)
    
    if stat == lector.OK:
        (stat, uid) = lector.SelectTagSN()
        if stat == lector.OK:
            identificador = int.from_bytes(bytes(uid), "little", False)
            return identificador