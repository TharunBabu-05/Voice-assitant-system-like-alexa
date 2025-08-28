import RPi.GPIO as GPIO
import config

GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)
GPIO.setup(config.GPIO_LED_PIN, GPIO.OUT)

def handle(text):
    if "turn on the light" in text.lower() or "light on" in text.lower():
        try:
            GPIO.output(config.GPIO_LED_PIN, GPIO.HIGH)
            print(f"GPIO {config.GPIO_LED_PIN} set to HIGH")
            return "Light turned on."
        except Exception as e:
            print(f"GPIO error: {e}")
            return "Error controlling light."
    elif "turn off the light" in text.lower() or "light off" in text.lower():
        try:
            GPIO.output(config.GPIO_LED_PIN, GPIO.LOW)
            print(f"GPIO {config.GPIO_LED_PIN} set to LOW")
            return "Light turned off."
        except Exception as e:
            print(f"GPIO error: {e}")
            return "Error controlling light."
    return None
