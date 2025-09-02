#!/usr/bin/env python3
"""
Test script to check audio recording volume levels
"""
import numpy as np
from utils.audio_recorder import AudioRecorder
import config

def test_audio_volume():
    print("Testing audio recording volume...")
    recorder = AudioRecorder(device_index=config.AUDIO_DEVICE_INDEX, channels=2)
    
    print("Recording 3 seconds of audio...")
    print("Please speak normally after this message...")
    
    audio_data = recorder.record(seconds=3)
    
    # Convert to numpy array for analysis
    if isinstance(audio_data, bytes):
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
    else:
        audio_array = audio_data
    
    # Calculate volume statistics
    max_amplitude = np.max(np.abs(audio_array))
    rms = np.sqrt(np.mean(audio_array.astype(np.float64) ** 2))
    
    print(f"\nAudio Analysis:")
    print(f"Max amplitude: {max_amplitude} (range: 0-32767)")
    print(f"RMS level: {rms:.2f}")
    print(f"Audio length: {len(audio_array)} samples")
    print(f"Duration: {len(audio_array) / 16000:.2f} seconds")
    print(f"Channels used: {recorder.actual_channels}")
    
    # Check if audio is too quiet
    if max_amplitude < 1000:
        print("⚠️  Audio seems very quiet. Try speaking louder or closer to microphone.")
    elif max_amplitude < 5000:
        print("🔸 Audio is somewhat quiet but should work.")
    else:
        print("✅ Audio volume looks good!")
    
    # Check for silence
    if max_amplitude < 100:
        print("❌ Audio appears to be mostly silence.")
    
    print(f"\nDevice used: {recorder.device_index}")

if __name__ == "__main__":
    test_audio_volume()
