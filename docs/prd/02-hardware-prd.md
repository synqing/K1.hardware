# K1 Lightwave — Hardware PRD

## Electrical Architecture

### **Power Distribution**

| Rail | Voltage | Max Current | Source | Notes |
|------|---------|-------------|--------|-------|
| VCC_5V_IN | 5V ±0.25V | 5A (budget) | USB-C or barrel jack | Unregulated input |
| VCC_5V | 5V ±0.1V | 3A | Ferrite bead filtered from VCC_5V_IN | LED power bus (direct) |
| VCC_3V3 | 3.3V ±0.1V | 2A | LDO from VCC_5V (TPS7333 or similar) | Logic + Audio (MCU, codec, mics) |
| VDDA_3V3 | 3.3V ±0.05V | 0.5A | LDO with analog filtering | Analog reference for audio codec (if used) |

**Decoupling:**
- 100µF bulk cap near each power entry
- 10µF per MCU (VDD, VDDA)
- 100nF per IC, min 0603 footprint
- Star grounding at power entry; separate analog/digital returns if codec used

---

### **Microcontroller (MCU)**

**Part:** 2× ESP32-S3-WROOM-1/1U (or -1U-N4, 8MB variant TBD)
- **Core:** Xtensa dual-core LX7, up to 240 MHz
- **RAM:** 512 KB SRAM (embedded)
- **Flash:** 8 MB (on-module)
- **I/O:** 43 GPIO (shared with USB, JTAG)
- **Wireless:** 802.11b/g/n Wi-Fi; BLE 5.0

**Key GPIO Assignments (TBD):**
| Signal | ESP32-S3 Pin | Alt Func | Purpose |
|--------|--------------|----------|---------|
| I2S_BCLK | GPIO8 | I2S0 | Audio clock |
| I2S_LRCLK | GPIO9 | I2S0 | Audio left/right |
| I2S_SD | GPIO10 | I2S0 | Audio data in (from mic) |
| LED_DATA | GPIO11 | GPIO | WS2812B data (via level shifter) |
| LED_CLK | GPIO12 | GPIO | Optional secondary LED strand |
| UART_TX | GPIO43 | UART0 | Serial console (bringup/debug) |
| UART_RX | GPIO44 | UART0 | Serial console |

*Note: Pin assignments to be confirmed during schematic phase.*

---

### **Audio Input Chain**

**Option A: Digital I2S Microphones (Baseline)**
- **SPH0645:** MEMS omni-directional, 94 dBSPL, PDM→I2S converter on-chip
- **IM69D130:** Omnidirectional, ~120 dB SPL dynamic range, PDM→I2S
- **Count:** 2 mics (stereo capture, spatial info)
- **Clock:** 64 kHz I2S master clock from MCU; 16-bit left-justified
- **Connector:** 4-pin JST-PH (VCC_3V3, GND, I2S_SD, I2S_BCLK) + shared LRCLK

**Option B: Analog Audio Codec (Future, if analog line-in needed)**
- **ES8388 or SGTL5000** (full-featured audio codec)
- **Not in v1 baseline**

---

### **LED Output**

**Addressable LED Standard:**
- **WS2812B or SK6812 (RGB/RGBW):** 5V logic, 800 kHz PWM protocol
- **Level Shifter:** SN74AHCT125 (3.3V → 5V translation, max 50Ω load)
- **Max LEDs per strand:** 300 (current design); expandable to 600+ with buffer

**LED Power Budget:**
- **Per LED:** ~20 mA white @ full brightness (RGB) → ~60 mA
- **300 LEDs @ 50% avg:** 9A continuous (budget 15A at 5V input)
- **5V rail:** Current limit via ferrite bead + sense resistor (TBD)

**Connectors:**
- 3-pin JST-XH (GND, 5V, DATA) for main strand
- Optional 2-pin JST-XH (CLK, GND) if using CLK-based LEDs (APA102, DotStar)

---

### **High-Speed Signals**

**I2S Audio:**
- BCLK, LRCLK, SD: Differential pair treatment preferred (minimize skew)
- Length-matched within ±2 mm
- Ground plane spacing: min 0.5 mm from adjacent high-speed signals
- Termination: None (I2S is 1:1 master→slave)

**SPI (if used for future external memory/sensor):**
- MOSI, MISO, CLK: Group together, ground guard if needed
- Trace width: 0.15 mm (typical SPI)

**LED Data:**
- Single-ended, 50Ω driver (SN74AHCT125)
- 1–2 m max length without active buffer (design constraint)
- NO ground guard (1-wire protocol; guard would break signal)

---

### **Power Connectors**

**Input:**
- **USB-C (preferred):** VBUS → 5V rail (with reverse-protection diode if not integrated)
- **Barrel jack (optional):** 5.5 mm OD × 2.1 mm ID, center positive (alternative or redundant)

**Test Points:**
- TP_VCC_5V (5V input)
- TP_VCC_3V3 (3.3V logic)
- TP_GND (signal/power return)
- TP_I2S_BCLK, TP_I2S_LRCLK, TP_I2S_SD (audio debug)
- TP_LED_DATA (LED signal debug)

---

## PCB Layout & Stackup

### **4-Layer Stackup (JLC/PCBWay Standard)**

| Layer | Purpose | Notes |
|-------|---------|-------|
| Layer 1 | Signal / Components (top) | Traces, pads, silkscreen |
| Layer 2 | Ground plane | Continuous (analog/digital common) |
| Layer 3 | Power plane | 5V + 3.3V zones (not separated unless needed) |
| Layer 4 | Signal / Ground (bottom) | Traces, test points, back-side components |

### **Design Rules (JLC 4-Layer)**

| Parameter | Value | Notes |
|-----------|-------|-------|
| Min trace width | 0.1 mm | Fine-pitch devices OK |
| Min clearance | 0.1 mm | Standard spacing |
| Min via diameter | 0.3 mm (finished) | Plated through |
| Via antipad | 0.2 mm | Via-to-plane spacing |
| Copper weight | 1 oz (35 µm) | Standard for both signals & planes |
| Solder mask | ±0.025 mm | Fine details OK |

### **Layout Priorities**

1. **Power distribution:** 5V input near connector; 3.3V LDO near MCU
2. **Ground plane:** Continuous on Layer 2; stitching vias every 0.5 mm at high-current areas
3. **Audio path:** I2S mics → MCU isolated from LED switching; ground guard traces if needed
4. **RF keepout:** 5 mm no-trace zone around ESP32-S3 antenna (module datasheet)
5. **Thermal vias:** 8–16× 0.3 mm vias under LDO and LED driver (if separate IC)

---

## Manufacturing & Assembly

### **Component Sourcing (LCSC/JLC Prioritized)**

| Component | LCSC Mfg | LCSC Part # | Qty | Notes |
|-----------|----------|------------|-----|-------|
| ESP32-S3-WROOM-1U | Espressif | C... | 2 | 8MB flash |
| SPH0645 | Knowles | C... | 1–2 | PDM→I2S mic |
| IM69D130 | InvenSense/TDK | C... | 0–1 | Alt digital mic |
| WS2812B (bare die / strip) | Worldsemi | C... | 1–N | Addressable LED |
| SN74AHCT125 | TI | C... | 1 | Level shifter |
| TPS7333 (or alternative LDO) | TI | C... | 1 | 3.3V regulator |
| USB-C connector | Various | C... | 1 | USB 2.0 (power only) |
| JST-XH 3pin | JST | C... | 2 | LED connectors |
| JST-PH 4pin | JST | C... | 1 | Mic connectors |

**BOM Total:** ~12–15 components (mostly passives + 2× MCU)

### **Panelization (Future)**

- **Target:** 4×8 grid (32 boards per panel)
- **V-cuts + mousebites:** 0.4 mm clearance (JLC standard)
- **Rails:** 5 mm top/bottom for handling
- **Breakaway time:** <1 minute manual

### **Solder Mask & Silkscreen**

- White solder mask (standard contrast for rework)
- Black silkscreen: Reference designators (R1, C1, U1), test point labels, revision
- No copper-to-mask isolation issues expected (standard 0.1 mm process)

---

## Electrical Compliance & Risk Mitigation

### **ESD Protection**

- **Mic connectors:** 100 kΩ series resistor on each audio line (input protection)
- **USB VBUS:** 5V clamp diode (if not in connector module)
- **LED data:** Optional ferrite + cap (if susceptible during testing)

### **EMI Hotspots**

- **LED switching (800 kHz PWM):** Keep away from audio, antenna
- **Microphone input:** Low-impedance lines, ground coupling caps on codec inputs
- **USB data lines:** Not routed; power-only USB (simplified EMI)

### **Known Risks & Mitigations**

| Risk | Symptom | Mitigation |
|------|---------|-----------|
| 1-wire LED noise | Corrupted colors / LED flicker | Ground guard on data line; use level shifter with proper termination |
| I2S clock jitter | Audio dropouts / skipped frames | PLL bypass if available; 64 kHz gen from internal oscillator (stable enough) |
| Thermal runaway @ full LEDs | LDO shutdown / MCU brown-out | Sense 5V current; software current limit if >4A; heatsink evaluation |
| Ground bounce | Glitches in digital signals | Multi-point ground return; stitching vias under high-current pads |
| Antenna detuning | Reduced Wi-Fi range | 5 mm keepout respected; antenna traces routed to edge |

---

## Acceptance Criteria

### **Design-Complete Gate**

- [ ] ERC clean (no violations)
- [ ] DRC clean (JLC 4-layer rules)
- [ ] BOM 100% sourced (all parts available on LCSC)
- [ ] Datasheets present for all active components
- [ ] 3D STEP model generated (clearance check)

### **Manufacturing Gate**

- [ ] Gerber, drill, and IPC-2581 exported
- [ ] Panelization validated (if applicable)
- [ ] Assembly BOM & pick-and-place generated
- [ ] Lead time confirmed with fab (<3 weeks)

### **Electrical Validation Gate**

- [ ] Power-up test passes (no shorts, correct rail voltages)
- [ ] Audio capture confirmed @ 16 kHz (I2S loopback)
- [ ] LEDs respond to test pattern
- [ ] Thermal rise <50°C @ full load

---

## References

- **Datasheets:** `/docs/datasheets/`
  - ESP32-S3 (SoC & module)
  - SPH0645 & IM69D130 (microphones)
  - WS2812B & SK6812 (LEDs)
  - SN74AHCT125 (level shifter)
  - TPS7333 (LDO example)

- **Governance:** `/claude/GOVERNANCE.md` (design change protocol)
- **Product Brief:** `/docs/prd/01-product-brief.md`
- **Validation Plan:** `/docs/prd/03-validation-plan.md`

---

**Version:** 0.1 (Alpha PRD)
**Last updated:** Oct 23, 2025
**Status:** Design input phase; ready for schematic entry
