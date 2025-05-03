from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.ext import MessageHandler
from dotenv import load_dotenv
import verificacion as encode
import os
import requests
import json
import random

load_dotenv()
TELE_API = os.getenv("TELEGRAM_API")

# Elige una palabra de la base de datos
with open('palabras.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
palabras = data['palabras']
passwd = random.choice(palabras)

# Url de la raspi
url = "http://192.168.45.32/led/on"

# Carpetas
audios_prueba = "audios_prueba"
audios_recibidos = "audios_recibidos"
os.makedirs(audios_prueba, exist_ok=True)
os.makedirs(audios_recibidos, exist_ok=True)

# Iniciar con el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"¡Hola! Tu contraseña de un solo uso es >> {passwd} <<. ¡Ahora envía un mensaje de voz!")

# Control de auidio
async def audio_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    try:
        file_path = os.path.join(audios_recibidos, "Audio_recibido.wav")
        if os.path.exists(file_path):
            os.remove(file_path)

        file = await context.bot.get_file(update.message.voice.file_id)
        await file.download_to_drive(file_path)
        await update.message.reply_text("Su audio ha sido recibido, muchas gracias culón 😘💓")

        similitud = encode.comparar_audios(audios_prueba, audios_recibidos)
        if similitud > 0.7:
            response = requests.get(url)
            print("LED encendido:", response.text)

    except Exception as e:
        print("Error al procesar el audio:", e)
        await update.message.reply_text("Error al procesar audio")

# Configuracion del bot
app = ApplicationBuilder().token(TELE_API).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VOICE, audio_bot))
app.run_polling()
#=======================================================================================================================