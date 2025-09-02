import whisper
import numpy as np
import tempfile
import os
import soundfile as sf

class WhisperSTT:
    def __init__(self, model_size="base"):
        """
        Initialize Whisper STT with specified model size
        Model sizes: tiny, base, small, medium, large
        For Raspberry Pi, recommend: tiny (fastest) or base (good balance)
        """
        print(f"🎤 Loading Whisper {model_size} model...")
        try:
            self.model = whisper.load_model(model_size)
            print(f"✅ Whisper {model_size} model loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load Whisper model: {e}")
            # Fallback to tiny model if requested model fails
            if model_size != "tiny":
                print("🔄 Trying tiny model as fallback...")
                self.model = whisper.load_model("tiny")
            else:
                raise e
    
    def transcribe(self, audio_data, channels=1):
        """
        Transcribe audio data using Whisper
        
        Args:
            audio_data: Raw audio bytes from AudioRecorder
            channels: Number of audio channels (1 for mono, 2 for stereo)
        
        Returns:
            str: Transcribed text
        """
        try:
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
            
            # Convert bytes to numpy array
            if isinstance(audio_data, bytes):
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
            else:
                audio_array = audio_data
            
            # Convert to float32 and normalize (Whisper expects float32 between -1 and 1)
            audio_float = audio_array.astype(np.float32) / 32768.0
            
            # Handle stereo to mono conversion if needed
            if channels == 2 and len(audio_float) > 0:
                audio_float = audio_float.reshape(-1, 2)
                audio_float = np.mean(audio_float, axis=1)  # Convert to mono
            
            # Save as WAV file for Whisper
            sf.write(temp_filename, audio_float, 16000)
            
            # Transcribe using Whisper
            result = self.model.transcribe(
                temp_filename,
                language="en",  # Force English for better performance
                task="transcribe",
                fp16=False,  # Use fp32 for better compatibility on RPi
                verbose=False
            )
            
            # Extract text
            text = result["text"].strip()
            
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            
            return text
            
        except Exception as e:
            print(f"❌ Whisper transcription error: {e}")
            # Clean up on error
            if 'temp_filename' in locals() and os.path.exists(temp_filename):
                os.unlink(temp_filename)
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
