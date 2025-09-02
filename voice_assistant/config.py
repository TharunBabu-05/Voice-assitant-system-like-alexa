# Configuration for Voice Assistant
OPENWEATHER_API_KEY = '16ebeafd632800074eedb5b0a38401c7'
WAKEWORD_FILE = 'wakeword/hey_pi.ppn'
AUDIO_DEVICE_INDEX = 1  # ReSpeaker device (auto-detected)
RECORDING_DURATION = 3  # Recording duration in seconds after wake word (for fallback)

# Voice Activity Detection (VAD) Configuration
VAD_SILENCE_DURATION = 2.0  # Stop recording after this many seconds of silence
VAD_MAX_DURATION = 30.0     # Maximum recording duration in seconds
VAD_VOLUME_THRESHOLD = 50   # Audio level threshold to detect speech (lowered for better sensitivity)

# Whisper STT Configuration
WHISPER_MODEL_SIZE = "tiny"  # Options: tiny, base, small, medium, large

GPIO_LED_PIN = 17
PORCUPINE_ACCESS_KEY = 'wtH/bRfku05C3oGSTh30TU1quw74RpTsQVHgYVER8UGpl5mvmPZxKw=='

# Gemini AI Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = "AIzaSyB0VqfCJH_ks9Wgi8ZAlZe_r5x322TUkp8"  # Set this to your Gemini API key or use environment variable

# AI Settings
ENABLE_AI = True  # Set to False to disable AI features
AI_MAX_RESPONSE_LENGTH = 200  # Maximum tokens for AI responses
AI_TEMPERATURE = 0.7  # Creativity level (0.0 to 1.0)
