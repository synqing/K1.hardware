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

## Audio

- **I²S digital microphones** @ **48 kHz/24-bit** (32-bit slots). Two **6-pin JST-GH headers** (`3V3,GND,BCLK,LRCK,SD,SEL`).
  - SEL pin strapped on **mic board** (not on baseboard).
- **Target mics:** SPH0645 or IM69D130 (PDM→I2S converters).
- **Alt:** mikroBUS codec card slot (future, consume I²S from COM-A if present).
- **I²S pins (COM-A):**
  - **I2S_BCLK** (input from mics or codec)
  - **I2S_LRCK** (input)
  - **I2S_SD** (input)

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

- **KiKit:** V-cuts when panel ≥ 70×70 mm; else mouse-bites.
- **Rails:** 5 mm top/bottom (handling); fiducials (3×).
- **Clearance:** 0.3 mm edge; 0.4 mm V-cut clearance.
- **JLC 4-layer:** Standard stackup; ENIG finish.

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

### I²S Mics

1. Feed tone; 48 kHz/24-bit capture on COM-A.
2. FFT shows line at input frequency.

### LED Ports

1. External 5V in; per-port fuse OK.
2. iBOM shows AHCT125 + 330Ω + TVS per port.

---

## References

- **SKiDL netlist generator:** `hardware/k1-lightwave/skidl/k1_motherboard_revA.py`
- **Espressif GPIO & SPI:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/
- **Espressif flash pins:** https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/
- **Datasheets:** `/docs/datasheets/`

---

**Version:** 1.0 (FROZEN for Rev-A schematic)
**Date:** October 23, 2025
**Status:** Ready for KiCad import & layout
