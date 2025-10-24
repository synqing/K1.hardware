# K1 Unified Design System — Contract + Orchestrator Integration

**Date:** 2025-10-24  
**Status:** ✓ COMPLETE INTEGRATION  
**Components:** Design Contract + K1_ContractedPlace Plugin + Orchestrator

---

## What This Is

A **unified, deterministic PCB design system** where:

1. **Design Contract** (`tools/k1_project.json`) — Single source of truth for board dimensions, placement zones, connectors, keepouts, stackup, rules, DFM profile
2. **K1_ContractedPlace Plugin** — Enforces the contract inside KiCad (draws outline, places holes, connectors, zones, keepouts)
3. **Orchestrator** (`agent/orchestrator/run.py`) — Routes the board, validates DRC/DFM, exports fab pack

Edit the contract once; the rest is mechanical, repeatable, deterministic.

---

## The Complete Workflow (15 minutes)

### Step 1: Understand the Design Contract (2 min)

The contract is your board specification. It defines:

```json
{
  "mechanical": {
    "outline": {"width": 100, "height": 70},
    "mounting_holes": [...],
    "keepouts": [...]
  },
  "stackup": {
    "layers": 4,
    "map": ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu"],
    "roles": {"L1": "signals", "L2": "GND plane", ...}
  },
  "io": {
    "usb": {"ref": "JUSB1", "edge": "south"},
    "led_ports": {"refs": ["JLED1",...], "edge": "north"}
  },
  "placement_zones": [
    {"name": "COM_A", "refs": ["U_COMA"], "x": 20, "y": 30, "w": 35, "h": 30}
  ],
  "netclasses": {
    "SPI": {"width_mm": 0.2, "match_mm": 5.0},
    "USB_FS": {"diff_impedance_ohm": 90.0}
  },
  "rules": {
    "design_rules": {"copper_to_edge_mm": 0.4, "trace_min_mm": 0.15},
    "thermal": {"decap_placement_max_mm": 3.0}
  },
  "dfm": {
    "profile": "jlc_standard",
    "jlc_standard": {"trace_width_min_mm": 0.15, ...}
  }
}
```

See `tools/k1_project.json` for the full, pre-filled example.

### Step 2: Edit the Contract (if needed) (2 min)

Customize for your board:

```bash
# Open the contract
nano tools/k1_project.json

# Change these if different from K1:
# - mechanical.outline.width / .height
# - io.usb.edge, io.led_ports.edge, io.led_ports.margin_mm
# - placement_zones (component zone placements)
# - stackup.layers, .thickness_mm (if 2-layer, 4-layer, etc.)
# - dfm.profile ("jlc_standard" or "jlc_advanced")

# Save and exit
```

### Step 3: Run K1_ContractedPlace Plugin in KiCad (5 min)

This enforces the contract:

1. **Open the board** in KiCad PCB Editor:
   ```bash
   kicad hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb
   ```

2. **Menu: Tools → External Plugins → K1: Contracted Place (Design Contract)**

3. **Plugin applies the contract:**
   - Draws outline (100×70 mm rectangle on Edge.Cuts)
   - Places 4 mounting holes (corners)
   - Places USB connector on south edge
   - Spreads JLED1–4 evenly along north edge (flipped to face outward)
   - Places COM-A and COM-B in their zones
   - Creates antenna keepout (copper/mask/paste blocked)
   - Saves the board

4. **You'll see a message:** `Contract applied. Outline created: 1, Mounting holes added: 4, LED ports placed: 4, ...`

5. **Board now has:**
   - Clear outline with dimensions
   - Four corner mounting holes
   - Connectors on edges (ready for routing)
   - Component zones defined
   - Keepouts enforced
   - Ready to route

### Step 4: Run the Orchestrator (5–10 min, depending on routing)

The orchestrator reads the same contract and automates phases 4–7:

```bash
# From repo root
python agent/orchestrator/run.py tools/k1_project.json
```

**Output:**

```
======================================================================
K1 Expert PCB Design Agent - Orchestrator
======================================================================
Design Contract: tools/k1_project.json

PHASE 1: Project Intake & Verification
  ✓ kicad-cli: 9.0
  ✓ Board file: ... (populated)
  ✓ FreeRouting JAR: tools/freerouting.jar
  ✓ Output directory: fabpack_out

PHASE 2: Netlist & Footprint Resolution
  ℹ Board file size: 234.5 KB (populated)

PHASE 3: Board Prep & Placement
  ℹ Placement completed by K1: Contracted Place plugin

PHASE 4: Routing
  [4.1] Exporting DSN...
    ✓ fabpack_out/board.dsn
  [4.2] Running FreeRouting (timeout: 1800s)...
    (... routing in progress ...)
    ✓ fabpack_out/board.ses
  [4.3] Importing SES...
    ✓ SES imported and board updated

PHASE 5: Validation (DRC + DFM)
  [5.1] Running DRC...
    Violations: 0
    Unconnected: 0
  [5.2] Running DFM checks...
    ✓ All DFM checks passed
  ✓ Validation passed (DRC clean, DFM clean)

PHASE 6: Exports (Fab Pack)
  [6.1] Exporting Gerbers + Drill...
    ✓ Gerbers: fabpack_out/gerbers
    ✓ Drill: fabpack_out/drill
    ✓ IPC-2581: fabpack_out/k1.ipc2581.xml
    ✓ ODB++: fabpack_out/k1.odb

PHASE 7: Archive & Manifest
  [7.1] Creating manifest...
    ✓ fabpack_out/manifest.json
  [7.2] Fab pack directory: fabpack_out

======================================================================
✓ ALL PHASES COMPLETE - FAB PACK READY
Outputs: fabpack_out/
======================================================================
```

### Step 5: Check the Fab Pack

```bash
ls -la fabpack_out/
```

You'll see:

```
board.dsn                    # Routed DSN (output from FreeRouting)
board.ses                    # Routed session (from FreeRouting)
drc.json                     # DRC report (zero violations expected)
manifest.json                # Metadata + artifact hashes
validation_failures.txt      # (empty if DFM passed)
gerbers/                     # Gerber files (F.Cu, B.Cu, masks, silk, edge)
  K1_Lightwave-F_Cu.gbr
  K1_Lightwave-B_Cu.gbr
  K1_Lightwave-F_Mask.gbr
  K1_Lightwave-B_Mask.gbr
  K1_Lightwave-F_SilkS.gbr
  K1_Lightwave-Edge_Cuts.gbr
drill/
  K1_Lightwave.xln           # Excellon drill file
k1.ipc2581.xml              # IPC-2581 (industry standard)
k1.odb                      # ODB++ (advanced)
```

### Step 6: Upload to Fab

```bash
# JLCPCB or your fab of choice:
# - Upload gerbers/ + drill/ files
# - Or upload k1.ipc2581.xml + k1.odb (both are complete)
# - Attach manifest.json for reference (hashes, board dimensions, stackup)
```

Done. 🎉

---

## File Structure (After Integration)

```
K1.hardware/
├── tools/
│   └── k1_project.json                    ← UNIFIED CONTRACT (source of truth)
├── plugins/
│   ├── K1_ImportAndPlace.py               (basic netlist import)
│   └── K1_ContractedPlace.py              ← CONTRACT ENFORCEMENT PLUGIN
├── agent/
│   ├── orchestrator/
│   │   └── run.py                         ← ORCHESTRATOR (reads contract, runs phases 1-7)
│   ├── dfm/
│   │   └── checker.py                     (uses contract rules)
│   ├── drivers/
│   │   └── kicad_cli.py                   (kicad-cli wrappers)
│   └── routing/
│       └── freerouting.py                 (FreeRouting executor)
├── fabpack_out/                           ← OUTPUTS (created by orchestrator)
│   ├── board.dsn
│   ├── board.ses
│   ├── drc.json
│   ├── manifest.json
│   ├── gerbers/
│   ├── drill/
│   ├── k1.ipc2581.xml
│   └── k1.odb
└── INTEGRATION_UNIFIED_SYSTEM.md           ← THIS FILE
```

---

## Key Principles

### 1. Single Source of Truth

Everything flows from `tools/k1_project.json`:

- **Plugin reads it** → draws outline, places holes/connectors, enforces zones
- **Orchestrator reads it** → uses stackup, netclasses, DFM profile for validation
- **DFM checker reads it** → validates against contract-defined rules

Edit once; use everywhere.

### 2. Deterministic & Reproducible

Same contract → same board layout → same design every time. No guessing.

Version-control the contract; board is reproducible from git.

### 3. Strict Gating

- Plugin **fails hard** if contract is invalid (missing dimensions, bad footprints, etc.)
- Orchestrator **fails hard** if DRC violations or DFM failures occur
- No silent failures; no junk artifacts

### 4. Fallbacks

- **Plugin can't find a footprint** → Error message tells you which library to import
- **FreeRouting times out** → Orchestrator tells you to route manually, import SES, re-run
- **SES import via CLI unsupported** → Fallback to GUI one-click

---

## Common Edits to the Contract

### Change Board Dimensions

```json
"mechanical": {
  "outline": {
    "width": 120.0,      ← Change here
    "height": 80.0,      ← And here
    "corner_radius": 1.5
  }
}
```

**Then re-run the plugin.** New outline is drawn.

### Change Connector Placement

```json
"io": {
  "usb": {
    "ref": "JUSB1",
    "edge": "south",      ← Change to "north", "east", "west"
    "offset_mm": 10.0     ← Offset from edge
  },
  "led_ports": {
    "edge": "north",      ← Change to another edge
    "margin_mm": 8.0      ← Space from corners
  }
}
```

**Then re-run the plugin.** Connectors are re-placed.

### Change Component Zones

```json
"placement_zones": [
  {
    "name": "COM_A",
    "refs": ["U_COMA"],
    "x": 30.0,            ← Change position
    "y": 35.0,
    "w": 40.0,            ← Change zone size
    "h": 30.0,
    "rotation": 0         ← Rotate if needed
  }
]
```

**Then re-run the plugin.** Components are moved to new zone centers.

### Change Stackup

```json
"stackup": {
  "layers": 2,           ← Change to 2, 4, 6, 8, etc.
  "thickness_mm": 0.8,   ← Change PCB thickness
  "copper_oz": 2.0,      ← 1 oz, 2 oz, etc.
  "map": ["F.Cu", "B.Cu"],   ← Adjust layer names
  "roles": {
    "L1": "signals",
    "L2": "GND plane"
  }
}
```

**Then re-run orchestrator.** Stackup is used in impedance checks and DFM validation.

### Change DFM Profile

```json
"dfm": {
  "profile": "jlc_advanced"  ← Change from "jlc_standard" to "jlc_advanced"
}
```

**Then re-run orchestrator.** Stricter rules (4/4 mil trace/space) are enforced.

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Plugin says "Could not locate tools/k1_project.json" | Contract not in right place | Verify: `ls tools/k1_project.json` |
| Plugin says "Missing footprint: MountingHole" | KiCad doesn't have mounting hole library | Import footprint lib from KiCad standard (Mechanical) |
| Plugin says "Unknown layer: In1.Cu" | Contract specifies layers board doesn't have | Edit contract stackup.map to match board |
| Orchestrator says "Config missing required contract fields" | Old config format | Use unified `tools/k1_project.json` |
| Orchestrator says "DRC violations: 5" | Design has spacing issues | Fix in KiCad, re-run orchestrator |
| Orchestrator says "DFM violations" | Trace widths, via specs wrong | Check contract netclasses and dfm.profile |
| FreeRouting times out (>30 min) | Large board or slow machine | Increase `routing.freerouting.timeout_s` in contract |

---

## Advanced: Extending the Contract

The contract is designed to be extended. Add new sections for:

- **Panel array**: `"panelization": {"fiducials": [...], "tabs": [...]}`
- **Assembly constraints**: `"assembly": {"testpoints": [...], "restricted_areas": [...]}`
- **Custom keepouts**: Add more to `"mechanical.keepouts"`
- **Additional netclasses**: Add to `"netclasses"` (e.g., `"GND_PLANE"`, `"HIGH_CURRENT"`)

Both plugin and orchestrator will read and validate any additional fields.

---

## Summary: The Three-Component System

| Component | What It Does | Uses Contract For |
|-----------|--------------|-------------------|
| **Contract** (`tools/k1_project.json`) | Single source of truth | Everything |
| **Plugin** (K1_ContractedPlace.py) | Draws outline, places components, enforces zones, creates keepouts | mechanical, io, placement_zones |
| **Orchestrator** (agent/orchestrator/run.py) | Routes, validates DRC/DFM, exports | stackup, netclasses, rules, dfm, constraints |

**Workflow:**

```
Edit Contract
    ↓
Run Plugin (inside KiCad)
    Board gets: outline, holes, connectors, zones, keepouts
    ↓
Run Orchestrator
    Route (FreeRouting) → DRC check → DFM validation → Export Gerbers
    ↓
Fab pack ready
```

---

## Next Steps

1. ✓ Understand the contract structure → see `tools/k1_project.json`
2. ✓ Run the plugin → Tools → External Plugins → K1: Contracted Place
3. ✓ Run the orchestrator → `python agent/orchestrator/run.py tools/k1_project.json`
4. ✓ Upload fab pack → `fabpack_out/` files to JLCPCB

Questions? See `agent/README.md` for orchestrator details, or `K1_Agent_Contract_Addon/README.txt` for plugin details.

---

**System Status:** ✓ Complete & Integrated  
**Last Updated:** 2025-10-24
