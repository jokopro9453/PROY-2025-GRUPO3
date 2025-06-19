import socket
import wifi
from machine import Pin
import funcion_lector as lector
import asyncio
import time

wifi.connect()

# Verifica que estos pines sean correctos para tu placa
led = Pin(13, Pin.OUT)
cerradura = Pin(12, Pin.OUT)
TARJETA = 582725291
LLAVERO = 805714588

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setblocking(False)
s.bind(addr)
s.listen(1)

print("Servidor escuchando en http://0.0.0.0:80")

async def rfid_get():
    while True:
        identificador = lector.verificar_rfid()
        if identificador in [TARJETA, LLAVERO]:
            print("Acceso concedido")
            led.value(1)
            await asyncio.sleep(5)
            led.value(0)
        await asyncio.sleep(0.1)

async def web():
    while True:
        try:
            cl, addr = s.accept()
            print('Cliente conectado desde', addr)
            cl.setblocking(False)
            
            request = b''
            start_time = time.time()
            timeout = 1.0  # 1 segundo de timeout
            
            # Bucle de recepción de datos con timeout
            while time.time() - start_time < timeout:
                try:
                    chunk = cl.recv(128)  # Lee en bloques pequeños
                    if chunk:
                        request += chunk
                        # Si recibimos el fin de petición HTTP (CRLFx2)
                        if b'\r\n\r\n' in request:
                            break
                    else:
                        await asyncio.sleep(0.01)
                except OSError as e:
                    if e.errno == 11:  # EAGAIN/EWOULDBLOCK
                        await asyncio.sleep(0.01)
                        continue
                    else:
                        raise
            
            if request:
                request_str = request.decode('utf-8')
                print("Solicitud recibida:", request_str.strip())
                
                if "GET /led/on" in request_str:
                    print("Encender LED")
                    led.value(1)
                    await asyncio.sleep(5)
                    led.value(0)
                elif "GET /led/off" in request_str:
                    print("Apagar LED")
                    led.value(0)
                
                # Construye respuesta HTTP
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    "Connection: close\r\n\r\n"
                    f"<html><body><h1>LED: {'ON' if led.value() else 'OFF'}</h1></body></html>"
                )
                
                try:
                    await cl.sendall(response.encode())
                except OSError as e:
                    print("Error enviando respuesta:", e)
            else:
                print("Timeout: No se recibieron datos")
                try:
                    cl.sendall("HTTP/1.1 408 Request Timeout\r\n\r\n".encode())
                except OSError:
                    pass
            
        except Exception as e:
            pass
        finally:
            try:
                cl.close()
            except:
                pass
            await asyncio.sleep(0.1)

async def main():
    await asyncio.gather(rfid_get(), web())

asyncio.run(main())
