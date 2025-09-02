#!/usr/bin/env python3
"""
Test Whisper STT functionality
"""
from stt.stt_whisper import WhisperSTT
from utils.audio_recorder import AudioRecorder
import config

def test_whisper():
    print("🎤 Testing Whisper STT...")
    
    # Initialize Whisper with tiny model for faster testing
    stt = WhisperSTT(model_size="tiny")
    
    # Initialize audio recorder
    recorder = AudioRecorder(device_index=config.AUDIO_DEVICE_INDEX)
    
    print("Recording 3 seconds of audio...")
    print("Say something clearly...")
    
    # Record audio
    audio_data = recorder.record(seconds=3)
    
    print("🧠 Transcribing with Whisper...")
    text = stt.transcribe(audio_data, channels=recorder.actual_channels)
    
    print(f"📝 Whisper heard: '{text}'")
    
    if text.strip():
        print("✅ Whisper is working correctly!")
    else:
        print("❌ Whisper didn't detect any speech")

if __name__ == "__main__":
    test_whisper()
