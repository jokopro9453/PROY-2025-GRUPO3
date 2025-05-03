import socket
import wifi
from machine import Pin
wifi.connect()

led = Pin(22,Pin.OUT)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Servidor escuchando en http://%s/")

while True:
    cl, addr = s.accept()
    print('Cliente conectado desde', addr)
    request = cl.recv(1024).decode()
    print("Petición:", request)

    if "GET /led/on" in request:
        print("Encender LED")
        led.value(1)

    elif "GET /led/off" in request:
        print("Apagar LED")
        led.value(0)
    response = """\
HTTP/1.1 200 OK

¡Señal recibida!
"""
    cl.send(response)
    cl.close()