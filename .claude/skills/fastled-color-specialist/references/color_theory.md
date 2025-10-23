# Color Theory for LED Animations

## The Color Wheel

Colors exist on a circular spectrum, where:
- **Red (0°)**: High energy, arousal, danger, passion
- **Yellow (60°)**: Warmth, joy, optimism
- **Green (120°)**: Nature, growth, calm, safety
- **Cyan (180°)**: Cool, fresh, clarity
- **Blue (240°)**: Trust, stability, sadness
- **Magenta (300°)**: Mystery, magic, creativity

In FastLED's HSV system: 0-255 maps to 0-360°, so divide by 255 and multiply by 360 to convert.

## Perception & Psychology

### Saturation Impact
- **High saturation (255)**: Vibrant, energetic, attention-grabbing
- **Mid saturation (128)**: Balanced, natural-looking
- **Low saturation (<64)**: Muted, calm, sophisticated

### Brightness/Value Impact
- **Full brightness (255)**: Intense, energetic, can be harsh
- **Mid brightness (200)**: Comfortable, most pleasant for sustained viewing
- **Low brightness (100-150)**: Intimate, dramatic

### Color Psychology

**Warm colors (Red, Orange, Yellow):**
- Increase perceived temperature
- Draw attention, energize
- Associated with action, excitement, danger
- Best for alerts, highlights, dynamic effects

**Cool colors (Blue, Cyan, Green):**
- Perceived as calming
- Recede visually (feel farther away)
- Associated with stability, trust, nature
- Best for backgrounds, sustained animations

**Neutral transitions:**
- White/near-white → perceived as calm, clean
- Black/off → mysterious, dramatic endings

## Harmony Rules

### Complementary (2-color contrast)
- **Formula**: Hue + 128 (opposite on wheel)
- **Psychological**: High contrast, exciting, can clash
- **Best for**: Highlights, alerts, dramatic effects
- **Caution**: Can be tiring if both at high saturation and brightness

### Analogous (3-color harmony)
- **Formula**: Pick base hue, ±30° on each side
- **Psychological**: Harmonious, pleasing, cohesive
- **Best for**: Gradients, flowing animations, professional look
- **Always works**: These colors naturally look good together

### Triadic (3-color balanced energy)
- **Formula**: Hue, Hue+120°, Hue+240° (3 equal points)
- **Psychological**: Vibrant but balanced
- **Best for**: Dynamic animations with multiple elements
- **Visual weight**: Each color gets equal attention

### Tetradic/Square (4-color complex)
- **Formula**: Two complementary pairs (Hue, Hue+120°, Hue+180°, Hue+300°)
- **Psychological**: Complex, rich, requires skill to balance
- **Best for**: Advanced animations, full-featured displays
- **Visual weight**: Needs careful brightness management

## Saturation + Brightness Combinations

Different combinations create different moods:

| Saturation | Brightness | Feel | Use Case |
|-----------|----------|------|----------|
| High | High | Intense, harsh | Alerts, highlights |
| High | Medium | Vibrant, energetic | Dynamic animations |
| High | Low | Deep, dramatic | Moody effects |
| Medium | High | Pleasant, bright | Most animations |
| Medium | Medium | Balanced, natural | General animations |
| Medium | Low | Intimate, elegant | Calm effects |
| Low | High | Pale, washed | Backgrounds, overlays |
| Low | Medium | Muted, sophisticated | Subtle effects |
| Low | Low | Dull, dark | Very dramatic moments |

## Color Temperature (Warm vs Cool)

**Warm colors (Red → Yellow)**
- Perceived as energetic
- Make objects appear closer
- Associated with fire, sun, warmth
- HSV hue range: 0-60°

**Cool colors (Cyan → Magenta)**
- Perceived as calm
- Make objects appear farther
- Associated with ice, water, cool air
- HSV hue range: 120-240°

**Neutral (Green)**
- Balanced temperature
- Natural, organic
- HSV hue: 120°

Mixing warm and cool colors in same animation creates visual tension (useful for drama) or visual harmony (if balanced carefully).

## Contrast & Visibility

**Luminance contrast** (perceived brightness difference) matters more than hue:
- Blue + Yellow = high contrast (easy to read)
- Red + Green = medium contrast (colorblind issue)
- Red + Blue = low contrast (hard to distinguish)

**For accessibility:**
- Use brightness differences in addition to color
- Avoid pure red + green combinations
- Include white or black boundaries between colors

## Color Mixing in Light

Unlike paint, light colors mix additively:
- Red + Green light = Yellow light
- Red + Blue light = Magenta light
- Red + Green + Blue light = White light

This means:
- Overlapping LED colors blend (important for addressable LEDs)
- High saturation colors remain pure
- Low saturation colors approach white

## Perception Over Distance

Color perception changes with distance:
- **Close viewing**: Fine details visible, saturation matters
- **Distance**: Brightness dominates, colors blur/merge
- **Very far**: Only overall brightness perceived

For distance viewing, increase brightness/value and decrease saturation.

## Color in Context

The same color looks different depending on surroundings:
- Color surrounded by brighter colors appears darker
- Color surrounded by darker colors appears brighter
- Color surrounded by similar hues appears more saturated
- Color surrounded by complementary hues appears more vibrant

This means your animation context matters - test colors in context of surrounding elements.
