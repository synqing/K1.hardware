# Palette Design Patterns

## Pattern Categories

### 1. Monochromatic (Single Hue)
Same hue with varying saturation and brightness.

**Characteristics:**
- Harmonious, professional
- Limited visual excitement
- Good for subtle effects
- High cohesion

**Code:**
```cpp
CHSV monochromatic[] = {
  CHSV(85, 255, 255),  // Bright green
  CHSV(85, 255, 200),  // Medium-bright green
  CHSV(85, 200, 200),  // Medium green
  CHSV(85, 100, 150),  // Muted green
  CHSV(85, 0, 100),    // Gray-green
};

// Or shade variation
CHSV shades[] = {
  CHSV(85, 255, 255),  // Bright
  CHSV(85, 255, 200),  // Medium
  CHSV(85, 255, 100),  // Dark
};
```

**Best for:**
- Pulsing/breathing effects
- Gradients with one color family
- Professional, understated animations

---

### 2. Analogous (Neighboring Colors)
Adjacent colors on the color wheel (30-60° apart).

**Characteristics:**
- Natural, harmonious
- Flows smoothly
- Calming or warm depending on hue choice
- High visual comfort

**Code:**
```cpp
CHSV analogous_warm[] = {
  CHSV(0, 255, 255),     // Red (0°)
  CHSV(21, 255, 255),    // Red-orange (30°)
  CHSV(42, 255, 255),    // Orange (60°)
  CHSV(63, 255, 255),    // Yellow-orange (90°)
  CHSV(85, 255, 255),    // Yellow (120°)
};

CHSV analogous_cool[] = {
  CHSV(128, 255, 255),   // Cyan (180°)
  CHSV(149, 255, 255),   // Blue-cyan (210°)
  CHSV(170, 255, 255),   // Blue (240°)
  CHSV(191, 255, 255),   // Blue-magenta (270°)
  CHSV(213, 255, 255),   // Magenta (300°)
};

// Formula: base_hue ± 30°
```

**Best for:**
- Flowing animations
- Gradients that feel natural
- Calming effects (cool) or energetic (warm)
- Multi-color transitions

---

### 3. Complementary (Opposite Colors)
Colors opposite on the color wheel (180° apart).

**Characteristics:**
- High contrast, exciting
- Can look harsh at full saturation
- Vibrant and attention-grabbing
- Visual tension

**Code:**
```cpp
CHSV complementary[] = {
  CHSV(0, 255, 255),     // Red (0°)
  CHSV(128, 255, 255),   // Cyan (180°)
};

CHSV complementary_advanced[] = {
  CHSV(42, 255, 255),    // Orange (60°)
  CHSV(170, 255, 255),   // Blue (240°)
};

// Formula: base_hue + 128
```

**Best for:**
- High-contrast highlights
- Alerts and attention
- Dynamic, energetic effects
- Toggle/switch patterns

**Tip:** Lower saturation or value to reduce harshness:
```cpp
CHSV complementary_soft[] = {
  CHSV(0, 200, 240),     // Muted red
  CHSV(128, 200, 240),   // Muted cyan
};
```

---

### 4. Triadic (Evenly Spaced)
Three colors equally spaced around the wheel (120° apart).

**Characteristics:**
- Vibrant, balanced energy
- More complex than complementary
- Each color gets equal visual weight
- Dynamic but not chaotic

**Code:**
```cpp
CHSV triadic[] = {
  CHSV(0, 255, 255),     // Red (0°)
  CHSV(85, 255, 255),    // Green (120°)
  CHSV(170, 255, 255),   // Blue (240°)
};

CHSV triadic_warm[] = {
  CHSV(42, 255, 255),    // Orange (60°)
  CHSV(127, 255, 255),   // Green (180°)
  CHSV(212, 255, 255),   // Magenta (300°)
};

// Formula: base_hue, base_hue + 85, base_hue + 170
```

**Best for:**
- Complex multi-element animations
- Eye-catching displays
- Balanced, energetic effects
- RGB-based effects (natural fit)

---

### 5. Tetradic/Square (Four Colors)
Four colors forming a rectangle (two complementary pairs).

**Characteristics:**
- Rich, complex
- Requires careful balance
- Multiple focal points
- Sophisticated, busy

**Code:**
```cpp
CHSV tetradic[] = {
  CHSV(0, 255, 255),     // Red (0°)
  CHSV(85, 255, 255),    // Green (120°)
  CHSV(128, 255, 255),   // Cyan (180°) - complement of red
  CHSV(213, 255, 255),   // Magenta (300°) - complement of green
};

// Formula: base_hue, base_hue + 85, base_hue + 128, base_hue + 213
```

**Best for:**
- Full-featured complex displays
- Multiple independent elements
- Advanced animations

**Caution:** Needs careful brightness/saturation management:
```cpp
// Make it less overwhelming with reduced saturation
CHSV tetradic_balanced[] = {
  CHSV(0, 200, 240),
  CHSV(85, 200, 240),
  CHSV(128, 180, 240),
  CHSV(213, 180, 240),
};
```

---

### 6. Split-Complementary
Base hue + two neighbors of its complement.

**Characteristics:**
- High contrast without harshness
- Balanced energy
- Sophisticated feel
- Good harmony

**Code:**
```cpp
CHSV split_complementary[] = {
  CHSV(0, 255, 255),     // Base: Red
  CHSV(106, 255, 255),   // Complement-neighbor-1 (150°)
  CHSV(149, 255, 255),   // Complement-neighbor-2 (210°)
};

// Formula:
// base_hue
// (base_hue + 128 - 21) = complement - 30°
// (base_hue + 128 + 21) = complement + 30°
```

**Best for:**
- Sophisticated, balanced animations
- High contrast without harshness
- Modern, professional look

---

## Intensity Variations

All patterns can be modified by brightness and saturation:

### High Energy (Bright + Saturated)
```cpp
CHSV energetic[] = {
  CHSV(0, 255, 255),   // Brilliant
  CHSV(85, 255, 255),
};
// Use for: Alerts, action, excitement
```

### Medium Energy (Bright but Muted)
```cpp
CHSV balanced[] = {
  CHSV(0, 180, 255),   // Muted but bright
  CHSV(85, 180, 255),
};
// Use for: General animations, most effects
```

### Calm (Mid-Bright, Low Saturation)
```cpp
CHSV calm[] = {
  CHSV(0, 100, 200),   // Soft, gentle
  CHSV(85, 100, 200),
};
// Use for: Subtle effects, backgrounds
```

### Dramatic (Dark + Saturated)
```cpp
CHSV dramatic[] = {
  CHSV(0, 255, 100),   // Deep, rich
  CHSV(85, 255, 100),
};
// Use for: Moody, intense effects
```

---

## Temperature Combinations

### Warm + Cool (Dynamic)
```cpp
CHSV warm_cool[] = {
  CHSV(0, 255, 255),    // Red (warm)
  CHSV(170, 255, 255),  // Blue (cool)
};
// High visual tension, dynamic
```

### All Warm (Energetic)
```cpp
CHSV all_warm[] = {
  CHSV(0, 255, 255),    // Red
  CHSV(42, 255, 255),   // Orange
  CHSV(85, 255, 255),   // Yellow
};
// Cohesive, energetic, warm feel
```

### All Cool (Calm)
```cpp
CHSV all_cool[] = {
  CHSV(128, 255, 255),  // Cyan
  CHSV(170, 255, 255),  // Blue
  CHSV(213, 255, 255),  // Magenta
};
// Cohesive, calm, cool feel
```

---

## Practical Generation

### Random Palette (High Contrast)
```cpp
CHSV random_palette[5];
for(int i = 0; i < 5; i++) {
  random_palette[i] = CHSV(random8() * 51, 255, 255); // Evenly spaced random hues
}
```

### Rotating Hue (Rainbow)
```cpp
CHSV rainbow[256];
for(int h = 0; h < 256; h++) {
  rainbow[h] = CHSV(h, 255, 255);  // All hues, full saturation/brightness
}
```

### Fade to White
```cpp
CHSV fade_white[] = {
  CHSV(42, 255, 255),   // Bright orange
  CHSV(42, 200, 255),   // Orange
  CHSV(42, 100, 255),   // Desaturating orange
  CHSV(42, 0, 255),     // White
};
```

---

## Choosing a Palette Pattern

| Effect Needed | Best Pattern | Mood |
|--------------|-------------|------|
| Professional, subtle | Monochromatic or Analogous | Calm, cohesive |
| Dynamic, exciting | Complementary or Triadic | Vibrant, energetic |
| High contrast | Complementary or Split-Complementary | Alert, striking |
| Natural, flowing | Analogous | Organic, smooth |
| Complex, balanced | Tetradic or Split-Complementary | Sophisticated |
| Rainbow effect | Multi-hue progression | Playful, diverse |
