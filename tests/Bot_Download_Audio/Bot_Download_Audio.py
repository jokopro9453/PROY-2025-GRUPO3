from telegram import Update 
from telegram.ext import ApplicationBuilder, filters, ContextTypes
from telegram.ext import MessageHandler
import os
audios_prueba= "audios_recibidos"
os.makedirs(audios_prueba, exist_ok=True)#asegura que exista la carpeta
async def audio_bot (update: Update, context: ContextTypes.DEFAULT_TYPE):
    file= await context.bot.get_file(update.message.voice.file_id)
    file_path= os.path.join(audios_prueba, f"{update.message.voice.file_id}.ogg")#ruta completa donde guardar el archivo
    await file.download_to_drive(file_path)#descarga el archivo a esta ruta
    await update.message.reply_text("Audio prueba recibido")
app= ApplicationBuilder().token("AQUI VA TU TOKEN").build()
app.add_handler(MessageHandler(filters.VOICE, audio_bot))
app.run_polling()
