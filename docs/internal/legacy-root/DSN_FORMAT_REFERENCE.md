# Specctra DSN Format Complete Reference

## Table of Contents
1. [Format Overview](#format-overview)
2. [Complete Grammar](#complete-grammar)
3. [Real-World K1 Example](#real-world-k1-example)
4. [Common Pitfalls](#common-pitfalls)
5. [KiCad Export Details](#kicad-export-details)

---

## Format Overview

**Specctra DSN** (Design Space Notation) is an S-expression-based text format for representing PCB designs.

### Key Characteristics
- **Text-based:** Human-readable, version-controllable
- **S-expressions:** Lisp-like parenthesized notation
- **Hierarchical:** Nested structures for board organization
- **Standardized:** Cadence Specctra reference (1990s–2000s)
- **Language-agnostic:** Tool-independent representation

### File Structure (Top-Level)

```
(pcb <filename>
  (parser <parser_info>)
  (resolution <resolution>)
  (unit <unit>)
  (structure <board_structure>)
  (placement <component_placement>)
  (library <component_library>)
  (network <electrical_networks>)
  (wiring <routed_or_unrouted_connections>)
)
```

---

## Complete Grammar

### 1. Root Element: PCB

```
(pcb <string>           ; Filename (e.g., "board.dsn")
  <parser>
  <resolution>
  <unit>
  [<structure>]
  [<placement>]
  [<library>]
  [<network>]
  [<wiring>]
)
```

### 2. Parser Section (Configuration)

```
(parser
  (string_quote <char>)           ; Character for string quoting (usually ")
  (space_in_quoted_tokens <on|off>) ; Allow spaces in quoted identifiers
  (host_cad <string>)             ; Source CAD (e.g., "kicad", "eagle")
  (host_version <string>)         ; CAD version (e.g., "8.0")
  [<other_settings>]
)
```

**Example:**
```
(parser
  (string_quote ")
  (space_in_quoted_tokens on)
  (host_cad "kicad")
  (host_version "8.0")
)
```

### 3. Resolution (Coordinate System)

```
(resolution <unit> <scale>)
```

- `<unit>`: `um` (micrometers), `mil` (mils), `inch`
- `<scale>`: Integer multiplier (typically 10)

**Example:**
```
(resolution um 10)        ; 1 unit = 10 micrometers
(resolution mil 100)      ; 1 unit = 100 mils
```

**Interpretation:** Coordinates are stored as integers; actual measurement = coordinate × scale.

### 4. Unit (Coordinate Unit Type)

```
(unit <unit_type>)
```

- `um`: Micrometers
- `mil`: Mils
- `inch`: Inches
- `cm`: Centimeters
- `mm`: Millimeters

**Example:**
```
(unit mm)                 ; All dimensions interpreted as millimeters
```

### 5. Structure Section (Board Definition)

```
(structure
  (layer_descriptor
    (layer <num> <name> <type> [<properties>])
    ...
  )
  [<boundary>]
  [<via>]
  [<rule>]
  [<plane>]
)
```

#### 5.1 Layer Descriptor

```
(layer <number> <name>
  (type <signal|power|dielectric>)
  [<properties>]
)
```

**Example:**
```
(layer_descriptor
  (layer 1 "F.Cu" (type signal))
  (layer 2 "In1" (type power))
  (layer 3 "In2" (type signal))
  (layer 4 "B.Cu" (type signal))
)
```

#### 5.2 Board Boundary

```
(boundary
  (path <width> <x0> <y0> <x1> <y1> ... <xn> <yn>)
)
```

**Example (100×80 mm board in um, scale 10):**
```
(boundary
  (path 0
    0 0                    ; Origin
    100000 0               ; 100 mm right
    100000 80000           ; 80 mm up
    0 80000                ; Back to start
    0 0
  )
)
```

#### 5.3 Via Definition

```
(via <name>
  (at <x> <y> <layer>)
  (size <diameter>)
  (drill <drill_diameter>)
  [<padstack_id>]
)
```

**Example:**
```
(via "Via0.8"
  (at 0 0 "F.Cu")
  (size 800)              ; 800 µm = 0.8 mm
  (drill 400)             ; 400 µm drill
)
```

#### 5.4 Design Rules

```
(rule
  (width <minimum>)
  (clearance <minimum>)
  (via_spacing <minimum>)
  [<other_rules>]
)
```

**Example:**
```
(rule
  (width 200)             ; 200 µm = 0.2 mm minimum trace width
  (clearance 250)         ; 250 µm = 0.25 mm minimum clearance
  (via_spacing 300)       ; 300 µm via-to-via spacing
)
```

### 6. Placement Section (Component Placement)

```
(placement
  (component <reference>
    (place <x> <y> <angle> <side>)
    [<shape>]
  )
  ...
)
```

- `<reference>`: Component reference (R1, U1, C3, etc.)
- `<x>, <y>`: Placement coordinates
- `<angle>`: Rotation angle (0, 90, 180, 270)
- `<side>`: `front` or `back`

**Example:**
```
(placement
  (component "U1"
    (place 25000 25000 0 front)  ; U1 at (25mm, 25mm), no rotation, front
  )
  (component "R1"
    (place 35000 25000 90 front) ; R1 at (35mm, 25mm), 90° rotation, front
  )
  (component "C1"
    (place 45000 25000 0 back)   ; C1 on back side
  )
)
```

### 7. Library Section (Component Definitions)

```
(library
  (image <component_name>
    [<outline>]
    [<pin>]
    [<keepout>]
  )
  ...
)
```

#### 7.1 Image (Component Symbol)

```
(image <name>
  [<outline>]
  [<pin>]
)
```

#### 7.2 Pin Definition

```
(pin <number>
  (at <x> <y>)
  [<padstack_id>]
  [<pin_name>]
)
```

**Example:**
```
(library
  (image "SOIC-8"
    (pin 1 (at 0 0) "GND")
    (pin 2 (at 1270 0) "RX")
    (pin 3 (at 2540 0) "TX")
    (pin 4 (at 3810 0) "VCC")
    (pin 5 (at 3810 -1270))
    (pin 6 (at 2540 -1270))
    (pin 7 (at 1270 -1270))
    (pin 8 (at 0 -1270))
  )
)
```

### 8. Network Section (Electrical Connectivity)

```
(network
  (net <net_name>
    (pins <ref.pad> <ref.pad> ...)
    [<class>]
  )
  ...
  [<class_descriptor>]
)
```

#### 8.1 Net Definition

```
(net <name>
  (pins <component>.<pin> ...)
  [(class <class_name>)]
)
```

#### 8.2 Net Class

```
(class <name>
  (rule_width <width>)
  (rule_clearance <clearance>)
  [<other_rules>]
)
```

**Example:**
```
(network
  (net "GND"
    (pins U1.1 R1.1 C1.1 C1.2)
    (class "GND")
  )
  (net "VCC"
    (pins U1.8 R2.1 C2.1)
    (class "PWR")
  )
  (net "CLK"
    (pins U1.5 U2.3)
    (class "CLK")
  )

  (class "GND"
    (rule_width 500)        ; 0.5 mm GND traces
    (rule_clearance 250)    ; 0.25 mm clearance
  )
  (class "PWR"
    (rule_width 600)        ; 0.6 mm power traces
    (rule_clearance 250)
  )
  (class "CLK"
    (rule_width 200)        ; 0.2 mm signal traces
    (rule_clearance 250)
  )
)
```

### 9. Wiring Section (Routed Connections)

**In DSN (Unrouted):** Typically empty or contains hints
**In SES (Routed):** Contains actual routed traces and vias

```
(wiring
  [(wire <wire_path>)]
  [(wire_via <via_placement>)]
)
```

#### 9.1 Wire Path

```
(wire
  (path <layer> <width> <x0> <y0> <x1> <y1> ... <xn> <yn>)
)
```

**Example:**
```
(wire
  (path "F.Cu" 250     ; Front copper layer, 250 µm width
    0 0                 ; Start at origin
    10000 0             ; Route 10 mm right
    10000 5000          ; Turn and route 5 mm up
    20000 5000          ; Route 10 mm right
  )
)
```

#### 9.2 Via Placement

```
(wire_via <via_name> <x> <y> <from_layer> <to_layer>)
```

**Example:**
```
(wire_via "Via0.8" 15000 5000 "F.Cu" "B.Cu")
```

---

## Real-World K1 Example

**Minimal K1-like PCB:** ESP32-S3 + LED + Power

```
(pcb "K1_Lightwave_minimal.dsn"
  (parser
    (string_quote ")
    (space_in_quoted_tokens on)
    (host_cad "kicad")
    (host_version "8.0")
  )

  (resolution um 10)
  (unit mm)

  (structure
    (layer_descriptor
      (layer 1 "F.Cu" (type signal))
      (layer 2 "B.Cu" (type signal))
    )
    (boundary
      (path 0
        0 0
        100000 0
        100000 80000
        0 80000
        0 0
      )
    )
    (via "Via0.8"
      (at 0 0 "F.Cu")
      (size 800)
      (drill 400)
    )
    (rule
      (width 200)
      (clearance 250)
      (via_spacing 300)
    )
  )

  (placement
    (component "U1"
      (place 25000 25000 0 front)
    )
    (component "LED1"
      (place 50000 25000 0 front)
    )
    (component "C1"
      (place 75000 25000 90 front)
    )
  )

  (library
    (image "QFN-48"
      (pin 1 (at 0 0) "GND")
      (pin 2 (at 500 0) "GPIO0")
      (pin 3 (at 1000 0) "GPIO1")
      (pin 48 (at 5000 -2000) "VDDA")
    )
    (image "LED-5050"
      (pin 1 (at 0 0) "GND")
      (pin 2 (at 500 0) "VCC")
      (pin 3 (at 1000 0) "DATA")
    )
    (image "CAP-1206"
      (pin 1 (at 0 0) "C_1")
      (pin 2 (at 3000 0) "C_2")
    )
  )

  (network
    (net "GND"
      (pins U1.1 LED1.1 C1.1)
      (class "GND")
    )
    (net "VCC"
      (pins U1.48 LED1.2 C1.2)
      (class "PWR")
    )
    (net "LED_DATA"
      (pins U1.2 LED1.3)
      (class "SIGNAL")
    )
    (class "GND"
      (rule_width 500)
      (rule_clearance 250)
    )
    (class "PWR"
      (rule_width 600)
      (rule_clearance 250)
    )
    (class "SIGNAL"
      (rule_width 200)
      (rule_clearance 250)
    )
  )

  (wiring
  )
)
```

**Notes:**
- `<wiring>` section is empty (unrouted design)
- FreeRouting will fill this with actual traces
- All coordinates in µm (resolution um 10)
- Pin coordinates are relative to component placement

---

## Common Pitfalls

### 1. Incorrect Resolution/Unit Mismatch

**Problem:**
```
(resolution um 10)      ; 1 unit = 10 µm
(unit inch)             ; But units are inches?
```

**Fix:** Ensure consistency:
```
(resolution um 10)      ; 1 unit = 10 µm
(unit um)               ; Units in µm
```

### 2. Missing Pin Connectivity

**Problem:**
```
(net "VCC"
  (pins U1.1 R1.1)      ; Missing C1 connection
)
```

**Fix:** List all pins:
```
(net "VCC"
  (pins U1.1 R1.1 C1.1 C2.1)
)
```

### 3. Boundary Coordinates Don't Loop

**Problem:**
```
(boundary
  (path 0 0 0 100000 0 100000 100000 0 100000)  ; Doesn't close loop
)
```

**Fix:** Ensure path closes:
```
(boundary
  (path 0 0 0 100000 0 100000 100000 0 100000 0 0)  ; Loops back to start
)
```

### 4. Invalid Character in Identifiers

**Problem:**
```
(net "5V Supply"        ; Space without quotes handled?
  (pins U1.1)
)
```

**Fix:** Quote identifiers with special characters:
```
(net "5V_Supply"        ; Use underscore instead
  (pins U1.1)
)
```

### 5. Mismatched Layer Names

**Problem:**
```
(layer 1 "Front.Copper" (type signal))     ; DSN
(wire
  (path "F.Cu" ...)                        ; SES uses different name
)
```

**Fix:** Use consistent layer names:
```
(layer 1 "F.Cu" (type signal))
(wire
  (path "F.Cu" ...)
)
```

---

## KiCad Export Details

### How KiCad Generates DSN

When you export from KiCad PCBnew:

```
File > Export > Specctra DSN
  ↓
KiCad reads: board.kicad_pcb
             board.kicad_sch
KiCad calls: DSN::SPECCTRA_DB::ExportPCB()
KiCad writes: board.dsn
```

**Exact KiCad DSN Export Behavior:**

| KiCad Element | → | DSN Element | Notes |
|---|---|---|---|
| kicad_pcb file | → | (pcb ...) | Root element |
| Layers (PCB) | → | (layer_descriptor ...) | Each layer becomes entry |
| PCB outline | → | (boundary ...) | Board perimeter |
| Vias | → | (via ...) | Via definitions |
| Design rules | → | (rule ...) | Design constraints |
| Footprints | → | (placement ...) | Component X,Y,angle,side |
| Pads/pins | → | (library image pin) | Pin locations relative to ref point |
| Nets | → | (network net) | Connectivity |
| Traces (if any) | → | (wiring wire) | As hints only, not binding |
| Zones | → | (plane) | Power/ground planes |

### Python API for KiCad DSN Export

```python
import sys
sys.path.insert(0, "/Applications/KiCad/KiCad.app/Contents/SharedSupport/scripting")

from pcbnew import DSN

# Create SPECCTRA_DB object
db = DSN.SPECCTRA_DB()

# Load PCB file
db.LoadPCB("board.kicad_pcb")

# Set parser options (optional)
# (Most defaults work fine)

# Export to DSN
db.ExportPCB("board.dsn")

print("DSN exported successfully")
```

### Python API for SES Import

```python
import pcbnew
from pcbnew import DSN

# Load KiCad board
board = pcbnew.LoadBoard("board.kicad_pcb")

# Load routed SES
db = DSN.SPECCTRA_DB()
db.LoadSESSION("board.ses")

# Import session (adds traces/vias to board)
db.ImportSession(board)

# Save updated board
board.Save("board_routed.kicad_pcb")
```

---

## Coordinate System Examples

### Example 1: 100×80 mm Board (um, scale 10)

```
Resolution: um, scale 10
Unit: mm
Board corners:
  (0, 0)       → 0 × 10 µm, 0 × 10 µm → (0 mm, 0 mm)
  (100000, 0)  → 100000 × 10 µm, 0 → (1000 mm, 0 mm) ✗ WRONG
```

**Correct interpretation:**
```
Coordinate 100000 in DSN units
= 100000 × (10 µm) = 1,000,000 µm = 1000 mm ✗ Still too big!

Actually:
Coordinate 10000 in DSN units
= 10000 × (10 µm) = 100,000 µm = 100 mm ✓
```

**Board outline for 100×80 mm:**
```
(boundary
  (path 0
    0 0                ; (0, 0) mm
    10000 0            ; (100, 0) mm
    10000 8000         ; (100, 80) mm
    0 8000             ; (0, 80) mm
    0 0
  )
)
```

### Example 2: Component Placement (Coordinates)

Component U1 at (25 mm, 30 mm):

```
DSN coordinates:
x = 25 mm / (10 µm) = 25,000 µm / (10 µm) = 2500 units

In DSN:
(component "U1"
  (place 2500 3000 0 front)
)
```

---

## Summary Table: DSN Elements

| Element | Purpose | Required | Example |
|---------|---------|----------|---------|
| `(pcb ...)` | Root element | ✓ | `(pcb "board.dsn" ...)` |
| `(parser ...)` | Configuration | ✓ | Parser settings |
| `(resolution ...)` | Coordinate scaling | ✓ | `(resolution um 10)` |
| `(unit ...)` | Dimension unit | ✓ | `(unit mm)` |
| `(structure ...)` | Board definition | ✓ | Layers, boundary, rules |
| `(placement ...)` | Component placement | ✓ | Component X, Y, angle |
| `(library ...)` | Component library | ✓ | Pin definitions |
| `(network ...)` | Electrical connectivity | ✓ | Nets and classes |
| `(wiring ...)` | Routed traces | Optional | Empty in DSN, filled in SES |

---

## Validation Checklist

Before routing, verify DSN:

- [ ] `(parser ...)` present with host_cad, host_version
- [ ] `(resolution ...)` and `(unit ...)` match and make sense
- [ ] `(boundary ...)` forms closed loop (first point = last point)
- [ ] All components in `(placement ...)` have entries in `(library ...)`
- [ ] All net pins reference valid components and pin numbers
- [ ] No duplicate net names
- [ ] Design rules reasonable (width > 0, clearance > 0)
- [ ] Via definitions match layers in layer_descriptor
- [ ] No mismatched layer names between placement and wiring

---

## References

- **Cadence Specctra DSN Reference:** https://cdn.hackaday.io/files/1666717130852064/specctra.pdf
- **KiCad DSN Implementation:** https://docs.kicad.org/doxygen/namespaceDSN.html
- **tscircuit DSN Viewer:** https://dsn.tscircuit.com/
- **KiCad Source:** https://github.com/KiCad/kicad-source-mirror/tree/master/pcbnew/specctra_import_export

---

**Document Version:** 1.0
**Last Updated:** 2025-10-24
**Status:** Reference Guide (Authoritative)
