import time
import spidev

class ReSpeakerLEDs:
    def __init__(self):
        # Initialize SPI for APA102 LEDs on ReSpeaker
        try:
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)   # bus 0, device 0
            self.spi.max_speed_hz = 8000000
            self.num_leds = 3  # ReSpeaker 2-Mics has 3 LEDs
            print("✓ ReSpeaker LEDs initialized")
        except Exception as e:
            print(f"✗ LED initialization failed: {e}")
            self.spi = None
    
    def apa102_send_all(self, colors):
        """Send data to all APA102 LEDs"""
        if not self.spi:
            return
            
        try:
            # Start frame
            self.spi.xfer2([0x00, 0x00, 0x00, 0x00])
            
            # LED frames (brightness + BGR for each LED)
            for color in colors:
                brightness = 0xE0 | 0x1F  # Full brightness
                self.spi.xfer2([brightness, color[2], color[1], color[0]])  # BGR format
            
            # End frame
            self.spi.xfer2([0xFF, 0xFF, 0xFF, 0xFF])
        except Exception as e:
            print(f"LED error: {e}")
    
    def set_individual_colors(self, color1, color2, color3):
        """Set each LED to a different color"""
        colors = [color1, color2, color3]
        self.apa102_send_all(colors)
    
    def set_color_all(self, red, green, blue):
        """Set all 3 LEDs to the same color"""
        colors = [(red, green, blue)] * self.num_leds
        self.apa102_send_all(colors)
    
    def wake_word_animation(self):
        """Blue wave animation for wake word detection"""
        print("🔵 Wake word detected!")
        for cycle in range(3):  # 3 cycles of animation
            for step in range(6):  # 6 steps for smooth transition
                # Create a blue wave effect
                colors = []
                for i in range(3):
                    # Calculate intensity based on step and LED position
                    intensity = abs(((step + i) % 6) - 3) * 85  # 0 to 255
                    colors.append((0, 0, intensity))
                
                self.set_individual_colors(*colors)
                time.sleep(0.1)
    
    def listening_animation(self):
        """Green gradient while listening"""
        print("🟢 Listening...")
        # Create green gradient: bright -> medium -> dim
        self.set_individual_colors(
            (0, 255, 0),  # LED 1: Bright green
            (0, 180, 0),  # LED 2: Medium green  
            (0, 100, 0)   # LED 3: Dim green
        )
    
    def speaking_animation(self):
        """Orange flowing animation while speaking"""
        print("🟠 Speaking...")
        # Create flowing orange effect
        for cycle in range(2):  # 2 quick cycles
            for step in range(3):
                colors = [(0, 0, 0)] * 3  # Start with all off
                
                # Light up LEDs in sequence with orange gradient
                for i in range(3):
                    if (step + i) % 3 == 0:
                        colors[i] = (255, 165, 0)  # Bright orange
                    elif (step + i) % 3 == 1:
                        colors[i] = (200, 100, 0)  # Medium orange
                    else:
                        colors[i] = (100, 50, 0)   # Dim orange
                
                self.set_individual_colors(*colors)
                time.sleep(0.2)
    
    def error_animation(self):
        """Red pulsing animation for errors"""
        print("🔴 Error!")
        for pulse in range(3):
            # Pulse all LEDs red with different intensities
            self.set_individual_colors(
                (255, 0, 0),  # LED 1: Bright red
                (180, 0, 0),  # LED 2: Medium red
                (100, 0, 0)   # LED 3: Dim red
            )
            time.sleep(0.3)
            self.set_color_all(50, 0, 0)  # All dim red
            time.sleep(0.3)
        self.turn_off()
    
    def turn_off(self):
        """Turn off all LEDs"""
        self.set_color_all(0, 0, 0)
        print("⚫ LEDs off")
    
    def __del__(self):
        """Clean up SPI connection"""
        if self.spi:
            self.turn_off()
            self.spi.close()

# Global LED controller instance
led_controller = ReSpeakerLEDs()
