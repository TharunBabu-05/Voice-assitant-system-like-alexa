<<<<<<< HEAD
# Configuration for Voice Assistant
# Porcupine Access Key (get from https://picovoice.ai/console/)
PORCUPINE_ACCESS_KEY = 'wtH/bRfku05C3oGSTh30TU1quw74RpTsQVHgYVER8UGpl5mvmPZxKw=='
OPENWEATHER_API_KEY = '16ebeafd632800074eedb5b0a38401c7'  # Only needed for weather
WAKEWORD_FILE = 'wakeword/hey_pi.ppn'
AUDIO_DEVICE_INDEX = None  # Auto-detect ReSpeaker device
GPIO_LED_PIN = 17
=======
OPENWEATHER_API_KEY = '16ebeafd632800074eedb5b0a38401c7'
WAKEWORD_FILE = 'wakeword/hey_pi.ppn'
AUDIO_DEVICE_INDEX = 1  # ReSpeaker device (auto-detected)
RECORDING_DURATION = 3  # Recording duration in seconds after wake word

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
>>>>>>> master
