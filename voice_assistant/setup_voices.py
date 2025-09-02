#!/usr/bin/env python3
"""
Voice Setup Script for Voice Assistant
Installs and configures various TTS voices including female voices
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a system command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def install_espeak_voices():
    """Install additional espeak voices"""
    commands = [
        ("sudo apt-get update", "Updating package list"),
        ("sudo apt-get install -y espeak espeak-data", "Installing espeak"),
        ("sudo apt-get install -y espeak-mbrola mbrola", "Installing MBROLA voices"),
        ("sudo apt-get install -y mbrola-us1 mbrola-us2 mbrola-us3", "Installing US English voices"),
        ("sudo apt-get install -y mbrola-en1", "Installing British English voice"),
    ]
    
    for command, description in commands:
        run_command(command, description)

def install_festival():
    """Install Festival TTS with additional voices"""
    commands = [
        ("sudo apt-get install -y festival", "Installing Festival TTS"),
        ("sudo apt-get install -y festlex-cmu festlex-poslex", "Installing Festival lexicons"),
        ("sudo apt-get install -y festvox-kallpc16k", "Installing Kal voice"),
        ("sudo apt-get install -y festvox-kdlpc16k", "Installing female voice"),
    ]
    
    for command, description in commands:
        run_command(command, description)

def test_voices():
    """Test different voice options"""
    test_text = "Hello, I am your voice assistant. How does this sound?"
    
    print("\n🎤 Testing available voices...")
    
    # Test espeak female voices
    female_voices = ['en+f2', 'en+f3', 'en+f4', 'en+f5']
    
    for i, voice in enumerate(female_voices, 1):
        print(f"\n🔊 Testing espeak female voice {i} ({voice})")
        cmd = f'espeak -v {voice} -s 160 -p 50 -a 180 "{test_text}"'
        run_command(cmd, f"Testing voice {voice}")
        
        response = input("Do you like this voice? (y/n/skip): ").lower()
        if response == 'y':
            print(f"✅ You selected voice: {voice}")
            update_config_voice(voice)
            return voice
        elif response == 'skip':
            continue
    
    # Test MBROLA voices if available
    mbrola_voices = ['mb-us1', 'mb-us2', 'mb-us3', 'mb-en1']
    
    for voice in mbrola_voices:
        print(f"\n🔊 Testing MBROLA voice ({voice})")
        cmd = f'espeak -v {voice} -s 160 "{test_text}"'
        if run_command(cmd, f"Testing MBROLA voice {voice}"):
            response = input("Do you like this voice? (y/n/skip): ").lower()
            if response == 'y':
                print(f"✅ You selected MBROLA voice: {voice}")
                update_config_voice(voice)
                return voice

def update_config_voice(voice):
    """Update config.py with selected voice"""
    config_file = "config.py"
    
    try:
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Update voice type in config
        if 'VOICE_TYPE =' in content:
            # Replace existing voice type
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('VOICE_TYPE ='):
                    lines[i] = f"VOICE_TYPE = 'custom'  # Using {voice}"
                    break
            content = '\n'.join(lines)
        
        # Add custom voice config
        if 'CUSTOM_VOICE =' not in content:
            content += f"\nCUSTOM_VOICE = '{voice}'  # Selected during setup\n"
        
        with open(config_file, 'w') as f:
            f.write(content)
            
        print(f"✅ Updated config.py with voice: {voice}")
        
    except Exception as e:
        print(f"❌ Failed to update config: {e}")

def main():
    """Main setup function"""
    print("🎵 Voice Assistant - Voice Setup")
    print("=" * 40)
    
    print("\nThis script will:")
    print("1. Install additional TTS engines and voices")
    print("2. Let you test different female voices")
    print("3. Configure your preferred voice")
    
    response = input("\nContinue? (y/n): ").lower()
    if response != 'y':
        print("Setup cancelled.")
        return
    
    # Install voice engines
    print("\n📦 Installing voice engines...")
    install_espeak_voices()
    install_festival()
    
    # Test and select voice
    print("\n🎤 Voice selection...")
    selected_voice = test_voices()
    
    if selected_voice:
        print(f"\n✅ Setup complete! Selected voice: {selected_voice}")
        print("\nYou can now run your voice assistant with the new voice.")
        print("To change voices later, edit VOICE_TYPE in config.py")
    else:
        print("\n⚠️ No voice selected. Using default voice.")
    
    print("\n🎵 Available voice types in config.py:")
    print("- alexa_female: Alexa-like female voice")
    print("- siri_female: Siri-like female voice") 
    print("- assistant_female: Generic female assistant voice")
    print("- default_male: Male voice")

if __name__ == "__main__":
    main()
