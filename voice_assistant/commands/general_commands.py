import requests
import datetime

def handle(text):
    text = text.lower()
    
    # Name and identity
    if "your name" in text or "who are you" in text:
        return "I am your voice assistant. You can call me Pi Assistant."
    
    # Greetings
    if "hello" in text or "hi" in text or "hey" in text:
        return "Hello! How can I help you today?"
    
    # Time
    if "time" in text or "what time is it" in text:
        now = datetime.datetime.now().strftime('%H:%M')
        return f"The time is {now}."
    
    # Date
    if "date" in text or "what day is it" in text:
        today = datetime.datetime.now().strftime('%A, %B %d, %Y')
        return f"Today is {today}."
    
    # Wikipedia
    if "wikipedia" in text:
        try:
            import wikipedia
            query = text.replace("wikipedia", "").strip()
            summary = wikipedia.summary(query, sentences=1)
            return summary
        except Exception:
            return "Sorry, I couldn't fetch Wikipedia info."
    
    # News
    if "news" in text:
        return "Sorry, news feature not implemented yet."
    
    # Help
    if "help" in text or "what can you do" in text:
        return "I can tell you the time, control lights, play music, check weather, and answer questions. Try saying 'turn on the light' or 'what time is it'."
    
    return None
