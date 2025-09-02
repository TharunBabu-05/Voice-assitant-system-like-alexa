#!/usr/bin/env python3
"""
Voice Test Script - Test different female voices for the voice assistant
"""

import os
import sys
import time

# Add current directory to path to import config
sys.path.append('.')
import config

def test_voice(voice_name, voice_code, test_text):
    """Test a specific voice"""
    print(f"\n🎤 Testing: {voice_name} ({voice_code})")
    print(f"💬 Text: {test_text}")
    
    # Build espeak command
    cmd = f'espeak -v {voice_code} -s {config.VOICE_SPEED} -p 50 -a 180 "{test_text}"'
    
    try:
        # Force analog output
        os.system('amixer cset numid=3 1 > /dev/null 2>&1')
        result = os.system(cmd)
        
        if result == 0:
            return True
        else:
            print(f"❌ Voice {voice_name} failed")
            return False
    except Exception as e:
        print(f"❌ Error testing {voice_name}: {e}")
        return False

def main():
    """Main testing function"""
    print("🎵 Voice Assistant - Voice Testing")
    print("=" * 40)
    
    test_phrases = [
        "Hello! I am your voice assistant. How can I help you today?",
        "The weather today is sunny with a high of 75 degrees.",
        "I found 3 results for your search. Would you like me to read them?",
        "Setting a timer for 5 minutes. I'll let you know when it's ready.",
        "I'm sorry, I didn't understand that. Could you please repeat?"
    ]
    
    # Female voices to test
    female_voices = [
        ("Alexa-style Female", "en+f3"),
        ("Siri-style Female", "en+f4"),
        ("Assistant Female", "en+f2"),
        ("Friendly Female", "en+f5"),
        ("Professional Female", "en+f1"),
    ]
    
    print(f"\nAvailable female voices: {len(female_voices)}")
    print("Each voice will say a test phrase.\n")
    
    # Test each voice with different phrases
    for i, (voice_name, voice_code) in enumerate(female_voices, 1):
        print(f"\n{'='*50}")
        print(f"Voice {i}: {voice_name}")
        print(f"{'='*50}")
        
        # Test with first phrase
        test_phrase = test_phrases[0]
        if test_voice(voice_name, voice_code, test_phrase):
            
            # Ask user if they want to hear more
            response = input("\n🤔 What do you think? (g=good, m=more examples, n=next voice, s=select): ").lower()
            
            if response == 's':
                # Select this voice
                print(f"\n✅ Selected: {voice_name} ({voice_code})")
                update_config_voice(voice_code, voice_name)
                return
                
            elif response == 'm':
                # Play more examples
                print(f"\n🎤 More examples for {voice_name}:")
                for j, phrase in enumerate(test_phrases[1:], 2):
                    print(f"\nExample {j}:")
                    test_voice(voice_name, voice_code, phrase)
                    time.sleep(1)
                
                response = input(f"\n🤔 Select {voice_name}? (y/n): ").lower()
                if response == 'y':
                    print(f"\n✅ Selected: {voice_name} ({voice_code})")
                    update_config_voice(voice_code, voice_name)
                    return
            
            elif response == 'g':
                print(f"👍 You liked {voice_name}! Continuing to next voice...")
                
        else:
            print(f"⚠️ Skipping {voice_name} due to error")
    
    print("\n🤷 No voice selected. Using current default.")
    
def update_config_voice(voice_code, voice_name):
    """Update config.py with selected voice"""
    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Update voice type and custom voice
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if line.startswith('VOICE_TYPE ='):
                lines[i] = f"VOICE_TYPE = 'custom'  # {voice_name}"
            elif line.startswith('CUSTOM_VOICE ='):
                lines[i] = f"CUSTOM_VOICE = '{voice_code}'  # {voice_name}"
        
        # Add custom voice if not exists
        if 'CUSTOM_VOICE =' not in content:
            lines.append(f"CUSTOM_VOICE = '{voice_code}'  # {voice_name}")
        
        with open('config.py', 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Config updated with voice: {voice_name} ({voice_code})")
        
        # Test the selected voice
        print("\n🎤 Testing your selection:")
        test_voice(voice_name, voice_code, "Voice configuration updated successfully! Your assistant is ready.")
        
    except Exception as e:
        print(f"❌ Failed to update config: {e}")

if __name__ == "__main__":
    main()
