import RPi.GPIO as GPIO
import config

GPIO.setmode(GPIO.BCM)
GPIO.setup(config.GPIO_LED_PIN, GPIO.OUT)

def handle(text):
    if "turn on the light" in text.lower():
        GPIO.output(config.GPIO_LED_PIN, GPIO.HIGH)
        return "Light turned on."
    elif "turn off the light" in text.lower():
        GPIO.output(config.GPIO_LED_PIN, GPIO.LOW)
        return "Light turned off."
    return None
