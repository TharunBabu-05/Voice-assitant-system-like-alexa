import requests
import datetime
import re

def handle(text):
    text = text.lower()
    
    # Remove name/identity handling - let AI handle all name-related questions
    # This ensures conversation memory works properly
    
    # Greetings - use word boundaries to avoid false matches
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
    
    # Time - make more specific to avoid false matches
    time_patterns = [
        "what time is it", "current time", "tell me the time", 
        "what is the time", "time is it"
    ]
    if any(pattern in text for pattern in time_patterns):
        now = datetime.datetime.now().strftime('%I:%M %p')
        return f"The current time is {now}."
    
    # Date - make more specific to avoid false matches  
    date_patterns = [
        "what date is it", "current date", "tell me the date",
        "what is the date", "today's date", "what day is it"
    ]
    if any(pattern in text for pattern in date_patterns):
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
    return None
