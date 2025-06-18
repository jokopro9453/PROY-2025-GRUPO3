from pathlib import Path
from resemblyzer import preprocess_wav, VoiceEncoder
import numpy as np

def comparar_audios(target_audio, folder_audios="audios_verificacion"):
    carpeta_audios = Path(folder_audios)
    # Validar existencia de la carpeta principal
    if not carpeta_audios.exists() or not carpeta_audios.is_dir():
        raise FileNotFoundError(f"La carpeta '{folder_audios}' no existe o no es un directorio")
    
    # Obtener subcarpetas dentro de 'audios'
    subcarpetas = [carp for carp in carpeta_audios.iterdir() if carp.is_dir()]
    if not subcarpetas:
        raise FileNotFoundError(f"No se encontraron subcarpetas en '{folder_audios}'")

    # Procesar el audio objetivo
    try:
        wav_target = preprocess_wav(target_audio)
    except Exception as e:
        raise RuntimeError(f"Error al procesar el audio objetivo: {e}")
    encoder = VoiceEncoder()
    try:
        emb_target = encoder.embed_utterance(wav_target)
    except Exception as e:
        raise RuntimeError(f"Error al generar embedding del audio objetivo: {e}")
    
    mayor_sim = None
    # Extensiones de archivos de audio a considerar
    exts = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac", ".wma"}
    
    # Iterar por cada subcarpeta
    for carpeta in subcarpetas:
        # Listar archivos de audio válidos en la carpeta
        audios = [f for f in carpeta.iterdir() 
                  if f.is_file() and f.suffix.lower() in exts]
        if not audios:
            raise FileNotFoundError(f"No hay archivos de audio válidos en la carpeta '{carpeta.name}'")
        
        similitudes = []
        for audio_path in audios:
            try:
                wav = preprocess_wav(audio_path)
                emb = encoder.embed_utterance(wav)
            except Exception:
                # Saltar archivos que no se puedan procesar
                continue
            # Similaridad = producto punto (vectores normalizados)
            sim = float(np.dot(emb_target, emb))
            similitudes.append(sim)
        
        if not similitudes:
            raise RuntimeError(f"Ningún archivo procesable en la carpeta '{carpeta.name}'")
        # Promedio de similitudes en la carpeta
        promedio = sum(similitudes) / len(similitudes)
        # Actualizar la mayor similitud encontrada
        if (mayor_sim is None) or (promedio > mayor_sim):
            mayor_sim = promedio
            print("El resultado de la comparacion de audios es :", round(mayor_sim,3))
    
    if mayor_sim is None:
        raise RuntimeError("No se pudo calcular ninguna similitud")
    # Devolver valor redondeado a 3 decimales
    return round(mayor_sim, 3)