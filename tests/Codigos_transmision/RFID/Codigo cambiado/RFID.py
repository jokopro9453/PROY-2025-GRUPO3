from machine import Pin, PWM, SPI
from mfrc522 import MFRC522
import time

# Pines
sck_pin = Pin(14, Pin.OUT)  # GP14, PIN 19
mosi_pin = Pin(13, Pin.OUT)  # GP13, PIN 17 RX
miso_pin = Pin(12, Pin.IN)  # GP12, PIN 16 TX
sda_pin = Pin(15, Pin.OUT)  # GP15, PIN 20
rst_pin = Pin(11, Pin.OUT)  # GP11, PIN 15

# Configuración del lector RFID
spi = SPI(1, baudrate=2500000, polarity=0, phase=0, sck=sck_pin, mosi=mosi_pin, miso=miso_pin)
rfid = MFRC522(spi, sda_pin, rst_pin)

# Configuración de PWM para el LED
led_pwm = PWM(Pin(22, Pin.OUT))
led_pwm.freq(1000)
led_pwm.duty_u16(0)

# UID de la tarjeta autorizada (reemplaza con el UID real de tu tarjeta)
AUTHORIZED_CARD = [0x12, 0x34, 0x56, 0x78]  # Reemplaza con tu UID real

def main():
    print("Sistema de candado inteligente iniciado")
    print("Acerca una tarjeta RFID al lector...")

    while True:
        try:
            # Detectar tarjeta
            (status, tag_type) = rfid.request(rfid.REQIDL)
            if status == rfid.OK:
                (status, uid) = rfid.anticoll()
                if status == rfid.OK:
                    print(f"Tarjeta detectada con UID: {uid}")
                    
                    # Verificar si el UID coincide con la tarjeta autorizada
                    if uid == AUTHORIZED_CARD:
                        print("✅ Acceso autorizado")
                        led_pwm.duty_u16(32768)  # Enciende el LED al 50% de brillo
                        time.sleep(1)
                        led_pwm.duty_u16(0)  # Apaga el LED
                    else:
                        print("❌ Acceso denegado")
                        led_pwm.duty_u16(65535)  # Enciende el LED al 100% de brillo
                        time.sleep(1)
                        led_pwm.duty_u16(0)  # Apaga el LED
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario.")
    finally:
        led_pwm.duty_u16(0)  # Apaga el LED al finalizar
        led_pwm.deinit()
        print("Sistema apagado correctamente.")