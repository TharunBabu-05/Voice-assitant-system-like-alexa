# ReSpeaker LED System Documentation

## Overview
The ReSpeaker 2-Mic Hat has 3 RGB LEDs that can display different colors and patterns to indicate the voice assistant state.

## LED States

### 🔵 Wake Word Detection (Blue Wave)
- **Trigger**: When "Hey Pi" is detected
- **Pattern**: Flowing cyan-blue wave animation
- **Duration**: 4 cycles with smooth transitions
- **Colors**: Blue with cyan highlights, moving across LEDs

### 🟢 Listening (Green Breathing)
- **Trigger**: When assistant is listening for voice commands
- **Pattern**: Breathing effect with green gradient
- **Duration**: 3 breathing cycles
- **Colors**: Bright green → medium green → dim green

### 🟡 Speaking/Processing (Orange Flow)
- **Trigger**: When assistant is processing or speaking response
- **Pattern**: Dynamic flowing warm colors
- **Duration**: 3 cycles with 6 steps each
- **Colors**: Yellow-orange → orange → deep orange → red-orange

### �� Error (Red Warning)
- **Trigger**: When assistant doesn_t understand or encounters error
- **Pattern**: Alternating red flash with different intensities
- **Duration**: 4 pulses with brief off periods
- **Colors**: Bright red → medium red → dim red (alternating pattern)

### ⚫ Off (Idle)
- **Trigger**: Default state and after completing responses
- **Pattern**: All LEDs turned off
- **Colors**: None (all LEDs off)

## Technical Details

### Hardware
- 3 x APA102 RGB LEDs
- SPI communication (bus 0, device 0)
- 8MHz SPI speed
- Individual LED control with brightness

### LED Positioning
- LED 1: Usually brightest in patterns
- LED 2: Medium brightness
- LED 3: Dimmest for gradient effects

### Color Format
- RGB values (0-255 for each color)
- Format: (Red, Green, Blue)
- Example: (255, 0, 0) = Bright Red

## Testing
Run the test script to see all animations:
```bash
python3 test_led_animations.py
```

## Customization
You can modify the LED patterns by editing:
- `utils/respeaker_leds.py` - LED animations and colors
- Timing values (time.sleep() calls)
- Color values in RGB tuples
- Animation cycles and steps

