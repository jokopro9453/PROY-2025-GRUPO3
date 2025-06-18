from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.ext import MessageHandler
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
import noise_delete as antinoise
import speechtotxt as userpass
import verificacion as encode
import os, requests, json, random, time

# Elige una palabra de la base de  datos
with open('palabras.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
palabras = data['palabras']
#Cambia la contraseña
def rpass():
    passwd = random.choice(palabras)
    return passwd


load_dotenv()
TELE_API = os.getenv("TELEGRAM_API")



# Url de la raspi
url = "http://192.168.73.32/led/on"
#url2= "http://192.168.43.32/led/off"

# Carpetas
audios = "audios"
audios_recibidos = "audios_recibidos"
os.makedirs(audios, exist_ok=True)
os.makedirs(audios_recibidos, exist_ok=True)




# Iniciar con el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    passwd = rpass()
    context.user_data['passwd'] = passwd
    await update.message.reply_text(f"¡Hola! Tu contraseña de un solo uso es >> {passwd} <<. ¡Ahora envía un mensaje de voz!")
    
# Control de auidio
async def audio_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    try:
        file_path = os.path.join(audios_recibidos, "Audio_recibido.wav")
        if os.path.exists(file_path):
            os.remove(file_path)
        file_path = os.path.join(audios_recibidos, "Audio_recibido.ogg")
        if os.path.exists(file_path):
            os.remove(file_path)

        file = await context.bot.get_file(update.message.voice.file_id)
        await file.download_to_drive(file_path)
        await update.message.reply_text("Su audio ha sido recibido.")
        antinoise.limpiar_audio()
        upass = userpass.convert_to_text()
        str1 = upass
        str2 = context.user_data.get('passwd', '')
        similitud_audio = encode.comparar_audios(file_path)
        similitud_pass = fuzz.ratio(str1,str2)
        print(fuzz.ratio(str1,str2))
        if similitud_audio > 0.69 and similitud_pass > 0.6:
            response = requests.get(url)
            if response.text != "<html><body><h1>LED: OFF</h1></body></html>":
                response = requests.get(url)
                time.sleep(1)
                if response.text != "<html><body><h1>LED: OFF</h1></body></html>":
                    response = requests.get(url)
                    time.sleep(1)
                    if response.text != "<html><body><h1>LED: OFF</h1></body></html>":
                        response = requests.get(url)
                        time.sleep(1)
                        if response.text != "<html><body><h1>LED: OFF</h1></body></html>":
                            response = requests.get(url)
                            time.sleep(1)
                            if response.text != "<html><body><h1>LED: OFF</h1></body></html>":
                                response = requests.get(url)
                                time.sleep(1)
                                if response.text != "<html><body><h1>LED: OFF</h1></body></html>":
                                    response = requests.get(url)
                                    time.sleep(1)
                                    if response.text != "<html><body><h1>LED: OFF</h1></body></html>":
                                        response = requests.get(url)
                                        time.sleep(1)
                                        if response.text != "<html><body><h1>LED: OFF</h1></body></html>":
                                            response = requests.get(url)
                                            time.sleep(1)
            print("LED encendido:", response.text)
            print("Se ha abiero la cerradura.")
            await update.message.reply_text("¡Su cerradura se ha abierto exitosamente!")

        else:
            await update.message.reply_text("Hubo un error al identificarlo, si realmente es usted, porfavor repita el proceso.")
            return None
    except Exception as e:
        print("Error al procesar el audio:", e)
        await update.message.reply_text("Error al procesar audio")

# Configuracion del bot
app = ApplicationBuilder().token(TELE_API).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VOICE, audio_bot))
app.run_polling()
#=======================================================================================================================