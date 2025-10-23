# Color Spaces Explained

## RGB (Red-Green-Blue)

**What it is:** Additive color model where colors are combinations of red, green, and blue light.

**Range:** 0-255 per channel (8-bit, standard)

**Representation:**
```cpp
CRGB color(255, 128, 0);  // R, G, B
// or
CRGB color = CRGB(0xFF8000);  // Hex format
```

**When to use:**
- Storing colors efficiently (3 bytes)
- Direct hardware control
- When you think in terms of "how bright is each component"
- Web colors and hex notation

**Strengths:**
- Natural for LEDs (direct mapping to hardware)
- Compact storage
- Fast mixing/blending

**Weaknesses:**
- Non-intuitive for humans (hard to adjust single attribute)
- Not perceptually uniform
- Hard to create palettes (hard to reason about color relationships)

**Examples:**
```cpp
CRGB red(255, 0, 0);
CRGB green(0, 255, 0);
CRGB blue(0, 0, 255);
CRGB white(255, 255, 255);
CRGB black(0, 0, 0);
CRGB orange(255, 165, 0);
```

## HSV (Hue-Saturation-Value)

**What it is:** Color model that separates color (hue) from intensity (saturation) and brightness (value).

**Range:**
- Hue: 0-255 (maps to 0-360°)
- Saturation: 0-255 (0=gray, 255=pure color)
- Value: 0-255 (0=black, 255=bright)

**Representation:**
```cpp
CHSV color(42, 255, 255);  // H, S, V
```

**When to use:**
- Designing palettes (manipulate hue while keeping saturation/brightness)
- Creating smooth color transitions
- When you think in terms of "color, how much color, how bright"
- Adjusting single color attributes

**Strengths:**
- Intuitive for humans (separate color from intensity)
- Easy palette generation (just adjust hue)
- Smooth gradients in HSV space
- Natural for rotating through colors

**Weaknesses:**
- Slightly slower conversions to RGB
- Less direct hardware control
- Takes marginally more logic to use

**Examples:**
```cpp
// All bright, saturated colors with different hues
CHSV red(0, 255, 255);      // Hue 0°
CHSV yellow(42, 255, 255);  // Hue 60°
CHSV green(85, 255, 255);   // Hue 120°
CHSV cyan(128, 255, 255);   // Hue 180°
CHSV blue(170, 255, 255);   // Hue 240°
CHSV magenta(213, 255, 255);// Hue 300°

// Same hue, different saturation
CHSV bright(85, 255, 255);  // Pure green
CHSV muted(85, 128, 255);   // Muted green
CHSV gray(85, 0, 255);      // White (desaturated)

// Same hue, different value
CHSV full(85, 255, 255);    // Bright green
CHSV medium(85, 255, 128);  // Medium green
CHSV dark(85, 255, 32);     // Dark green
CHSV off(85, 255, 0);       // Black (no brightness)
```

## HEX Notation

**What it is:** Hexadecimal representation of RGB, commonly used in web colors.

**Format:** 0xRRGGBB (6 hex digits)

**Representation:**
```cpp
CRGB red(0xFF0000);
CRGB lime(0x00FF00);
CRGB blue(0x0000FF);
CRGB orange(0xFFA500);
```

**Conversion from RGB:**
```
R=255, G=128, B=0
In hex: FF (255) 80 (128) 00 (0)
Result: 0xFF8000
```

## Conversions

### RGB ↔ HSV

FastLED provides built-in functions:

```cpp
// RGB to HSV
CHSV hsv = rgb2hsv_approximate(CRGB(255, 128, 0));
// Result: H≈42, S=255, V=255 (orange)

// HSV to RGB (automatic with CHSV)
CRGB rgb = CHSV(42, 255, 255);  // Orange
// Result: R=255, G≈170, B=0
```

**Approximate vs Exact:**
```cpp
rgb2hsv_approximate(color);  // Fast, slightly less accurate
rgb2hsv(color);               // Slower, more accurate (rarely needed)
```

### Manual Conversion (reference)

**RGB → HSV Algorithm:**
```
Max = max(R, G, B)
Min = min(R, G, B)
Δ = Max - Min

Value = Max / 255
Saturation = (Δ / Max) × 255  [if Max ≠ 0]

Hue calculation:
  if Max = R:  H = 60 × (((G - B) / Δ) mod 6)
  if Max = G:  H = 60 × (((B - R) / Δ) + 2)
  if Max = B:  H = 60 × (((R - G) / Δ) + 4)
```

**HSV → RGB Algorithm:**
```
C = Value × Saturation  (chroma)
H' = Hue / 60
X = C × (1 - |H' mod 2 - 1|)

Based on H':
  0 ≤ H' < 1: (R', G', B') = (C, X, 0)
  1 ≤ H' < 2: (R', G', B') = (X, C, 0)
  2 ≤ H' < 3: (R', G', B') = (0, C, X)
  3 ≤ H' < 4: (R', G', B') = (0, X, C)
  4 ≤ H' < 5: (R', G', B') = (X, 0, C)
  5 ≤ H' < 6: (R', G', B') = (C, 0, X)

Then add adjustment:
m = Value - C
(R, G, B) = (R' + m, G' + m, B' + m)
```

## FastLED Color Types

### CRGB
```cpp
CRGB color;           // Default black (0,0,0)
CRGB color(r, g, b);  // RGB values
CRGB color(0xRRGGBB); // Hex format
```
**Use when:** Working directly with RGB, storing color arrays, hardware output

### CHSV
```cpp
CHSV color;           // Default (0,0,0)
CHSV color(h, s, v);  // HSV values
```
**Use when:** Designing palettes, creating smooth transitions, manipulating colors programmatically

### Predefined Web Colors
```cpp
CRGB::Red
CRGB::Green
CRGB::Blue
CRGB::Yellow
CRGB::Magenta
CRGB::Cyan
CRGB::White
CRGB::Black
CRGB::Orange
// ... many more
```

## Choosing a Color Space

| Task | Best Space | Why |
|------|-----------|-----|
| Store final colors | RGB | Compact, direct to hardware |
| Design palette | HSV | Manipulate hue, saturation, value independently |
| Smooth gradient | HSV | Perceptually smoother transitions |
| Blend colors | RGB | Faster mixing |
| Fade brightness | HSV | Just adjust value |
| Create harmony | HSV | Hue relationships are clear |
| Color temperature | RGB | Direct control of red/blue balance |

## Practical Workflow

1. **Design phase**: Think in HSV (design palettes, relationships)
2. **Implementation**: Use CHSV for palettes and gradients
3. **Storage**: Convert to RGB if memory is tight
4. **Output**: Convert to RGB for hardware (automatic in FastLED)

```cpp
// Example: Design and animate
CHSV palette[] = {
  CHSV(0, 255, 255),    // Red
  CHSV(85, 255, 255),   // Green
  CHSV(170, 255, 255),  // Blue
};

// Convert to RGB if needed
CRGB leds[NUM_LEDS];
for(int i = 0; i < NUM_LEDS; i++) {
  leds[i] = palette[i % 3];  // Automatic HSV→RGB conversion
}
```
