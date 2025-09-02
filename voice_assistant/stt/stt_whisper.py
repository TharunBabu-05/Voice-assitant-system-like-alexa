import whisper
import numpy as np
import tempfile
import os
import soundfile as sf

class WhisperSTT:
    def __init__(self, model_size="base"):
        """
        Initialize Whisper STT with local model
        
        Args:
            model_size (str): Size of Whisper model to use.
                             Options: tiny, base, small, medium, large
                             tiny is fastest but less accurate
                             base is a good balance
        """
        self.model_size = model_size
        print(f"🔄 Loading Whisper model '{model_size}'...")
        try:
            self.model = whisper.load_model(model_size)
            print(f"✅ Whisper model '{model_size}' loaded successfully!")
        except Exception as e:
            print(f"❌ Failed to load Whisper model: {e}")
            print("💡 Trying to download model...")
            try:
                self.model = whisper.load_model(model_size, download_root=None)
                print(f"✅ Whisper model '{model_size}' downloaded and loaded!")
            except Exception as e2:
                print(f"❌ Failed to download Whisper model: {e2}")
                # Fallback to tiny model if requested model fails
                if model_size != "tiny":
                    print("🔄 Trying tiny model as fallback...")
                    self.model = whisper.load_model("tiny")
                    self.model_size = "tiny"
                else:
                    raise

    def transcribe(self, audio_data, channels=1):
        """
        Transcribe audio data using local Whisper model
        
        Args:
            audio_data (bytes): Raw audio data
            channels (int): Number of audio channels (1 or 2)
            
        Returns:
            str: Transcribed text
        """
        try:
            # Convert bytes to numpy array
            if isinstance(audio_data, bytes):
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
            else:
                audio_array = audio_data
            
            # Handle multichannel audio by converting to mono
            if channels == 2 and len(audio_array) > 0:
                # Reshape to 2D array (samples, channels) and take mean
                audio_array = audio_array.reshape(-1, 2)
                audio_array = np.mean(audio_array, axis=1).astype(np.int16)
            
            # Convert to float32 and normalize to [-1, 1] range as required by Whisper
            audio_float = audio_array.astype(np.float32) / 32768.0
            
            # Create temporary WAV file for Whisper processing
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_filename = temp_file.name
            
            try:
                # Save audio as WAV file with 16kHz sample rate (Whisper's expected rate)
                sf.write(temp_filename, audio_float, 16000, format='WAV')
                
                # Transcribe using Whisper
                print("🎯 Transcribing with Whisper...")
                result = self.model.transcribe(
                    temp_filename,
                    language="en",  # Force English for better accuracy
                    task="transcribe",
                    fp16=False,  # Use fp32 for better compatibility on Pi
                    verbose=False  # Reduce output noise
                )
                
                text = result["text"].strip()
                
                if text:
                    print(f"✅ Whisper transcription: '{text}'")
                    return text
                else:
                    print("⚠️ Whisper returned empty transcription")
                    return ""
                    
            except Exception as e:
                print(f"❌ Whisper transcription failed: {e}")
                return ""
            finally:
                # Clean up temporary file
                if os.path.exists(temp_filename):
                    os.unlink(temp_filename)
                    
        except Exception as e:
            print(f"❌ Audio preprocessing failed: {e}")
            return ""

    def transcribe_audio_array(self, audio_array, sample_rate=16000):
        """
        Alternative method to transcribe directly from numpy array
        """
        try:
            # Ensure audio is float32 and normalized
            if audio_array.dtype != np.float32:
                audio_array = audio_array.astype(np.float32) / 32768.0
            
            # Ensure sample rate is 16kHz (Whisper's expected rate)
            if sample_rate != 16000:
                print(f"⚠️ Warning: Sample rate is {sample_rate}Hz, Whisper expects 16kHz")
            
            # Transcribe directly (more efficient, no file I/O)
            result = self.model.transcribe(
                audio_array,
                language="en",
                task="transcribe", 
                fp16=False,
                verbose=False
            )
            
            return result["text"].strip()
            
        except Exception as e:
            print(f"❌ Whisper direct transcription error: {e}")
            return ""

    def is_available(self):
        """Check if Whisper model is loaded and available"""
        return hasattr(self, 'model') and self.model is not None

    def get_model_info(self):
        """Get information about the loaded model"""
        if self.is_available():
            return {
                "model_size": self.model_size,
                "status": "loaded",
                "type": "local_whisper"
            }
        else:
            return {
                "model_size": self.model_size,
                "status": "not_loaded",
                "type": "local_whisper"
            }
