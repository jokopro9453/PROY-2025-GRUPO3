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
        Controlador RFID para integración en PROY-2025-GRUPO3.

        Args:
            sck_pin: Pin SCK del SPI (default GPIO14)
            mosi_pin: Pin MOSI del SPI (default GPIO13)
            miso_pin: Pin MISO del SPI (default GPIO12)
            sda_pin: Pin SDA del lector RFID (default GPIO15)
            rst_pin: Pin RST del lector RFID (default GPIO11)
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

    def _bytes_to_hex(self, uid):
        """Convierte el UID (bytes) a una cadena hexadecimal."""
        return ":".join(["{:02X}".format(byte) for byte in uid])

    def _detect_card(self):
        """
        Detecta una tarjeta RFID y devuelve su UID si se encuentra.

        Returns:
            tuple: (bool, UID) si se detecta una tarjeta, None si no se detecta.
        """
        try:
            (status, tag_type) = self.rfid.request(self.rfid.REQIDL)
            if status == self.rfid.OK:
                (status, uid) = self.rfid.anticoll()
                if status == self.rfid.OK:
                    return (True, uid)
            return (False, None)
        except Exception as e:
            print(f"Error al detectar tarjeta: {e}")
            return (False, None)

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

    def run(self):
        """
        Ejecuta el controlador RFID en un bucle infinito.
        """
        print("Sistema RFID iniciado. Acerca una tarjeta...")
        try:
            while True:
                detected, uid = self._detect_card()
                if detected:
                    uid_hex = self._bytes_to_hex(uid)
                    print(f"Tarjeta detectada con UID: {uid_hex}")
                    authorized = uid in self.authorized_cards
                    if authorized:
                        print("✅ Acceso autorizado")
                    else:
                        print("❌ Acceso denegado")
                    self._activate_led(authorized)
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nPrograma interrumpido por el usuario.")
        finally:
            self.led.duty_u16(0)
            self.led.deinit()
            print("Sistema apagado correctamente.")

# Uso del controlador RFID
if __name__ == "__main__":
    authorized_cards = [[0x12, 0x34, 0x56, 0x78]]  # Reemplaza con los UIDs autorizados
    rfid_controller = RFIDController(authorized_cards=authorized_cards)
    rfid_controller.run()