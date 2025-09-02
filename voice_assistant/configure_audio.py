#!/usr/bin/env python3
"""
Audio Device Configuration Utility
This script helps identify the correct ReSpeaker device and updates the config.py file
"""

import pyaudio
import re

def find_respeaker_device():
    """Find ReSpeaker device and return its index and channel count"""
    pa = pyaudio.PyAudio()
    
    print("🔍 Scanning for audio devices...")
    print("-" * 60)
    
    respeaker_device = None
    
    for i in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(i)
        name = info['name']
        max_inputs = info['maxInputChannels']
        max_outputs = info['maxOutputChannels']
        
        print(f"Device {i}: {name}")
        print(f"  Input channels: {max_inputs}, Output channels: {max_outputs}")
        
        # Check if this is a ReSpeaker device
        if max_inputs > 0 and ('seeed' in name.lower() or 'respeaker' in name.lower()):
            channels = min(max_inputs, 2)  # Use max 2 channels
            respeaker_device = (i, channels)
            print(f"  ✅ ReSpeaker device found! Using {channels} channels")
        
        print()
    
    pa.terminate()
    return respeaker_device

def update_config(device_index, channels):
    """Update the config.py file with the correct device index"""
    config_file = "config.py"
    
    try:
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Update AUDIO_DEVICE_INDEX
        content = re.sub(
            r'AUDIO_DEVICE_INDEX\s*=\s*\d+.*',
            f'AUDIO_DEVICE_INDEX = {device_index}  # ReSpeaker device (auto-detected)',
            content
        )
        
        with open(config_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {config_file}: AUDIO_DEVICE_INDEX = {device_index}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to update config file: {e}")
        return False

def main():
    print("🎤 ReSpeaker Audio Device Configuration")
    print("=" * 50)
    
    device_info = find_respeaker_device()
    
    if device_info:
        device_index, channels = device_info
        print(f"🎯 Found ReSpeaker at device index {device_index} with {channels} channels")
        
        # Update config file
        if update_config(device_index, channels):
            print("🎉 Configuration complete!")
            print(f"   Device Index: {device_index}")
            print(f"   Channels: {channels}")
            print("\n💡 You can now run the voice assistant with the correct audio device.")
        else:
            print("⚠️  Please manually update config.py:")
            print(f"   Set AUDIO_DEVICE_INDEX = {device_index}")
    else:
        print("❌ No ReSpeaker device found!")
        print("💡 Available options:")
        print("   1. Check if ReSpeaker is properly connected")
        print("   2. Run 'arecord -l' to list audio devices")
        print("   3. Manually set AUDIO_DEVICE_INDEX in config.py")

if __name__ == "__main__":
    main()
