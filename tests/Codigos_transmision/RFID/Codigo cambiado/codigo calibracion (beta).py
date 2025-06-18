from machine import Pin, SPI
import time
from mfrc522 import MFRC522

# Pines
sck_pin = Pin(14, Pin.OUT)  # GP14
mosi_pin = Pin(13, Pin.OUT)  # GP13
miso_pin = Pin(12, Pin.IN)  # GP12
sda_pin = Pin(15, Pin.OUT)  # GP15
rst_pin = Pin(11, Pin.OUT)  # GP11

# Configuración del lector RFID
spi = SPI(1, baudrate=100000, polarity=0, phase=0, sck=sck_pin, mosi=mosi_pin, miso=miso_pin)
rfid = MFRC522(spi, sda_pin, rst_pin)

def bytes_to_hex(uid):
    """Convierte el UID (bytes) a una cadena hexadecimal."""
    return ":".join(["{:02X}".format(byte) for byte in uid])

def detect_card():
    """
    Detecta una tarjeta RFID y devuelve su UID en formato hexadecimal.
    """
    try:
        print("Esperando tarjeta...")
        (status, tag_type) = rfid.request(rfid.REQIDL)
        if status == rfid.OK:
            (status, uid) = rfid.anticoll()
            if status == rfid.OK:
                uid_hex = bytes_to_hex(uid)
                print(f"Tarjeta detectada con UID: {uid_hex}")
                return uid_hex
        return None
    except Exception as e:
        print(f"no pude leer la targeta :(: {e}")
        return None

def main():
    """
    Función principal para calibrar el lector RFID.
    """
    print("=== Sistema de Calibración RFID ===")
    print("Acerca una tarjeta al lector para obtener su UID.")
    print("Presiona Ctrl+C para salir.\n")

    while True:
        uid = detect_card()
        if uid:
            print(f"UID leído: {uid}")
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
    finally:
        print("Sistema apagado correctamente.")