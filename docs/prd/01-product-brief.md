# K1 Lightwave — Product Brief

## Mission

Create a dual-ESP32-S3 real-time music visualizer that prioritizes **responsiveness and delight**—low-latency audio capture, synchronous LED output, and robust wireless connectivity.

**Target users:** Stage/installation creators; living-room ambient users seeking a professional-grade, hackable music display.

---

## Core Value Proposition

1. **Real-time responsiveness** — Sub-100ms audio→LED latency for rhythm synchronization
2. **Dual-processor architecture** — One MCU captures audio; one handles LED orchestration (lower contention)
3. **Professional aesthetics** — Clean industrial design; modular audio/LED connectors
4. **Open & hackable** — All firmware, hardware, and design files available for customization
5. **Scalable LED support** — From single strand to full-room installations (TBD max LED count)

---

## High-Level Requirements

### **Audio Capture**
- **Digital microphones:** SPH0645 + IM69D130 (I2S, 16-bit, 16kHz–48kHz sampling)
- **Input:** Either analog preamp (codec: ES8388/SGTL5000) *or* digital mic direct; TBD during design
- **Processing:** Real-time FFT (16–2048 bins); BPM detection (Goertzel); energy per frequency band

### **LED Output**
- **Addressable LEDs:** WS2812B or SK6812 (RGB/RGBW, 5V logic)
- **Level shifter:** SN74AHCT125 (5V tolerant, 3.3V→5V translation)
- **Scalability:** Currently 1–300 LEDs/strand; design for future expansion to multi-strand
- **FPS target:** ≥30 Hz refresh rate (12ms frame time)
- **Color profiles:** Spectrum, heatmap, amplitude-mapped, beat-sync animations (firmware TBD)

### **Connectivity**
- **Wi-Fi + BLE:** Via ESP32-S3 built-in (no external module)
- **OTA updates:** Firmware push without USB re-programming
- **Network profile:** Local network only (no cloud dependency) + optional BLE app

### **Power & Thermal**
- **Input:** 5V DC, USB-C or barrel jack (2A budget baseline; scale with LED load)
- **Logic rails:** 3.3V regulated from 5V supply (LDO or buck)
- **LED power:** Direct from 5V input (current budget per design)
- **Thermal:** Passive cooling preferred; active cooling if dissipation >5W

### **Physical Form Factor**
- **Enclosure:** Compact (TBD: ~100mm L × 80mm W × 40mm H as placeholder)
- **Connectors:** JST-XH for LEDs (3-pin: GND, 5V, DATA); JST-PH for microphone (4-pin: VCC, GND, I2S×2)
- **Mounting:** Holes for DIN rail or wall mounting (TBD)

---

## Non-Goals (v1)

- Battery operation (wall/USB powered only)
- Analog audio input (digital I2S only)
- Ethernet connectivity
- Commercial FCC/CE certification (hobbyist/maker product)
- Support for >300 LEDs per strand (future version)

---

## Key Constraints

### **Electrical**
- 4-layer PCB; JLC/PCBWay manufacturing (cost & lead time optimized)
- Single-side assembly preferred (simplifies production)
- Component sourcing: LCSC/JLC C-numbers prioritized (fast delivery, cheap)

### **Timing & Latency**
- Audio→LED latency budget: <100ms (to feel responsive)
- I2S clock: 64 kHz (4 × 16 kHz) or higher
- LED refresh: ≥30 Hz (12ms frame time)
- Contention: Dual MCU avoids audio processing blocking LED output

### **EMI & Signal Integrity**
- 1-wire LED output is prone to noise (SN74AHCT125 level shifter helps)
- Audio lines must be separated from LED switching (ground guard traces)
- Ground plane on both internal layers; star grounding at power entry

### **Manufacturability**
- No specialized components; all parts on LCSC/Digi-Key
- Panelization target: 4×8 grid for cost-per-unit optimization (later version)

---

## Success Criteria

1. ✅ Hardware prototype boots and runs basic firmware
2. ✅ Audio captures cleanly at 16 kHz, 16-bit, stereo via I2S
3. ✅ LEDs respond to audio in real-time (<100ms latency)
4. ✅ Wi-Fi / BLE connectivity stable (no frequent dropouts)
5. ✅ Thermal: <50°C at full LED load, 25°C ambient
6. ✅ ERC/DRC clean; all components ≥95% available on LCSC
7. ✅ Open-source design & firmware released (GitHub)

---

## Timeline & Phases

| Phase | Deliverable | Timeline |
|-------|-------------|----------|
| **Alpha** | Schematic + PCB layout (design-complete) | Week 1–2 |
| **Beta** | Prototype received; power-up & firmware bringup | Week 3–4 |
| **Release** | Full validation (thermal, EMI, assembly docs) + GitHub release | Week 5–6 |

---

## Stakeholders & Roles

- **Hardware Designer:** PCB schematic, layout, DFM
- **Firmware Engineer(s):** Audio DSP, LED animation, wireless stack
- **Validation Engineer:** Bringup, DVT, EMI pre-scan (TBD)

---

## Scope (Out of v1)

- Cloud dashboard / web interface
- Multi-color synchronized effects (single static/animated profile per session)
- Microphone auto-leveling / AGC
- Battery operation or ultra-low-power mode

---

## References

- **Hardware PRD:** `/docs/prd/02-hardware-prd.md`
- **Validation Plan:** `/docs/prd/03-validation-plan.md`
- **Governance:** `/claude/GOVERNANCE.md`
- **Datasheets:** `/docs/datasheets/`

---

**Version:** 0.1 (Alpha)
**Last updated:** Oct 23, 2025
**Status:** Project scaffold complete; design work to begin
