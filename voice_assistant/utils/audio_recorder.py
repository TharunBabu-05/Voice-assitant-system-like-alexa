import pyaudio
import wave
import io

class AudioRecorder:
    def __init__(self, device_index=None, rate=16000, channels=1, chunk=1024):
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.device_index = device_index
        self.format = pyaudio.paInt16

    def record(self, seconds=5):
        pa = pyaudio.PyAudio()
        
        # If no device specified, find best input device
        if self.device_index is None:
            self.device_index, self.channels = self._find_best_input_device(pa)
        
        # Try multiple configurations until one works
        configurations = [
            (self.device_index, self.channels),  # Detected config
            (1, 2),  # ReSpeaker device with 2 channels
            (1, 1),  # ReSpeaker device with 1 channel
            (2, 1),  # PulseAudio with 1 channel
            (3, 1),  # Default with 1 channel
            (None, 1),  # Let PyAudio choose default
        ]
        
        for device_idx, channels in configurations:
            try:
                print(f"Trying device {device_idx} with {channels} channels...")
                self.channels = channels
                self.device_index = device_idx
                
                stream = pa.open(
                    format=self.format, 
                    channels=self.channels, 
                    rate=self.rate, 
                    input=True, 
                    frames_per_buffer=self.chunk, 
                    input_device_index=self.device_index
                )
                break  # Success! Exit the loop
            except Exception as e:
                print(f"Failed: {e}")
                continue
        else:
            # If all configurations failed
            pa.terminate()
            raise RuntimeError("Could not open any audio input device")
        
        print(f"Successfully opened device {self.device_index} with {self.channels} channels")
        print(f"Recording for {seconds} seconds...")
        frames = []
        for _ in range(0, int(self.rate / self.chunk * seconds)):
            data = stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        pa.terminate()
        audio_data = b''.join(frames)
        return audio_data

    def _find_best_input_device(self, pa):
        """Find best input device and determine its max channels"""
        # First try to find ReSpeaker or seeed device
        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            name = info['name'].lower()
            if ('seeed' in name or 'respeaker' in name) and info['maxInputChannels'] > 0:
                channels = min(info['maxInputChannels'], 2)  # Use max 2 channels
                print(f"Found ReSpeaker device: {info['name']} (Device {i}, {channels} channels)")
                return i, channels
        
        # Try pulse audio (often works well)
        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            if 'pulse' in info['name'].lower() and info['maxInputChannels'] > 0:
                channels = 1  # Use 1 channel for pulse to be safe
                print(f"Found PulseAudio device: {info['name']} (Device {i}, {channels} channels)")
                return i, channels
        
        # If no ReSpeaker found, use default input device
        default_device = pa.get_default_input_device_info()
        device_index = default_device['index']
        channels = min(default_device['maxInputChannels'], 1)  # Use 1 channel for safety
        print(f"Using default input device: {default_device['name']} (Device {device_index}, {channels} channels)")
        return device_index, channels
