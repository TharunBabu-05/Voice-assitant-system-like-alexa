import pyttsx3
import subprocess
import os
import time

def speak_text(text):
    """Speak text using the method that works best on Pi"""
    try:
        # Longer delay to ensure PyAudio completely releases audio device
        time.sleep(0.5)
        
        # Kill any hanging audio processes (just in case)
        subprocess.run(['pkill', '-f', 'python.*audio'], 
                      check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Force analog output (3.5mm jack) first
        subprocess.run(['amixer', 'cset', 'numid=3', '1'], 
                      check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Ensure volume is up
        subprocess.run(['amixer', 'sset', 'Master', '90%'], 
                      check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Use espeak directly with good volume and speed (same as your working test)
        result = subprocess.run(['espeak', '-a', '200', '-s', '150', text], 
                               check=True, 
                               timeout=10)
        print(f"✓ Spoke: {text}")
        return True
        
    except subprocess.TimeoutExpired:
        print(f"✗ espeak timeout for: {text}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"✗ espeak failed: {e}")
        return False
    except Exception as e:
        print(f"✗ TTS error: {e}")
        print(f"Response (no audio): {text}")
        return False
