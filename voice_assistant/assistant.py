from wakeword.wakeword_detector import WakeWordDetector
from utils.audio_recorder import AudioRecorder
from stt.stt_whisper import WhisperSTT
from tts.tts_pyttsx3 import speak_text
from commands import gpio_control, music_player, weather, general_commands
from utils.respeaker_leds import led_controller
from ai.gemini_ai import initialize_gemini, get_ai_response, should_use_ai
import config


def main():
    # Initialize AI if enabled
    if hasattr(config, 'ENABLE_AI') and config.ENABLE_AI:
        print('🤖 Initializing Gemini AI...')
        initialize_gemini(config.GEMINI_API_KEY)
    
    wakeword = WakeWordDetector(config.WAKEWORD_FILE)
    recorder = AudioRecorder(device_index=config.AUDIO_DEVICE_INDEX)
    
    # Initialize Whisper STT
    print('🎤 Initializing Whisper speech recognition...')
    whisper_model = getattr(config, 'WHISPER_MODEL_SIZE', 'base')
    stt = WhisperSTT(model_size=whisper_model)

    print('🎤 Voice Assistant is running. Say "Hey Pi" to start...')
    led_controller.turn_off()  # Start with LEDs off
    
    while True:
        if wakeword.detect():
            print('🔵 Wake word detected! Listening...')
            led_controller.wake_word_animation()  # Enhanced blue wave
            led_controller.listening_animation()   # Enhanced green breathing
            
            # Small delay to ensure wake word detector has released the audio device
            import time
            time.sleep(0.1)
            
            audio = recorder.record(seconds=config.RECORDING_DURATION)
            text = stt.transcribe(audio, channels=recorder.actual_channels)
            print(f'👂 Heard: {text}')
            
            if not text.strip():  # If no text detected
                led_controller.error_animation()
                speak_text("Sorry, I didn't hear you clearly.")
                led_controller.turn_off()
                continue
            
            led_controller.speaking_animation()    # Enhanced orange/yellow flowing
            
            # Try hardware/system commands first
            response = general_commands.handle(text)
            if response is None:
                response = gpio_control.handle(text)
            if response is None:
                response = music_player.handle(text)
            if response is None:
                response = weather.handle(text)
            
            # If no system command matched, try AI
            if response is None and should_use_ai(text):
                print('🧠 Using AI to respond...')
                response = get_ai_response(text)
            
            # Fallback response
            if response is None:
                response = "Sorry, I didn't understand that command."
                led_controller.error_animation()  # Enhanced red warning
            
            speak_text(response)
            led_controller.turn_off()  # Turn off LEDs after response

if __name__ == '__main__':
    main()
