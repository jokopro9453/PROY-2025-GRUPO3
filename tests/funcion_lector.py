from machine import Pin
from mfrc522 import MFRC522
import time


cerradura = Pin(13, Pin.OUT)
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

            if identificador == TARJETA:
                print("UID: " + str(identificador) + " Acceso concedido")
                cerradura.value(1)
                time.sleep(5)
                cerradura.value(0)

            elif identificador == LLAVERO:
                print("UID: " + str(identificador) + " Acceso concedido")
                cerradura.value(1)
                time.sleep(5)
                cerradura.value(0)

            else:
                print("UID: " + str(identificador) + " desconocido: Acceso denegado")
                cerradura.value(0)
