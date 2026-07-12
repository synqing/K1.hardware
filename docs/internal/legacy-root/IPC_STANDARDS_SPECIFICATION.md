# IPC Standards Library - Complete Technical Specification

## Executive Summary

This document provides complete technical specifications for the IPC Standards Library, a production-ready Python implementation of IPC-2221A, IPC-6012, and IPC-A-610 standards with K1 Lightwave audio-reactive LED controller specific configurations.

**Library Version:** 1.0.0 (Production Release)
**Created:** 2025-10-24
**Target Platform:** K1 Lightwave ESP32-S3 Dual-MCU Controller
**Manufacturing:** JLCPCB Standard 4-Layer (JLC02160H-1LG)

---

## Table of Contents

1. [IPC-2221A: Trace Width and Clearance](#ipc-2221a-trace-width-and-clearance)
2. [IPC-6012: PCB Class Requirements](#ipc-6012-pcb-class-requirements)
3. [IPC-A-610: Assembly Standards](#ipc-a-610-assembly-standards)
4. [K1 Configuration](#k1-configuration)
5. [Implementation Guide](#implementation-guide)
6. [Reference Tables](#reference-tables)

---

## IPC-2221A: Trace Width and Clearance

### 1.1 Trace Width Calculation Formula

The exact IPC-2221A formula for calculating current capacity is:

```
I = 0.048 × ΔT^0.44 × A^0.725  (external layers)
I = 0.024 × ΔT^0.44 × A^0.725  (internal layers)
```

Where:
- **I** = Current capacity (amperes)
- **ΔT** = Allowable temperature rise (°C)
- **A** = Cross-sectional area of trace (mils²)
- **k** = Constant: 0.048 (external), 0.024 (internal)

**Rearranged for trace width calculation:**

```
A = (I / (k × ΔT^0.44))^(1/0.725)
Trace Width (mils) = A / Copper Thickness (mils)
```

### 1.2 Temperature Rise Constants (ΔT)

The following temperature rise classes are defined for different signal types and board locations:

| Class | Location | Application | ΔT (°C) |
|-------|----------|-------------|---------|
| LOW_FREQ_INTERNAL | Internal | Low-frequency signals | 10 |
| LOW_FREQ_EXTERNAL | External | Low-frequency signals | 20 |
| DIGITAL_INTERNAL | Internal | Digital signals | 15 |
| DIGITAL_EXTERNAL | External | Digital signals | 25 |
| POWER_INTERNAL | Internal | Power distribution | 20 |
| POWER_EXTERNAL | External | Power distribution | 30 |
| HIGH_SPEED_INTERNAL | Internal | High-speed digital | 25 |
| HIGH_SPEED_EXTERNAL | External | High-speed digital | 40 |
| CRITICAL_INTERNAL | Internal | Mission-critical | 15 |
| CRITICAL_EXTERNAL | External | Mission-critical | 20 |

**K1 Application Recommendations:**
- VBUS_USB_5V domain (5V logic): Use DIGITAL_EXTERNAL (25°C)
- LED_5V domain (high-current power): Use POWER_EXTERNAL (30°C)
- 3V3_LOGIC domain (digital signals): Use DIGITAL_INTERNAL (15°C)

### 1.3 Copper Thickness Conversion

Standard PCB copper weights:

| Designation | Weight (oz/ft²) | Thickness (mils) |
|-------------|-----------------|------------------|
| 0.5 oz | 0.5 | 0.689 |
| 1 oz (standard) | 1.0 | 1.378 |
| 2 oz (high-current) | 2.0 | 2.756 |

**Conversion:** 1 oz/ft² = 1.378 mils

### 1.4 Trace Width Calculation Example

**Example: K1 LED_5V Domain (8A Peak Current)**

Given:
- Current: 8000 mA (8 A)
- Temperature rise: 30°C (POWER_EXTERNAL)
- Copper weight: 1 oz/ft² (1.378 mils)
- Layer: External

Calculation:
```
1. Temperature factor: 30^0.44 = 3.39
2. Required area: (8 / (0.048 × 3.39))^(1/0.725)
                = (8 / 0.1627)^1.379
                = (49.15)^1.379
                = 145.2 mils²
3. Trace width: 145.2 / 1.378 = 105.5 mils
4. Rounded to standard: 125 mils (IPC standard)
5. Design rule: Apply 1.5× safety factor = 125 mils acceptable
```

**Result:** Minimum 63 mils, recommended 125 mils for LED_5V domain

### 1.5 Standard Trace Widths (IPC Manufacturing)

The following widths are standard manufacturing increments:

```
1, 2, 3, 5, 8, 10, 15, 20, 25, 32, 40, 50, 63, 80, 100, 125+ mils
```

All calculated trace widths must be rounded UP to the nearest standard width.

### 1.6 Clearance Tables (Complete)

#### 1.6.1 Trace-to-Trace Clearance (mils)

| Voltage Class | Class 1 | Class 2A | Class 2B | Class 3A | Class 3B |
|---------------|---------|----------|----------|----------|----------|
| ULTRA_LOW (0-6V) | 3 | 3 | 4 | 5 | 6 |
| LOW (7-15V) | 3 | 4 | 5 | 6 | 8 |
| MEDIUM_LOW (16-30V) | 4 | 5 | 6 | 8 | 10 |
| MEDIUM (31-100V) | 6 | 8 | 10 | 12 | 15 |
| MEDIUM_HIGH (101-200V) | 10 | 12 | 15 | 20 | 25 |
| HIGH (201-500V) | 15 | 20 | 25 | 30 | 40 |

**K1 Context:**
- VBUS_USB_5V (5V): VoltageClass.LOW → 3-4 mils (Class 2A)
- LED_5V (5V): VoltageClass.LOW → 3-4 mils (Class 2A)
- 3V3_LOGIC (3.3V): VoltageClass.ULTRA_LOW → 3 mils (Class 2A)

#### 1.6.2 Trace-to-Board-Edge Clearance (mils)

| Voltage Class | Class 1 | Class 2A | Class 2B | Class 3A | Class 3B |
|---------------|---------|----------|----------|----------|----------|
| ULTRA_LOW | 10 | 10 | 15 | 20 | 25 |
| LOW | 10 | 15 | 20 | 25 | 30 |
| MEDIUM_LOW | 15 | 20 | 25 | 30 | 40 |
| MEDIUM | 20 | 25 | 30 | 40 | 50 |
| MEDIUM_HIGH | 30 | 40 | 50 | 60 | 75 |
| HIGH | 50 | 60 | 75 | 100 | 125 |

#### 1.6.3 Trace-to-Component-Leads Clearance (mils)

| Voltage Class | Class 1 | Class 2A | Class 2B | Class 3A | Class 3B |
|---------------|---------|----------|----------|----------|----------|
| ULTRA_LOW | 8 | 10 | 12 | 15 | 20 |
| LOW | 10 | 12 | 15 | 20 | 25 |
| MEDIUM_LOW | 12 | 15 | 20 | 25 | 30 |
| MEDIUM | 15 | 20 | 25 | 30 | 40 |
| MEDIUM_HIGH | 25 | 30 | 40 | 50 | 60 |
| HIGH | 40 | 50 | 60 | 75 | 100 |

**Environmental Classification (IPC-2221A):**
- **Class 1:** Controlled environment, dry (manufacturing facility)
- **Class 2A:** Room temperature, moderate humidity, altitude < 2500m
- **Class 2B:** Room temperature, moderate humidity, altitude > 2500m
- **Class 3A:** Uncontrolled, high humidity, altitude < 2500m
- **Class 3B:** Uncontrolled, high humidity, altitude > 2500m

**K1 Default:** Class 2A (controlled indoor environment, moderate humidity)

---

## IPC-6012: PCB Class Requirements

### 2.1 PCB Class Overview

IPC-6012 defines three PCB classes with increasing manufacturing and quality requirements:

| Class | Name | Environment | Repair | Applications |
|-------|------|-------------|--------|--------------|
| 1 | General Electronics | Controlled manufacturing | Permitted | Consumer, non-critical industrial |
| 2 | Dedicated Service | Commercial/industrial | Limited | Automotive, industrial controllers, audio/visual |
| 3 | High-Reliability | Demanding | Severely restricted | Military, aerospace, medical, safety-critical |

### 2.2 Detailed Requirements (Class 1, 2, 3)

#### 2.2.1 Copper Pattern Definition

| Requirement | Class 1 | Class 2 | Class 3 |
|-------------|---------|---------|---------|
| Tolerance | ±0.005" typical | ±0.003" typical | ±0.002" typical |
| Effect | General spacing | Tighter trace control | High-density designs |

#### 2.2.2 Via and Hole Size Tolerance

| Requirement | Class 1 | Class 2 | Class 3 |
|-------------|---------|---------|---------|
| Tolerance | ±0.005" | ±0.003" | ±0.002" |
| Impact | Standard drilling | Tighter control | Precision drilling |

#### 2.2.3 Solder Mask Thickness

| Requirement | Class 1 | Class 2 | Class 3 |
|-------------|---------|---------|---------|
| Thickness | 0.0008-0.0015" | 0.001-0.002" | 0.0015-0.0025" |
| Purpose | Basic trace protection | Enhanced isolation | Maximum protection |

#### 2.2.4 Minimum Trace Width and Spacing

| Requirement | Class 1 | Class 2 | Class 3 |
|-------------|---------|---------|---------|
| Trace / Spacing | 5 mil / 5 mil | 4 mil / 4 mil | 3 mil / 3 mil |
| Note | Voltage-dependent; higher voltage requires larger spacing |

#### 2.2.5 Copper Plating Thickness (Via/Hole Walls)

| Requirement | Class 1 | Class 2 | Class 3 |
|-------------|---------|---------|---------|
| Minimum | ≥0.0007" | ≥0.001" | ≥0.0015" |
| Reliability | Standard | Enhanced | Maximum |

#### 2.2.6 Registration Tolerance (Layer-to-Layer Alignment)

| Requirement | Class 1 | Class 2 | Class 3 |
|-------------|---------|---------|---------|
| Tolerance | ±0.005" | ±0.003" | ±0.002" |
| Impact | General alignment | Tight control | Precision alignment |

#### 2.2.7 Minimum Annular Ring (Copper Ring Around Via)

| Requirement | Class 1 | Class 2 | Class 3 |
|-------------|---------|---------|---------|
| Minimum | 0.005" | 0.008" | 0.010" |
| Purpose | Ensure via connectivity | Enhanced reliability | Maximum margin |

### 2.3 Electrical Testing Requirements

#### 2.3.1 Hi-Pot (High Voltage) Testing

| Parameter | Class 1 | Class 2 | Class 3 |
|-----------|---------|---------|---------|
| Test Voltage | 100V min | 250V min | 500V min |
| Duration | 1 minute | 2 minutes | 5 minutes |
| Fault Current Limit | 500mA max | 200mA max | 100mA max |
| Required | Optional | Required | Required (critical) |

#### 2.3.2 Insulation Resistance

| Parameter | Class 1 | Class 2 | Class 3 |
|-----------|---------|---------|---------|
| Minimum (dry) | ≥100MΩ (optional) | ≥100MΩ | ≥500MΩ |
| Test Conditions | 500VDC | 500VDC | 500VDC |

### 2.4 K1 PCB Class Selection: CLASS 2

**Rationale:**
- Audio-reactive LED controller with continuous operation
- Consumer electronics with moderate reliability requirements
- Commercial manufacturing environment (JLCPCB)
- Suitable for audio/visual equipment per IPC-6012

**K1 Manufacturing Specifications:**
```
PCB Class: 2 (Dedicated Service)
Manufacturing: JLCPCB Standard 4-Layer (JLC02160H-1LG)
Copper Weight: 1 oz/ft² (standard)
Solder Mask: LPI (Liquid Photo-Imageable)
Silkscreen: White
Via Type: Mechanical drilling, standard plating
Test Voltage: 250V, 2 minutes
Insulation Resistance: ≥100MΩ
```

---

## IPC-A-610: Assembly Standards

### 3.1 Solder Joint Visual Acceptance Criteria

IPC-A-610 defines three acceptance levels:
- **Type I:** General electronics (Class 1 PCB)
- **Type II:** Dedicated service (Class 2 PCB) - K1 standard
- **Type III:** High-reliability (Class 3 PCB)

### 3.2 Solder Joint Quality Criteria

#### 3.2.1 Fillet Shape (45° Angle Expected)

| Criterion | Acceptable | Rework | Reject |
|-----------|-----------|--------|--------|
| Description | Smooth, continuous, 45° angle | Slightly uneven, <5mm² missing | Completely missing or severely deformed |
| Visual | Clear continuous flow | Minor irregularities | No visible solder |

#### 3.2.2 Wetting (Lead Surface Coverage)

| Criterion | Acceptable | Rework | Reject |
|-----------|-----------|--------|--------|
| Coverage | >75% of lead wetted | 50-75% wetted | <50% wetted |
| Appearance | Shiny, smooth | Dull, partial | Cold joint appearance |

#### 3.2.3 Solder Volume

| Criterion | Acceptable | Rework | Reject |
|-----------|-----------|--------|--------|
| Volume | Adequate to fill fillet | Slightly insufficient/excess | Insufficient or excessive |
| Assessment | No void visibility | Minor excess visible | Inadequate solder mass |

#### 3.2.4 Voiding (Internal Void Percentage)

| Criterion | Acceptable | Rework | Reject |
|-----------|-----------|--------|--------|
| Internal | <10% void area | 10-25% void area | >25% void area |
| Pad Area | <1% interconnect pad voids | Small isolated voids | Large voids affecting connectivity |

#### 3.2.5 Pad Coverage (Solder on Pad)

| Criterion | Acceptable | Rework | Reject |
|-----------|-----------|--------|--------|
| Coverage | ≥75% of pad | 50-75% of pad | <50% of pad |
| Effect | Ensures good electrical connection | Marginal connection | Poor electrical contact |

#### 3.2.6 Coplanarity (Component Height Variation)

| Criterion | Acceptable | Rework | Reject |
|-----------|-----------|--------|--------|
| Max Deviation | ≤0.10 inch | 0.10-0.20 inch | >0.20 inch |
| Impact | Reflow oven uniform | Minor wave-solder issues | Reflow soldering problems |

#### 3.2.7 Component Lead Bending

| Criterion | Acceptable | Rework | Reject |
|-----------|-----------|--------|--------|
| Condition | No visible bending | <0.015" offset | Significant bending |
| Offset | Within spec | Minor deviation | Out of specification |

#### 3.2.8 Solder Bridging

| Criterion | Acceptable | Rework | Reject |
|-----------|-----------|--------|--------|
| Bridging | No bridging | <0.010" wide, isolated | Significant bridging |
| Function | No electrical shorts | Isolated, non-functional | Affects electrical function |

### 3.3 Component Placement Tolerances (IPC-A-610)

#### 3.3.1 Chip Component Placement (X/Y, mils)

| Component Type | Class 1 | Class 2 | Class 3 |
|----------------|---------|---------|---------|
| Standard chips | ±100 | ±75 | ±50 |
| Fine-pitch | ±50 | ±40 | ±25 |

#### 3.3.2 Chip Component Rotation (degrees)

| Component Type | Class 1 | Class 2 | Class 3 |
|----------------|---------|---------|---------|
| Standard | ±5.0° | ±3.0° | ±2.0° |

#### 3.3.3 BGA and Connector Pin Placement (mils)

| Type | Class 1 | Class 2 | Class 3 |
|------|---------|---------|---------|
| BGA columns | ±50 | ±40 | ±25 |
| Connector pins | ±50 | ±40 | ±25 |

### 3.4 Pad Size Requirements

#### 3.4.1 Chip Component Pad Sizes

| Package | Min Length | Min Width | Paste Coverage |
|---------|-----------|-----------|-----------------|
| 0402 | 30 mils | 30 mils | 50% |
| 0603 | 40 mils | 40 mils | 50% |
| 0805 | 50 mils | 50 mils | 50% |
| 1206 | 60 mils | 60 mils | 50% |

#### 3.4.2 QFP Package Pads

| Parameter | Value |
|-----------|-------|
| Min pad length | 20 mils |
| Min pad width | 8 mils |
| Paste coverage | 50% |

#### 3.4.3 BGA Pads

| Parameter | Value |
|-----------|-------|
| Min pad diameter | 8 mils |
| Paste coverage | 75% (higher than standard) |

### 3.5 Test Point Requirements

| Parameter | Specification |
|-----------|--------------|
| Diameter (min) | 25 mils |
| Diameter (max) | 50 mils |
| Center-to-center spacing | 100 mils minimum |
| Clearance from component | 50 mils |
| Clearance from pad | 50 mils |
| Placement | Via or raised pad |

### 3.6 Lead/Pin Size Requirements

| Component Type | Lead Diameter | Hole Diameter | Notes |
|----------------|---------------|--------------|-------|
| Single In-Line (SIL) | 0.030-0.045" | 0.035-0.050" | DIP-style |
| Dual In-Line (DIP) | 0.030-0.045" | 0.035-0.050" | 0.100" pitch |
| Axial (resistor, diode) | 0.015-0.035" | 0.020-0.045" | Depends on package |
| Ball Grid Array (BGA) | 0.030-0.050" | N/A | Solder ball diameter |

---

## K1 Configuration

### 4.1 K1 Power Domains

K1 Lightwave uses three isolated power domains:

#### 4.1.1 VBUS_USB_5V Domain

| Parameter | Value |
|-----------|-------|
| Voltage | 5.0V |
| Typical Current | 500 mA |
| Peak Current | 1200 mA |
| Temperature Rise Class | DIGITAL_EXTERNAL (25°C) |
| Voltage Class | LOW (7-15V) |
| Isolation Required | No |
| Purpose | USB input, logic power only |
| Load | MCU, digital logic (no high-current output) |

**Trace Width Calculation:**
```
Width @ 1200mA peak: ~8-10 mils (with safety factor)
Minimum clearance (trace-to-trace): 4 mils (Class 2A)
```

#### 4.1.2 LED_5V Domain

| Parameter | Value |
|-----------|-------|
| Voltage | 5.0V |
| Typical Current | 2000 mA |
| Peak Current | 8000 mA |
| Temperature Rise Class | POWER_EXTERNAL (30°C) |
| Voltage Class | LOW (7-15V) |
| Isolation Required | **Yes** |
| Purpose | High-current LED output (isolated from USB) |
| Load | 4× 320-LED NeoPixel output ports (WS2812B-class) |

**Trace Width Calculation:**
```
Width @ 8000mA peak: ~63-125 mils (with safety factor)
Minimum clearance (trace-to-trace): 4 mils (Class 2A)
Note: High current drives very wide traces
```

#### 4.1.3 3V3_LOGIC Domain

| Parameter | Value |
|-----------|-------|
| Voltage | 3.3V |
| Typical Current | 400 mA |
| Peak Current | 800 mA |
| Temperature Rise Class | DIGITAL_INTERNAL (15°C) |
| Voltage Class | ULTRA_LOW (0-6V) |
| Isolation Required | No |
| Purpose | MCU and digital logic |
| Supply | Regulated from VBUS_USB_5V via LDO |

**Trace Width Calculation:**
```
Width @ 800mA peak: ~3-5 mils (with safety factor)
Minimum clearance (trace-to-trace): 3 mils (Class 2A)
```

### 4.2 K1 Design Rules (IPC-2221A, IPC-6012 Class 2)

| Parameter | Value | Reference |
|-----------|-------|-----------|
| PCB Class | Class 2 | IPC-6012 |
| Minimum trace width | 5 mils | Power domain dependent |
| Minimum trace spacing | 5 mils | Low voltage, Class 2A |
| Board edge clearance | 10 mils | Low voltage, Class 2A |
| Minimum via diameter | 10 mils | Manufacturing capability |
| Minimum pad size | 8 mils | Component specific |
| Copper weight | 1 oz/ft² | Standard JLCPCB |
| Solder mask | LPI | Liquid Photo-Imageable |
| Silkscreen | White | Standard |

### 4.3 K1 Recommended Trace Widths (with 1.5× Safety Factor)

| Domain | Peak Current | Rise Class | Width (rounded) |
|--------|--------------|-----------|-----------------|
| VBUS_USB_5V | 1200 mA | DIGITAL_EXT (25°C) | **10 mils** |
| LED_5V | 8000 mA | POWER_EXT (30°C) | **125 mils** |
| 3V3_LOGIC | 800 mA | DIGITAL_INT (15°C) | **5 mils** |

### 4.4 K1 Clearance Requirements (Class 2A Environment)

| Domain | Trace-to-Trace | Trace-to-Edge | Trace-to-Leads |
|--------|-----------------|---------------|-----------------|
| All (5V) | 4 mils | 15 mils | 12 mils |
| All (3.3V) | 3 mils | 10 mils | 10 mils |

### 4.5 K1 Signal Integrity Specifications

| Signal | Max Frequency | Impedance Control | Length Matching |
|--------|---------------|-------------------|-----------------|
| Inter-MCU SPI | 40 MHz | Not required | Not critical |
| Audio I2S | 2.822 MHz | Not required | Not critical |
| LED output | 10 MHz | Not required | Not critical |

**Rationale:** K1 frequencies are low enough that transmission line effects and impedance discontinuities are not significant. Conservative trace routing without complex rules is appropriate.

### 4.6 K1 Operating Conditions

| Parameter | Value |
|-----------|-------|
| Ambient temperature (min) | 0°C |
| Ambient temperature (max) | 50°C |
| Allowable temperature rise | 20°C |
| Maximum component temperature | 70°C |
| Environmental class (IPC-2221A) | Class 2A |
| Humidity (operation) | 30-85% RH (non-condensing) |

### 4.7 K1 Test Requirements (IPC-6012 Class 2)

| Test | Specification |
|------|--------------|
| Hi-pot voltage | 250V |
| Duration | 2 minutes |
| Insulation resistance | ≥100MΩ @ 500VDC |
| Continuity test | Required |
| Electrical test | Required (open/short) |
| Functional test | Required (basic verification) |
| Burn-in | Not required (Class 2) |

---

## Implementation Guide

### 5.1 Python Library Usage

#### 5.1.1 Trace Width Calculation

```python
from ipc_standards_library import IPC2221A, TemperatureRise

# Calculate trace width for LED_5V domain (8A peak)
trace_width_mils, area_mils2 = IPC2221A.calculate_trace_width(
    current_ma=8000,
    temp_rise=TemperatureRise.POWER_EXTERNAL,
    is_external=True,
    copper_oz=1.0,
)

# Round to standard width
standard_width = IPC2221A.round_trace_width(trace_width_mils)
print(f"Required trace width: {standard_width} mils")
```

#### 5.1.2 Clearance Lookup

```python
from ipc_standards_library import IPC2221A, VoltageClass, EnvironmentalCondition

# Get clearance for 5V signal in Class 2A environment
clearance_mils = IPC2221A.get_clearance(
    clearance_type='trace_to_trace',
    voltage_class=VoltageClass.LOW,
    environmental=EnvironmentalCondition.CLASS_2A,
)
print(f"Minimum clearance: {clearance_mils} mils")
```

#### 5.1.3 K1 Configuration

```python
from ipc_standards_library import K1Configuration

# Get recommended trace width for LED domain
led_trace_width = K1Configuration.get_recommended_trace_width('LED_5V')
print(f"LED_5V recommended width: {led_trace_width} mils")

# Get all clearances for domain
clearances = K1Configuration.get_clearance_for_domain('VBUS_USB_5V')
print(f"VBUS clearances: {clearances}")
```

#### 5.1.4 Design Validation

```python
from ipc_standards_library import validate_design

valid, message = validate_design(
    trace_width_mils=125.0,
    clearance_mils=4.0,
    voltage=5.0,
)
print(f"Valid: {valid}, Message: {message}")
```

### 5.2 Report Generation

```python
from ipc_standards_library import IPCReporter

report = IPCReporter.generate_pcb_design_report("K1 Lightwave PCB")
print(report)
```

---

## Reference Tables

### Appendix A: Conversion Factors

| From | To | Factor |
|------|----|----|
| Inches | Mils | ×1000 |
| Inches | MM | ×25.4 |
| Ounces (copper) | Mils | ×1.378 |
| Amperes | Milliamps | ×1000 |
| MM | Mils | ×39.37 |

### Appendix B: Common Trace Width Applications

| Application | Typical Current | Recommended Width | Notes |
|-------------|-----------------|-------------------|-------|
| Signal (digital) | <100 mA | 5-10 mils | Low power |
| Power (3.3V) | 500 mA | 15-20 mils | Medium power |
| Power (5V) | 1-2 A | 25-50 mils | High power |
| Power distribution | 8+ A | 100+ mils | Very high power |

### Appendix C: Standard Manufacturing Capabilities

**JLCPCB Standard 4-Layer (JLC02160H-1LG):**
- Minimum trace/space: 4 mil / 4 mil
- Standard via: 10 mil diameter
- Via aspect ratio: 8:1 (typical)
- Board thickness: 1.6 mm
- Copper weight: 1 oz/ft² (standard)
- Lead time: 24-48 hours

### Appendix D: Quick Reference - K1 Design Summary

```
PCB Class:               IPC-6012 Class 2
Manufacturing:           JLCPCB Standard 4-Layer
Test Voltage:            250V, 2 minutes
Insulation Resistance:   ≥100MΩ

Power Domains:
  VBUS_USB_5V:    5V, 1.2A peak, 10 mil traces, isolated
  LED_5V:         5V, 8.0A peak, 125 mil traces, isolated
  3V3_LOGIC:      3.3V, 0.8A peak, 5 mil traces

Environmental:          Class 2A (controlled, moderate humidity)
Temperature Rise:       20°C above ambient
Operating Range:        0-50°C ambient

Clearances (Low voltage, Class 2A):
  Trace-to-trace:       4 mils
  Trace-to-edge:        15 mils
  Trace-to-leads:       12 mils
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-10-24 | Initial production release |

---

## Document Control

**Status:** Released - Production Use
**Next Review:** 2026-10-24
**Document Owner:** Electronics Manufacturing Standards
**Last Updated:** 2025-10-24
**Confidentiality:** Internal Use

---

## End of Document

For questions or clarifications on IPC standards implementation, refer to:
- IPC-2221A: Generic Standard on Printed Board Design
- IPC-6012: Specification for Printed Circuit Boards
- IPC-A-610: Acceptability of Electronic Assemblies
