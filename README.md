# Voice Assistant System (Like Alexa)

A Raspberry Pi-based voice assistant with offline speech recognition, AI integration, and LED feedback. Built with Python and designed to work locally without requiring cloud services for core functionality.

## Features

- 🎙️ **Offline Speech Recognition** - Uses Vosk for local speech-to-text processing
- 🎯 **Wake Word Detection** - "Hey Pi" wake word using Porcupine
- 🤖 **AI Integration** - Gemini AI for intelligent responses with conversation memory
- 💡 **LED Feedback** - ReSpeaker LED animations for visual status
- 🎵 **Music Control** - Local music playback and control
- ⚡ **GPIO Control** - Smart home device control via GPIO
- 🌤️ **Weather Information** - Current weather updates
- 🔊 **Text-to-Speech** - Multiple TTS engines (pyttsx3, Google TTS)

## Hardware Requirements

- Raspberry Pi (3B+ or newer recommended)
- ReSpeaker Mic Array v2.0
- Speakers or headphones for audio output
- Optional: LEDs and GPIO devices for smart home control

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/TharunBabu-05/Voice-assitant-system-like-alexa.git
cd Voice-assitant-system-like-alexa
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r voice_assistant/requirements.txt
```

### 4. Configure Audio (Raspberry Pi)
```bash
cd voice_assistant
chmod +x install_espeak.sh
./install_espeak.sh
python configure_audio.py
```

### 5. Set Up AI (Optional)
```bash
python setup_gemini.py
```

## Usage

### Start the Voice Assistant
```bash
cd voice_assistant
python assistant.py
```

### Voice Commands
- **Wake Word**: "Hey Pi"
- **General**: "What time is it?", "Hello", "Good morning"
- **AI Questions**: "What is Python?", "Tell me about space"
- **Music**: "Play music", "Stop music", "Next song"
- **GPIO**: "Turn on light", "Turn off light"
- **Weather**: "What's the weather?"

## Project Structure

```
voice_assistant/
├── assistant.py              # Main application
├── config.py                 # Configuration settings
├── ai/                       # AI integration
│   └── gemini_ai.py         # Gemini AI handler
├── commands/                 # Command handlers
│   ├── general_commands.py  # Basic commands
│   ├── gpio_control.py      # GPIO device control
│   ├── music_player.py      # Music playback
│   └── weather.py           # Weather information
├── stt/                      # Speech-to-Text
│   ├── stt_vosk.py          # Vosk offline STT
│   ├── stt_whisper.py       # Whisper STT
│   └── stt_google.py        # Google STT
├── tts/                      # Text-to-Speech
│   ├── tts_pyttsx3.py       # Local TTS
│   ├── tts_google.py        # Google TTS
│   └── tts_playback.py      # Audio playback
├── utils/                    # Utilities
│   ├── audio_recorder.py    # Audio recording
│   ├── logger.py            # Logging system
│   └── respeaker_leds.py    # LED control
├── wakeword/                 # Wake word detection
│   └── wakeword_detector.py # Porcupine integration
└── tests/                    # Unit tests
```

## Configuration

Edit `config.py` to customize:
- Audio settings (sample rate, channels)
- STT engine selection
- TTS engine selection
- LED patterns and colors
- API keys and endpoints

## Testing

Run the test suite:
```bash
pytest
```

Run specific tests:
```bash
pytest tests/test_stt/
```

## Troubleshooting

### Audio Issues
```bash
# Test audio devices
python list_devices.py

# Configure audio
python configure_audio.py

# Test audio recording
./test_audio.sh
```

### LED Issues
- Check LED documentation: `LED_DOCUMENTATION.md`
- Verify ReSpeaker connections

### AI Issues
- Verify API keys in config
- Check internet connection for Gemini AI

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source. Feel free to use and modify as needed.

## Acknowledgments

- [Vosk](https://alphacephei.com/vosk/) for offline speech recognition
- [Porcupine](https://picovoice.ai/) for wake word detection
- [ReSpeaker](https://github.com/respeaker) for hardware integration
- Google and OpenAI for AI services
