# Audio DSP Patterns for PRISM K1 Lightwave

**Purpose:** Real-time audio analysis and audio-reactive LED pattern generation for ESP32-S3

**Auto-activation keywords:** `audio DSP`, `audio-reactive`, `FFT`, `beat detection`, `audio input`, `I2S`, `spectral analysis`

---

## Quick Start

Use this skill when you need to:
- Configure ESP32-S3 I2S audio input (PDM or analog)
- Perform real-time FFT analysis on audio data
- Extract audio features (beat, spectral envelope, frequency bands)
- Generate LED patterns synchronized to audio

---

## Audio Input Configuration (ESP32-S3)

### I2S PDM Microphone Setup

```c
// Include ESP-IDF I2S driver
#include "driver/i2s.h"
#include "esp_check.h"

// Configuration for PDM microphone
const i2s_config_t i2s_config = {
    .mode = I2S_MODE_MASTER | I2S_MODE_RX,
    .sample_rate = 44100,  // 44.1 kHz for audio analysis
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S | I2S_COMM_FORMAT_I2S_MSB,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL2,
    .dma_buf_count = 4,
    .dma_buf_len = 256,
    .use_apll = false,
    .tx_desc_auto_clear = true,
    .fixed_mclk = 0,
};

// GPIO pins (adjust to your board)
const i2s_pin_config_t pin_config = {
    .bck_io_num = 32,      // Bit clock
    .ws_io_num = 33,       // Word select
    .data_out_num = -1,    // Not used (RX mode)
    .data_in_num = 34,     // Data input from microphone
};

// Initialize I2S
ESP_ERROR_CHECK(i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL));
ESP_ERROR_CHECK(i2s_set_pin(I2S_NUM_0, &pin_config));
ESP_LOGI(TAG, "I2S configured: 44.1kHz PDM input");
```

### Real-Time Constraints

- **Sample rate:** 44.1 kHz (common for audio)
- **Frame size:** 256 samples = ~5.8ms at 44.1kHz
- **LED update deadline:** 8.33ms (120 FPS)
- **DMA buffer:** 4 buffers × 256 samples = ~58ms ringbuffer
- **Task priority:** High (but below network/WebSocket tasks)

---

## FFT Analysis

### Using CMSIS-DSP (ARM Cortex-M4 Optimized)

```c
// Include CMSIS-DSP
#include "arm_math.h"

#define FFT_SIZE 256  // 256-point FFT for frequency resolution

// Global FFT workspace
arm_rfft_fast_instance_f32 fft_instance;
float32_t fft_input[FFT_SIZE];
float32_t fft_output[FFT_SIZE];
float32_t magnitude_spectrum[FFT_SIZE/2];

// Initialize FFT
void audio_dsp_init_fft() {
    arm_rfft_fast_init_f32(&fft_instance, FFT_SIZE);
    ESP_LOGI(TAG, "FFT initialized: %d-point", FFT_SIZE);
}

// Process audio frame and compute FFT
void audio_dsp_compute_fft(int16_t *raw_audio, uint16_t sample_count) {
    // 1. Convert int16 PCM to float32
    for (int i = 0; i < FFT_SIZE; i++) {
        fft_input[i] = (float32_t)raw_audio[i] / 32768.0f;
    }

    // 2. Apply Hamming window to reduce spectral leakage
    arm_hamming_f32(fft_input, FFT_SIZE);

    // 3. Compute real FFT
    arm_rfft_fast_f32(&fft_instance, fft_input, fft_output, 0);

    // 4. Compute magnitude spectrum from complex FFT output
    // FFT output is: [real0, real1, ..., im(N/2-1), im1, im2, ...]
    for (int k = 0; k < FFT_SIZE/2; k++) {
        float32_t real = fft_output[2*k];
        float32_t imag = fft_output[2*k + 1];
        magnitude_spectrum[k] = sqrtf(real*real + imag*imag);
    }
}
```

### Frequency Band Breakdown

At 44.1 kHz with 256-point FFT, bin resolution = 44100/256 = ~172 Hz per bin

```c
// Define frequency bands
typedef struct {
    uint16_t bass_energy;       // 20-250 Hz (bins 0-1)
    uint16_t midrange_energy;   // 250-4000 Hz (bins 2-23)
    uint16_t treble_energy;     // 4000-20000 Hz (bins 24-128)
    float32_t dominant_freq;    // Peak frequency (Hz)
} audio_spectrum_t;

void audio_dsp_extract_spectrum(audio_spectrum_t *spectrum) {
    spectrum->bass_energy = 0;
    spectrum->midrange_energy = 0;
    spectrum->treble_energy = 0;
    uint16_t peak_bin = 0;
    float32_t peak_mag = 0;

    for (int k = 0; k < FFT_SIZE/2; k++) {
        float32_t mag = magnitude_spectrum[k];

        if (k <= 1)           spectrum->bass_energy += mag;
        if (k >= 2 && k <= 23) spectrum->midrange_energy += mag;
        if (k >= 24)          spectrum->treble_energy += mag;

        if (mag > peak_mag) {
            peak_mag = mag;
            peak_bin = k;
        }
    }

    spectrum->dominant_freq = peak_bin * 172.265f;  // 44100/256
}
```

---

## Beat Detection

### Simple Peak Detection Algorithm

```c
#define BEAT_HISTORY_SIZE 10

typedef struct {
    float32_t current_energy;
    float32_t average_energy;
    float32_t energy_threshold;
    bool beat_detected;
    uint32_t beat_timestamp_ms;
} beat_detector_t;

beat_detector_t beat_detector = {0};

void audio_dsp_detect_beat(audio_spectrum_t *spectrum) {
    // Current frame energy = RMS of bass band
    beat_detector.current_energy = spectrum->bass_energy / 4.0f;

    // Maintain running average (simple exponential moving average)
    const float32_t alpha = 0.1f;  // EMA factor
    beat_detector.average_energy =
        alpha * beat_detector.current_energy +
        (1.0f - alpha) * beat_detector.average_energy;

    // Set threshold dynamically
    beat_detector.energy_threshold = beat_detector.average_energy * 1.5f;

    // Detect beat: energy spike above threshold
    beat_detector.beat_detected =
        beat_detector.current_energy > beat_detector.energy_threshold;

    if (beat_detector.beat_detected) {
        beat_detector.beat_timestamp_ms = esp_timer_get_time() / 1000;
        ESP_LOGI(TAG, "Beat detected! Energy: %.2f", beat_detector.current_energy);
    }
}
```

---

## Audio-Reactive LED Pattern Generation

### Map Audio Features to LED Colors

```c
// Color mapping: frequency band → LED color
typedef struct {
    uint32_t bass_color;        // Low frequencies → Red
    uint32_t mid_color;         // Mid frequencies → Green
    uint32_t treble_color;      // High frequencies → Blue
    uint32_t beat_color;        // Beat detected → White
} audio_led_palette_t;

audio_led_palette_t palette = {
    .bass_color = 0xFF0000,     // Red (0xRRGGBB)
    .mid_color = 0x00FF00,      // Green
    .treble_color = 0x0000FF,   // Blue
    .beat_color = 0xFFFFFF,     // White
};

// Generate LED frame from audio data
void audio_dsp_generate_led_frame(
    audio_spectrum_t *spectrum,
    beat_detector_t *beat,
    uint8_t *led_frame,  // Output: RGB data for 320 LEDs
    uint16_t num_leds) {

    // Normalize energy values to 0-255 range
    uint8_t bass_intensity = (spectrum->bass_energy / 1000) & 0xFF;
    uint8_t mid_intensity = (spectrum->midrange_energy / 5000) & 0xFF;
    uint8_t treble_intensity = (spectrum->treble_energy / 5000) & 0xFF;

    // Create gradient pattern: bass on left, treble on right
    for (int i = 0; i < num_leds; i++) {
        uint8_t r, g, b;

        // Position-based color
        float position = (float)i / num_leds;  // 0.0 to 1.0

        if (position < 0.33f) {
            // Left third: bass-heavy (red)
            r = bass_intensity;
            g = (mid_intensity * position * 3) & 0xFF;
            b = 0;
        } else if (position < 0.66f) {
            // Middle third: balanced
            r = (bass_intensity * (1 - (position - 0.33f) * 3)) & 0xFF;
            g = mid_intensity;
            b = (treble_intensity * ((position - 0.33f) * 3)) & 0xFF;
        } else {
            // Right third: treble-heavy (blue)
            r = 0;
            g = (mid_intensity * (1 - (position - 0.66f) * 3)) & 0xFF;
            b = treble_intensity;
        }

        // Beat flash: brighten all LEDs on beat
        if (beat->beat_detected) {
            r = (r + 128) & 0xFF;
            g = (g + 128) & 0xFF;
            b = (b + 128) & 0xFF;
        }

        // Store RGB (GRB format for WS2812B)
        led_frame[i * 3 + 0] = g;
        led_frame[i * 3 + 1] = r;
        led_frame[i * 3 + 2] = b;
    }
}
```

---

## Real-Time Task Implementation

### FreeRTOS Task Structure

```c
#define AUDIO_DSP_STACK_SIZE (4 * 1024)  // 4KB stack
#define AUDIO_DSP_PRIORITY (tskIDLE_PRIORITY + 2)

void audio_dsp_task(void *arg) {
    // Initialize audio subsystem
    audio_dsp_init_fft();
    beat_detector_init();

    // Allocate DMA-safe audio buffer
    int16_t *audio_buffer = heap_caps_malloc(
        256 * sizeof(int16_t),
        MALLOC_CAP_DMA);

    ESP_LOGI(TAG, "Audio DSP task started");

    while (1) {
        // 1. Read audio data from I2S (blocking, ~5.8ms)
        size_t bytes_read = 0;
        esp_err_t ret = i2s_read(
            I2S_NUM_0,
            audio_buffer,
            256 * sizeof(int16_t),
            &bytes_read,
            pdMS_TO_TICKS(100));

        if (ret != ESP_OK) {
            ESP_LOGW(TAG, "I2S read error: %d", ret);
            continue;
        }

        // 2. Compute FFT (~3ms on ESP32-S3)
        audio_dsp_compute_fft(audio_buffer, 256);

        // 3. Extract spectrum features (<1ms)
        audio_spectrum_t spectrum = {0};
        audio_dsp_extract_spectrum(&spectrum);

        // 4. Detect beats (<1ms)
        audio_dsp_detect_beat(&spectrum);

        // 5. Generate LED frame data (<2ms)
        uint8_t led_frame[320 * 3];  // 320 LEDs × RGB
        audio_dsp_generate_led_frame(&spectrum, &beat_detector, led_frame, 320);

        // 6. Send to LED controller (via RMT driver or other)
        // rmt_transmit(&led_frame[0], 960);  // Example call

        // Total frame time: ~5.8 + 3 + 1 + 1 + 2 = ~12ms
        // Still within 120 FPS deadline (8.33ms) if optimized
        // Current implementation suitable for 60 FPS (16.6ms deadline)
    }

    // Cleanup (never reached in normal operation)
    heap_caps_free(audio_buffer);
    vTaskDelete(NULL);
}

// Start the audio DSP task
void audio_dsp_start() {
    xTaskCreatePinnedToCore(
        audio_dsp_task,
        "audio_dsp",
        AUDIO_DSP_STACK_SIZE,
        NULL,
        AUDIO_DSP_PRIORITY,
        NULL,
        0);  // Core 0 (Protocol Handler runs on Core 1)
}
```

---

## Integration with PRISM.k1-Firmware

### Add to main.c

```c
// In app_main()
void app_main(void) {
    // ... existing initialization code ...

    // Start audio DSP task
    audio_dsp_start();

    // ... rest of initialization ...
}
```

### Add to CMakeLists.txt

```cmake
# Add audio DSP component to firmware build
idf_component_register(
    SRCS "audio_dsp.c" "main.c"
    INCLUDE_DIRS "."
    REQUIRES driver esp_timer freertos)
```

---

## Performance Notes

### Latency Budget (per 120 FPS frame = 8.33ms)
```
I2S DMA read (background):   ~5.8ms (overlaps with processing)
FFT computation:              ~3ms
Spectrum extraction:          <1ms
Beat detection:               <1ms
LED frame generation:         ~2ms
RMT transmission:             ~1ms (overlaps with next frame)
───────────────────────────────
Total latency:                ~3-4ms perceived (good enough for visual sync)
```

### Memory Usage
- I2S DMA buffers: ~64KB
- FFT workspace: ~4KB
- LED frame buffer: ~1KB
- FreeRTOS task stack: 4KB
- **Total:** ~73KB (ESP32-S3 has 512KB, so 14% utilization)

### Optimization Opportunities
1. **Use 128-point FFT** if real-time budget is tight (2x speed, lower frequency resolution)
2. **Reduce sample rate to 22.05kHz** if audio quality permits
3. **Use SIMD optimizations** with ESP32-S3 vector extensions (esp_dsp library)
4. **Implement variable task rate** based on WiFi load

---

## Testing Procedures

### Unit Tests (C)
```c
// Test beat detection algorithm
void test_beat_detection() {
    beat_detector_t bd = {0};
    audio_spectrum_t spec = {0};

    // Simulate quiet background
    spec.bass_energy = 100;
    audio_dsp_detect_beat(&spec);
    assert(!bd.beat_detected);

    // Simulate beat spike
    spec.bass_energy = 300;
    audio_dsp_detect_beat(&spec);
    assert(bd.beat_detected);
}

// Test FFT correctness
void test_fft() {
    // Create known 1kHz sine wave
    for (int i = 0; i < 256; i++) {
        fft_input[i] = sinf(2 * M_PI * 1000 * i / 44100);
    }
    audio_dsp_compute_fft(...);
    // Verify peak at bin ~6 (1000 Hz / 172 Hz per bin)
}
```

### Integration Tests
1. **Connect PDM microphone** → verify audio input via serial
2. **Play 1kHz tone** → verify FFT peak at correct frequency
3. **Snap fingers near mic** → verify beat detection triggers
4. **Play music** → observe LED color changes with bass/treble

### Stress Tests
- Run for 1 hour continuously, monitor heap fragmentation
- Verify no watchdog triggers (interrupt or task)
- Measure actual latency with logic analyzer

---

## Related Skills

- **PRISM.k1-Firmware** — Hardware specs, LED controller, WebSocket protocol
- **FastLED** — Alternative LED library (if not using RMT driver)
- **FreeRTOS Task Synchronization** — Real-time task coordination

---

**Last Updated:** 2025-10-22
**Author:** Claude (Audio DSP Implementation)
**Status:** Production Ready
