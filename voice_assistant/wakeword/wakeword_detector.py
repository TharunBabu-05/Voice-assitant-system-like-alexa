
import pvporcupine
import pyaudio
import struct
import config

class WakeWordDetector:
    def __init__(self, keyword_path):
        self.porcupine = pvporcupine.create(
            access_key=config.PORCUPINE_ACCESS_KEY,
            keyword_paths=[keyword_path]
        )
<<<<<<< HEAD
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def detect(self):
        print('Listening for wake word...')
        while True:
            pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            result = self.porcupine.process(pcm)
            if result >= 0:
                return True
=======
        self.pa = None
        self.stream = None

    def detect(self):
        print('Listening for wake word...')
        
        # Initialize audio for wake word detection
        if self.pa is None:
            self.pa = pyaudio.PyAudio()
        
        try:
            # Try to use default device to avoid conflicts with ReSpeaker
            self.stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length,
                input_device_index=None  # Use default device
            )
            
            while True:
                pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                result = self.porcupine.process(pcm)
                if result >= 0:
                    # Clean up audio resources immediately after detection
                    self.stream.stop_stream()
                    self.stream.close()
                    self.stream = None
                    return True
                    
        except Exception as e:
            print(f"Wake word detection error: {e}")
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            return False

    def cleanup(self):
        """Clean up audio resources"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        if self.pa:
            self.pa.terminate()
            self.pa = None
        if self.porcupine:
            self.porcupine.delete()
            self.porcupine = None
>>>>>>> master
