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
            print("✅ ReSpeaker LEDs initialized")
        except Exception as e:
            print(f"❌ LED initialization failed: {e}")
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
        """Enhanced blue wave animation for wake word detection"""
        print("🔵 Wake word detected!")
        for cycle in range(4):  # 4 cycles of animation
            for step in range(9):  # 9 steps for smoother transition
                colors = []
                for i in range(3):
                    # Create a more dynamic wave with different intensities
                    wave_position = (step + i * 3) % 9
                    if wave_position < 3:
                        # Bright blue wave
                        intensity = int(255 * (wave_position + 1) / 3)
                        colors.append((0, 50, intensity))  # Add slight green for cyan effect
                    elif wave_position < 6:
                        # Peak brightness with white-blue
                        intensity = 255
                        colors.append((20, 100, intensity))  # Bright cyan-blue
                    else:
                        # Fade out
                        intensity = int(255 * (9 - wave_position) / 3)
                        colors.append((0, 0, intensity))
                
                self.set_individual_colors(*colors)
                time.sleep(0.08)
    
    def listening_animation(self):
        """Enhanced green breathing animation while listening"""
        print("🟢 Listening...")
        # Breathing effect with green gradient
        for breath in range(3):  # 3 breathing cycles
            # Breathe in - increasing brightness
            for intensity in range(50, 256, 25):
                self.set_individual_colors(
                    (0, intensity, 0),           # LED 1: Main green
                    (0, max(0, intensity-30), 0), # LED 2: Slightly dimmer
                    (0, max(0, intensity-60), 0)  # LED 3: Dimmest
                )
                time.sleep(0.05)
            
            # Breathe out - decreasing brightness
            for intensity in range(255, 49, -25):
                self.set_individual_colors(
                    (0, intensity, 0),           # LED 1: Main green
                    (0, max(0, intensity-30), 0), # LED 2: Slightly dimmer
                    (0, max(0, intensity-60), 0)  # LED 3: Dimmest
                )
                time.sleep(0.05)

    def speaking_animation(self):
        """Enhanced orange/yellow flowing animation while speaking"""
        print("🟡 Speaking...")
        # Create a dynamic flowing effect with warm colors
        for cycle in range(3):  # 3 cycles
            for step in range(6):
                colors = []
                for i in range(3):
                    # Create flowing warm color effect
                    position = (step + i * 2) % 6
                    if position == 0:
                        colors.append((255, 200, 0))    # Bright yellow-orange
                    elif position == 1:
                        colors.append((255, 150, 0))    # Orange
                    elif position == 2:
                        colors.append((255, 100, 0))    # Deep orange
                    elif position == 3:
                        colors.append((200, 50, 0))     # Red-orange
                    elif position == 4:
                        colors.append((150, 25, 0))     # Dim red-orange
                    else:
                        colors.append((100, 0, 0))      # Very dim red
                
                self.set_individual_colors(*colors)
                time.sleep(0.15)
    
    def error_animation(self):
        """Enhanced red warning animation for errors"""
        print("🔴 Error!")
        for pulse in range(4):  # 4 pulses
            # Flash all LEDs bright red with different patterns
            if pulse % 2 == 0:
                self.set_individual_colors(
                    (255, 0, 0),  # LED 1: Bright red
                    (150, 0, 0),  # LED 2: Medium red
                    (100, 0, 0)   # LED 3: Dim red
                )
            else:
                self.set_individual_colors(
                    (100, 0, 0),  # LED 1: Dim red
                    (255, 0, 0),  # LED 2: Bright red
                    (150, 0, 0)   # LED 3: Medium red
                )
            time.sleep(0.2)
            
            # Brief off period
            self.set_color_all(20, 0, 0)  # Very dim red
            time.sleep(0.1)
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