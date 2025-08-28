import requests
import config

class WhisperSTT:
    def __init__(self, api_key):
        self.api_key = api_key

    def transcribe(self, audio_data):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        files = {"file": ("audio.wav", audio_data, "audio/wav")}
        data = {"model": "whisper-1"}
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers=headers,
            data=data,
            files=files
        )
        if response.ok:
            return response.json().get("text", "")
        return ""
