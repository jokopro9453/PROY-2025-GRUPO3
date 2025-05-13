import librosa
import noisereduce as nr
import soundfile as sf

def limpiar_audio():

    noise_audio, noise_sr = librosa.load("audios_recibidos/ruidofondo.ogg", sr=None)
    input_audio, input_sr = librosa.load("audios_recibidos/Audio_recibido.ogg", sr=None)
    if noise_sr != input_sr:
        raise ValueError("Las tasas de muestreo de los audios no coinciden")

    reduced_noise = nr.reduce_noise(y=input_audio, sr=input_sr, y_noise=noise_audio)

    sf.write("audios_recibidos/Audio_recibido.wav", reduced_noise, input_sr)

    return None