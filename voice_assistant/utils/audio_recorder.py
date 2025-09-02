import pyaudio
import wave
import io
import subprocess
import tempfile
import os
import numpy as np

class AudioRecorder:
    def __init__(self, device_index=None, rate=16000, channels=1, chunk=1024):
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.device_index = device_index
        self.actual_channels = channels  # Track actual channels used in recording
        self.format = pyaudio.paInt16
        self._device_configured = False
        self._configure_device()

    def _configure_device(self):
        """Configure the audio device once during initialization"""
        if self._device_configured:
            return
            
        pa = pyaudio.PyAudio()
        
        # If no device specified, find best input device
        if self.device_index is None:
            self.device_index, self.channels = self._find_best_input_device(pa)
        else:
            # Verify the specified device exists and get its capabilities
            try:
                info = pa.get_device_info_by_index(self.device_index)
                if info['maxInputChannels'] > 0:
                    self.channels = min(info['maxInputChannels'], 2)
                    print(f"Using specified device {self.device_index}: {info['name']} ({self.channels} channels)")
                else:
                    print(f"Specified device {self.device_index} has no input channels, finding alternative...")
                    self.device_index, self.channels = self._find_best_input_device(pa)
            except Exception as e:
                print(f"Specified device {self.device_index} not available: {e}")
                self.device_index, self.channels = self._find_best_input_device(pa)
        
        pa.terminate()
        self._device_configured = True

    def record(self, seconds=5):
        # If using ReSpeaker device (index 1), try ALSA method first
        if self.device_index == 1:
            try:
                return self.record_with_alsa(seconds)
            except Exception as e:
                print(f"ALSA recording failed: {e}")
                print("Falling back to PyAudio...")
                # Add a small delay before trying PyAudio
                import time
                time.sleep(0.1)
        
        pa = pyaudio.PyAudio()
        
        try:
            print(f"Recording for {seconds} seconds using device {self.device_index} with {self.channels} channels...")
            
            stream = pa.open(
                format=self.format, 
                channels=self.channels, 
                rate=self.rate, 
                input=True, 
                frames_per_buffer=self.chunk, 
                input_device_index=self.device_index
            )
            
            frames = []
            for _ in range(0, int(self.rate / self.chunk * seconds)):
                data = stream.read(self.chunk, exception_on_overflow=False)
                frames.append(data)
                
            stream.stop_stream()
            stream.close()
            self.actual_channels = self.channels  # Used configured channels
            
        except Exception as e:
            print(f"Direct device recording failed: {e}")
            print("Trying with default device...")
            
            # Try with default device (PulseAudio/PipeWire)
            try:
                stream = pa.open(
                    format=self.format, 
                    channels=1,  # Try mono for compatibility 
                    rate=self.rate, 
                    input=True, 
                    frames_per_buffer=self.chunk, 
                    input_device_index=None  # Use default device
                )
                
                frames = []
                for _ in range(0, int(self.rate / self.chunk * seconds)):
                    data = stream.read(self.chunk, exception_on_overflow=False)
                    frames.append(data)
                    
                stream.stop_stream()
                stream.close()
                print("Successfully recorded using default device")
                self.actual_channels = 1  # Default device used mono
                
            except Exception as e2:
                print(f"Default device recording also failed: {e2}")
                pa.terminate()
                raise RuntimeError(f"Could not record audio with any device: {e}, {e2}")
        
        pa.terminate()
        audio_data = b''.join(frames)
        return audio_data
    
    def record_with_alsa(self, seconds=5):
        """Alternative recording method using ALSA directly for ReSpeaker"""
        print(f"Recording for {seconds} seconds using ALSA hw:3,0 (ReSpeaker)...")
        
        # Use a temporary file for recording
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Use arecord to capture audio directly from the ReSpeaker device
            cmd = [
                'arecord',
                '-D', 'hw:3,0',  # ReSpeaker device
                '-f', 'S16_LE',  # 16-bit signed little-endian
                '-r', str(self.rate),  # Sample rate
                '-c', '2',  # Stereo (ReSpeaker has 2 channels)
                '-d', str(seconds),  # Duration
                temp_filename
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise RuntimeError(f"arecord failed: {result.stderr}")
            
            # Read the recorded file
            import soundfile as sf
            audio_data, sample_rate = sf.read(temp_filename)
            
            # Convert to mono if stereo (take left channel)
            if len(audio_data.shape) > 1:
                audio_data = audio_data[:, 0]
            
            # Convert to int16 format for compatibility
            audio_data = (audio_data * 32767).astype(np.int16)
            
            # Set actual channels used
            self.actual_channels = 1  # We convert to mono
            
            # Convert to bytes
            return audio_data.tobytes()
            
        except Exception as e:
            raise RuntimeError(f"ALSA recording failed: {e}")
        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

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
