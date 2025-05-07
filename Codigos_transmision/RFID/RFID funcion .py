from machine import Pin, PWM, SPI
from mfrc522 import MFRC522
import time

class RFIDController:
    def __init__(self, 
                 sck_pin=14, 
                 mosi_pin=13, 
                 miso_pin=12, 
                 sda_pin=15, 
                 rst_pin=11, 
                 led_pin=22,
                 authorized_cards=None):
        """
        Controlador RFID para integración en PROY-2025-GRUPO3
        
        Args:
            sck_pin: Pin SCK (default GPIO14)
            mosi_pin: Pin MOSI (default GPIO13)
            miso_pin: Pin MISO (default GPIO12)
            sda_pin: Pin SDA (default GPIO15)
            rst_pin: Pin RST (default GPIO11)
            led_pin: Pin LED (default GPIO22)
            authorized_cards: Lista de UIDs autorizados (en formato list[list[int]])
        """
        # Configuración hardware
        self.spi = SPI(1, baudrate=2500000, polarity=0, phase=0,
                      sck=Pin(sck_pin, Pin.OUT),
                      mosi=Pin(mosi_pin, Pin.OUT),
                      miso=Pin(miso_pin, Pin.IN))
        
        self.rfid = MFRC522(self.spi, Pin(sda_pin, Pin.OUT), Pin(rst_pin, Pin.OUT))
        self.led = PWM(Pin(led_pin, Pin.OUT))
        self.led.freq(1000)
        self.led.duty_u16(0)
        
        # Tarjetas autorizadas (ahora soporta múltiples)
        self.authorized_cards = authorized_cards or []

    def check_card(self):
        """
        Verifica si hay una tarjeta presente y si está autorizada
        
        Returns:
            tuple: (status, uid)
            - status: bool (True=autorizada, False=no autorizada)
            - uid: list[int] (UID de la tarjeta detectada)
            - None si no hay tarjeta
        """
        (status, _) = self.rfid.request(self.rfid.REQIDL)
        
        if status == self.rfid.OK:
            (status, raw_uid) = self.rfid.anticoll()
            if status == self.rfid.OK:
                uid = list(raw_uid)
                if uid in self.authorized_cards:
                    self._activate_led(True)
                    return (True, uid)
                else:
                    self._activate_led(False)
                    return (False, uid)
        return None

    def _activate_led(self, authorized):
        """Controla el LED de feedback"""
        if authorized:
            self.led.duty_u16(32768)  # 50% de intensidad
            time.sleep(1)
        else:
            # Parpadeo rápido para no autorizado
            for _ in range(3):
                self.led.duty_u16(32768)
                time.sleep(0.1)
                self.led.duty_u16(0)
                time.sleep(0.1)
        self.led.duty_u16(0)

    def add_authorized_card(self, uid):
        """Añade un nuevo UID a la lista de autorizados"""
        if uid not in self.authorized_cards:
            self.authorized_cards.append(uid)

# Ejemplo de uso (para testing)
if __name__ == "__main__":
    # Configuración compatible con el proyecto
    rfid = RFIDController(
        authorized_cards=[
            [0x12, 0x34, 0x56, 0x78],  # Ejemplo
            [0xAA, 0xBB, 0xCC, 0xDD]   # Ejemplo 2
        ]
    )
    
    print("Módulo RFID - Modo prueba")
    while True:
        result = rfid.check_card()
        if result:
            authorized, uid = result
            print(f"Tarjeta {'AUTORIZADA' if authorized else 'NO AUTORIZADA'}: {uid}")
        time.sleep(0.5)