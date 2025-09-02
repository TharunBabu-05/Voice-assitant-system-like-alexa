#!/usr/bin/env python3
"""
Setup script for Gemini AI integration
"""

import os
import sys

def setup_gemini_api():
    print("🤖 Gemini AI Setup")
    print("=" * 50)
    print()
    print("To use Gemini AI with your voice assistant, you need an API key.")
    print()
    print("Steps to get your Gemini API key:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account (the one with Gemini Premium)")
    print("3. Click Create API Key")
    print("4. Copy the generated API key")
    print()
    
    api_key = input("Enter your Gemini API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Save to environment variable file
        env_file = ".env"
        with open(env_file, "w") as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
        
        # Also update config.py
        config_file = "config.py"
        with open(config_file, "r") as f:
            content = f.read()
        
        # Replace the API key line
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("GEMINI_API_KEY"):
                lines[i] = f"GEMINI_API_KEY = \"{api_key}\""
                break
        
        with open(config_file, "w") as f:
            f.write("\n".join(lines))
        
        print("✅ API key saved successfully!")
        print("🎉 Your assistant now has AI superpowers!")
        print()
        print("Try asking questions like:")
        print("- Hey Pi, what is the capital of France?")
        print("- Hey Pi, explain quantum physics")
        print("- Hey Pi, tell me a joke")
        print("- Hey Pi, how do solar panels work?")
        
    else:
        print("⚠️  Skipping AI setup. You can run this script again later.")
        print("The assistant will work with basic commands only.")

if __name__ == "__main__":
    setup_gemini_api()

