import pvporcupine
import pyaudio
import struct

class WakeWordDetector:
    def __init__(self, keyword_path):
        self.porcupine = pvporcupine.create(keyword_paths=[keyword_path])
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
