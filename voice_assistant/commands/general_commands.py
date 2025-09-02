import requests
import datetime

def handle(text):
    text = text.lower()
    
    # Name and identity
    if "your name" in text or "who are you" in text:
<<<<<<< HEAD
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
    
=======
        return "I am Pi Assistant, your intelligent voice assistant powered by Raspberry Pi and Gemini AI. How can I help you today?"
    
    # Greetings - use word boundaries to avoid false matches
    import re
    greeting_patterns = [
        r'\bhello\b', r'\bhi\b', r'\bhey\b', 
        r'\bgood morning\b', r'\bgood afternoon\b', r'\bgood evening\b'
    ]
    
    if any(re.search(pattern, text) for pattern in greeting_patterns):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            return "Good morning! How can I assist you today?"
        elif 12 <= hour < 17:
            return "Good afternoon! What can I help you with?"
        elif 17 <= hour < 22:
            return "Good evening! How may I help you?"
        else:
            return "Hello! I'm here to help. What do you need?"
    
    # Time
    if "time" in text and ("what" in text or "current" in text or "tell me" in text):
        now = datetime.datetime.now().strftime('%I:%M %p')
        return f"The current time is {now}."
    
    # Date
    if "date" in text and ("what" in text or "today" in text or "current" in text):
        today = datetime.datetime.now().strftime('%A, %B %d, %Y')
        return f"Today is {today}."
    
    # System status
    if "how are you" in text or "status" in text:
        return "I'm running perfectly on your Raspberry Pi! All systems are green and ready to help."
    
    # Help
    if "help" in text or "what can you do" in text or "capabilities" in text:
        return "I can control smart home devices, play music, check weather, answer questions using AI, tell you the time, and much more. I have Gemini AI integration for intelligent conversations. Try asking me anything!"
    
    # Shutdown/restart commands
    if "shutdown" in text or "turn off" in text and "system" in text:
        return "I cannot shut down the system for safety reasons. Please use the physical controls."
    
    # Thank you
    if "thank you" in text or "thanks" in text:
        return "You're very welcome! I'm always happy to help."
    
    # Goodbye
    if any(bye in text for bye in ["goodbye", "bye", "see you", "exit", "quit"]):
        return "Goodbye! Have a wonderful day!"
    
    # Let other modules or AI handle more complex queries
>>>>>>> master
    return None
