import subprocess
import os
import time

def speak_text(text):
    """Speak text using espeak with proper audio device handling"""
    try:
        # Longer delay to ensure audio device is free
        time.sleep(0.8)
        
        # Force analog output and set volume
        os.system('amixer cset numid=3 1 > /dev/null 2>&1')
        os.system('amixer sset Master 90% > /dev/null 2>&1')
        
        # Use os.system instead of subprocess to avoid audio conflicts
        result = os.system(f'espeak -a 200 -s 150 "{text}"')
        
        if result == 0:
<<<<<<< HEAD
            print(f"✓ Spoke: {text}")
            return True
        else:
            print(f"✗ espeak failed with code: {result}")
            return False
            
    except Exception as e:
        print(f"✗ TTS error: {e}")
=======
            print(f"? Spoke: {text}")
            return True
        else:
            print(f"? espeak failed with code: {result}")
            return False
            
    except Exception as e:
        print(f"? TTS error: {e}")
>>>>>>> master
        print(f"Response (no audio): {text}")
        return False
