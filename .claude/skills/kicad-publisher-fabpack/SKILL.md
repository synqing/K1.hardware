# Publisher & Fab Pack Generator

## Purpose
Generates **manufacturing-ready deliverables** (Gerbers, drills, IPC-2581, STEP, BOM, panelization) and packages them for JLCPCB submission.

## When Auto-Activate
**Keywords:** `publish`, `export`, `Gerbers`, `fab pack`, `manufacturing`, `release`, `panelization`

## Core Workflow

### 1. Generate Gerbers (Industry Standard)
```bash
kicad-cli pcb export gerbers k1_lightwave_routed.kicad_pcb \
  --output-dir fab/gerbers/ \
  --precision 4 \
  --subtract-soldermask
```

Outputs:
- F.Cu → `k1_lightwave-F_Cu.gbr` (top copper)
- B.Cu → `k1_lightwave-B_Cu.gbr` (bottom copper)
- In1.Cu → `k1_lightwave-In1_Cu.gbr` (internal layer 1)
- In2.Cu → `k1_lightwave-In2_Cu.gbr` (internal layer 2)
- F.Mask → `k1_lightwave-F_Mask.gbr` (top solder mask)
- B.Mask → `k1_lightwave-B_Mask.gbr` (bottom solder mask)
- F.SilkS → `k1_lightwave-F_SilkS.gbr` (top silk screen)
- B.SilkS → `k1_lightwave-B_SilkS.gbr` (bottom silk screen)
- Edge.Cuts → `k1_lightwave-Edge_Cuts.gbr` (board outline)

### 2. Generate Drill Files
```bash
kicad-cli pcb export drills k1_lightwave_routed.kicad_pcb \
  --output-dir fab/gerbers/ \
  --format excellon  # Standard drill format for manufacturers
```

Output: `k1_lightwave-Unplated.drl` (via + hole drills)

### 3. Generate IPC-2581 (Machine-Readable)
```bash
kicad-cli pcb export ipc2581 k1_lightwave_routed.kicad_pcb \
  --output fab/k1_lightwave.ipc2581
```

Why: Eliminates Gerber ambiguity; manufacturer can auto-load specs (impedance, min trace width, etc.)

### 4. Generate 3D STEP Model
```bash
kicad-cli pcb export step k1_lightwave_routed.kicad_pcb \
  --output fab/k1_lightwave.step
```

Why: Enclosure design, 3D printing, mechanical fit verification

### 5. Generate Interactive HTML BOM
```bash
python3 scripts/InteractiveHtmlBom/generate_ibom.py \
  --board k1_lightwave_routed.kicad_pcb \
  --output fab/k1_lightwave_bom.html
```

Why: Assembly techs can click components and see placement

### 6. Panelization (KiKit)
```bash
kikit panelize \
  --layout grid 2 2 \
  --cuts vcuts \
  --mouse true \
  --fiducials 1 1 \
  k1_lightwave_routed.kicad_pcb \
  fab/k1_lightwave_panel.kicad_pcb
```

Generates: Panel with 4 boards (2×2), V-cuts separators, fiducials, mounting holes

Export panel Gerbers:
```bash
kicad-cli pcb export gerbers fab/k1_lightwave_panel.kicad_pcb \
  --output-dir fab/gerbers_panel/
```

### 7. Generate Manufacturing Notes
Create `fab/MANUFACTURING_NOTES.txt`:

```
K1 LIGHTWAVE PCB — Manufacturing Notes

BOARD SPECIFICATIONS:
  Dimensions: 100 × 80 mm (single board)
  Panel: 200 × 160 mm (4 boards in 2×2 grid)
  Layers: 4 (FR-4, 1.6mm, 1oz copper)
  Finish: HASL (lead-free)
  Copper weight: 1oz per layer

STACKUP:
  Layer 1 (F.Cu): 35µm (1oz)
  Dielectric: ~0.1mm (FR4)
  Layer 2 (In1.Cu): 35µm (1oz) — GND plane
  Dielectric: ~0.8mm
  Layer 3 (In2.Cu): 35µm (1oz) — PWR plane
  Dielectric: ~0.1mm
  Layer 4 (B.Cu): 35µm (1oz)

IMPEDANCE:
  50Ω target for high-speed nets (I2S CLK, SPI MOSI/MISO)
  Via aspect ratio: <6:1 (OK for JLCPCB)

ASSEMBLY:
  JLC Assembly: YES (all parts JLCPCB-compatible)
  Fiducials: 2 per side, 3mm diameter
  BOM: See k1_lightwave_bom.csv
  Test points: GPIO debug pads (see silk screen)

SOLDER MASK & SILK:
  Solder mask: Green (standard)
  Silk screen: White
  Min trace width: 0.2mm (adhered to)
  Min text height: 0.8mm

PANELIZATION:
  Method: V-cuts (0.5mm groove depth)
  Mouse-bites: Not used (V-cuts preferred)
  Spacing: 1mm between boards (for V-cut)
  Fiducials: Corner fiducials on panel (1 per side)

SPECIAL NOTES:
  - ESP32-S3 modules are hand-soldered post-assembly (BGA-style, not JLC-compatible for auto-placement)
  - OR: Use pre-soldered ESP32-S3-WROOM modules if full JLC assembly desired
  - Antenna area: Keep-out zone 10mm around ESP32 antenna (not routed)
  - No modifications to this design without re-running ERC/DRC

DELIVERY:
  Gerbers: fab/gerbers/
  Drill: fab/gerbers/k1_lightwave-Unplated.drl
  IPC-2581: fab/k1_lightwave.ipc2581
  3D STEP: fab/k1_lightwave.step
  iBOM: fab/k1_lightwave_bom.html
  Panel Gerbers: fab/gerbers_panel/
```

### 8. Generate Final Delivery Package
```bash
cd fab/
zip -r k1_lightwave_fab_package.zip \
  gerbers/ \
  gerbers_panel/ \
  k1_lightwave.ipc2581 \
  k1_lightwave.step \
  k1_lightwave_bom.csv \
  k1_lightwave_bom.html \
  MANUFACTURING_NOTES.txt

# Size check (should be <100MB)
du -sh k1_lightwave_fab_package.zip

# Upload to JLCPCB.com
echo "✅ Package ready for upload: fab/k1_lightwave_fab_package.zip"
```

### 9. Generate CI/CD Artifact (GitHub Actions)
Commit all outputs:
```bash
git add fab/
git commit -m "PCB manufacturing package v1.0: Gerbers, IPC-2581, STEP, iBOM, panel"
git tag -a v1.0-fab -m "Manufacturing-ready design"
git push origin v1.0-fab
```

### 10. Create Release Notes
```markdown
# K1 Lightwave PCB v1.0 — Manufacturing Release

## What's Included
- **Gerber files** (ready for JLCPCB submission)
- **Drill file** (Excellon format)
- **IPC-2581** (machine-readable alternative)
- **3D STEP model** (for enclosure design)
- **Interactive BOM** (assembly reference)
- **Panelization design** (4 boards in 2×2 grid)
- **Manufacturing notes** (specs, assembly instructions)

## Quick Start (JLCPCB)
1. Go to https://jlcpcb.com
2. Click "Add Gerber File"
3. Upload `fab/gerbers/` (or `k1_lightwave.ipc2581`)
4. Review specs → should auto-detect:
   - 4-layer, 1.6mm FR-4
   - 100×80mm board size
5. Select JLCPCB Assembly (all parts available)
6. Review BOM (use `k1_lightwave_bom.csv`)
7. Place order

## Cost Estimate
- PCB: ~$50 (5-piece 2×2 panel = 20 boards)
- Assembly: ~$1.50/board (SMD parts + labor)
- Total: ~$80-100 per unit in small volumes

## Assembly Notes
- Most components: Automatic (JLCPCB pick & place)
- ESP32-S3 modules: Hand-solder post-assembly (BGA pads)
  - Alternative: Use pre-soldered modules (adds $2-5/unit)
- Inspect fiducials before assembly
- Test points: GPIO pads for post-assembly QA

## Design Files
- Schematic: `kicad/k1_lightwave.kicad_sch`
- Layout: `kicad/k1_lightwave_routed.kicad_pcb`
- Panel: `fab/k1_lightwave_panel.kicad_pcb`
- BOM: `k1_lightwave_bom.csv`

## Next Steps
1. Order PCBs from JLCPCB
2. Assemble firmware (see `firmware/` directory)
3. Test with K1 Lightwave firmware stack
```

---

## Tool Calls

**MCP Tools:**
- `export_gerbers()` (kicad-cli)
- `export_drills()` (kicad-cli)
- `export_step()` (kicad-cli)
- `make_fab_pack()` (fabops) — All-in-one packaging
- `kikit_panelize()` (kikit) — Panelization

---

## Outputs

1. **fab/gerbers/** — Manufacturing Gerber files
2. **fab/k1_lightwave.ipc2581** — Machine-readable design spec
3. **fab/k1_lightwave.step** — 3D model
4. **fab/k1_lightwave_bom.html** — Interactive assembly reference
5. **fab/gerbers_panel/** — Panelized Gerbers
6. **fab/MANUFACTURING_NOTES.txt** — Assembly & specifications
7. **fab/k1_lightwave_fab_package.zip** — Complete delivery package

---

## Example Output

```
✅ Manufacturing package generated:

  Gerbers:
    ✅ F.Cu, B.Cu, In1.Cu, In2.Cu (4 copper layers)
    ✅ F.Mask, B.Mask (solder mask)
    ✅ F.SilkS, B.SilkS (silk screen)
    ✅ Edge.Cuts (board outline)
    ✅ Drill file (Excellon)

  Alternative formats:
    ✅ IPC-2581 (machine-readable)
    ✅ STEP 3D model
    ✅ Interactive HTML BOM

  Panelization:
    ✅ 4 boards (2×2 grid) with V-cuts
    ✅ Fiducials + tooling holes
    ✅ Panel Gerbers exported

  Documentation:
    ✅ Manufacturing notes
    ✅ Assembly checklist
    ✅ Release notes

  Package: fab/k1_lightwave_fab_package.zip (12 MB)

✏️ Committed: v1.0-fab tag

→ Ready for JLCPCB submission or equivalent
```

---

## Integration
- Downstream: Manufacturing team uses outputs for board ordering & assembly

---

## Notes
- Gerbers are **industry standard** (compatible with any PCB fab)
- IPC-2581 is **future-proof** (less ambiguity than Gerbers)
- Panelization uses **V-cuts** (JLCPCB preferred, cheaper than mouse-bites)
- ESP32-S3 modules require **hand-soldering** (BGA not supported by JLC auto-placement)
  - Mitigation: Consider pre-soldered modules or hand-assembly at PCB house
