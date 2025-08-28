import requests
import config

def handle(text):
    if "weather" in text.lower():
        url = f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={config.OPENWEATHER_API_KEY}&units=metric"
        r = requests.get(url)
        if r.ok:
            data = r.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"The weather in London is {desc} with a temperature of {temp}°C."
        return "Couldn't fetch weather."
    return None
