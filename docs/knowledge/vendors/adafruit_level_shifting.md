# Adafruit NeoPixel Level Shifting Guide

## Level Shifting Requirements

When connecting 3.3V logic sources (like ESP32-S3) to 5V NeoPixels, a level shifter is required.

## Recommended Component

**74AHCT125 - Quad Level-Shifter (3V to 5V)**

This component converts the 3.3V output signals to 5V signals needed by NeoPixel LED strips.

## Why Level Shifting Matters

NeoPixels typically operate at 5V logic levels. The ESP32-S3 operates at 3.3V. Without proper level shifting:
- Signal integrity may be compromised
- NeoPixels may not respond reliably
- Data corruption can occur during high-speed transitions

## Implementation Pattern

1. Connect ESP32-S3 GPIO (3.3V) to the input of the 74AHCT125
2. Connect 5V power to the 74AHCT125 VCC
3. Connect the output to NeoPixel data line (5V)
4. Add series resistor (100Ω typical) between shifter output and NeoPixel data input
5. Decouple 74AHCT125 with 0.1µF ceramic near VCC

## Alternative Level Shifters

- 74LVC125 (slower, but compatible)
- TXB0104 (more channels, lower power)
- Dedicated NeoPixel amplifier chips

## PCB Layout Considerations

- Keep level shifter close to NeoPixel connector
- Minimize trace lengths for signal integrity
- Separate 3.3V and 5V ground planes if possible
- Add 100nF bypass capacitors near each IC

Source: Adafruit NeoPixel Wiring Guide
