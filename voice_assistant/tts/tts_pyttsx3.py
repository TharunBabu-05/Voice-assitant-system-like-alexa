import subprocess
import os
import time
import pyttsx3
import config
from config import VOICE_TYPE, VOICE_SPEED, VOICE_VOLUME

# Voice configuration
VOICE_PROFILES = {
    'alexa_female': {
        'espeak_voice': 'en+f3',  # Female voice variant 3
        'espeak_speed': 140,
        'espeak_pitch': 50,
        'espeak_amplitude': 200,
        'pyttsx3_voice': 'female'
    },
    'siri_female': {
        'espeak_voice': 'en+f4',  # Female voice variant 4
        'espeak_speed': 160,
        'espeak_pitch': 60,
        'espeak_amplitude': 180,
        'pyttsx3_voice': 'female'
    },
    'assistant_female': {
        'espeak_voice': 'en+f2',  # Female voice variant 2
        'espeak_speed': 150,
        'espeak_pitch': 45,
        'espeak_amplitude': 190,
        'pyttsx3_voice': 'female'
    },
    'default_male': {
        'espeak_voice': 'en+m3',  # Male voice
        'espeak_speed': 150,
        'espeak_pitch': 50,
        'espeak_amplitude': 200,
        'pyttsx3_voice': 'male'
    }
}

def speak_text_pyttsx3(text, voice_type='alexa_female'):
    """Speak text using pyttsx3 with female voice"""
    try:
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        
        # Set female voice if available
        profile = VOICE_PROFILES.get(voice_type, VOICE_PROFILES['alexa_female'])
        
        for voice in voices:
            if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        # Set voice properties
        engine.setProperty('rate', VOICE_SPEED)    # Speed
        engine.setProperty('volume', VOICE_VOLUME) # Volume (0.0 to 1.0)
        
        # Ensure audio device is free
        time.sleep(0.5)
        
        print(f"🔊 Speaking with {voice_type}: {text}")
        engine.say(text)
        engine.runAndWait()
        
        engine.stop()
        return True
        
    except Exception as e:
        print(f"❌ pyttsx3 TTS error: {e}")
        return False

def speak_text_espeak(text, voice_type='alexa_female'):
    """Speak text using espeak with enhanced female voices"""
    try:
        profile = VOICE_PROFILES.get(voice_type, VOICE_PROFILES['alexa_female'])
        
        # Longer delay to ensure audio device is free
        time.sleep(0.8)
        
        # Force analog output and set volume
        os.system('amixer cset numid=3 1 > /dev/null 2>&1')
        os.system('amixer sset Master 90% > /dev/null 2>&1')
        
        # Build espeak command with female voice parameters
        espeak_cmd = (
            f'espeak -v {profile["espeak_voice"]} '
            f'-s {profile["espeak_speed"]} '
            f'-p {profile["espeak_pitch"]} '
            f'-a {profile["espeak_amplitude"]} '
            f'"{text}"'
        )
        
        result = os.system(espeak_cmd)
        
        if result == 0:
            print(f"🔊 Spoke with {voice_type}: {text}")
            return True
        else:
            print(f"❌ espeak failed with code: {result}")
            return False
            
    except Exception as e:
        print(f"❌ espeak TTS error: {e}")
        return False

def speak_text_festival(text, voice_type='alexa_female'):
    """Speak text using Festival with female voice"""
    try:
        # Ensure audio device is free
        time.sleep(0.5)
        
        # Force analog output
        os.system('amixer cset numid=3 1 > /dev/null 2>&1')
        
        # Festival command with female voice
        festival_cmd = f'echo "{text}" | festival --tts'
        
        result = os.system(festival_cmd)
        
        if result == 0:
            print(f"🔊 Spoke with Festival: {text}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Festival TTS error: {e}")
        return False

def speak_text(text, voice_type=None):
    """Main TTS function with multiple engine fallback"""
    if voice_type is None:
        voice_type = getattr(config, 'VOICE_TYPE', 'alexa_female')
    
    # Handle custom voice selection
    if voice_type == 'custom' and hasattr(config, 'CUSTOM_VOICE'):
        return speak_text_espeak_custom(text, config.CUSTOM_VOICE)
    
    # Try different TTS engines in order of preference
    tts_engines = [
        ('pyttsx3', speak_text_pyttsx3),
        ('espeak', speak_text_espeak),
        ('festival', speak_text_festival)
    ]
    
    for engine_name, engine_func in tts_engines:
        try:
            if engine_func(text, voice_type):
                return True
        except Exception as e:
            print(f"❌ {engine_name} failed: {e}")
            continue
    
    # Fallback: print text if all TTS engines fail
    print(f"❌ All TTS engines failed. Response: {text}")
    return False

def speak_text_espeak_custom(text, custom_voice):
    """Speak text using espeak with custom selected voice"""
    try:
        # Longer delay to ensure audio device is free
        time.sleep(0.8)
        
        # Force analog output and set volume
        os.system('amixer cset numid=3 1 > /dev/null 2>&1')
        os.system('amixer sset Master 90% > /dev/null 2>&1')
        
        # Build espeak command with custom voice
        espeak_cmd = (
            f'espeak -v {custom_voice} '
            f'-s {config.VOICE_SPEED} '
            f'-p 50 '
            f'-a 180 '
            f'"{text}"'
        )
        
        result = os.system(espeak_cmd)
        
        if result == 0:
            print(f"🔊 Spoke with custom voice ({custom_voice}): {text}")
            return True
        else:
            print(f"❌ espeak failed with code: {result}")
            return False
            
    except Exception as e:
        print(f"❌ espeak custom TTS error: {e}")
        return False

# Convenience functions for different voice styles
def speak_alexa(text):
    """Speak with Alexa-like female voice"""
    return speak_text(text, 'alexa_female')

def speak_siri(text):
    """Speak with Siri-like female voice"""
    return speak_text(text, 'siri_female')

def speak_assistant(text):
    """Speak with generic assistant female voice"""
    return speak_text(text, 'assistant_female')
