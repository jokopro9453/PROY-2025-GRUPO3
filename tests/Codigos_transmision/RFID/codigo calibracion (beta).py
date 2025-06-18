from machine import Pin, SPI
import time
from mfrc522 import MFRC522

# pines
sck_pin = Pin(14, Pin.OUT)   
mosi_pin = Pin(13, Pin.OUT)  
miso_pin = Pin(12, Pin.IN)   
sda_pin = Pin(15, Pin.OUT)   
rst_pin = Pin(11, Pin.OUT)   


spi = SPI(1, baudrate=100000, polarity=0, phase=0, sck=sck_pin, mosi=mosi_pin, miso=miso_pin)
rfid = MFRC522(spi, sda_pin, rst_pin)

def bytes_to_hex(uid):
    """Convierte el UID (bytes) a una cadena hexadecimal."""
    return ":".join(["{:02X}".format(byte) for byte in uid])

print("Acerca una tarjeta RFID al sensor para leer su UID...")

while True:
    try:
        
        (status, tag_type) = rfid.request(rfid.REQIDL)
        
        if status == rfid.OK:
            (status, uid) = rfid.anticoll()
            
            if status == rfid.OK:
                uid_hex = bytes_to_hex(uid)
                print(f"el UID es: {uid_hex}")
                time.sleep(1)  
    
    except Exception as e:
        print(f"no pude leer la targeta :( : {e}")
        break