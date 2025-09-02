import pyaudio
import wave
import io
import subprocess
import tempfile
import os
import numpy as np
import time
import threading

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

    def record_with_vad(self, silence_duration=2.0, max_duration=30.0, volume_threshold=300):
        """
        Record continuously until silence is detected for specified duration
        
        Args:
            silence_duration: Duration of silence in seconds to stop recording
            max_duration: Maximum recording duration in seconds
            volume_threshold: Audio level threshold to detect speech (lowered to 100)
        """
        print(f"🎤 Recording continuously... (Stop after {silence_duration}s of silence)")
        
        # Always use PyAudio for better VAD control
        return self._record_with_vad_pyaudio(silence_duration, max_duration, volume_threshold)

    def _record_with_vad_pyaudio(self, silence_duration, max_duration, volume_threshold):
        """Voice Activity Detection recording using PyAudio with improved detection"""
        pa = pyaudio.PyAudio()
        
        try:
            # Try direct device first
            try:
                stream = pa.open(
                    format=self.format, 
                    channels=self.channels, 
                    rate=self.rate, 
                    input=True, 
                    frames_per_buffer=self.chunk, 
                    input_device_index=self.device_index
                )
                device_channels = self.channels
            except Exception as e:
                print(f"Direct device failed: {e}")
                print("Using default device...")
                stream = pa.open(
                    format=self.format, 
                    channels=1, 
                    rate=self.rate, 
                    input=True, 
                    frames_per_buffer=self.chunk, 
                    input_device_index=None
                )
                device_channels = 1
            
            frames = []
            silence_start = None
            recording_start = time.time()
            speech_detected = False
            last_speech_time = None
            
            print("🟢 Speak now...")
            
            # Simple calibration - just a few samples to get baseline
            calibration_volumes = []
            for _ in range(3):
                data = stream.read(self.chunk, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                # Use peak volume instead of RMS for better speech detection
                volume = np.max(np.abs(audio_data))
                calibration_volumes.append(volume)
                frames.append(data)
            
            # Set a reasonable threshold based on calibration
            base_noise = np.mean(calibration_volumes)
            # Use much lower threshold - speech typically 5-10x louder than silence
            speech_threshold = max(volume_threshold, base_noise * 3)
            print(f"🎚️ Speech threshold: {speech_threshold:.0f} (base: {base_noise:.0f})")
            
            consecutive_silence_chunks = 0
            chunks_per_second = self.rate // self.chunk
            silence_chunks_needed = int(silence_duration * chunks_per_second)
            
            while True:
                # Read audio chunk
                data = stream.read(self.chunk, exception_on_overflow=False)
                frames.append(data)
                
                # Calculate volume using peak detection (better for speech)
                audio_data = np.frombuffer(data, dtype=np.int16)
                peak_volume = np.max(np.abs(audio_data))
                
                current_time = time.time()
                
                # Check if this chunk contains speech
                if peak_volume > speech_threshold:
                    # Speech detected!
                    speech_detected = True
                    last_speech_time = current_time
                    consecutive_silence_chunks = 0
                    print("🗣️", end="", flush=True)
                else:
                    # Silence detected
                    consecutive_silence_chunks += 1
                    if consecutive_silence_chunks == 1:  # First silence chunk
                        print(" 🤫", end="", flush=True)
                    
                    # Check if we've had enough consecutive silence
                    if consecutive_silence_chunks >= silence_chunks_needed:
                        if speech_detected:
                            print(f"\n✅ Stopped after {silence_duration}s of silence")
                            break
                        else:
                            # Reset if no speech detected yet
                            consecutive_silence_chunks = 0
                
                # Check maximum duration
                if current_time - recording_start >= max_duration:
                    print(f"\n⏰ Max duration reached ({max_duration}s)")
                    break
            
            stream.stop_stream()
            stream.close()
            self.actual_channels = device_channels
            
        finally:
            pa.terminate()
        
        # Convert frames to audio data
        audio_data = b''.join(frames)
        
        # Convert to mono if needed for compatibility
        if device_channels > 1:
            audio_np = np.frombuffer(audio_data, dtype=np.int16)
            audio_np = audio_np.reshape(-1, device_channels)
            audio_np = np.mean(audio_np, axis=1).astype(np.int16)
            audio_data = audio_np.tobytes()
            self.actual_channels = 1
        
        duration = len(audio_data) // (2 * self.actual_channels * self.rate)
        print(f"📊 Recorded {duration:.1f} seconds of audio")
        
        return audio_data

    def _record_with_vad_alsa(self, silence_duration, max_duration, volume_threshold):
        """Voice Activity Detection recording using ALSA"""
        import tempfile
        import subprocess
        import threading
        import queue
        
        # Create temporary file for continuous recording
        temp_fd, temp_filename = tempfile.mkstemp(suffix='.wav', prefix='vad_recording_')
        os.close(temp_fd)
        
        try:
            print("📡 Recording with ALSA VAD...")
            
            # Start arecord process for continuous recording
            cmd = [
                'arecord',
                '-D', 'hw:3,0',  # ReSpeaker device
                '-f', 'S16_LE',
                '-r', str(self.rate),
                '-c', '1',  # Mono
                '-t', 'wav',
                temp_filename
            ]
            
            # Start recording process
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Monitor the recording file for voice activity
            recording_start = time.time()
            silence_start = None
            last_size = 0
            
            while True:
                current_time = time.time()
                
                # Check if file is growing (indicates audio activity)
                try:
                    current_size = os.path.getsize(temp_filename)
                    size_diff = current_size - last_size
                    
                    # Simple VAD: if file is growing significantly, there's audio
                    if size_diff > 1000:  # More than 1KB growth indicates audio
                        silence_start = None
                        print("🗣️", end="", flush=True)
                        last_size = current_size
                    else:
                        # Possible silence
                        if silence_start is None:
                            silence_start = current_time
                            print(" 🤫", end="", flush=True)
                        elif current_time - silence_start >= silence_duration:
                            print(f"\n✅ Recording stopped after {silence_duration}s of silence")
                            break
                    
                    # Check maximum duration
                    if current_time - recording_start >= max_duration:
                        print(f"\n⏰ Recording stopped - reached maximum duration ({max_duration}s)")
                        break
                        
                except OSError:
                    # File might not exist yet
                    pass
                
                time.sleep(0.1)  # Check every 100ms
            
            # Stop the recording process
            process.terminate()
            process.wait()
            
            # Read the recorded audio
            with open(temp_filename, 'rb') as f:
                # Skip WAV header (44 bytes)
                f.seek(44)
                audio_data = f.read()
            
            # Convert to numpy array and ensure correct format
            audio_np = np.frombuffer(audio_data, dtype=np.int16)
            self.actual_channels = 1  # ALSA records in mono
            
            duration = len(audio_data) // (2 * self.actual_channels * self.rate)
            print(f"📊 Recorded {duration:.1f} seconds of audio")
            
            return audio_data
            
        except Exception as e:
            raise RuntimeError(f"ALSA VAD recording failed: {e}")
        finally:
            # Clean up
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
