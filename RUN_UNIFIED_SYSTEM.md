# K1 Unified Design System — Quick Reference

**One page. Everything you need to run the complete system.**

---

## The Contract (Source of Truth)

**File:** `tools/k1_project.json`

Defines everything: board dimensions (100×70 mm), 4-layer stackup, connector placements (USB south, LEDs north), component zones (COM-A, COM-B), DFM profile (JLC standard), design rules, constraints.

**Edit once. Use everywhere.**

```bash
nano tools/k1_project.json
# Change: outline.width/height, io edges, placement_zones, stackup, dfm.profile
```

---

## Step 1: Run the Contract Enforcement Plugin

**Where:** Inside KiCad PCB Editor  
**Time:** ~5 minutes

```bash
# 1. Open KiCad
kicad hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb

# 2. In KiCad menu:
Tools → External Plugins → K1: Contracted Place (Design Contract)

# Plugin does:
#   ✓ Draws board outline (100×70 mm on Edge.Cuts)
#   ✓ Places 4 mounting holes (corners)
#   ✓ Places USB on south edge
#   ✓ Spreads JLED1-4 on north edge
#   ✓ Places COM-A and COM-B in their zones
#   ✓ Creates antenna keepout (copper/mask/paste blocked)
#   ✓ Saves the board

# You'll see: "Contract applied. Outline created: 1, Mounting holes: 4, ..."
```

---

## Step 2: Run the Orchestrator

**Where:** Command line (repo root)  
**Time:** ~5–10 minutes (depending on routing time)

```bash
python agent/orchestrator/run.py tools/k1_project.json
```

**What it does:**

| Phase | What | Time |
|-------|------|------|
| 1 | Verify tools (kicad-cli, FreeRouting JAR), board file | <1s |
| 2–3 | Verify board is populated | <1s |
| 4 | **Route:** DSN → FreeRouting → SES import | 1–10 min |
| 5 | **Validate:** DRC (should be zero violations) + DFM checks | <1s |
| 6 | **Export:** Gerbers, Drill, IPC-2581, ODB++ | <10s |
| 7 | **Archive:** Create manifest.json with metadata | <1s |

**Output:**

```
fabpack_out/
├── board.dsn                (routed DSN)
├── board.ses                (routed session)
├── drc.json                 (DRC report)
├── manifest.json            (metadata)
├── gerbers/                 (F.Cu, B.Cu, masks, silk)
├── drill/                   (Excellon)
├── k1.ipc2581.xml          (industry standard)
└── k1.odb                  (advanced format)
```

---

## Step 3: Troubleshooting

| Problem | Solution |
|---------|----------|
| Plugin error: "Could not locate tools/k1_project.json" | Verify file exists: `ls tools/k1_project.json` |
| Plugin error: "Missing footprint: MountingHole" | Import KiCad standard "Mechanical" library |
| Orchestrator error: "DRC violations: 5" | Fix in KiCad, re-run orchestrator |
| Orchestrator error: "FreeRouting timeout" | Increase `routing.freerouting.timeout_s` in contract |
| SES import fails "CLI not available" | Fallback: File → Import → Specctra Session (GUI), then re-run |

---

## Step 4: Send to Fab

```bash
# JLCPCB or your fab:
# Option A: Upload Gerbers + Drill
#   fabpack_out/gerbers/*.gbr
#   fabpack_out/drill/*.xln

# Option B: Upload IPC-2581 (all-in-one)
#   fabpack_out/k1.ipc2581.xml

# Option C: Upload ODB++ (advanced)
#   fabpack_out/k1.odb

# Attach manifest.json for reference
```

---

## Customization Examples

### Change board size
```json
"mechanical": {
  "outline": {
    "width": 120.0,      ← Change
    "height": 80.0       ← Change
  }
}
```

### Move USB to different edge
```json
"io": {
  "usb": {
    "edge": "south"      ← Change to "north", "east", "west"
  }
}
```

### Use stricter DFM profile (4/4 mil instead of 6/6 mil)
```json
"dfm": {
  "profile": "jlc_advanced"   ← Change from "jlc_standard"
}
```

Then re-run plugin + orchestrator.

---

## Key Files

| File | What |
|------|------|
| `tools/k1_project.json` | **Design Contract** (source of truth) |
| `plugins/K1_ContractedPlace.py` | **Plugin** (run in KiCad) |
| `agent/orchestrator/run.py` | **Orchestrator** (run from terminal) |
| `INTEGRATION_UNIFIED_SYSTEM.md` | Full documentation |

---

## Full Workflow (One Command Each)

```bash
# Step 1: Understand the contract
cat tools/k1_project.json | head -50

# Step 2: Customize contract (if needed)
nano tools/k1_project.json

# Step 3: Run plugin in KiCad
#   Tools → External Plugins → K1: Contracted Place (Design Contract)

# Step 4: Run orchestrator
python agent/orchestrator/run.py tools/k1_project.json

# Step 5: Check outputs
ls -la fabpack_out/

# Step 6: Upload to fab
#   Copy fabpack_out/gerbers/ + fabpack_out/drill/ to JLCPCB
```

---

## FAQ

**Q: Do I have to use the contract?**  
A: Yes. It's the source of truth for both the plugin and orchestrator. Everything else reads from it.

**Q: Can I edit the contract while working?**  
A: Yes. Edit it, re-run the plugin to apply changes, then re-run the orchestrator.

**Q: What if FreeRouting fails?**  
A: Route manually in FreeRouting GUI, export SES, save in `fabpack_out/board.ses`, re-run orchestrator.

**Q: Will the same contract always produce the same board?**  
A: Yes. Deterministic, reproducible, version-controllable.

**Q: Can I add more design rules to the contract?**  
A: Yes. Both plugin and orchestrator read any additional fields.

---

## Support

- **Contract structure:** See `tools/k1_project.json` (fully commented)
- **Plugin details:** See `K1_Agent_Contract_Addon/README.txt`
- **Orchestrator details:** See `agent/README.md`
- **Full integration guide:** See `INTEGRATION_UNIFIED_SYSTEM.md`

---

**Status:** ✓ Ready to use  
**Last updated:** 2025-10-24
