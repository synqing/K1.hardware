# K1 PCB Pipeline Readiness Checklist

## Status: ✅ READY FOR END-TO-END RUN

All three critical blockers have been resolved. The system is now configured for a clean, uninterrupted end-to-end execution.

---

## Verification Checklist

### 1️⃣ Board Stackup (4-Layer Configuration)

**Status**: ✅ **FIXED**

```
F.Cu (0.035 mm) ← Front copper
  ↓
Dielectric (0.17 mm FR4)
  ↓
In1.Cu (0.035 mm) ← Internal plane 1
  ↓
Dielectric (0.17 mm FR4)
  ↓
In2.Cu (0.035 mm) ← Internal plane 2
  ↓
Dielectric (0.17 mm FR4)
  ↓
B.Cu (0.035 mm) ← Back copper
```

**Total thickness**: 0.6 mm (2 oz copper + standard FR4)

**Location**: `hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb`

**Verification**:
```bash
grep -A 3 "(stackup" hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb | head -5
# Should show In1.Cu and In2.Cu layers
```

### 2️⃣ Board Outline (100×70mm)

**Status**: ✅ **FIXED**

- **Current**: Outline rectangle from (0, 0) to (100, 70)
- **Contract**: `tools/k1_project_v2.json` specifies 100×70mm
- **Match**: ✅ Perfect alignment

**Verification**:
```bash
grep -A 2 "gr_rect" hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb | head -4
# Should show: start (0 0) end (100 70)
```

### 3️⃣ FreeRouting JAR

**Status**: ✅ **CONFIRMED**

- **Location**: `tools/freerouting.jar`
- **Size**: 64 MB
- **Purpose**: Automated PCB routing engine
- **Status**: Ready for orchestrator

**Verification**:
```bash
ls -lh tools/freerouting.jar
# Should show ~64MB file
```

---

## Pre-Pipeline Setup

### Step 1: Open Board in KiCad and Verify Layers

```bash
open -a KiCad hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb
```

In KiCad:
- `Setup` → `Board Setup` → `Layers`
- Verify you see: F.Cu, In1.Cu, In2.Cu, B.Cu
- Verify stackup shows dielectric layers
- **Save** the board (Ctrl+S)

### Step 2: Run K1_ContractedPlace_PRO Plugin

In KiCad (with board open):
- `Tools` → `External Plugins` → `K1: Contracted Place PRO`
- This will:
  - Import 65 components from netlist
  - Apply board outline (100×70mm, 1.5mm corner radius)
  - Add mounting holes at corners (3mm, 3.2mm M3 holes)
  - Place keepouts around mounting holes
  - Add power planes (3V3, LED_5V, GND)
  - Add GND edge via ring
  - Add SPI guard corridor (GND stitching between COM_A/COM_B)
  - Define netclasses for SPI/USB signal integrity
  - Place auto-decouplers near IC power pads
  - Add thermal via grids under hot parts
  - Add testpoints on critical nets
- **Save** when complete

### Step 3: Run the Orchestrator

Once the board is populated and saved:

```bash
python agent/orchestrator/run.py tools/k1_project_v2.json
```

This will execute the 7-phase pipeline:
1. **Phase 1**: Project intake (board validation, design contract loading)
2. **Phase 2**: Schematic → netlist → footprint resolution
3. **Phase 3**: Board prep & placement verification
4. **Phase 4**: Routing (DSN export → FreeRouting → SES import)
5. **Phase 5**: Validation (DRC + DFM checks)
6. **Phase 6**: Manufacturing exports (Gerbers, drill, IPC-2581, ODB++)
7. **Phase 7**: Archive and reporting

**Expected output**: `out_fab/` directory with:
- DRC report (violations, unconnected items)
- Manufacturing files (Gerber layers, drill data)
- IPC-2581 file (standard PCB data format)
- ODB++ files (advanced CAM format)
- Validation report

---

## Key Files Summary

| File | Purpose | Status |
|------|---------|--------|
| `hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb` | Board file (4-layer, 100×70mm) | ✅ Fixed |
| `hardware/k1-lightwave/k1_motherboard_revA.net` | Netlist (65 components) | ✅ Valid |
| `tools/k1_project_v2.json` | Design contract (PRO edition) | ✅ Current |
| `plugins/K1_ContractedPlace_PRO.py` | Board population & contract plugin | ✅ Installed |
| `tools/freerouting.jar` | Automated routing engine | ✅ Ready |
| `agent/orchestrator/run.py` | 7-phase pipeline orchestrator | ✅ Ready |
| `tools/k1_route_validate_export.py` | Mfg export & validation | ✅ Ready |

---

## Execution Command

When ready for end-to-end execution:

```bash
# After populating board in KiCad with K1_ContractedPlace_PRO plugin

python agent/orchestrator/run.py tools/k1_project_v2.json

# Monitor output for:
# - Phase completion status
# - DRC/DFM validation results
# - Manufacturing file generation
# - Final archive creation
```

---

## What Each Phase Does

### Phase 1: Project Intake
- Load design contract from JSON
- Validate board dimensions (100×70mm)
- Check stackup configuration (4-layer)
- Confirm schematic linkage

### Phase 2: Schematic → Netlist → Footprints
- Parse netlist (K1 has 65 components)
- Resolve footprint mappings
- Verify no missing footprints

### Phase 3: Board Prep & Placement
- Confirm outline matches contract
- Verify mounting holes placed
- Check placement zones (COM_A, COM_B)
- Validate keepouts

### Phase 4: Routing
- Export board to DSN format (Design Space file)
- Invoke FreeRouting with design rules
- Import solved SES file (Session file)
- Confirm no routing failures

### Phase 5: Validation
- Run DRC (Design Rule Check) on routed board
- Run DFM (Design for Manufacturability) checks
- Verify clearances, widths, trace lengths
- Generate validation report

### Phase 6: Manufacturing Exports
- Generate Gerber files (one per copper/mask layer)
- Generate drill file (EXCELLON format)
- Generate IPC-2581 (standard OEM format)
- Generate ODB++ (advanced manufacturer format)
- Generate BOM (Bill of Materials)

### Phase 7: Archive
- Bundle all outputs
- Generate execution log
- Create validation summary
- Output to `out_fab/` directory

---

## Troubleshooting

### If Plugin Doesn't Appear in Tools Menu
1. Verify plugin file exists: `~/Library/Preferences/kicad/9.0/scripting/plugins/K1_ContractedPlace_PRO.py`
2. Restart KiCad
3. Check `Window` → `Scripting Console` for errors

### If Board Won't Load
```bash
# Restore skeleton if file corrupts
cp hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb.backup \
   hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb
```

### If Orchestrator Fails
1. Check netlist exists: `hardware/k1-lightwave/k1_motherboard_revA.net`
2. Check FreeRouting JAR: `ls -lh tools/freerouting.jar`
3. Check design contract: `cat tools/k1_project_v2.json | python -m json.tool`

### If Manufacturing Exports are Empty
1. Verify board was routed (no unconnected nets)
2. Check DRC report for violations
3. Run Phase 4 again (FreeRouting routing)

---

## Next Steps

1. ✅ Board stackup: 4-layer (DONE)
2. ✅ Board outline: 100×70mm (DONE)
3. ✅ FreeRouting JAR: Present (DONE)
4. **→ Open board in KiCad** (DO THIS NEXT)
5. **→ Run K1_ContractedPlace_PRO plugin** (DO AFTER STEP 4)
6. **→ Run orchestrator** (FINAL STEP)

The system is now **ready to execute clean**. All blockers removed.
