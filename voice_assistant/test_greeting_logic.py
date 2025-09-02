#!/usr/bin/env python3

text = "what is the best thing in the world"
text = text.lower()

greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]

print(f"Testing text: '{text}'")
for greeting in greetings:
    if greeting in text:
        print(f"✅ Found greeting: '{greeting}' in text")
    else:
        print(f"❌ '{greeting}' not in text")

# Test the any() logic
result = any(greeting in text for greeting in greetings)
print(f"\nResult of any(): {result}")
