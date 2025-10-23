---
title: DSP on ESP32-S3 - Reference & Patterns
description: ESP-DSP library usage, FFT, filtering, and audio processing for ESP32-S3
keywords:
  - ESP32-S3
  - FFT
  - Digital Signal Processing
  - Audio
  - I2S
  - esp-dsp
  - beat detection
categories:
  - Embedded
  - Audio Processing
  - Firmware
allowed_tools:
  - Read
  - Grep
  - Glob
---

# DSP on ESP32-S3: Complete Reference

## Why ESP-DSP (Not CMSIS)

For PRISM K1 and ESP32-S3 based projects, **ESP-DSP is the preferred choice**:

- ✅ **Official** - Espressif's optimized library for ESP32/ESP32-S3
- ✅ **Optimized** - Hand-tuned assembly for ESP32-S3 RISC-V core
- ✅ **Apache 2.0** - Open source, permissive license
- ✅ **IDF Integration** - Ships with ESP-IDF, no external dependencies
- ❌ **Not CMSIS** - CMSIS is ARM-centric; ESP32-S3 is RISC-V

## ESP-DSP Component Path

```
$IDF_PATH/components/esp-dsp/
├── modules/
│   ├── fft/              # Fast Fourier Transform
│   ├── filter/           # FIR/IIR filters
│   ├── conv/             # Convolution
│   ├── corr/             # Correlation
│   ├── matrix/           # Matrix operations
│   ├── windows/          # Window functions
│   └── math/             # Math operations
├── examples/
└── include/
    └── esp_dsp.h         # Main header
```

## Core Functions Reference

### FFT (Fast Fourier Transform)

**Use Case**: Frequency analysis, beat detection, spectral visualization

```c
#include "esp_dsp.h"

// 256-point FFT (typical for audio)
#define FFT_SIZE 256
float input[FFT_SIZE];
float output[FFT_SIZE];

// Initialize FFT plan
dsps_fft2r_init_fc32(NULL, FFT_SIZE);

// Compute FFT (input must be real)
dsps_fft2r_fc32(input, FFT_SIZE);

// Get magnitude spectrum
dsps_sqrt_f32(input, output, FFT_SIZE);
```

**Memory**: 256-point FFT ≈ 2-3 KB
**Time**: ≈ 5-10 ms for 256-point on ESP32-S3

### FIR Filters

**Use Case**: Smoothing, noise reduction, tone extraction

```c
#include "esp_dsp.h"

// 32-tap FIR filter
#define FIR_TAPS 32
float coef[FIR_TAPS];        // Filter coefficients
float state[FIR_TAPS];       // Filter state
float input_sample;
float output_sample;

// Apply one sample
dsps_fir_f32_ae32(&input_sample, &output_sample, 1,
                  coef, state, FIR_TAPS);
```

**Memory**: 32-tap filter ≈ 256 bytes (coefficients + state)
**Time**: ≈ 50 µs per sample

### IIR Filters

**Use Case**: Real-time filtering (biquad, high-pass, low-pass)

```c
// Biquad (second-order IIR)
typedef struct {
    float b0, b1, b2;        // Numerator coefficients
    float a1, a2;            // Denominator coefficients
    float x1, x2;            // Previous inputs
    float y1, y2;            // Previous outputs
} biquad_t;

// Apply biquad
float input_sample = adc_read();
biquad_t filter = {...};     // Initialize with cutoff freq

float output = filter.b0 * input_sample +
               filter.b1 * filter.x1 + filter.b2 * filter.x2 -
               filter.a1 * filter.y1 - filter.a2 * filter.y2;
```

**Memory**: Biquad ≈ 40 bytes
**Time**: ≈ 10 µs per sample (real-time safe!)

### Window Functions

**Use Case**: Reduce spectral leakage in FFT

```c
#include "esp_dsp.h"

#define WINDOW_SIZE 256
float window[WINDOW_SIZE];
float signal[WINDOW_SIZE];

// Create Hann window (smooth, good for audio)
dsps_wind_hann_f32(window, WINDOW_SIZE);

// Apply window to signal
dsps_mulc_f32(signal, signal, WINDOW_SIZE, 0.5, 1);
```

**Window Types**:
- `dsps_wind_hann_f32` - Hann (audio, smooth)
- `dsps_wind_hamm_f32` - Hamming (narrower lobe)
- `dsps_wind_blackman_f32` - Blackman (best sidelobe)

## Audio Input: I2S PDM Microphone

### Hardware Connection
```
Microphone PDM → I2S_CLK, I2S_DATA → ESP32-S3
             → GPIO pins (typically I2S0)
```

### FreeRTOS + I2S Configuration

```c
#include "driver/i2s_pdm.h"
#include "esp_dsp.h"

// I2S PDM configuration
i2s_pdm_rx_config_t pdm_cfg = {
    .io_cfg = {
        .clk = GPIO_NUM_2,      // I2S clock pin
        .din = GPIO_NUM_3,      // I2S data pin
        .mode = I2S_ROLE_MASTER,
    },
    .pcm_cfg = {
        .sample_rate = 16000,   // 16 kHz (typical for voice)
        .frame_size_ms = 20,    // 20 ms frames (320 samples)
        .slot_mask = I2S_PDM_SLOT_LEFT,
    },
};

i2s_handle_t handle;
i2s_new_pdm_rx_channel(&pdm_cfg, &handle);

// Create audio buffer task
void audio_task(void *arg) {
    int16_t buffer[320];
    while (1) {
        i2s_channel_read(handle, buffer, 320*2, NULL, 100);
        // Process: buffer → FFT → beat detection
    }
}
```

## Beat Detection Pattern

**Typical Algorithm**:
1. Read 256 audio samples (≈16 ms at 16 kHz)
2. Apply Hann window to reduce leakage
3. Compute FFT
4. Extract low-frequency energy (bass, 40-250 Hz)
5. Compare to running average
6. If energy > threshold + margin, trigger beat

```c
// Simplified beat detection
void detect_beat(float *fft_output, int fft_size) {
    // Sum energy in bass region (40-250 Hz, bins ~2-12 at 16kHz)
    float bass_energy = 0;
    for (int i = 2; i < 12; i++) {
        bass_energy += fft_output[i] * fft_output[i];
    }
    bass_energy = sqrt(bass_energy);

    // Update running average
    static float avg_energy = 0;
    avg_energy = 0.95 * avg_energy + 0.05 * bass_energy;

    // Detect spike
    if (bass_energy > avg_energy * 1.5) {
        trigger_beat_effect();  // Fire LED pattern
    }
}
```

## Memory & Timing Budget

| Operation | Memory | Time (ESP32-S3) | Notes |
|-----------|--------|-----------------|-------|
| 256-pt FFT | 2-3 KB | 5-10 ms | Real-time safe |
| 32-tap FIR | 256 B | 50 µs/sample | Low latency |
| Biquad IIR | 40 B | 10 µs/sample | Very fast |
| Hann window | 1 KB | <1 ms | Pre-compute once |
| Beat detection | 100 B | <1 ms | Per frame |
| **Total for 16 kHz audio** | **5 KB** | **~10 ms** | **Plenty of headroom!** |

## Real-World Constraints for K1

| Constraint | Value | Impact |
|-----------|-------|--------|
| Sample rate | 16 kHz | Standard for voice |
| Frame size | 256 samples | ≈16 ms latency |
| LED update rate | 120 FPS | Update every 8.3 ms |
| Available CPU | ~50% | Firmware + WiFi + DSP |

**Result**: Audio processing easily fits in spare CPU cycles; no bottleneck for beat detection.

## Example: K1 Beat-Reactive LED

```c
void beat_reactive_led_task(void *arg) {
    float window[256];
    float fft_in[256], fft_out[256];

    dsps_wind_hann_f32(window, 256);
    dsps_fft2r_init_fc32(NULL, 256);

    int16_t audio_buf[256];

    while (1) {
        // Read audio
        i2s_channel_read(i2s_handle, audio_buf, 256*2, NULL, 100);

        // Convert to float, apply window
        for (int i = 0; i < 256; i++) {
            fft_in[i] = (float)audio_buf[i] * window[i] / 32768.0;
        }

        // FFT
        dsps_fft2r_fc32(fft_in, 256);

        // Extract spectrum magnitude
        for (int i = 0; i < 128; i++) {
            fft_out[i] = sqrt(fft_in[2*i]*fft_in[2*i] +
                             fft_in[2*i+1]*fft_in[2*i+1]);
        }

        // Beat detection & LED update
        detect_beat(fft_out, 256);
        update_led_pattern();  // 120 FPS

        vTaskDelay(20 / portTICK_PERIOD_MS);  // 50 ms = 20 FPS for DSP
    }
}
```

## Key Takeaways

1. **ESP-DSP is built for ESP32-S3** — Use it, not CMSIS
2. **FFT is fast enough** — 256-point takes ~10 ms, real-time safe
3. **Filtering is negligible** — IIR biquads are microseconds
4. **Memory is abundant** — K1 has 500+ KB available
5. **Beat detection is straightforward** — Energy thresholding works great
6. **Latency is acceptable** — ~20 ms total acceptable for visual effects

## References

- [ESP-DSP GitHub](https://github.com/espressif/esp-dsp)
- [ESP-IDF I2S Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/peripherals/i2s.html)
- [ESP-DSP Examples](https://github.com/espressif/esp-dsp/tree/master/examples)
- PRISM K1 Hardware: ESP32-S3 (RISC-V, not ARM)

---

**Last Updated**: October 22, 2025
**Skill Type**: Reference + Patterns
**Allowed Tools**: Read, Grep, Glob only
