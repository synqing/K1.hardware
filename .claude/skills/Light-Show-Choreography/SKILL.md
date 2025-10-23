---
name: Light-Show-Choreography
keywords: animation, choreography, effect, transition, mode, blend, state machine, easing, fade, crossfade, beat sync, tempo sync, layer, composition, timing
---

# Light Show Choreography

## Quick Reference

Choreography is the orchestration of visual effects with precise timing, synchronization to audio events, and smooth transitions between modes.

## Core Concepts

### Effect Lifecycle
```
START → STARTING (fade in) → ACTIVE (main loop) → STOPPING (fade out) → END
```

Each effect has a state that progresses with time and external triggers.

### Audio Synchronization Events
1. **Beat Detection** (0-5ms latency): Flash on beat onset
2. **FFT Updates** (10-20ms): Color based on frequency content
3. **Tempo Tracking** (100-500ms): Pulse synchronized to BPM
4. **Mode Transitions** (500-2000ms): Smooth crossfade between effects

## Effect State Machine Implementation

### Basic State Enum
```c
typedef enum {
    EFFECT_IDLE,       // Waiting to start
    EFFECT_STARTING,   // Fade in (0-500ms)
    EFFECT_ACTIVE,     // Main animation loop
    EFFECT_STOPPING,   // Fade out (500ms-1s)
} effect_state_t;
```

### Context Structure
```c
typedef struct {
    effect_state_t state;
    uint32_t state_start_time;
    uint32_t state_duration;      // ms to spend in this state
    float progress;               // 0.0 to 1.0 within state
    uint32_t frame_counter;
    bool audio_reactive;          // Responds to beat/tempo
} effect_context_t;
```

### State Update Logic
```c
void update_effect_state(effect_context_t *ctx) {
    uint32_t elapsed = millis() - ctx->state_start_time;
    ctx->progress = (float)elapsed / (float)ctx->state_duration;

    // Clamp progress
    if (ctx->progress > 1.0f) {
        ctx->progress = 1.0f;

        // Auto-transition between states
        switch (ctx->state) {
            case EFFECT_STARTING:
                ctx->state = EFFECT_ACTIVE;
                ctx->state_duration = UINT32_MAX;  // Indefinite
                break;
            case EFFECT_STOPPING:
                ctx->state = EFFECT_IDLE;
                break;
            default:
                break;
        }

        ctx->state_start_time = millis();
    }

    ctx->frame_counter++;
}
```

## Common Easing Functions

### Linear
```c
float ease_linear(float t) {
    return t;  // 0→1, no acceleration
}
```

### Ease In (slow start, fast end)
```c
float ease_in_quad(float t) {
    return t * t;
}

float ease_in_cubic(float t) {
    return t * t * t;
}
```

### Ease Out (fast start, slow end)
```c
float ease_out_quad(float t) {
    return 1.0f - (1.0f - t) * (1.0f - t);
}

float ease_out_cubic(float t) {
    float f = t - 1.0f;
    return 1.0f + f * f * f;
}
```

### Ease In-Out (smooth both ends)
```c
float ease_in_out_cubic(float t) {
    return (t < 0.5f) ?
        4.0f * t * t * t :
        1.0f - pow(-2.0f * t + 2.0f, 3.0f) / 2.0f;
}
```

### Usage
```c
// Apply easing to transition
float eased = ease_out_cubic(ctx->progress);
uint8_t brightness = (uint8_t)(255.0f * eased);
```

## Effect Transitions (Crossfade)

### Transition State
```c
typedef struct {
    effect_context_t *current;
    effect_context_t *next;
    uint32_t transition_start;
    uint32_t transition_duration;
    bool in_transition;
} effect_transition_t;
```

### Trigger Transition
```c
void initiate_transition(effect_transition_t *trans,
                        effect_context_t *next_effect,
                        uint32_t duration_ms) {
    trans->next = next_effect;
    trans->transition_start = millis();
    trans->transition_duration = duration_ms;
    trans->in_transition = true;

    // Start stopping current effect
    trans->current->state = EFFECT_STOPPING;
}
```

### Blend During Transition
```c
void blend_transition(effect_transition_t *trans, uint32_t *led_out) {
    uint32_t elapsed = millis() - trans->transition_start;
    float alpha = (float)elapsed / trans->transition_duration;

    if (alpha >= 1.0f) {
        // Transition complete
        trans->current = trans->next;
        trans->in_transition = false;
        return;
    }

    // Render both effects
    uint32_t current_out[NUM_LEDS], next_out[NUM_LEDS];

    render_effect(trans->current, current_out);
    render_effect(trans->next, next_out);

    // Crossfade (linear interpolation)
    for (int i = 0; i < NUM_LEDS; i++) {
        // Extract RGB components
        uint8_t cr = (current_out[i] >> 16) & 0xFF;
        uint8_t cg = (current_out[i] >> 8) & 0xFF;
        uint8_t cb = current_out[i] & 0xFF;

        uint8_t nr = (next_out[i] >> 16) & 0xFF;
        uint8_t ng = (next_out[i] >> 8) & 0xFF;
        uint8_t nb = next_out[i] & 0xFF;

        // Blend: current * (1-alpha) + next * alpha
        uint8_t r = (uint8_t)(cr * (1.0f - alpha) + nr * alpha);
        uint8_t g = (uint8_t)(cg * (1.0f - alpha) + ng * alpha);
        uint8_t b = (uint8_t)(cb * (1.0f - alpha) + nb * alpha);

        led_out[i] = (r << 16) | (g << 8) | b;
    }
}
```

## Beat-Reactive Flash

### Beat Flash Effect
```c
typedef struct {
    bool detected;
    uint32_t detection_time;
    float confidence;  // 0-100
} beat_event_t;

void apply_beat_flash(const beat_event_t *beat, uint32_t *led_out,
                      uint32_t base_color) {
    if (!beat->detected) return;

    // Flash duration: 100ms from beat onset
    uint32_t elapsed = millis() - beat->detection_time;
    if (elapsed > 100) return;  // Flash expired

    // Decay brightness over 100ms
    float decay = 1.0f - ((float)elapsed / 100.0f);

    // Interpolate from white (flash) to base color
    uint32_t flash_color = 0xFFFFFF;  // White

    for (int i = 0; i < NUM_LEDS; i++) {
        // Blend: flash_color * decay + base_color * (1-decay)
        uint8_t fr = (flash_color >> 16) & 0xFF;
        uint8_t fg = (flash_color >> 8) & 0xFF;
        uint8_t fb = flash_color & 0xFF;

        uint8_t br = (base_color >> 16) & 0xFF;
        uint8_t bg = (base_color >> 8) & 0xFF;
        uint8_t bb = base_color & 0xFF;

        uint8_t r = (uint8_t)(fr * decay + br * (1.0f - decay));
        uint8_t g = (uint8_t)(fg * decay + bg * (1.0f - decay));
        uint8_t b = (uint8_t)(fb * decay + bb * (1.0f - decay));

        led_out[i] = (r << 16) | (g << 8) | b;
    }
}
```

## Tempo Synchronization

### BPM to Milliseconds
```c
uint32_t bpm_to_beat_duration(float bpm) {
    return (uint32_t)(60000.0f / bpm);  // ms per beat
}

// Example: 120 BPM = 500ms per beat
```

### Pulse Effect Synchronized to BPM
```c
typedef struct {
    float bpm;
    uint32_t last_beat_time;
} tempo_data_t;

void apply_tempo_pulse(const tempo_data_t *tempo, uint32_t *led_out,
                       uint32_t base_color) {
    if (tempo->bpm <= 0) return;

    uint32_t beat_duration = bpm_to_beat_duration(tempo->bpm);
    uint32_t phase = millis() % beat_duration;
    float progress = (float)phase / beat_duration;  // 0.0 to 1.0

    // Brightness varies: 100% at beat start, fades to 30%
    float brightness = 1.0f - (progress * 0.7f);  // Range: 0.3 to 1.0

    // Apply to all LEDs
    uint8_t r = ((base_color >> 16) & 0xFF) * brightness;
    uint8_t g = ((base_color >> 8) & 0xFF) * brightness;
    uint8_t b = (base_color & 0xFF) * brightness;

    uint32_t pulsing_color = (r << 16) | (g << 8) | b;

    for (int i = 0; i < NUM_LEDS; i++) {
        led_out[i] = pulsing_color;
    }
}
```

## Multi-Layer Composition

### Layer Structure
```c
typedef struct {
    uint32_t base_layer[NUM_LEDS];      // Main visualization
    uint32_t reactive_layer[NUM_LEDS];  // Beat/audio reactions
    uint32_t overlay_layer[NUM_LEDS];   // UI, status, transitions
    float layer_opacity[3];              // 0.0 to 1.0 blend weights
} composition_t;
```

### Composite Blending
```c
void composite_layers(composition_t *comp, uint32_t *led_out) {
    for (int i = 0; i < NUM_LEDS; i++) {
        float r = 0.0f, g = 0.0f, b = 0.0f;

        // Blend each layer by opacity
        uint32_t colors[3] = {
            comp->base_layer[i],
            comp->reactive_layer[i],
            comp->overlay_layer[i]
        };

        for (int layer = 0; layer < 3; layer++) {
            uint8_t cr = (colors[layer] >> 16) & 0xFF;
            uint8_t cg = (colors[layer] >> 8) & 0xFF;
            uint8_t cb = colors[layer] & 0xFF;

            float opacity = comp->layer_opacity[layer];
            r += cr * opacity;
            g += cg * opacity;
            b += cb * opacity;
        }

        // Clamp to 8-bit
        uint8_t out_r = (r > 255) ? 255 : (uint8_t)r;
        uint8_t out_g = (g > 255) ? 255 : (uint8_t)g;
        uint8_t out_b = (b > 255) ? 255 : (uint8_t)b;

        led_out[i] = (out_r << 16) | (out_g << 8) | out_b;
    }
}
```

## Mode Auto-Rotation

### Mode Sequence
```c
typedef enum {
    MODE_SPECTRUM,
    MODE_HARMONIC,
    MODE_WAVE,
    MODE_RHYTHM_BREEZE,
    MODE_COUNT,
} visualization_mode_t;

visualization_mode_t next_mode(visualization_mode_t current) {
    return (current + 1) % MODE_COUNT;
}
```

### Auto-Rotate Timer
```c
void update_mode_rotation(void) {
    static uint32_t last_rotation = 0;
    static uint32_t rotation_interval = 30000;  // 30 seconds per mode

    if (millis() - last_rotation > rotation_interval) {
        current_mode = next_mode(current_mode);
        last_rotation = millis();
        initiate_transition(&transition, &modes[current_mode], 1000);  // 1s crossfade
    }
}
```

## Main Choreography Loop

### Core Update Function
```c
void update_choreography(audio_data_t *audio, beat_event_t *beat,
                        tempo_data_t *tempo) {
    // 1. Update effect states
    update_effect_state(&current_effect);

    // 2. Render base effect
    uint32_t base_out[NUM_LEDS];
    render_effect(&current_effect, base_out);

    // 3. Add beat reactivity if beat detected
    uint32_t reactive_out[NUM_LEDS] = {0};
    if (beat->detected) {
        apply_beat_flash(beat, reactive_out, 0xFFFFFF);
    }

    // 4. Add tempo sync pulsing
    uint32_t tempo_out[NUM_LEDS];
    apply_tempo_pulse(tempo, tempo_out, get_mode_color());

    // 5. Handle transitions
    uint32_t final_out[NUM_LEDS];
    if (transition.in_transition) {
        blend_transition(&transition, final_out);
    } else {
        memcpy(final_out, base_out, sizeof(base_out));
    }

    // 6. Composite all layers
    composition_t comp = {
        .base_layer = final_out,
        .reactive_layer = reactive_out,
        .overlay_layer = tempo_out,
        .layer_opacity = {0.7f, 0.3f, 0.2f}
    };
    uint32_t display_out[NUM_LEDS];
    composite_layers(&comp, display_out);

    // 7. Send to LEDs
    update_leds(display_out);

    // 8. Check for mode rotation
    update_mode_rotation();
}
```

## Timing Budget

| Component | Time | CPU % |
|---|---|---|
| State updates | <1ms | 5% |
| Effect render | 5-10ms | 40% |
| Beat flash | <1ms | 5% |
| Tempo pulse | <1ms | 5% |
| Layer composite | 2-3ms | 15% |
| LED update | <1ms | 5% |
| **Total (30FPS target)** | **<33ms** | **~75%** |

## Anti-Patterns

### ❌ WRONG: Blocking in choreography update
```c
void bad_choreography(void) {
    // Don't do this in main loop!
    delay(500);  // ← Will break timing
    vTaskDelay(100);  // ← Still blocks
}
```

### ✅ CORRECT: Use non-blocking state machines
```c
void good_choreography(void) {
    // All timing via millis() comparisons
    // No blocking calls
    // Completes in <33ms
}
```

### ❌ WRONG: Allocating frame buffers in loop
```c
void bad_buffer_handling(void) {
    uint32_t led_out[NUM_LEDS];  // Stack allocation each frame!
}
```

### ✅ CORRECT: Reuse static buffers
```c
static uint32_t led_out[NUM_LEDS];  // Global, allocated once
void good_buffer_handling(void) {
    // Reuse same buffer each frame
}
```

## References

- Animation easing: https://easings.net/
- State machines: https://en.wikipedia.org/wiki/Finite-state_machine
- Color blending: sRGB vs linear RGB considerations
- Frame rate sync: 30Hz=33ms, 60Hz=16.6ms budgets
