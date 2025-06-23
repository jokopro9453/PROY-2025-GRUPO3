import os
import time
import requests
from dotenv import load_dotenv

def convert_to_text() -> str:
    try:
        load_dotenv()
        api_key = os.getenv("ASSEMBLY_API")

        filepath = "Audios_recibidos/Audio_recibido.wav"

        with open(filepath, "rb") as f:
            headers_upload = {
                "authorization": api_key,
                "content-type": "application/octet-stream"
            }
            response = requests.post("https://api.assemblyai.com/v2/upload", headers=headers_upload, data=f)
            response.raise_for_status()
            audio_url = response.json()["upload_url"]

        headers_transcript = {
            "authorization": api_key,
            "content-type": "application/json"
        }
        json_data = {
            "audio_url": audio_url
        }
        response = requests.post("https://api.assemblyai.com/v2/transcript", headers=headers_transcript, json=json_data)
        response.raise_for_status()
        transcript_id = response.json()["id"]

        polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        while True:
            response = requests.get(polling_endpoint, headers=headers_transcript)
            response.raise_for_status()
            status = response.json()["status"]

            if status == "completed":
                print("La respuesta de el usuario fue: ",response.json()["text"])
                return response.json()["text"]
            elif status == "error":
                raise RuntimeError(f"Error en transcripción: {response.json()['error']}")
            else:
                time.sleep(3)

    except Exception as e:
        return f"Error: {e}"