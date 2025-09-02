#!/usr/bin/env python3
"""
Test script to demonstrate LED animations
"""
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.respeaker_leds import led_controller

def test_leds():
    print("Testing LED animations...")
    
    print("1. Wake word (Blue wave)")
    led_controller.wake_word_animation()
    time.sleep(1)
    
    print("2. Listening (Green breathing)")
    led_controller.listening_animation()
    time.sleep(1)
    
    print("3. Speaking (Orange flow)")
    led_controller.speaking_animation()
    time.sleep(1)
    
    print("4. Error (Red warning)")
    led_controller.error_animation()
    time.sleep(1)
    
    print("5. Individual colors")
    led_controller.set_individual_colors((255,0,0), (0,255,0), (0,0,255))
    time.sleep(1)
    led_controller.turn_off()
    
if __name__ == "__main__":
    test_leds()

