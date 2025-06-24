# PROY-2025-GRUPO3

Repositorio del grupo 3 para el proyecto del ramo *Proyecto Inicial* – 2025.
---

## 👥 Integrantes del grupo

| Nombre y Apellido | Usuario GitHub | Correo USM               | Rol          |
| ----------------- | -------------- | ------------------------ | ------------ |
| Joaqun Carey      | @jokopro9453   | jcarey@usm.cl            | 202530002-8  |
| Samuel Pinto      | @SamuelP-27    | spintom@usm.cl           | 202530021-4  |
| Felipe Hinrichsen | @mitrono24     | fhinrichsen@usm.cl       | 202530007-9  |
| Vicente Venegas   | @vichous       | vvenegas@usm.cl          | 202530011-7  |

---

## 📝 Descripción del proyecto

*V-Lock es un innovador conjunto de herramientas para desarrolladores que integra reconocimiento de voz, reducción de ruido y control de dispositivos IoT (Internet of things) para la creación de sistemas seguros activados por voz. Este sistema integra diversas funciones, como el procesamiento de voz, la verificación de hablantes nativos y la gestión de dispositivos inalámbricos, en una única plataforma cohesiva diseñada para soluciones de seguridad inteligentes.*

### ¿Por que V-Lock?

Este proyecto apunta a agilizar el desarrollo de aplicaciones de seguridad y automatización basadas en la voz. Entre sus características más notables, cabe destacar las siguientes:

- Verificación por voz: se implementa un proceso riguroso de identificación y autenticación del hablante para garantizar la seguridad del acceso.
- Reducción de ruido: se implementan técnicas de limpieza de audio para garantizar la claridad de los comandos de voz en entornos ruidosos.
- Transcripción voz a texto: sistema de transcripción automatizada para una interacción de voz fluida y eficiente.
- Integración de hardware: Fácil control de dispositivos IoT como una Raspberry pi pico w para la gestión remota de dispositivos
- Lector RFID: se instala un sensor RFID al dispositivo para garantizar su funcionamiento sin conexión a internet.
- Arquitectura modular: Componentes escalables diseñados para una implementación y personalización flexibles.

---

## 🎯 Objetivos

- Objetivo general:
 El objetivo principal del proyecto es innovar en la seguridad física de pertenencias aplicando una mejora tecnológica a los sistemas convencionales, logrando un aumento en su efectividad.
- Objetivos específicos:
  - Conexión de raspberry pi pico w 2 a wifi
  - Creación del circuito
  - Creación de programa para detectar y descargar audios para el reconocimiento
  - Conexión y calibración de sensores
  - Unión de las áreas del proyecto
---

## 🧩 Alcance del proyecto

V-Lock constituye una solución de protección adicional para una amplia gama de entornos, adaptándose a las necesidades específicas de cada situación, como la apertura de puertas o portones. Dentro de los principales inconvenientes que se plantean entra la alimentación de electricidad al sistema, la cual puede complicarse en algunos contextos, y la necesidad de disponer de una red wifi y un dispositivo con acceso a Telegram para garantizar su funcionamiento, cosa que solucionamos con la implementación de un lector RFID.

---

## 🛠️ Tecnologías y herramientas utilizadas

- Lenguaje(s) de programación:
  - Python, Micropython
- Microcontroladores:
  - Raspberry Pi Pico W 2
- Sensores:
  - RFID-RC522

---

## 🗂️ Estructura del repositorio

```
/PROY-2025-GRUPOX
│
├── docs/               # Documentación general y reportes
├── src/                # Código fuente del proyecto
├── tests/              # Casos de prueba
└── README.md           # Este archivo
```
---

## ⚙ Instalación Raspberry pi pico w 2


#### Paso 1: Recrear el circuito de la Raspberry pi pico w 2

*El Circuito se encuentra en la siguiente foto:*

![Diagrama del circuito](/docs/Diagrama_circuito.jpeg)

[Mas información del circuito](/docs/Circuito%20y%20conexiones.pdf)

*Con resistencia a convenir nos referimos al lugar donde va conectado el dispositivo que recibe la señal eléctrica, en el caso de ejemplo, usamos un diodo LED*

#### Paso 2: Conectar la Raspberry al puerto USB

#### Paso 3: [Descarga Thonny](https://thonny.org/) 

#### Paso 5: Configura Thonny a tu Raspberry

[Guia de configuración](https://core-electronics.com.au/guides/how-to-setup-a-raspberry-pi-pico-and-code-with-thonny/)


*El archivo de firmware lo encontraras:* [aqui](https://github.com/jokopro9453/PROY-2025-GRUPO3/blob/main/src/raspi/mp_firmware_unofficial_latest.uf2)

#### Paso 6: Carga los archivos de src/raspi/ a la Raspberry

[Aqui los archivos](https://github.com/jokopro9453/PROY-2025-GRUPO3/tree/main/src/raspi)

#### Paso 7: Configura tus credenciales de wifi

#### Paso 8: Inicia la ejecución del codigo

---

## 🔧 Instalación Servidor Host

#### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/jokopro9453/PROY-2025-GRUPO3
cd PROY-2025-GRUPO3
```

#### Paso 2: Crear entorno virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

#### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

#### Paso 4: Configurar variables de entorno

```bash
cd src
cp .env.example .env
```

*Aquí debes ingresar los tokens de API necesarios(Bot Telegram, Assembly)*

#### Paso 5: Configura la ip de la Raspberry en main.py

#### Paso 6: Ejecutar la aplicación

```bash
python main.py
```
---

## 🧪 Metodología

 La metodología de este proyecto se basa en la división de tareas por área para un progreso eficiente, para lograr las diferentes metas que finalmente arman el proyecto completo, todo esto siguiendo los tiempos y las tareas asignadas en la carta Gantt. 

---

## 📅 Cronograma de trabajo

[Carta Gantt](https://github.com/jokopro9453/PROY-2025-GRUPO3/blob/f0c69187953bafe6986e80a4990b6b98f9f3f9c5/docs/Carta_Gantt.xlsx)
---

## 📚 Bibliografía

ComputadorasySensores. (s.f.). *Capitulo70* [Repositorio en GitHub](https://github.com/ComputadorasySensores/Capitulo70)

Carglglz. (s.f.). *NFC_PN532_SPI* [Repositorio en GitHub](https://github.com/Carglglz/NFC_PN532_SPI)

## 📺 Video de presentación V-Lock

[Aquí el video](https://youtube.com/shorts/LS934KOGzr0)