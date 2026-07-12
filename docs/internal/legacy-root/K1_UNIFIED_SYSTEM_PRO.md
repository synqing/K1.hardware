# K1 Unified Design System — PRO Edition

**Date:** 2025-10-24  
**Status:** ✓ COMPLETE + PRO UPGRADE  
**Components:** Design Contract v2 (PRO) + K1_ContractedPlace_PRO Plugin + Orchestrator

---

## What PRO Means

The PRO edition adds **missing intelligence before routing:**

✓ **Auto-decoupler placement** — Capacitors automatically placed ≤2.5 mm from IC power pins  
✓ **GND via ring** — EMI fence around board perimeter (every 3 mm)  
✓ **SPI return-path guard** — Stitching via lines from COM-A to COM-B (keeps return where it belongs)  
✓ **Power islands** — Rectangular 3V3/LED_5V zones on power layer (L3)  
✓ **Thermal via grids** — Under LDOs/regulators for heat spreading  
✓ **Netclasses with assignments** — SPI and USB netclasses created and nets assigned upfront  
✓ **Testpoints** — TP footprints placed on key nets (SPI, power, GND)  
✓ **All contract-driven** — Every decision editable in `tools/k1_project_v2.json`

Router now has:
- Proper anchors (outline, holes, edge connectors)
- Return paths (via guards for SPI)
- Keepouts (antenna, EMI fence)
- Thermal strategy (via grids under hot parts)
- Netclass rules (width/clearance for SPI, USB)
- Testpoint coverage

Not a starfield. A **real PCB**.

---

## The Three-Part PRO System

### 1. Design Contract v2 (Source of Truth)

**File:** `tools/k1_project_v2.json`

Defines everything:

```json
{
  "mechanical": {
    "outline": {"width": 100, "height": 70},
    "mounting_holes": [...],
    "keepouts": [{"name":"Antenna",...}],
    "edge_via_ring": {"enabled": true, "pitch_mm": 3.0}
  },
  "stackup": {
    "layers": 4,
    "map": ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu"],
    "roles": {"L1": "signals", "L2": "GND plane", "L3": "power (3V3 & LED_5V)"}
  },
  "power_nets": {"gnd": "GND", "logic_3v3": "3V3", "led_5v": "LED_5V"},
  "io": {
    "usb": {"ref": "JUSB1", "edge": "south"},
    "led_ports": {"refs": ["JLED1",...], "edge": "north"}
  },
  "placement_zones": [
    {"name": "COM_A", "refs": ["U_COMA"], "x": 18, "y": 30, "w": 38, "h": 30}
  ],
  "routing": {
    "spi": {
      "nets": {"sck": "SPI_SCK", "mosi": "SPI_MOSI", ...},
      "guard": {"enabled": true, "offset_mm": 1.2, "pitch_mm": 2.0}
    },
    "netclasses": {
      "SPI": {"width_mm": 0.2, "clear_mm": 0.2, "nets": ["SPI_SCK", ...]},
      "USB_FS": {"diff_gap_mm": 0.25, "nets": ["USB_D+", ...]}
    }
  },
  "planes": {
    "gnd": {"layer": "In1.Cu"},
    "power_islands": [
      {"net": "3V3", "layer": "In2.Cu", "rect": {"x": 5, "y": 35, "w": 45, "h": 28}}
    ]
  },
  "decoupling": {"max_distance_mm": 2.5},
  "thermal": {
    "hot_parts": [
      {"refs": ["U_LDO1"], "via_grid": {"pitch_mm": 1.2, "rows": 2, "cols": 3}}
    ]
  },
  "testpoints": {"nets": ["SPI_SCK", "3V3", "GND"], "footprint": "TestPoint:TestPoint_Pad_D1.00mm"}
}
```

See `tools/k1_project_v2.json` for full, pre-filled example.

### 2. K1_ContractedPlace_PRO Plugin

**File:** `plugins/K1_ContractedPlace_PRO.py`

Runs inside KiCad (Tools → External Plugins). Does:

1. **Mechanical:** Draws outline, places mounting holes, applies keepouts (antenna + hole rings)
2. **Edge placements:** USB on south, LEDs on north (oriented correctly)
3. **Zone placements:** COM-A/COM-B in their zones
4. **Auto-decouplers:** Finds C* parts, pairs them to IC power pads, places ≤2.5 mm away
5. **GND via ring:** Perimeter fence (every 3 mm, stitched to GND, inset 0.8 mm from edge)
6. **SPI guard:** Two rows of stitching vias from COM-A to COM-B (keeps return path tight)
7. **Power planes:** GND on L2 (full), 3V3/LED_5V islands on L3 (rectangular)
8. **Thermal vias:** Grids under LDOs/regulators (configurable rows/cols, 1.2 mm pitch)
9. **Netclasses:** Creates SPI/USB netclasses, assigns nets
10. **Testpoints:** Adds TP footprints on key nets
11. **Saves board**

Result: A **fully prepared board** ready to route. Not a starfield.

### 3. Expert Orchestrator (Routing + Validation + Export)

**File:** `agent/orchestrator/run.py`

Routes, validates DRC/DFM, exports fab pack. Reads contract for:
- Stackup (layer roles)
- Netclass rules (width, clearance, diff-pair gap)
- DFM profile (JLC standard/advanced)
- Thermal requirements

---

## The Workflow (20 minutes)

### Step 1: Understand the Contract (2 min)

```bash
cat tools/k1_project_v2.json | head -80
```

It defines board dimensions, stackup, connector edges, component zones, decoupler placement, SPI guard specs, power islands, thermal vias, testpoints.

### Step 2: Customize (if needed) (2 min)

```bash
nano tools/k1_project_v2.json

# Change if different from K1:
# - mechanical.outline (width/height)
# - io.usb.edge, io.led_ports.edge
# - placement_zones (COM-A/COM-B positions)
# - routing.spi.guard.offset_mm, pitch_mm (guard via spacing)
# - planes.power_islands (3V3/LED_5V rectangles)
# - decoupling.max_distance_mm (how close caps to power pins)
# - thermal.hot_parts (which ICs get via grids)
# - testpoints.nets (which nets get TPs)
```

### Step 3: Run PRO Plugin in KiCad (5 min)

```bash
# Open the board
kicad hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb

# Menu: Tools → External Plugins → K1: Contracted Place PRO

# Plugin applies entire contract and saves
# You'll see message: "Contract applied. Outline: 1, Holes: 4, LED ports: 4, 
#                     Decouplers: 12, GND via ring: 45, SPI guard: 30, 
#                     Power planes: 1, Thermal vias: 18, Testpoints: 6"
```

**Board now has:**
- Clear outline with dimensions
- Four corner mounting holes (with keepouts)
- USB connector on south edge
- LEDs spread evenly on north edge
- COM-A/COM-B placed in their zones
- Antenna keepout applied
- **Auto-placed decoupling capacitors** (≤2.5 mm from IC power pins)
- **GND via ring** around perimeter
- **SPI return-path guard** (two via rows from COM-A to COM-B)
- **GND plane** (full L2)
- **3V3/LED_5V power islands** (rectangular on L3)
- **Thermal via grids** under regulators
- **Netclasses created** (SPI, USB) with nets assigned
- **Testpoints placed** on SPI nets, power rails

Ready to route.

### Step 4: Run Orchestrator (5–10 min routing, <1 min validation/export)

```bash
python agent/orchestrator/run.py tools/k1_project_v2.json
```

**Phases:**
1. Verify tools, contract, board
2. Check board is populated
3. Checkpoint
4. **Route** (DSN → FreeRouting → SES import)
5. **Validate** (DRC + DFM using contract rules)
6. **Export** (Gerbers, Drill, IPC-2581, ODB++)
7. **Archive** (manifest with metadata)

**Output:**

```
fabpack_out/
├── board.dsn, board.ses
├── drc.json (zero violations expected)
├── manifest.json
├── gerbers/ (F.Cu, B.Cu, masks, silk, edge)
├── drill/ (Excellon)
├── k1.ipc2581.xml
└── k1.odb
```

### Step 5: Send to Fab

```bash
# JLCPCB or your fab:
# Upload fabpack_out/gerbers/ + fabpack_out/drill/
# Or: fabpack_out/k1.ipc2581.xml (all-in-one)
```

Done. 🎉

---

## Key PRO Features (Concrete)

### Auto-Decoupler Placement

Plugin finds all `C*` footprints with a GND pad and a power net pad (VDD, VCC, 3V3, 1V8, etc.), then:
- Finds the matching IC power pin on the same net
- Places the cap ≤2.5 mm away (editable)
- Orients for shortest loop (GND pad closest to IC GND)

Result: Decouplers are within spec without manual hunt-and-place.

### SPI Return-Path Guard

Plugin computes the midline between COM-A and COM-B placement zones, then:
- Drops **two parallel rows** of 0.3 mm via (0.6 mm diameter) every 2 mm (editable)
- Both rows tied to GND, offset 1.2 mm (editable) from the centerline
- Creates a "fence" that keeps high-frequency return current constrained

Result: Return path doesn't wander; far-field EMI reduced.

### GND Via Ring

Plugin adds a rectangular ring of 0.3 mm vias (0.6 mm diameter) every 3 mm (editable), inset 0.8 mm (editable) from the board edge:
- All tied to GND plane (L2)
- Prevents edge radiation
- Helps with board shielding

Result: Clean EMI boundary.

### Power Islands

Plugin creates rectangular copper zones on L3 (power layer):
- **GND:** Full board (slight shrink to avoid conflicts)
- **3V3, LED_5V:** User-defined rectangles (editable x, y, w, h)

Result: Low-impedance power distribution without needing manual plane editing.

### Thermal Via Grids

Plugin finds hot parts (LDOs, regulators) by reference, places a configurable grid of vias under each:
- Rows, cols, pitch (all editable)
- Tied to GND
- Spreads heat to back layer via In2.Cu

Result: Thermal performance without manual via farm creation.

### Netclasses with Assignments

Plugin creates netclasses for SPI and USB, then assigns the actual nets:
- **SPI:** SCK, MOSI, MISO, CS → width 0.2 mm, clear 0.2 mm
- **USB_FS:** D+, D- → width 0.25 mm, diff gap 0.25 mm, impedance rule

Result: Router respects SPI length match and USB differential pair constraints from the start.

### Testpoints

Plugin adds TP footprints (`TestPoint:TestPoint_Pad_D1.00mm`) on specified nets (SPI, power, GND):
- Placed automatically near pad centers
- Ready for probe connections
- Editable list in contract

Result: No guessing where to probe; all key signals covered.

---

## Customization Guide

### Change Decoupler Distance

```json
"decoupling": {
  "max_distance_mm": 1.5    ← Tighter (default: 2.5)
}
```

Re-run plugin. Caps move closer to power pins.

### Adjust SPI Guard Spacing

```json
"routing": {
  "spi": {
    "guard": {
      "offset_mm": 2.0,      ← Further from SPI centerline (default: 1.2)
      "pitch_mm": 1.0        ← Closer via spacing (default: 2.0)
    }
  }
}
```

Re-run plugin. Guard vias placed differently.

### Change Power Island Locations

```json
"planes": {
  "power_islands": [
    {"net": "3V3", "layer": "In2.Cu", "rect": {"x": 10, "y": 40, "w": 50, "h": 20}}
  ]
}
```

Re-run plugin. Islands redrawn.

### Add More Testpoints

```json
"testpoints": {
  "nets": ["SPI_SCK", "SPI_MOSI", "SPI_MISO", "SPI_CS", "3V3", "LED_5V", "GND"],
  "footprint": "TestPoint:TestPoint_Pad_D1.00mm"
}
```

Re-run plugin. TPs placed on all listed nets.

### Disable GND Via Ring

```json
"mechanical": {
  "edge_via_ring": {
    "enabled": false    ← Disable it
  }
}
```

Re-run plugin. No via ring.

---

## File Structure (PRO)

```
tools/
├── k1_project.json                  (basic version)
└── k1_project_v2.json               ← PRO CONTRACT (use this)

plugins/
├── K1_ImportAndPlace.py             (netlist import)
├── K1_ContractedPlace.py            (basic plugin)
└── K1_ContractedPlace_PRO.py        ← PRO PLUGIN (run this)

agent/orchestrator/
└── run.py                           ← ORCHESTRATOR (same for both versions)

fabpack_out/                         ← OUTPUTS
├── gerbers/
├── drill/
├── k1.ipc2581.xml
└── k1.odb
```

---

## PRO vs. Basic

| Feature | Basic | PRO |
|---------|-------|-----|
| Board outline, holes, connectors | ✓ | ✓ |
| Component zone placement | ✓ | ✓ |
| Antenna keepout | ✓ | ✓ |
| **Auto-decoupler placement** | ✗ | ✓ |
| **GND via ring** | ✗ | ✓ |
| **SPI return-path guard** | ✗ | ✓ |
| **Power islands** | ✗ | ✓ |
| **Thermal via grids** | ✗ | ✓ |
| **Netclass creation + assignment** | ✗ | ✓ |
| **Testpoint placement** | ✗ | ✓ |

---

## Next Steps (PRO)

1. ✓ Edit `tools/k1_project_v2.json` (if customizing)
2. ✓ Run K1_ContractedPlace_PRO in KiCad (Tools → External Plugins)
3. ✓ Run orchestrator: `python agent/orchestrator/run.py tools/k1_project_v2.json`
4. ✓ Send fab pack to JLCPCB

---

## Limitations & Guards (Already Handled)

✓ If a zone name doesn't exist, plugin skips it (no crash)  
✓ If a netclass can't be created, plugin continues (no crash)  
✓ If thermal via footprint doesn't exist, logs warning (no crash)  
✓ If contract is missing, plugin fails loudly with clear error  
✓ If outline is missing and can't be drawn, plugin fails hard  

---

## Future Enhancements (PRO Ready)

* **Heuristics v2:** Auto-cluster passives by net connectivity
* **Impedance JSON → KiCad stack import:** Generate stackup from contract
* **Rule-area corridors:** Create rule-areas over SPI corridor only
* **Autorouter hints:** Export Specctra keepouts for FreeRouting

---

## Summary: PRO Edition

**Design Contract v2** defines every decision.  
**K1_ContractedPlace_PRO Plugin** enforces it (auto-decouplers, via guards, planes, thermal, testpoints).  
**Orchestrator** routes, validates, exports.

**Result:** A **professional-grade PCB**, deterministic and reproducible, from a single contract file.

Not guessing. Not hand-placing decouplers. Not hunting for return paths.

---

**Status:** ✓ COMPLETE & READY  
**Last Updated:** 2025-10-24
