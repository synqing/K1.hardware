# Verification & Manufacturability (DRC + DFM)

## Purpose
Validates **completed PCB design** against electrical (DRC) and manufacturing (DFM) rules. Gate for board release.

## When Auto-Activate
**Keywords:** `DRC`, `design review`, `validation`, `manufacturability`, `DFM`, `compliance check`, `electrical check`

## Core Workflow

### 1. Run Electrical DRC
```bash
kicad-cli pcb drc k1_lightwave_routed.kicad_pcb --output json > drc-report.json
```

Check:
- Trace clearance ✓
- Via size ✓
- Unconnected nets ✓
- Copper-to-edge clearance ✓
- Polygon isolation ✓

### 2. Run Manufacturability Checks (DFM)

**Stackup validation:**
- Layer count matches spec (4-layer) ✓
- Impedance targets met (diff pairs) ✓
- Via aspect ratio acceptable (<6:1) ✓

**Component placement:**
- No components overlapping ✓
- No parts too close to edges (<2mm) ✓
- No hand-soldered BGAs (not allowed on JLCPCB) ✓

**Routing:**
- No acute angles (router generated >45°) ✓
- Minimum trace width met (0.2mm) ✓
- No isolated copper islands (shorts risk) ✓

**Power integrity:**
- Power plane coverage >70% ✓
- Via stitching adequate ✓
- Return path clear ✓

### 3. Assembly Checklist
- [ ] BOM ≥95% available at LCSC
- [ ] All parts JLCPCB assembly-compatible
- [ ] Fiducials placed (1 per side minimum)
- [ ] Test points accessible
- [ ] Connector clearance adequate

### 4. Thermal Analysis
- Peak dissipation <5W ✓
- Component temp < 50°C (at 25°C ambient) ✓
- Heatsink required? No ✓

### 5. Signal Integrity Spot-Check
- High-speed nets (I2S, SPI) traced on internal layers ✓
- Return path adjacent ✓
- No long stubs ✓

### 6. Generate Verification Report
```json
{
  "drc": {"violations": 0, "status": "PASS"},
  "dfm_stackup": {"status": "PASS"},
  "dfm_assembly": {"status": "PASS", "notes": "All parts JLCPCB-ready"},
  "dfm_routing": {"status": "PASS"},
  "thermal": {"peak_watts": 2.3, "status": "PASS"},
  "signal_integrity": {"status": "PASS", "note": "Spot-check OK"},
  "overall": "READY FOR MANUFACTURING ✅"
}
```

### 7. Commit Release
```bash
git tag -a v1.0-pcb -m "PCB design complete: DRC=0, DFM=PASS, ready for fab"
git push origin v1.0-pcb
```

---

## Tool Calls

**MCP Tools:**
- `pcb_drc()` (kicad-cli) — Run full DRC
- `rag_query()` — Fetch DFM rules for JLCPCB (panelization, assembly constraints, etc.)

---

## Outputs

1. **verification-report.json** — Structured pass/fail for all checks
2. **assembly-checklist.md** — Human-readable assembly notes
3. **release-notes.md** — Summary for manufacturing team

---

## Example Output

```
✅ DESIGN VERIFICATION COMPLETE:

  Electrical (DRC):
    ✅ Clearance: 0 violations
    ✅ Via sizing: 0 violations
    ✅ Copper integrity: 0 violations

  Manufacturing (DFM):
    ✅ Stackup: 4-layer JLC standard, impedance OK
    ✅ Assembly: All parts JLCPCB-compatible
    ✅ Routing: >0.2mm clearance, no acute angles
    ✅ Thermal: 2.3W max, passive cooling adequate

  Assembly:
    ✅ BOM: 35/35 parts in stock at LCSC
    ✅ Fiducials: 2 per side
    ✅ Test points: GPIO debug pads accessible

  Signal Integrity:
    ✅ I2S clocks: internal layers, adjacent return
    ✅ SPI data: short traces, minimal stub

  ✅ OVERALL STATUS: READY FOR MANUFACTURING

→ Ready for Publisher (next step)
```

---

## Integration
- **Publisher** uses verification report to gate Gerber generation
- Manufacturing team uses assembly checklist

---

## Notes
- DFM rules are **JLCPCB-specific** (should parameterize by target fab)
- Thermal analysis is **simplified** (real design needs FEA for high power)
- Signal integrity is **spot-check only** (full SI needs 3D EM solver)
