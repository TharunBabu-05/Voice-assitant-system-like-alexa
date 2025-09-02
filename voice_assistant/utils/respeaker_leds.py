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
            
            # LED data
            for color in colors:
                brightness = 0xFF  # Max brightness
                blue = color & 0xFF
                green = (color >> 8) & 0xFF
                red = (color >> 16) & 0xFF
                
                # APA102 format: [brightness, blue, green, red]
                self.spi.xfer2([brightness, blue, green, red])
            
            # End frame
            self.spi.xfer2([0xFF, 0xFF, 0xFF, 0xFF])
            
        except Exception as e:
            print(f"LED error: {e}")

    def turn_off(self):
        """Turn off all LEDs"""
        colors = [0x000000] * self.num_leds  # All black
        self.apa102_send_all(colors)

    def set_solid_color(self, color):
        """Set all LEDs to the same solid color"""
        colors = [color] * self.num_leds
        self.apa102_send_all(colors)

    def wake_word_animation(self):
        """Quick blue flash for wake word detection"""
        print("🔵 Wake word detected - Blue flash")
        
        # Quick blue flash - no delay
        self.set_solid_color(0x0066FF)  # Blue
        time.sleep(0.1)  # Very brief flash

    def listening_animation(self):
        """Solid green during recording - no animation delay"""
        print("🟢 Recording - Green LED")
        
        # Solid green - no breathing animation to avoid delays
        self.set_solid_color(0x00FF00)  # Solid green

    def speaking_animation(self):
        """Enhanced orange/yellow flowing animation while speaking/processing"""
        print("🟡 Speaking/Processing - Orange flowing animation")
        
        # Flowing orange/yellow pattern
        for cycle in range(4):  # Multiple cycles for longer responses
            for i in range(self.num_leds * 3):
                colors = [0x000000] * self.num_leds
                
                # Create flowing pattern
                for led in range(self.num_leds):
                    phase = (i + led) % (self.num_leds * 2)
                    if phase < self.num_leds:
                        # Orange to yellow gradient
                        intensity = min(255, max(0, 255 - abs(phase - self.num_leds//2) * 60))
                        red = intensity
                        green = intensity // 2
                        colors[led] = (red << 16) | (green << 8)  # Orange/yellow
                
                self.apa102_send_all(colors)
                time.sleep(0.06)

    def error_animation(self):
        """Enhanced red warning animation for errors"""
        print("🔴 Error - Red warning animation")
        
        # Pulsing red warning
        for pulse in range(3):
            # Quick flash
            self.set_solid_color(0xFF0000)  # Bright red
            time.sleep(0.1)
            self.set_solid_color(0x330000)  # Dim red
            time.sleep(0.1)
        
        # Fade out
        for intensity in range(51, 0, -5):
            color = intensity << 16  # Red channel
            self.set_solid_color(color)
            time.sleep(0.05)

    def success_animation(self):
        """Green success animation"""
        print("✅ Success - Green confirmation")
        
        # Quick green flash
        self.set_solid_color(0x00FF00)  # Bright green
        time.sleep(0.2)
        self.set_solid_color(0x003300)  # Dim green
        time.sleep(0.1)
        self.turn_off()

    def rainbow_animation(self, duration=3):
        """Fun rainbow animation"""
        print("🌈 Rainbow animation")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            for hue in range(0, 360, 30):
                colors = []
                for i in range(self.num_leds):
                    # Convert HSV to RGB
                    color = self._hsv_to_rgb((hue + i * 120) % 360, 1.0, 1.0)
                    colors.append(color)
                
                self.apa102_send_all(colors)
                time.sleep(0.1)

    def _hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB color"""
        h = h / 360.0
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        elif i == 5:
            r, g, b = v, p, q
        
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        
        return (r << 16) | (g << 8) | b

    def cleanup(self):
        """Clean up SPI resources"""
        self.turn_off()
        if self.spi:
            self.spi.close()

# Create global LED controller instance
try:
    led_controller = ReSpeakerLEDs()
except Exception as e:
    print(f"❌ Failed to initialize LED controller: {e}")
    # Create dummy controller for systems without LEDs
    class DummyLEDs:
        def __getattr__(self, name):
            def dummy_method(*args, **kwargs):
                print(f"LED: {name} (dummy)")
            return dummy_method
    
    led_controller = DummyLEDs()
