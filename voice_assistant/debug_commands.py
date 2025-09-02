#!/usr/bin/env python3
"""
Debug script to test command handling and AI logic
"""

# Add the current directory to the path so we can import the modules
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commands import general_commands, gpio_control, music_player, weather
from ai.gemini_ai import should_use_ai, get_ai_response, initialize_gemini
import config

def test_command_handling(text):
    print(f"\n=== Testing: '{text}' ===")
    
    # Test each command handler
    response = general_commands.handle(text)
    print(f"general_commands.handle(): {response}")
    
    if response is None:
        response = gpio_control.handle(text)
        print(f"gpio_control.handle(): {response}")
    
    if response is None:
        response = music_player.handle(text)
        print(f"music_player.handle(): {response}")
    
    if response is None:
        response = weather.handle(text)
        print(f"weather.handle(): {response}")
    
    # Test AI logic
    if response is None:
        should_ai = should_use_ai(text)
        print(f"should_use_ai(): {should_ai}")
        
        if should_ai:
            print("🧠 Would use AI to respond...")
            ai_response = get_ai_response(text)
            print(f"AI response: {ai_response}")
        else:
            print("❌ AI would not be used")
            response = "Sorry, I didn't understand that command."
            print(f"Fallback response: {response}")

if __name__ == "__main__":
    # Initialize Gemini AI first
    print("🤖 Initializing Gemini AI...")
    initialize_gemini(config.GEMINI_API_KEY)
    
    # Test the exact query that was heard
    test_command_handling("what is the best thing in the world")
    
    # Test a few other queries
    test_command_handling("hello")
    test_command_handling("what time is it")
    test_command_handling("tell me about cats")
