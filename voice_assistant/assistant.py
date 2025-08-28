from wakeword.wakeword_detector import WakeWordDetector
from utils.audio_recorder import AudioRecorder
from stt.stt_vosk import VoskSTT
from tts.tts_pyttsx3 import speak_text
from commands import gpio_control, music_player, weather, general_commands
from utils.respeaker_leds import led_controller
import config


def main():
    wakeword = WakeWordDetector(config.WAKEWORD_FILE)
    recorder = AudioRecorder(device_index=config.AUDIO_DEVICE_INDEX)
    stt = VoskSTT()  # You may need to download Vosk model first

    print('Voice Assistant is running. Say "Hey Pi" to start...')
    led_controller.turn_off()  # Start with LEDs off
    
    while True:
        if wakeword.detect():
            print('Wake word detected! Listening...')
            led_controller.wake_word_animation()  # Blue pulsing
            led_controller.listening_animation()   # Green steady
            
            audio = recorder.record()
            text = stt.transcribe(audio, channels=recorder.channels)
            print(f'Heard: {text}')
            
            led_controller.speaking_animation()    # Orange while processing/speaking
            
            response = general_commands.handle(text)
            if response is None:
                response = gpio_control.handle(text)
            if response is None:
                response = music_player.handle(text)
            if response is None:
                response = weather.handle(text)
            if response is None:
                response = "Sorry, I didn't understand."
                led_controller.error_animation()  # Red for not understood
            
            speak_text(response)
            led_controller.turn_off()  # Turn off LEDs after response

if __name__ == '__main__':
    main()
