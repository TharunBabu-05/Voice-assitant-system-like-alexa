from google.cloud import speech
import io

class GoogleSTT:
    def __init__(self, credentials_path):
        self.client = speech.SpeechClient.from_service_account_file(credentials_path)

    def transcribe(self, audio_data, sample_rate=16000):
        audio = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code="en-US"
        )
        response = self.client.recognize(config=config, audio=audio)
        for result in response.results:
            return result.alternatives[0].transcript
        return ""
