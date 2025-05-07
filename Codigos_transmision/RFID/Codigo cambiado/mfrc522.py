from machine import Pin, SPI
from os import uname
import time

class MFRC522:
    """
    Controlador para el lector RFID MFRC522.

    Proporciona métodos para inicializar el lector, detectar tarjetas y realizar operaciones
    como autenticación y lectura/escritura de datos.
    """

    # Constantes de estado
    OK = 0
    NOTAGERR = 1
    ERR = 2

    # Comandos de solicitud
    REQIDL = 0x26  # Solicitar tarjetas en estado IDLE
    REQALL = 0x52  # Solicitar todas las tarjetas

    # Comandos de autenticación
    AUTHENT1A = 0x60  # Autenticación con clave A
    AUTHENT1B = 0x61  # Autenticación con clave B

    def __init__(self, sck, mosi, miso, rst, cs):
        """
        Inicializa el lector RFID MFRC522.

        Args:
            sck (Pin): Pin de reloj (SCK).
            mosi (Pin): Pin de datos MOSI.
            miso (Pin): Pin de datos MISO.
            rst (Pin): Pin de reinicio (Reset).
            cs (Pin): Pin de selección de chip (Chip Select).
        """
        self.sck = Pin(sck, Pin.OUT)
        self.mosi = Pin(mosi, Pin.OUT)
        self.miso = Pin(miso)
        self.rst = Pin(rst, Pin.OUT)
        self.cs = Pin(cs, Pin.OUT)

        self.rst.value(0)
        self.cs.value(1)
        
        board = uname()[0]

        if board == 'WiPy' or board == 'LoPy' or board == 'FiPy':
            self.spi = SPI(0)
            self.spi.init(SPI.MASTER, baudrate=1000000, pins=(self.sck, self.mosi, self.miso))
        elif board == 'esp8266' or board == 'esp32':
            self.spi = SPI(baudrate=100000, polarity=0, phase=0, sck=self.sck, mosi=self.mosi, miso=self.miso)
            self.spi.init()
        else:
            raise RuntimeError("Unsupported platform")

        self.rst.value(1)
        self.init()

    def init(self):
        """
        Inicializa el lector RFID configurando los registros necesarios.
        """
        self.reset()
        self._wreg(0x2A, 0x8D)
        self._wreg(0x2B, 0x3E)
        self._wreg(0x2D, 30)
        self._wreg(0x2C, 0)
        self._wreg(0x15, 0x40)
        self._wreg(0x11, 0x3D)
        self.antenna_on()
        print("Lector RFID inicializado correctamente.")

    def reset(self):
        """
        Reinicia el lector RFID.
        """
        self._wreg(0x01, 0x0F)

    def antenna_on(self, on=True):
        """
        Activa o desactiva la antena del lector.

        Args:
            on (bool): True para activar la antena, False para desactivarla.
        """
        if on and not (self._rreg(0x14) & 0x03):
            self._sflags(0x14, 0x03)
        else:
            self._cflags(0x14, 0x03)

    def _wreg(self, reg, val):
        """
        Escribe un valor en un registro del lector RFID.

        Args:
            reg (int): Dirección del registro.
            val (int): Valor a escribir.
        """
        self.cs.value(0)
        self.spi.write(b'%c' % int(0xff & ((reg << 1) & 0x7e)))
        self.spi.write(b'%c' % int(0xff & val))
        self.cs.value(1)

    def _rreg(self, reg):
        """
        Lee un valor de un registro del lector RFID.

        Args:
            reg (int): Dirección del registro.

        Returns:
            int: Valor leído del registro.
        """
        self.cs.value(0)
        self.spi.write(b'%c' % int(0xff & (((reg << 1) & 0x7e) | 0x80)))
        val = self.spi.read(1)[0]
        self.cs.value(1)
        return val

    def _sflags(self, reg, mask):
        """
        Establece los flags en un registro.

        Args:
            reg (int): Dirección del registro.
            mask (int): Máscara de bits a establecer.
        """
        self._wreg(reg, self._rreg(reg) | mask)

    def _cflags(self, reg, mask):
        """
        Borra los flags en un registro.

        Args:
            reg (int): Dirección del registro.
            mask (int): Máscara de bits a borrar.
        """
        self._wreg(reg, self._rreg(reg) & (~mask))

    def request(self, mode):
        """
        Envía una solicitud para detectar tarjetas.

        Args:
            mode (int): Modo de solicitud (REQIDL o REQALL).

        Returns:
            tuple: (estado, tipo de tarjeta) si se detecta una tarjeta, de lo contrario (NOTAGERR, None).
        """
        self._wreg(0x0D, 0x07)
        stat, recv, bits = self._tocard(0x0C, [mode])

        if stat != self.OK or bits != 0x10:
            stat = self.ERR

        return stat, bits

    def anticoll(self):
        """
        Realiza la operación de anticollision para obtener el UID de la tarjeta.

        Returns:
            tuple: (estado, UID) si se detecta una tarjeta, de lo contrario (NOTAGERR, None).
        """
        ser_chk = 0
        ser = [0x93, 0x20]

        self._wreg(0x0D, 0x00)
        stat, recv, bits = self._tocard(0x0C, ser)

        if stat == self.OK:
            if len(recv) == 5:
                for i in range(4):
                    ser_chk ^= recv[i]
                if ser_chk != recv[4]:
                    stat = self.ERR
            else:
                stat = self.ERR

        return stat, recv

    def select_tag(self, ser):
        """
        Selecciona una tarjeta específica usando su UID.

        Args:
            ser (list): UID de la tarjeta.

        Returns:
            int: Estado de la operación (OK o ERR).
        """
        buf = [0x93, 0x70] + ser[:5]
        buf += self._crc(buf)
        stat, recv, bits = self._tocard(0x0C, buf)
        return self.OK if stat == self.OK and bits == 0x18 else self.ERR

    def auth(self, mode, addr, sect, ser):
        """
        Autentica la tarjeta usando una clave.

        Args:
            mode (int): Modo de autenticación (AUTHENT1A o AUTHENT1B).
            addr (int): Dirección del sector.
            sect (list): Número del sector.
            ser (list): Clave de autenticación.

        Returns:
            int: Estado de la autenticación.
        """
        return self._tocard(0x0E, [mode, addr] + sect + ser[:4])[0]

    def stop_crypto1(self):
        """
        Detiene el proceso de criptografía.
        """
        self._cflags(0x08, 0x08)

    def read(self, addr):
        """
        Lee datos de una tarjeta.

        Args:
            addr (int): Dirección donde comenzar la lectura.

        Returns:
            list: Datos leídos o None en caso de error.
        """
        data = [0x30, addr]
        data += self._crc(data)
        stat, recv, _ = self._tocard(0x0C, data)
        return recv if stat == self.OK else None

    def write(self, addr, data):
        """
        Escribe datos en una tarjeta.

        Args:
            addr (int): Dirección donde comenzar la escritura.
            data (list): Datos a escribir.

        Returns:
            int: Estado de la operación (OK o ERR).
        """
        buf = [0xA0, addr]
        buf += self._crc(buf)
        stat, recv, bits = self._tocard(0x0C, buf)

        if not (stat == self.OK and bits == 4 and (recv[0] & 0x0F) == 0x0A):
            return self.ERR

        buf = []
        for i in range(16):
            buf.append(data[i])
        buf += self._crc(buf)
        stat, recv, bits = self._tocard(0x0C, buf)

        if not (stat == self.OK and bits == 4 and (recv[0] & 0x0F) == 0x0A):
            return self.ERR

        return self.OK

    def _tocard(self, cmd, send):
        """
        Envía un comando a la tarjeta y recibe la respuesta.

        Args:
            cmd (int): Comando a enviar.
            send (list): Datos a enviar.

        Returns:
            tuple: (estado, datos recibidos, bits recibidos).
        """
        recv = []
        bits = irq_en = wait_irq = n = 0
        stat = self.ERR

        if cmd == 0x0E:
            irq_en = 0x12
            wait_irq = 0x10
        elif cmd == 0x0C:
            irq_en = 0x77
            wait_irq = 0x30

        self._wreg(0x02, irq_en | 0x80)
        self._cflags(0x04, 0x80)
        self._sflags(0x0A, 0x80)
        self._wreg(0x01, 0x00)

        for c in send:
            self._wreg(0x09, c)
        self._wreg(0x01, cmd)

        if cmd == 0x0C:
            self._sflags(0x0D, 0x80)

        i = 2000
        while True:
            n = self._rreg(0x04)
            i -= 1
            if not ((i != 0) and not (n & 0x01) and not (n & wait_irq)):
                break

        self._cflags(0x0D, 0x80)

        if i:
            if (self._rreg(0x06) & 0x1B) == 0x00:
                stat = self.OK

                if n & irq_en & 0x01:
                    stat = self.NOTAGERR
                elif cmd == 0x0C:
                    n = self._rreg(0x0A)
                    lbits = self._rreg(0x0C) & 0x07
                    if lbits != 0:
                        bits = (n - 1) * 8 + lbits
                    else:
                        bits = n * 8

                    if n == 0:
                        n = 1
                    elif n > 16:
                        n = 16

                    for _ in range(n):
                        recv.append(self._rreg(0x09))
            else:
                stat = self.ERR
        else:
            stat = self.ERR

        return stat, recv, bits

    def _crc(self, data):
        """
        Calcula el CRC de los datos.

        Args:
            data (list): Datos para los cuales calcular el CRC.

        Returns:
            list: Valor del CRC.
        """
        self._cflags(0x05, 0x04)
        self._sflags(0x0A, 0x80)

        for c in data:
            self._wreg(0x09, c)

        self._wreg(0x01, 0x03)

        i = 0xFF
        while True:
            n = self._rreg(0x05)
            i -= 1
            if not ((i != 0) and not (n & 0x04)):
                break

        return [self._rreg(0x22), self._rreg(0x21)]
