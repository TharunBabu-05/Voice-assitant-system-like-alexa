import pyaudio

def list_audio_devices():
    pa = pyaudio.PyAudio()
    print("Available audio devices:")
    for i in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(i)
        print(f"Device {i}: {info['name']}")
        print(f"  - Channels: {info['maxInputChannels']} input, {info['maxOutputChannels']} output")
        print(f"  - Sample Rate: {info['defaultSampleRate']}")
        print()
    pa.terminate()

if __name__ == "__main__":
    list_audio_devices()
