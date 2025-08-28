from wakeword.wakeword_detector import WakeWordDetector
from utils.audio_recorder import AudioRecorder
from stt.stt_google import GoogleSTT
from tts.tts_google import GoogleTTS
from tts.tts_playback import play_audio
from commands import gpio_control, music_player, weather, general_commands
import config


def main():
    wakeword = WakeWordDetector(config.WAKEWORD_FILE)
    recorder = AudioRecorder(device_index=config.AUDIO_DEVICE_INDEX)
    stt = GoogleSTT(config.GOOGLE_CLOUD_SPEECH_CREDENTIALS)
    tts = GoogleTTS(config.GOOGLE_CLOUD_TTS_CREDENTIALS)

    print('Voice Assistant is running. Say "Hey Pi" to start...')
    while True:
        if wakeword.detect():
            print('Wake word detected! Listening...')
            audio = recorder.record()
            text = stt.transcribe(audio)
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
            tts_audio = tts.speak(response)
            play_audio(tts_audio)

if __name__ == '__main__':
    main()
