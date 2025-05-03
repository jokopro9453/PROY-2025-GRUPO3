from resemblyzer import preprocess_wav, VoiceEncoder
from pathlib import Path
import numpy as np
from tqdm import tqdm

def comparar_audios(carpeta_referencia: str, carpeta_objetivo: str) -> float:
    """
    Compara múltiples audios de una carpeta de referencia con múltiples audios de una carpeta objetivo
    usando embed_speaker() para ambos lados.

    Args:
        carpeta_referencia (str): Carpeta con varios audios del hablante conocido.
        carpeta_objetivo (str): Carpeta con varios audios del hablante a identificar.

    Returns:
        float: Similitud entre los embeddings de ambos hablantes.
    """

    encoder = VoiceEncoder()

    # Preprocesar audios de referencia
    print(f"\n Procesando audios de referencia desde: {carpeta_referencia}")
    ref_paths = list(Path(carpeta_referencia).glob("*.wav"))
    if not ref_paths:
        raise ValueError("No se encontraron audios en la carpeta de referencia.")
    ref_wavs = [preprocess_wav(p) for p in tqdm(ref_paths)]
    embed_ref = encoder.embed_speaker(ref_wavs)

    # Preprocesar audios objetivo
    print(f"\n Procesando audios del objetivo desde: {carpeta_objetivo}")
    obj_paths = list(Path(carpeta_objetivo).glob("*.wav"))
    if not obj_paths:
        raise ValueError("No se encontraron audios en la carpeta del objetivo.")
    obj_wavs = [preprocess_wav(p) for p in tqdm(obj_paths)]
    embed_obj = encoder.embed_speaker(obj_wavs)

    # Comparar embeddings
    similitud = np.dot(embed_ref, embed_obj)
    print("\n==============================")
    print("  Resultado de comparación")
    print("==============================")
    print(f"  Similitud speaker-to-speaker: {similitud:.4f}")
    print("==============================\n")

    return similitud