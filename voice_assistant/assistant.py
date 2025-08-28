from wakeword.wakeword_detector import WakeWordDetector
from utils.audio_recorder import AudioRecorder
from stt.stt_vosk import VoskSTT
from tts.tts_pyttsx3 import speak_text
from commands import gpio_control, music_player, weather, general_commands
import config


def main():
    wakeword = WakeWordDetector(config.WAKEWORD_FILE)
    recorder = AudioRecorder(device_index=config.AUDIO_DEVICE_INDEX)
    stt = VoskSTT()  # You may need to download Vosk model first

    print('Voice Assistant is running. Say "Hey Pi" to start...')
    while True:
        if wakeword.detect():
            print('Wake word detected! Listening...')
            audio = recorder.record()
            text = stt.transcribe(audio, channels=recorder.channels)
            print(f'Heard: {text}')
            response = general_commands.handle(text)
            if response is None:
                response = gpio_control.handle(text)
            if response is None:
                response = music_player.handle(text)
            if response is None:
                response = weather.handle(text)
            if response is None:
                response = "Sorry, I didn't understand."
            speak_text(response)

if __name__ == '__main__':
    main()
