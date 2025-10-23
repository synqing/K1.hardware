# K1 Lightwave — Validation Plan

## Overview

This document outlines the testing and validation strategy for K1 Lightwave hardware, from initial prototype bringup through Design Verification Testing (DVT) and production readiness.

**Target:** Confirm all requirements in `/docs/prd/01-product-brief.md` and `/docs/prd/02-hardware-prd.md` are met.

---

## Test Phases

### **Phase 1: EVT (Engineering Validation Test)**

**Objective:** Confirm design intent; identify critical issues before DVT

**Timeline:** Week 1–2 post-prototype

#### **1.1 Power-Up & Electrical**

| Test | Acceptance Criteria | Method | Owner |
|------|-------------------|--------|-------|
| No shorts on power rails | No smoke; no >100mA short-circuit draw | Bench PSU, measure VCC, GND continuity | HW Lead |
| VCC_5V rail stable | 5V ±0.2V under no-load | Multimeter; 10s observation | HW Lead |
| VCC_3V3 regulation | 3.3V ±0.1V under 0–2A load | Variable load bank (resistor); oscilloscope | HW Lead |
| No thermal issues (idle) | Ambient +5°C measured @ LDO, MCU | IR thermometer; 5min soak | HW Lead |

**Deliverable:** Power-up report (pass/fail + photos)

---

#### **1.2 MCU & UART Console**

| Test | Acceptance Criteria | Method | Owner |
|------|-------------------|--------|--------|
| MCU boots (flash readable) | UART console responds to MCU reset | Connect FTDI USB→UART; monitor output | FW Lead |
| Clock accuracy | System clock within ±1% of 240 MHz | Oscilloscope on GPIO square wave | FW Lead |
| GPIO toggle works | LED on GPIO11 blinks @ 1 Hz | Connect test LED; visual confirmation | FW Lead |
| Wi-Fi radio responds | Wi-Fi chip enumerated; no JTAG errors | `espefuse.py summary` over USB-JTAG | FW Lead |

**Deliverable:** Bringup log with timestamps; UART capture

---

#### **1.3 Audio Input (I2S Microphone)**

| Test | Acceptance Criteria | Method | Owner |
|------|-------------------|--------|--------|
| I2S clock present | BCLK 64 kHz ±1%, stable | Oscilloscope BCLK pin; 1s waveform | HW/FW |
| LRCLK framing | 16 kHz ±1%, ~50% duty | Oscilloscope LRCLK pin | HW/FW |
| Mic data output | 16-bit stereo capture, no all-zeros | MCU I2S DMA capture to SRAM; dump via UART | FW Lead |
| Audio quality | No excessive noise (SNR >60 dB baseline) | FFT of silence + 1kHz tone; spectrum analyzer | FW Lead |

**Deliverable:** I2S timing diagram; audio capture waveform (WAV file); SNR measurement

---

#### **1.4 LED Output (WS2812B)**

| Test | Acceptance Criteria | Method | Owner |
|------|-------------------|--------|--------|
| Data line toggles | GPIO11 output pulse train visible | Oscilloscope GPIO11; frequency ≈800 kHz | HW Lead |
| LED color response | RGB test pattern visible (Red→Green→Blue) | Power LED strip; observe color changes | FW Lead |
| LED brightness | Full range 0–255 addressable | Firmware command; visual inspection | FW Lead |
| Max LED count | 300 LEDs operational @ 30 Hz refresh | Connect 300-LED strip; no frame loss | FW Lead |

**Deliverable:** LED timing diagram; color test video; FPS measurement

---

### **Phase 2: DVT (Design Verification Test)**

**Objective:** Confirm production-level performance; quantify margins

**Timeline:** Week 3–4 post-prototype (if EVT passes)

#### **2.1 Thermal Analysis**

| Test | Acceptance Criteria | Method | Owner |
|------|-------------------|--------|--------|
| Idle temperature | <30°C @ 25°C ambient (no load) | IR thermometer + internal temp sensor (if firmware supports) | HW Lead |
| Full LED load (300 LEDs @ 100%) | <50°C @ 25°C ambient | 15 min soak @ max brightness white; measure TDK sensor | HW Lead |
| Thermal hysteresis | No oscillation around set-point | 30 min observation; log temps every 10s | HW Lead |
| LDO dissipation | <1W nominal (calculated I × V_dropout) | Measure VCC_5V drop & 3.3V current draw | HW Lead |

**Deliverable:** Thermal curve (time vs. temp); max junction temp estimate

---

#### **2.2 Power Consumption**

| Test | Acceptance Criteria | Method | Owner |
|------|-------------------|--------|--------|
| Idle (no LEDs) | <500 mA @ 5V | Current meter on VCC_5V | HW Lead |
| Audio capture only | <800 mA @ 5V | I2S capture + DSP running | FW Lead |
| LEDs @ 50% avg brightness | <4A @ 5V (acceptable; ≤5A budget) | LED load bank simulation or real strip | HW Lead |
| Peak burst (LEDs @ 100% + audio) | ≤5A for <100ms (burst acceptable) | Oscilloscope current sense (shunt resistor) | HW Lead |

**Deliverable:** Current profile graph (time vs. current); surge events logged

---

#### **2.3 Electromagnetic Interference (EMI)**

| Test | Acceptance Criteria | Method | Owner |
|------|-------------------|--------|--------|
| LED switching noise on audio | <3% THD on 1 kHz audio capture during LED activity | FFT of captured audio; simultaneous LED PWM | HW/FW |
| Wi-Fi range | ≥10 m indoor (line-of-sight) from AP | Walk-around test; signal strength measurement | FW Lead |
| Antenna detuning (PCB impact) | No >3 dB gain loss vs. module alone | Measure S11 (return loss) if lab available; otherwise skip | HW Lead |

**Deliverable:** EMI/audio cross-talk report; Wi-Fi link budget confirmation

---

#### **2.4 Reliability & Stress**

| Test | Acceptance Criteria | Method | Owner |
|------|-------------------|--------|--------|
| Power cycling (10× cycles) | No failures; consistent boot | Off→5s→On→10s soak; repeat 10×; check logs | HW Lead |
| Thermal stress (hot/cold) | Functionality across 0–50°C (industrial baseline) | If environmental chamber available; otherwise skip for v1 | HW Lead |
| Long-run stability (24h) | No crashes; audio/LED stable | 24h continuous operation @ typical load | FW Lead |
| Connector durability | ≥10 plug/unplug cycles | JST-XH/PH insertion tests; no contact issues | HW Lead |

**Deliverable:** Stress test log; pass/fail summary

---

### **Phase 3: DFM (Design For Manufacturability) Review**

**Objective:** Confirm producibility; identify potential assembly/test gaps

**Timeline:** Concurrent with DVT or after prototype receives approval

#### **3.1 Gerber & Drill Review**

| Item | Check | Method | Owner |
|------|-------|--------|-------|
| Gerber layers complete | All 10 layers (L1, L2, L3, L4 + solder mask, silk, drill) | Verify file count & naming in output | HW Lead |
| Drill file accuracy | All via sizes ≥0.3 mm; correct plating codes | Inspect .drill/.drl file; fab quotes | HW Lead |
| Solder mask detail | No isolation issues; pins accessible for rework | 2× magnification visual inspection or Gerber viewer | HW Lead |
| Silkscreen contrast | Legible reference designators; no clipping | 100% inspection of output | HW Lead |

**Deliverable:** Gerber checklist (pass); fab clearance confirmation

---

#### **3.2 BOM & Assembly**

| Item | Check | Method | Owner |
|------|-------|--------|-------|
| Part availability | All parts ≥95% stock on LCSC/Digi-Key | Run BOM check via Nexar / LCSC API; confirm C-numbers | HW Lead |
| Lead times | All parts <8 weeks (fast-track criteria) | Record supplier lead times | Procurement |
| Assembly compatibility | All footprints compatible with pick-and-place | Verify IPC-636 footprint compliance | HW Lead |
| Panelization (if applicable) | Tab/breakaway design robust; <1 min manual separation | Prototype panel breakaway test | HW Lead |

**Deliverable:** BOM with LCSC C-numbers + availability; assembly procedure

---

#### **3.3 Test Coverage**

| Test Point | Function | Method | Owner |
|------------|----------|--------|-------|
| TP_VCC_5V | 5V rail continuity | Continuity probe; voltage measurement | Assembly |
| TP_VCC_3V3 | 3.3V output check | Voltage check during power-on; functional trim | Assembly |
| TP_GND | Ground integrity | Continuity check; star-point verification | Assembly |
| TP_I2S_* | Audio clock/data present | Logic analyzer capture (if available); optional | Assembly |
| TP_LED_DATA | LED signal integrity | Oscilloscope waveform check (pulse train) | Assembly |

**Deliverable:** In-circuit test (ICT) procedure / checklist

---

## Acceptance Gates

### **Gate 1: Electrical (EVT 1.1–1.2)**

✅ **Pass if:**
- Power rails stable (no shorts, correct voltage)
- MCU responsive on UART
- Clock accuracy within ±1%

❌ **Fail → Stop:** Investigate electrical schematic or layout error; debug traces

---

### **Gate 2: Functional (EVT 1.3–1.4)**

✅ **Pass if:**
- Audio captures cleanly (SNR >60 dB)
- LEDs respond to firmware commands
- No data loss @ 30 Hz refresh

❌ **Fail → Conditional:** If audio/LED issues are firmware-only, proceed with caveats; hardware-level issues block progression

---

### **Gate 3: Thermal & Reliability (DVT 2.1–2.4)**

✅ **Pass if:**
- Idle <30°C, full load <50°C
- Power consumption <5A @ max load
- 24h uptime without crashes
- EMI within acceptable limits

❌ **Fail → Conditional:** If thermal >60°C, investigate layout/component selection; minor EMI issues may warrant re-layout but don't block production

---

### **Gate 4: Manufacturability (DFM 3.1–3.3)**

✅ **Pass if:**
- All components ≥90% available on LCSC
- BOM cost within budget (TBD)
- Assembly procedure documented
- Test coverage defined

❌ **Fail → Escalation:** Component substitution required; design may need iteration

---

## Rework & Issue Tracking

### **Minor Issues** (Doesn't block release)

- Silkscreen text slightly faint (remedied with brighter ink)
- Single non-critical component substitution (same footprint, equivalent spec)
- Documentation typos or clarifications

**Action:** Log in GitHub Issues; resolve in v1.1 respin

---

### **Major Issues** (Blocks release, may require layout change)

- Thermal runaway (>60°C full load)
- Audio noise >10% THD during LED activity
- Component unavailability (>30 day lead time, no substitute)
- Layout error affecting high-speed signals

**Action:** Root cause analysis; schematic/PCB revision; new prototype

---

### **Critical Issues** (Halt production; deep investigation)

- Functional failure @ room temperature (MCU won't boot, no I2S output)
- Power rail instability (brown-out, ripple >200 mV)
- Connector/mechanical failure preventing assembly

**Action:** Escalate to hardware designer; re-spin if necessary

---

## Approval & Sign-Off

| Role | Approval | Criteria |
|------|----------|----------|
| **Hardware Lead** | PCB & electrical | EVT power-up + DVT thermal/EMI pass; DFM checklist complete |
| **Firmware Lead** | Software stack | EVT audio/LED functional; 24h uptime pass; no unresolved faults |
| **Project Manager** | Production readiness | BOM sourced, lead times confirmed, assembly procedure documented |

**Sign-off required for:** Gerber release to fab; GitHub public release announcement

---

## Documentation Deliverables

### **For Internal Use**

- EVT power-up report (photos, voltage measurements, UART output)
- DVT thermal/power curves (plots, CSV data)
- EMI test report (audio FFT, Wi-Fi range measurements)
- 24h uptime log (firmware diagnostics)

### **For Production / Assembly**

- Final BOM (LCSC C-numbers, quantities, substitutes)
- Schematic PDF (with revision)
- PCB layout (top/bottom assembly diagrams)
- Gerber + drill + IPC-2581 (manufacturing data)
- Assembly procedure (step-by-step with photos)
- Test procedure (in-circuit checks; functional validation)

### **For End-Users / Makers**

- Quick-start guide (power-on, firmware install, Wi-Fi setup)
- Schematic (for reference/hacking)
- Hardware pinout diagram
- LED & mic connector pinout
- Firmware GitHub repo link

---

## Timeline & Responsibilities

| Phase | Week | Owner | Deliverable |
|-------|------|-------|-------------|
| EVT | 1–2 | HW + FW Lead | Power-up report, audio/LED validation |
| DVT | 3–4 | HW Lead | Thermal, EMI, reliability curves |
| DFM | Concurrent | HW Lead | Gerber review, BOM check, test plan |
| Approval | 4–5 | PM + HW + FW | Sign-off memo; GitHub release ready |

---

## References

- **Hardware PRD:** `/docs/prd/02-hardware-prd.md`
- **Product Brief:** `/docs/prd/01-product-brief.md`
- **Datasheets:** `/docs/datasheets/`
- **MCP Tools:** `/hardware/k1-lightwave/README.md#mcp-tool-commands`
- **Governance:** `/claude/GOVERNANCE.md`

---

**Version:** 0.1 (Alpha Validation Plan)
**Last updated:** Oct 23, 2025
**Status:** Template ready for prototype; adjustments based on actual hardware TBD
