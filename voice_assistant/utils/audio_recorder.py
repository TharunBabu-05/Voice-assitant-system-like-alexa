import pyaudio
import wave
import io

class AudioRecorder:
    def __init__(self, device_index=0, rate=16000, channels=1, chunk=1024):
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.device_index = device_index
        self.format = pyaudio.paInt16

    def record(self, seconds=5):
        pa = pyaudio.PyAudio()
        stream = pa.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk, input_device_index=self.device_index)
        frames = []
        for _ in range(0, int(self.rate / self.chunk * seconds)):
            data = stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        pa.terminate()
        audio_data = b''.join(frames)
        return audio_data
