"""
Gemini AI Integration for Voice Assistant
"""

import os
import json
import requests
from datetime import datetime

class GeminiAI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("Warning: No Gemini API key provided")
            self.enabled = False
        else:
            self.enabled = True
            print("Gemini AI initialized")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        self.system_prompt = """You are Pi Assistant, a helpful voice assistant on Raspberry Pi. 
        Provide concise, spoken-friendly responses (2-3 sentences max).
        Keep responses natural and conversational."""
        
        # Conversation memory - stores recent conversation history
        self.conversation_history = []
        self.max_history = 10  # Keep last 10 exchanges

    def generate_response(self, user_input, context=None):
        if not self.enabled:
            return None
            
        try:
            current_time = datetime.now().strftime("%A, %B %d, %Y at %H:%M")
            
            prompt = f"{self.system_prompt}\n\n"
            prompt += f"Current time: {current_time}\n"
            
            if context:
                prompt += f"Context: {context}\n"
            
            # Add conversation history for context
            if self.conversation_history:
                prompt += "\nRecent conversation:\n"
                for exchange in self.conversation_history[-5:]:  # Last 5 exchanges
                    prompt += f"User: {exchange['user']}\n"
                    prompt += f"Assistant: {exchange['assistant']}\n"
                prompt += "\n"
            
            prompt += f"User: {user_input}\n\nResponse:"
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 200
                }
            }
            
            headers = {"Content-Type": "application/json"}
            url = f"{self.base_url}?key={self.api_key}"
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and len(result["candidates"]) > 0:
                    ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
                    ai_response = ai_response.strip()
                    
                    # Store the conversation in memory
                    self.add_to_conversation_history(user_input, ai_response)
                    
                    return ai_response
            
            return "Sorry, I am having trouble thinking right now."
                
        except Exception as e:
            print(f"AI Error: {e}")
            return "Sorry, I encountered an error."

    def add_to_conversation_history(self, user_input, ai_response):
        """Add a conversation exchange to memory"""
        self.conversation_history.append({
            'user': user_input,
            'assistant': ai_response,
            'timestamp': datetime.now()
        })
        
        # Keep only the most recent exchanges
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def clear_conversation_history(self):
        """Clear conversation memory"""
        self.conversation_history = []
        print("🧠 Conversation memory cleared")

    def is_ai_appropriate_query(self, text):
        text_lower = text.lower()
        
        # Skip hardware commands
        hardware_commands = ["turn on", "turn off", "light", "led", "play music", "weather"]
        for cmd in hardware_commands:
            if cmd in text_lower:
                return False
        
        # Use AI for questions and conversations
        ai_triggers = ["what is", "how do", "why", "tell me", "explain", "calculate", 
                      "my name", "remember", "do you know", "who am i", "what am i"]
        for trigger in ai_triggers:
            if trigger in text_lower:
                return True
        
        # Use AI for longer queries
        return len(text.split()) > 3

# Global instance
gemini_ai = None

def initialize_gemini(api_key=None):
    global gemini_ai
    gemini_ai = GeminiAI(api_key)
    return gemini_ai

def get_ai_response(user_input, context=None):
    if gemini_ai and gemini_ai.enabled:
        return gemini_ai.generate_response(user_input, context)
    return None

def should_use_ai(user_input):
    if gemini_ai and gemini_ai.enabled:
        return gemini_ai.is_ai_appropriate_query(user_input)
    return False

