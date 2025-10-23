# K1 LIGHTWAVE — HARDWARE DESIGN GOVERNANCE

## Overview

This document governs how Claude agents interact with the K1 Lightwave hardware PCB design project. All changes to schematics, layout, component selections, and manufacturing data must follow this protocol to prevent cascading failures in electrical performance, manufacturability, and assembly.

---

## Project Context

**Hardware target**: K1 Lightwave dual-ESP32-S3 music visualizer
- **MCU**: 2× ESP32-S3-WROOM-1/1U (I/O mapping TBD)
- **Audio input**: SPH0645 + IM69D130 digital MEMS microphones
- **LED output**: WS2812B/SK6812 addressable LEDs with SN74AHCT125 level shifter
- **Power**: 5V input rail, LDO/buck regulators for 3.3V logic
- **PCB**: 4-layer, JLC/PCBWay manufacturing rules, DRC class per vendor

---

## Three-Phase Design Change Protocol

### **PHASE 1: IMPACT ASSESSMENT (Before ANY design change)**

**Step 1: Identify the change scope**
- What file(s) are you modifying? (`.kicad_sch`, `.kicad_sym`, `.kicad_pcb`)
- What component(s) or nets are affected?
- Why are you making this change?

**Step 2: Check risk level**

```
RISK LEVEL 1 (Low risk):
- Documentation, naming, comments
- Non-critical footprint improvements
→ Proceed normally

RISK LEVEL 2 (Medium risk):
- Component value changes (caps, resistors)
- Decoupling adjustments
- Clock/timing changes
- Layout spacing (non-critical paths)

RISK LEVEL 3 (Critical):
- MCU pin assignments, I2S/SPI routing
- Audio signal paths
- Power rail voltage/current
- Ground plane changes
- LED signal path or level shifter config
- Thermal via placement
- Manufacturing stackup changes

IF RISK LEVEL 2+: Continue to Phase 2
```

---

### **PHASE 2: DEPENDENCY ANALYSIS (For Risk Level 2+ ONLY)**

Before making ANY changes:

- [ ] **Identify electrical dependencies**
- [ ] **Understand thermal implications**
- [ ] **Verify signal integrity constraints**
- [ ] **Check manufacturing compatibility**
- [ ] **Cross-reference component datasheets**

---

### **PHASE 3: CHANGE VALIDATION (For Risk Level 2+ ONLY)**

After making changes:

- [ ] **ERC passes**: `sch_erc(project.kicad_sch, out="erc.json")` → error_count=0
- [ ] **DRC passes**: `pcb_drc(board.kicad_pcb, out="drc.json")` → no violations
- [ ] **BOM validates** against Nexar/LCSC availability
- [ ] **No critical net changes** without full re-verification
- [ ] **Thermal analysis passes** (if high-current)
- [ ] **Layout rules satisfied** (keepouts, impedance, routing)

---

## Critical Files

| File | Why Critical | Failure Cost |
|------|-------------|--------------|
| `kicad/K1_Lightwave.kicad_sch` | Master schematic | Full re-spin |
| `kicad/K1_Lightwave.kicad_pcb` | PCB layout + stackup | Manufacturability fail |
| `kicad/symbols/esp32-s3-wroom-1.kicad_sym` | MCU pinout | PCB rework impossible |
| `kicad/design_rules.kicad_dru` | DRC rules (vendor-locked) | Fab rejection |

---

## MCP Tools Available

- `sch_erc()` — schematic check
- `pcb_drc()` — PCB check
- `sch_export_bom()` — BOM export
- `parts_search()` — Nexar lookup
- `best_datasheet_url()` — datasheet fetch
- `kikit_panelize()` — panelization preview

**Better to ask for review than to spin a bad PCB.**
