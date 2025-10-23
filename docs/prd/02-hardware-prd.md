# K1 Lightwave — Hardware PRD (Rev-A Frozen)

**Status:** LOCKED for schematic design. All GPIO, power domains, and compute architecture final.

---

## Power

- **USB-C 5V, up to 3A** (Type-C current mode; no PD). Powers **controller logic only**.
- **LED power:** **external 5V** via locking connector; **no back-feed** to USB-C (ideal-diode/OR-FET).
- 5V→3.3V buck (≥2A), input fuse/e-fuse, inrush, ESD on CC/D+/D−.

| Rail | Voltage | Source | Usage | Notes |
|------|---------|--------|-------|-------|
| VBUS_USB_5V | 5V ±0.25V | USB-C | Logic only | Fused @ 1A; feeds buck |
| LED_5V | 5V ±0.1V | External connector | LED domain (high current) | Isolated via ideal diode |
| +3V3 | 3.3V ±0.1V | TPS62133 buck | MCU, codec, I2C, mics, LS drivers | ≥2A; 100µF bulk + 10µF per MCU |

---

## LED Outputs

- **Populate:** **4× one-wire** ports (WS2812B/SK6812) with **SN74AHCT125** (quad shifter) + 330Ω series resistor, polyfuse (0.75A), TVS diode, 3-pin locking headers (Molex KK-254).
- **Reserve (DNP):** **+4× one-wire** and **2× SPI (APA102/DotStar)** headers.
- **Throughput:** 1-wire @800 kHz ≈ 30 µs/LED → **60 FPS ~ 555 LEDs/port**, **120 FPS ~ 277 LEDs/port**.
- **Power protection:** Polyfuse per port; TVS across 5V-to-GND at connector; no back-feed to USB domain.

---

## Compute

### COM-A (Audio/DSP) — ESP32-S3-WROOM-1 Module

- **Form factor:** K1-M2B slot (M.2 B-key 2230; custom electrical mapping, not PC-M.2 standard).
- **USB-C connects here** (for flashing, CDC debug).
- **Consumes:** I²S from mic headers, SPI master to COM-B, UART debug, I²C mgmt.
- **Produces:** I²S_BCLK/LRCK/SD (sampled audio), SPI_MOSI/MISO/CS/SCK (high-rate), SYNC pulse (frame timing).

### COM-B (LED Renderer) — Bare ESP32-S3 QFN

- **Flash:** **QSPI 8–16 MB** (W25Q128JV or equivalent). **Dedicated SPI0/1 pins (26–32)** per Espressif; **do not repurpose for GPIO**.
- **Clock:** **40 MHz crystal** with 12pF load caps (tied to XIN/XOUT pins).
- **Boot:** EN/BOOT RC network (10k/1µ); BOOT strap to GND via pushbutton for download mode.
- **Consumes:** SPI slave from COM-A (20–40 MHz, CRC-16 frames), SYNC pulse for alignment.
- **Produces:** 4× GPIO to level shifter (LED_DATA1..4_IN), READY/ERR GPIO back to COM-A.

---

## Inter-MCU Link

- **Protocol:** SPI-DMA, **20–40 MHz**, CRC-16, sequence number, **200–400 Hz frame rate** (~400 B/frame typical).
- **Pins (COM-B):**
  - **GPIO12** = SPI_SCK_A2B (input from COM-A)
  - **GPIO11** = SPI_MOSI_A2B (input)
  - **GPIO13** = SPI_MISO_B2A (output)
  - **GPIO10** = SPI_CS_A2B (input)
  - **GPIO38** = SYNC_A2B (frame pulse from COM-A)
  - **GPIO39** = READY_B2A (back-pressure from COM-B)
- **All pins selected for clean IO_MUX mapping and no strap/memory conflicts.** ([Espressif Docs](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/))

---

## Audio (Microphone & I²S)

### Microphone Options & Voltage Domains

**SPH0645 (I²S, Recommended @ 3.3V)**
- Voltage: **1.62–3.6V** (spec'd optimally at 3.3V supply).
- Interface: **I²S** (standard 4-wire + SEL).
- SNR: **65 dB(A)** nominal; THD ≈ 2%.
- Connect **SEL to GND** for mono; leave open for stereo on some variants.
- **No translator needed** if using 3.3V rail directly.
- Reference: [ATCKIT SPH0645](https://datasheets.com/en/datasheets/ATCKIT-SPH0645)

**IM69D130 (PDM, 1.8V Optimized)**
- Voltage: **1.8V nominal** (can run 1.2–2.4V, but SNR degrades below 1.8V).
- Interface: **PDM** (clock + data serial stream @ Fpdm = Fs × 64 or Fs × 128; e.g., 3.072 MHz for 48 kHz).
- SNR: **65 dB(A)** @ 1.8V; drops ~1.5 dB per 100 mV below 1.8V.
- Requires **1.8V LDO** (separate from 3.3V rail) and **SN74AXC2T245 level translator** on clock/data.
- **Population options in SKiDL:**
  - **3.3V SPH0645 build:** DNP `U8`, `R_LVT_*` (translator); populate `R_BYPASS_CLK/DATA` (0Ω direct paths).
  - **1.8V IM69D130 build:** Populate `U8` (SN74AXC2T245), `R_LVT_*`; DNP bypass resistors.
- Reference: [Infineon IM69D130 Datasheet](https://www.infineon.com/en/products/sensors/im69d130)

### ESP-IDF Implementation

**PDM RX (for 1.8V IM69D130):**
- PDM available on **I2S0 only** (COM-B); outputs **16-bit PCM**.
- Clock frequency: **Fpdm = Fs × 64** or **Fs × 128** (e.g., 48 kHz → **3.072 MHz** @ ×64, **6.144 MHz** @ ×128).
- Initialize with `I2S_PDM_RX_DEFAULT_CONFIG()` (ESP-IDF > 4.4).
- COM-B GPIO: **GPIO12 (PDM_CLK_MCUSIDE)**, **GPIO13 (PDM_DATA_MCUSIDE)** → nets map to mic via translator or bypass.
- Latency: ~1 ms capture buffer; ideal for real-time effects.
- Reference: [Espressif I2S PDM RX](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/peripherals/i2s.html)

**I²S Standard (for 3.3V SPH0645 or external codec):**
- **BCLK:** bit clock (1.536 MHz mono @ 24-bit/48 kHz, 3.072 MHz stereo).
- **LRCK (WS):** frame sync (48 kHz).
- **SD:** serial data (MSB first, 32-bit slots with 24-bit fill).
- Master clock (MCLK) optional; leave floating if not on baseboard (codec/mic generates internally).
- Reference: [Espressif I2S Standard](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/peripherals/i2s.html)

### Headers & Wiring

- **Two 6-pin JST-GH headers** (`3V3, GND, BCLK, LRCK, SD, SEL`).
- **BCLK/LRCK series damping:** 22–47 Ω near clock driver to minimize ringing @ multi-MHz edges.
- **Connector placement:** Near COM-A to minimize loop area on fast edges.
- **Cable:** Shielded pairs recommended for runs >10 cm; shield to GND at one end.

### Bring-Up

1. Verify clock/data outputs from COM-A on logic analyzer.
2. If PDM: confirm Fpdm matches Fs × 64 or Fs × 128.
3. FFT capture on COM-A confirms frequency response @ 48 kHz / 24-bit stereo.

---

## Accessory I²C

- **Qwiic-compatible pin order:** `GND, VCC, SDA, SCL` (standard Qwiic footprint).
- **Dual footprints per port:** JST-SH (default) + JST-GH (alternate, placed in PCB as parallel pads).
- **4 ports:**
  - **I2C_PORT_1, I2C_PORT_2:** powered by **3.3V** (logic accessories, sensors, etc.).
  - **I2C_PORT_3, I2C_PORT_4:** powered by **5V** (supply only; data lines **level-shifted** on motherboard to 3.3V safe levels).
- **FRU EEPROM:** 24LC02 on I²C (slot/base identification).

---

## GPIO Summary (COM-B, Final)

| Function | GPIO | Rationale |
|----------|------|-----------|
| SPI_SCK_A2B (in) | **12** | IO_MUX SCLK for SPI2; robust 20–40 MHz. |
| SPI_MOSI_A2B (in) | **11** | IO_MUX MOSI for SPI2. |
| SPI_MISO_B2A (out) | **13** | IO_MUX MISO for SPI2. |
| SPI_CS_A2B (in) | **10** | IO_MUX CS0 for SPI2. |
| SYNC_A2B (in) | **38** | Clean, non-strap. |
| READY_B2A (out) | **39** | Clean, non-strap. |
| LED_DATA1_IN (out) | **8** | Free; goes to LS A1. |
| LED_DATA2_IN (out) | **18** | Free; goes to LS A2. |
| LED_DATA3_IN (out) | **21** | Free; goes to LS A3. |
| LED_DATA4_IN (out) | **47** | Free; goes to LS A4. |
| UART_TX_B | **14** | Optional debug (not a strap). |
| UART_RX_B | **15** | Optional debug. |
| EN (CHIP_PU) | **EN pin** | RC 10k/1µF; standard bring-up. |
| GPIO0 (BOOT) | **GPIO0** | 10k pullup + pushbutton to GND. |

**Avoided:** Strap pins (0, 3, 45, 46), memory/flash pins (26–32), and reserved Octal I/O (33–37).

---

## Panelization & DFM

### V-Cut Panel Requirements (JLCPCB Standard)

**Minimum panel size:** **70 × 70 mm** (KiKit enforces this; smaller panels use mouse-bites instead).
- Quoted from JLCPCB documentation: panels must be ≥ 70 × 70 mm for V-cut scoring.

**V-cut line rules:**
- **Full-length straight cuts** (no partial or curved lines); both horizontal and vertical lines must span the entire panel dimension.
- **Clearance from copper:** ≥ **0.4 mm** clearance on all copper traces (pads, vias, fills) to the V-cut score line.
- **Material thickness:** 1.6 mm (standard FR-4); JLC uses pneumatic V-scoring (60° or 90° angle, ~0.6 mm groove depth).
- **Breakability:** Post-scoring, boards separate with **hand pressure or light mechanical nudge** (no edge stress concentration).

### Rails & Tooling

- **Top/bottom rails:** **5 mm minimum** (2.54 mm typical) for handling and fixturing.
- **Left/right rails:** **3–5 mm** (same as top/bottom; full panel margin).
- **Fiducials:** 3× standard (Ø1.5 mm, no copper ring) placed at **panel corners + center** for vision alignment during depanel.
- **Test points:** Optional; route GND, +3V3 test pads to opposite corner from fiducials if automated.

### Copper & Soldermask Clearance

- **Edge clearance:** ≥ **0.3 mm** from board edge (Edge.Cuts) to nearest copper pad.
- **V-cut clearance:** ≥ **0.4 mm** (manufacturer minimum; Adafruit/SparkFun best practices use 0.5 mm for headroom).
- **Vias near V-cut:** Stagger vias in the 0.4–0.5 mm exclusion zone; never place via pad on the V-cut line itself.

### Post-Depanelization

- Boards separate cleanly when sawn or V-scored; no additional rework (shearing, sanding, or trimming) required in small volumes.
- Larger panels (100+ boards) benefit from **KiKit panelization script** which auto-assigns cuts, rails, and fiducials.
- JLC surcharge for V-cut: ≈ **$3–5 USD per order** (not per board); negligible for small runs.

### Layer Stack & Finish

- **4-layer FR-4** (standard): F.Cu / prepreg / GND / prepreg / PWR / prepreg / B.Cu (thickness 1.6 mm).
- **Copper weight:** 1 oz (1.4 mil / 35 µm) standard; 2 oz available for high-current rails (LED_5V busses).
- **Surface finish:** **ENIG** (electroless nickel immersion gold) ≥ 0.05 µm Ni, ≥ 0.025 µm Au; required for reliability on fine-pitch connectors and castellated edges.
- **Soldermask:** Green (standard); thickness ≥ 25 µm; clearance from solder bridges ≥ 0.1 mm.
- **Silkscreen:** White on black/green; min. text height 0.5 mm (readable by hand); auto-placement of reference designators on F.Fab layer.

**References:**
- JLCPCB V-cut specifications: https://jlcpcb.com/capabilities/pcb-assembly
- KiKit panelization tool: https://github.com/yaqwsx/KiKit
- Adafruit PCB design guide: https://learn.adafruit.com/faq-all-about-pcbs (v-cut section)

---

## Bring-Up Plan

### Power-Only Smoke

1. USB-C 5V in → 3.3V buck OK; no current on LED_5V.
2. Check **no continuity** between `VBUS_USB_5V` and `LED_5V`.
3. Fabops power-domain guard validates isolation in schematic.

### COM-B Minimal Life

1. Strap RC, EN high, BOOT pulled up; flash programming via UART.
2. QSPI flash wired; first blinky on **GPIO8** (LED_DATA1_IN) confirms IO.

### COM-A ↔ COM-B Link

1. SPI loop at 20–40 MHz on pins (12/11/13/10); toggle SYNC; ISR on COM-B.
2. MISO loopback; CRC-16 validation.

### Priority 2B: PDM/I2S Clock Verification (10 min)

1. **PDM Clock (if 1.8V IM69D130 build)**
   - Measure clock frequency on GPIO12
   - Expected: **3.072 MHz** (48 kHz × 64) or **6.144 MHz** (48 kHz × 128)
   - Tolerance: ±5% (2.92–3.22 MHz or 5.84–6.45 MHz)

2. **I2S Clock (if 3.3V SPH0645 build)**
   - Measure BCLK on GPIO43 (from COM-A)
   - Expected: **1.536 MHz** (mono) or **3.072 MHz** (stereo) @ 48 kHz
   - Use logic analyzer to verify phase alignment with LRCK

### I²S Mics

1. Feed tone; 48 kHz/24-bit capture on COM-A.
2. FFT shows line at input frequency.

### LED Ports

1. External 5V in; per-port fuse OK.
2. iBOM shows AHCT125 + 330Ω + TVS per port.

### Priority 3B: Thermal Validation (30 min)

1. **Setup**
   - Populate 300× WS2812B test strip on LED1_OUT
   - Set all pixels to 100% white (255, 255, 255) all channels
   - Soak for 15 minutes continuous operation

2. **Measurement**
   - FLIR thermal scan of power components (LTC4412, TPS7A2018, shunt resistors)
   - Measure junction temps at multiple points

3. **Acceptance Criteria**
   - **PASS**: <70°C (safe headroom for INA226 shunt 0.05Ω @ 3A)
   - **WARNING**: 60–70°C (firmware brightness capping recommended)
   - **FAIL**: >70°C (LTC4412 overheat risk, redesign required)

4. **Alternative (No FLIR)**
   - Touch-test: skin contact on U2 (LTC4412) and U5 (TPS7A2018) should be warm but safe (<60°C hand tolerance)
   - Record ambient temperature for baseline correction

---

## References & Technical Sources

### Architecture & Design

- **SKiDL netlist generator:** `hardware/k1-lightwave/skidl/k1_motherboard_revA.py` (complete BOM & net routing)
- **KiCad schematic:** `hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch` (all symbols, nets, ERC-validated)
- **KiCad PCB:** `hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb` (layout rules, net classes, DRC-ready)

### ESP32-S3 Hardware

- **Espressif ESP32-S3 Hardware Design Guidelines:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/hw-reference/esp32s3-devkitc-1/user-guide.html
- **Espressif I2S (PDM & Standard):** https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/peripherals/i2s.html
- **Espressif SPI Master:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/peripherals/spi_master.html
- **GPIO & Pinmux Reference:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/peripherals/gpio.html

### USB Type-C & Power

- **USB Type-C Spec (5V Sink):** Beyond Logic USB-C article on Rd = 5.1 kΩ current advertisement
- **ESD Protection:** Texas Instruments TPD4E05U06 datasheet (< 0.5 pF for USB2.0 compliance)
- **Ideal Diode (OR-FET):** Analog Devices LTC4412 datasheet (monolithic; LTC4411 ≤ 2.6 A variant)
- **Current Monitoring:** Texas Instruments INA226 datasheet (I2C high-side monitor, up to 36 V, ±16 addresses)

### Audio & Microphones

- **SPH0645 (I²S, 3.3V):** ATCKIT SPH0645 datasheet; 65 dB(A) SNR @ 3.3 V
- **IM69D130 (PDM, 1.8V optimized):** Infineon IM69D130 datasheet; SNR = 65 dB(A) @ 1.8V, ~1.5 dB/100mV below
- **SN74AXC2T245 (Voltage Translator):** Texas Instruments; dual-channel, push-pull, up to 380 Mb/s
- **Adafruit NeoPixel Best Practices:** https://learn.adafruit.com/adafruit-neopixel-uberguide (series resistor, TVS, bulk cap recommendations)

### LED Outputs & Drivers

- **SN74AHCT125 (Quad Buffer):** Texas Instruments; 5 V TTL-compatible, fast rise/fall for 1-wire data
- **300–500 Ω Series Damping:** Standard practice for WS2812B/SK6812 clock/data lines per Adafruit & NeoPixel specs
- **TVS Diodes (5V Lines):** Texas Instruments SMAJ series or Littelfuse 1.5KE series (≥ 5 V clamp, ≤ 1 pF)
- **Polyfuses (0.75A):** Littelfuse or Bourns (1206 SMD size, slow-blow for LED current transients)

### Manufacturing & Panelization

- **JLCPCB V-Cut Specifications:** https://jlcpcb.com/capabilities/pcb-assembly (≥ 70×70 mm panel, full-length cuts, 0.4 mm copper clearance)
- **KiKit Panelization Tool:** https://github.com/yaqwsx/KiKit (automated v-cut, rails, fiducials, test points)
- **Adafruit PCB Design Guide:** https://learn.adafruit.com/faq-all-about-pcbs (manufacturing best practices, v-cut, depanel)
- **ENIG Surface Finish:** IPC-A-610 standard for nickel/gold thickness and reliability on fine-pitch connectors

### FabOps & Validation

- **Fabops Power-Domain Guard:** `mcp/mcp-fabops/server.py` (prevents VBUS_USB_5V ↔ LED_5V shorts at netlist level)
- **KiBot CI Pipeline:** `.github/workflows/kibot.yml` (automated Gerber, STEP, GLB, iBOM generation per commit)

### Full Datasheets Archive

- Location: `docs/datasheets/` (indexed by part number)

---

**Version:** 1.0 (FROZEN for Rev-A schematic)
**Date:** October 23, 2025
**Status:** Ready for KiCad import & layout
