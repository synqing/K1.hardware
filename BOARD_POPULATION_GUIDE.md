# K1 PCB Board Population Guide

## Current Status

- **Board file**: `hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb` (skeleton, 1.9 KB)
- **Netlist**: `hardware/k1-lightwave/k1_motherboard_revA.net` (65 components with proper footprints)
- **Design contract**: `tools/k1_project_v2.json` (outline, zones, routing rules, planes, etc.)
- **Plugin installed**: `K1_ContractedPlace_PRO.py` (available in KiCad Tools menu)

## Problem Summary

Programmatic board population approaches (command-line scripts) fail because:
- KiCad's binary format has strict requirements not documented in CLI tools
- `kicad-cli` has limited ability to validate or create boards on macOS
- Creating footprints requires library context only available inside KiCad GUI

## Solution: Use K1_ContractedPlace_PRO Plugin

The K1_ContractedPlace_PRO plugin solves all these issues by:
1. Running inside KiCad GUI (has full library access)
2. Reading the design contract from `tools/k1_project_v2.json`
3. Automatically placing components in logical zones
4. Adding design features (outlines, holes, keepouts, planes, testpoints, etc.)

## Workflow

### Step 1: Open the Board in KiCad
```bash
open -a KiCad hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb
```

### Step 2: Import Footprints
**Option A: Using K1_ImportAndPlace Plugin (Fast, Basic)**
- `Tools` → `External Plugins` → `K1: Import Footprints and Place`
- This reads the netlist and creates footprints in a grid layout
- Note: Footprints will be minimal placeholders - refinement happens in Step 3

**Option B: Using Schematic Update (Recommended if schematic exists)**
- `Tools` → `Update PCB from Schematic`
- This syncs all components from the schematic automatically

### Step 3: Apply Design Contract & Placement
**Use K1_ContractedPlace_PRO Plugin (PRO Edition features)**
- `Tools` → `External Plugins` → `K1: Contracted Place PRO`
- This applies the complete design contract:
  - Board outline and mounting holes
  - Placement zones for COM_A and COM_B
  - Edge keepouts
  - Power planes (3V3, LED_5V)
  - GND plane with stitching vias
  - Edge via ring
  - SPI guard corridor (GND stitching between COM_A/COM_B)
  - Netclasses for SPI/USB
  - Auto-decoupler placement
  - Thermal via grids
  - Testpoints

### Step 4: Manual Refinement (if needed)
- Adjust component placement in zones
- Verify no DRC violations (Design Rules Check)
- Route signals or prepare for auto-routing

### Step 5: Export Manufacturing Files
```bash
python3 tools/k1_route_validate_export.py
```

This generates:
- Gerber files (copper, silkscreen, mask, etc.)
- Drill file
- IPC-2581 (standard format for PCB data)
- ODB++ (for advanced manufacturers)
- DRC report

## Files Reference

| File | Purpose |
|------|---------|
| `tools/generate_board_final.py` | Direct S-expression generation (CLI, limited) |
| `tools/populate_board_direct.py` | Direct board population (CLI, limited) |
| `plugins/K1_ImportAndPlace.py` | Import footprints from netlist (GUI plugin) |
| `plugins/K1_ContractedPlace_PRO.py` | Apply design contract + advanced placement (GUI plugin) |
| `tools/k1_route_validate_export.py` | Manufacturing export pipeline (CLI) |
| `tools/k1_project_v2.json` | Design specification / contract |

## Why GUI Plugins Are Required

KiCad's C++ code is wrapped with SWIG, creating pcbnew Python bindings that **only work inside KiCad's execution context**. This means:

- ✓ Works: Running plugin code from KiCad GUI → access to pcbnew, libraries, design rules
- ✗ Fails: Running arbitrary Python scripts with import pcbnew → module not found
- ✗ Fails: Using kicad-cli tools → limited functionality, format validation issues

The K1_ContractedPlace_PRO plugin works because it's executed **by KiCad itself**, not by external scripts.

## Next Steps

1. **Immediate**: Open board in KiCad and run K1_ImportAndPlace to populate footprints
2. **Then**: Run K1_ContractedPlace_PRO to apply the full design contract
3. **After**: Verify placement with DRC, then export manufacturing files

## Troubleshooting

**Plugin doesn't appear in Tools menu:**
- Verify it's in: `~/Library/Preferences/kicad/9.0/scripting/plugins/`
- Restart KiCad
- Check KiCad console for errors: `Window` → `Scripting Console`

**Footprints missing from netlist:**
- Verify netlist file exists: `hardware/k1-lightwave/k1_motherboard_revA.net`
- Regenerate netlist from schematic if needed

**Board won't load:**
- Ensure board file isn't corrupted
- Use skeleton: `cp hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb.backup hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb`
