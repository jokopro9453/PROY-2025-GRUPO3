from machine import Pin, PWM, SPI
from mfrc522 import MFRC522
import time

# pines
sck_pin = Pin(14, Pin.OUT)  # GP14, PIN 19
mosi_pin = Pin(13, Pin.OUT) # GP13, PIN 17 RX
miso_pin = Pin(12, Pin.IN)  # GP12, PIN 16 TX
sda_pin = Pin(15, Pin.OUT)  # GP15, PIN 20
rst_pin = Pin(11, Pin.OUT)  # GP11, PIN 15

#  lector RFID
spi = SPI(1, baudrate=2500000, polarity=0, phase=0, sck=sck_pin, mosi=mosi_pin, miso=miso_pin)
rfid = MFRC522(spi, sda_pin, rst_pin)

# Configuración de PWM 
led_pwm = PWM(Pin(22, Pin.OUT))
led_pwm.freq(1000)  
led_pwm.duty_u16(0)  

# UID de la tarjeta autorizada (debes reemplazarlo con uid de la tarjeta que lo puede sver con la calibracion que subi)
# Ejemplo: [0x12, 0x34, 0x56, 0x78]
AUTHORIZED_CARD = [0x12, 0x34, 0x56, 0x78]  # Reemplaza con tu UID real

def main():
    print("Sistema de candado inteligente iniciado")
    print("Acerca una tarjeta RFID al lector...")
    
    while True:
        (status, tag_type) = rfid.request(rfid.REQIDL)
        
        if status == rfid.OK:
            (status, raw_uid) = rfid.anticoll()
            
            if status == rfid.OK:
                uid = list(raw_uid)
                print(f"Tarjeta detectada - UID: {uid}")
                
                if uid == AUTHORIZED_CARD:
                    print("Tarjeta autorizada - Activando LED")
                    led_pwm.duty_u16(32768)  
                    time.sleep(3)  
                    led_pwm.duty_u16(0)  
                else:
                    print("Tarjeta no autorizada")
                    
        time.sleep(0.1)  

if __name__ == "__main__":
    main()