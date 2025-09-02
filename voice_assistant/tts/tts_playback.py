import simpleaudio as sa

def play_audio(audio_data):
    play_obj = sa.play_buffer(audio_data, 1, 2, 16000)
    play_obj.wait_done()
