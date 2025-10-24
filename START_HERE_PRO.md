# K1 Unified Design System — PRO Edition Quick Start

**One command. Everything you need.**

---

## The System

| Component | File | What It Does |
|-----------|------|--------------|
| **Contract (PRO)** | `tools/k1_project_v2.json` | Defines: board dimensions, stackup, zones, decoupler placement, SPI guard, power islands, thermal vias, netclasses, testpoints |
| **PRO Plugin** | `plugins/K1_ContractedPlace_PRO.py` | Runs in KiCad; applies contract (auto-decouplers, via guards, planes, thermal, netclasses, testpoints) |
| **Orchestrator** | `agent/orchestrator/run.py` | Routes, validates DRC/DFM, exports Gerbers/Drill/IPC-2581 |

---

## Four Commands (20 minutes)

### 1. Understand the Contract

```bash
head -100 tools/k1_project_v2.json
```

Defines: 100×70 mm board, 4-layer stackup, USB south, LEDs north, COM-A/COM-B zones, GND via ring, SPI guard, 3V3/LED_5V power islands, thermal vias, testpoints.

### 2. Customize (Optional)

```bash
nano tools/k1_project_v2.json
# Change: outline, io edges, zones, stackup, decoupler distance, guard spacing, planes, thermal
```

### 3. Run PRO Plugin in KiCad (5–10 min)

```bash
kicad hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb
# Menu: Tools → External Plugins → K1: Contracted Place PRO

# Plugin applies entire contract:
# ✓ Outline, holes, keepouts
# ✓ USB south, LEDs north
# ✓ COM-A/COM-B placement
# ✓ Auto-placed decouplers (≤2.5 mm from IC power pins)
# ✓ GND via ring (perimeter fence)
# ✓ SPI return-path guard (two via rows from COM-A to COM-B)
# ✓ GND plane (L2)
# ✓ Power islands (3V3/LED_5V on L3)
# ✓ Thermal vias under LDOs
# ✓ Netclasses (SPI, USB) with nets assigned
# ✓ Testpoints on key nets
# Saves board
```

Board is now **fully prepared** for routing.

### 4. Run Orchestrator (5–10 min routing + validation + export)

```bash
python agent/orchestrator/run.py tools/k1_project_v2.json

# Phases:
# Phase 1: Verify tools & contract
# Phase 4: Route (DSN → FreeRouting → SES)
# Phase 5: Validate (DRC zero violations + DFM checks)
# Phase 6: Export (Gerbers, Drill, IPC-2581, ODB++)

# Output: fabpack_out/
```

Done. Fab pack ready in `fabpack_out/`.

---

## What PRO Adds

| Feature | Benefit |
|---------|---------|
| **Auto-decoupler placement** | Caps within spec (≤2.5 mm) without hunting |
| **GND via ring** | EMI fence around board perimeter |
| **SPI return-path guard** | Two stitched via rows keep return current tight |
| **Power islands** | 3V3/LED_5V zones on power layer |
| **Thermal vias** | Under LDOs for heat spreading |
| **Netclasses** | SPI & USB rules created and nets assigned |
| **Testpoints** | TP footprints on key nets (ready to probe) |

---

## Customization Examples

### Change Decoupler Placement Distance

```json
"decoupling": {
  "max_distance_mm": 1.5    ← Tighter (default 2.5)
}
```

### Adjust SPI Guard Via Spacing

```json
"routing": {
  "spi": {
    "guard": {
      "pitch_mm": 1.0        ← Closer vias (default 2.0)
    }
  }
}
```

### Add More Testpoints

```json
"testpoints": {
  "nets": ["SPI_SCK", "SPI_MOSI", "SPI_MISO", "SPI_CS", "3V3", "LED_5V", "GND"]
}
```

### Disable GND Via Ring

```json
"mechanical": {
  "edge_via_ring": {
    "enabled": false
  }
}
```

Then re-run plugin. Contract is applied again.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Plugin error: "Could not find k1_project_v2.json" | Verify: `ls tools/k1_project_v2.json` |
| Plugin error: "Missing footprint: MountingHole" | Import KiCad "Mechanical" library |
| Plugin says "Edge.Cuts outline missing" | Ensure board file loads in KiCad first |
| Orchestrator DRC violations | Fix in KiCad, re-run orchestrator |
| FreeRouting timeout | Increase `routing.freerouting.timeout_s` in contract |

---

## Workflow Summary

```
Edit Contract v2
    ↓
Run K1_ContractedPlace_PRO in KiCad
    ↓
    Board gets:
      ✓ Outline, holes, connectors
      ✓ Auto-placed decouplers
      ✓ GND via ring (EMI fence)
      ✓ SPI guard (return-path vias)
      ✓ Power planes
      ✓ Thermal vias
      ✓ Netclasses
      ✓ Testpoints
    ↓
Run Orchestrator
    ↓
    Route → DRC → DFM → Export
    ↓
Fab Pack Ready
    ✓ fabpack_out/gerbers/
    ✓ fabpack_out/drill/
    ✓ fabpack_out/k1.ipc2581.xml
```

---

## Files

| File | Purpose |
|------|---------|
| `tools/k1_project_v2.json` | PRO Design Contract (edit this) |
| `plugins/K1_ContractedPlace_PRO.py` | PRO Plugin (run in KiCad) |
| `agent/orchestrator/run.py` | Orchestrator (run from terminal) |
| `K1_UNIFIED_SYSTEM_PRO.md` | Full PRO guide |

---

## FAQ

**Q: Do I have to use the PRO version?**  
A: Recommended. Basic version skips auto-decouplers, via guards, power planes, thermal vias, netclass assignments. PRO is professional-grade.

**Q: Can I mix basic + PRO?**  
A: Yes. Use `k1_project.json` (basic) with PRO plugin, or vice versa. But PRO contract is richer and recommended.

**Q: What if I don't want auto-decouplers?**  
A: Set `"decoupling": {"max_distance_mm": 999}` (effectively disabled). Re-run plugin.

**Q: Can I edit the board after the plugin runs?**  
A: Yes. Plugin sets up the smart defaults; you can adjust placement/routing as needed.

**Q: Will the same contract always produce the same board?**  
A: Yes. Deterministic, reproducible, version-controllable.

---

## Next Steps

1. ✓ `tools/k1_project_v2.json` — Review/customize
2. ✓ **Run PRO Plugin** — `Tools → External Plugins → K1: Contracted Place PRO`
3. ✓ **Run Orchestrator** — `python agent/orchestrator/run.py tools/k1_project_v2.json`
4. ✓ **Upload to JLCPCB** — `fabpack_out/gerbers/ + fabpack_out/drill/`

---

**Status:** ✓ Ready to use  
**Last Updated:** 2025-10-24
