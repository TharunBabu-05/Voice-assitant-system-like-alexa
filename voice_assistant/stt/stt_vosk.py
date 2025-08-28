import json
import vosk
import wave
import tempfile
import numpy as np

class VoskSTT:
    def __init__(self, model_path="vosk-model-small-en-us-0.15"):
        self.model = vosk.Model(model_path)
        self.rec = vosk.KaldiRecognizer(self.model, 16000)

    def transcribe(self, audio_data, channels=1):
        # Save audio data to temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            with wave.open(temp_file.name, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Vosk works best with mono
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)
                
                # Convert stereo to mono if needed
                if channels == 2:
                    # Convert stereo bytes to numpy array
                    audio_np = np.frombuffer(audio_data, dtype=np.int16)
                    # Reshape to stereo (2 channels)
                    stereo = audio_np.reshape(-1, 2)
                    # Convert to mono by averaging channels
                    mono = np.mean(stereo, axis=1).astype(np.int16)
                    audio_data = mono.tobytes()
                
                wav_file.writeframes(audio_data)
            
            # Transcribe using Vosk
            with wave.open(temp_file.name, 'rb') as wav_file:
                while True:
                    data = wav_file.readframes(4000)
                    if len(data) == 0:
                        break
                    if self.rec.AcceptWaveform(data):
                        result = json.loads(self.rec.Result())
                        text = result.get('text', '')
                        if text:
                            return text
                
                final_result = json.loads(self.rec.FinalResult())
                return final_result.get('text', '')
