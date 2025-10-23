# Debugging Color Issues

## Systematic Troubleshooting

### Issue: Colors Look Wrong (Unexpected Colors)

**Check 1: Color Order**
```cpp
// Your LED type determines color order
FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);    // RGB order
FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);    // GRB order
FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, BGR>(leds, NUM_LEDS); // BGR order

// If colors are swapped, try different order
// Red appearing as Blue? Likely wrong color order
```

**Diagnosis:**
```cpp
// Set a single known color and observe
leds[0] = CRGB::Red;
FastLED.show();
// If appears blue or green, color order is wrong
```

---

### Issue: Colors Look Washed Out / Desaturated

**Likely Causes:**
1. Saturation set to 0 (in HSV mode)
2. Brightness too low
3. Gamma correction applied incorrectly
4. Power supply insufficient (colors dim with low power)

**Debug:**
```cpp
// Test with maximum saturation and brightness
CHSV test_color(42, 255, 255);  // Bright orange
leds[0] = test_color;
FastLED.show();

// If still washed out, likely power issue or gamma
```

**Solution:**
```cpp
// Increase saturation explicitly
CHSV vibrant(42, 255, 255);  // Full saturation

// If using HSV, ensure value is high
// If using RGB, avoid mixing with white
CRGB pure_orange(255, 165, 0);
CRGB not_recommended(200, 140, 100);  // Washed out due to RGB mixing
```

---

### Issue: Brightness Inconsistent (Some LEDs Appear Dimmer)

**Likely Causes:**
1. Insufficient power delivery
2. Data line signal degradation (too many LEDs)
3. Capacitor not properly sized
4. Gamma correction applied unevenly

**Debug:**
```cpp
// Test with all LEDs set to same color
fill_solid(leds, NUM_LEDS, CRGB::White);
FastLED.show();

// If some are dimmer, power issue likely
// If brightness inconsistency is color-specific, gamma issue
```

**Solution:**
```cpp
// Add decoupling capacitor (100µF) across power lines
// Add series resistor (470Ω) on data line to reduce reflections
// Reduce total number of LEDs if possible
// Increase power budget
```

---

### Issue: Colors Flicker or Unstable

**Likely Causes:**
1. Refresh rate too fast (overwhelming LEDs)
2. Insufficient power causing voltage drops
3. Data line noise from nearby electronics
4. Incorrect pin configuration

**Debug:**
```cpp
// Slow down animation refresh
void loop() {
  animation();
  FastLED.show();
  delay(50);  // Try slower refresh
}

// Single color test
fill_solid(leds, NUM_LEDS, CRGB::White);
FastLED.show();
delay(100);

// If still flickering, likely power/hardware issue
```

**Solution:**
```cpp
// Add delay between update and show
FastLED.show();
delay(1000 / FRAMES_PER_SECOND);  // Control refresh rate

// Use FastLED's built-in timing
EVERY_N_MILLISECONDS(30) {
  animation();
  FastLED.show();
}
```

---

### Issue: Banding Visible (Posterization, Stepped Gradients)

**Likely Causes:**
1. Gradient in RGB space instead of HSV
2. Not enough color steps in gradient
3. 8-bit color depth insufficient for smooth transition

**Debug:**
```cpp
// Compare RGB gradient vs HSV gradient
// RGB gradient (steppy)
CRGB rgb_gradient[] = {
  CRGB(255, 0, 0),
  CRGB(0, 255, 0),
};
fill_gradient_RGB(leds, NUM_LEDS, CRGB::Red, CRGB::Green);

// HSV gradient (smooth)
fill_gradient(leds, NUM_LEDS, CHSV(0, 255, 255), CHSV(85, 255, 255), SHORTEST_HUES);
```

**Solution:**
```cpp
// Use HSV color space for gradients
fill_gradient(leds, NUM_LEDS,
  CHSV(0, 255, 255),      // Start: red
  CHSV(85, 255, 255),     // End: green
  SHORTEST_HUES);         // Use shorter path around wheel

// Or blend in HSV before converting to RGB
CHSV hsv_leds[NUM_LEDS];
fill_gradient(hsv_leds, NUM_LEDS, CHSV(0, 255, 255), CHSV(85, 255, 255), SHORTEST_HUES);
// Convert to RGB when needed
for(int i = 0; i < NUM_LEDS; i++) {
  leds[i] = hsv_leds[i];
}
```

---

### Issue: Red Tones Look Orange, Blue Tones Look Purple

**Likely Causes:**
1. Gamma correction mismatch
2. Color temperature sensitivity in your perception
3. Insufficient saturation

**Debug:**
```cpp
// Test pure colors
CHSV pure_red(0, 255, 255);
CHSV pure_blue(170, 255, 255);
leds[0] = pure_red;
leds[1] = pure_blue;
FastLED.show();
```

**Solution:**
```cpp
// Adjust hue slightly if perception differs
// Red shift: use slightly lower hue value
CHSV adjusted_red(250, 255, 255);  // Shift back from orange

// Or ensure gamma tables are applied correctly
const uint8_t gamma8[] = { /* proper gamma table */ };
// Apply to individual channels
```

---

### Issue: Animation Looks Sluggish / Low Frame Rate

**Likely Causes:**
1. Color calculations too expensive
2. Frequent HSV↔RGB conversions
3. Palette lookups inefficient
4. Memory allocation in loops

**Debug:**
```cpp
// Monitor FPS with Serial output
uint32_t last_show = millis();
FastLED.show();
uint32_t show_time = millis() - last_show;
Serial.println(show_time);  // Should be < 5ms for 30+ FPS
```

**Solution:**
```cpp
// Pre-calculate colors
CHSV palette[] = { /* pre-calculated */ };
// Use palette indices instead of calculating each frame

// Pre-allocate arrays
CRGB leds[NUM_LEDS];  // Not in loop

// Use faster color functions
rgb2hsv_approximate(color);  // Instead of rgb2hsv()

// Reduce FastLED's internal processing
FastLED.setMaxPowerInVolts(5);
FastLED.setCorrection(TypicalPixelStrip);  // Faster than other corrections
```

---

## Diagnostic LED Test

```cpp
void diagnostic_test() {
  // Test 1: Pure red
  fill_solid(leds, NUM_LEDS, CRGB::Red);
  FastLED.show();
  delay(1000);

  // Test 2: Pure green
  fill_solid(leds, NUM_LEDS, CRGB::Green);
  FastLED.show();
  delay(1000);

  // Test 3: Pure blue
  fill_solid(leds, NUM_LEDS, CRGB::Blue);
  FastLED.show();
  delay(1000);

  // Test 4: White (all channels)
  fill_solid(leds, NUM_LEDS, CRGB::White);
  FastLED.show();
  delay(1000);

  // Test 5: Off (all black)
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
  delay(1000);
}
```

**Interpretation:**
- If all colors look the same → Color order likely wrong
- If colors are dim → Power issue likely
- If specific colors flicker → Data line noise or power issue
- If brightness varies across strip → Power delivery issue

---

## Quick Checklist

- [ ] Correct color order (RGB, GRB, BGR)?
- [ ] Saturation > 0 (not grayscale)?
- [ ] Brightness/Value > 0 (not black)?
- [ ] Power supply adequate for number of LEDs?
- [ ] Decoupling capacitor present (100µF)?
- [ ] Series resistor on data line (470Ω)?
- [ ] Gamma correction applied correctly?
- [ ] Data line properly terminated?
- [ ] Refresh rate not too fast?
- [ ] No power hungry operations in loop?
