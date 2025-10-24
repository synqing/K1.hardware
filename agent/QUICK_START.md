# K1 Agent Quick Start

**Get from netlist to fab pack in ~15 minutes.**

## Step 1: One-time Setup (5 min)

### Verify KiCad & tools

```bash
kicad-cli --version
# KiCad 9.0... ✓

ls -la tools/freerouting.jar
# tools/freerouting.jar ✓
```

### Run K1: Import Netlist + Place plugin

1. Open KiCad PCB Editor
2. File → Open → `hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb`
3. Tools → Scripting Console
4. Load + run the K1 plugin (provided separately)
5. Watch footprints populate and place
6. File → Save

✓ Board is now populated with routed-ready placement.

## Step 2: Run the Orchestrator (5–10 min, depending on routing time)

```bash
python agent/orchestrator/run.py agent/configs/k1_project.json
```

You'll see:

```
PHASE 1: Project Intake & Verification ✓
PHASE 2: Netlist & Footprint Resolution ✓
PHASE 3: Board Prep & Placement ✓
PHASE 4: Routing (DSN → FreeRouting → SES) ...
  [may take 1–5 min; timeout after 30 min]
PHASE 5: Validation (DRC + DFM) ✓
PHASE 6: Exports (Gerbers, Drill, IPC-2581) ✓
PHASE 7: Archive & Manifest ✓

✓ ALL PHASES COMPLETE - FAB PACK READY
Outputs: fabpack_out/
```

## Step 3: Send to Fab

In `fabpack_out/`:

- **Gerbers** (`*.gbr`) → Upload to JLCPCB or your fab
- **Drill** (`*.xln`) → Auto-detected
- **IPC-2581** (`*.ipc2581`) → Advanced fabs (Flex, Altium, etc.)

Done. 🎉

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Phase 1 fails: "kicad-cli not available" | Add KiCad to PATH: `export PATH="/Applications/KiCad/Contents/MacOS:$PATH"` (macOS example) |
| Phase 1 fails: "Board looks unpopulated" | Run the K1 plugin first (Step 1, item 4) |
| Phase 4 times out | FreeRouting is slow on large boards. Either:<br/>1. Increase timeout in `agent/configs/k1_project.json`<br/>2. Route manually in FreeRouting GUI, then import SES in KiCad |
| Phase 4 fails: "SES import via CLI failed" | One-click fallback:<br/>1. File → Import → Specctra Session<br/>2. Select `fabpack_out/board.ses`<br/>3. File → Save<br/>4. Re-run orchestrator |
| Phase 5 fails: "DRC violations" | Open board in KiCad, fix violations, re-run |

---

## What Gets Created

```
fabpack_out/
├── board.dsn                      # Input to FreeRouting
├── board.ses                      # Output from FreeRouting
├── drc.json                       # DRC report
├── manifest.json                  # Metadata
├── validation_failures.txt        # DFM issues (if any)
├── gerbers/
│   ├── K1_Lightwave-F_Cu.gbr
│   ├── K1_Lightwave-B_Cu.gbr
│   ├── K1_Lightwave-F_Mask.gbr
│   └── ...
├── drill/
│   └── K1_Lightwave.xln
├── k1.ipc2581.xml                # IPC-2581 format
└── k1.odb                        # ODB++ format
```

---

## Command Reference

```bash
# Show full orchestrator logs
python agent/orchestrator/run.py agent/configs/k1_project.json 2>&1 | tee run.log

# Use a different config
python agent/orchestrator/run.py path/to/custom_config.json

# Manual DRC only (no routing)
kicad-cli pcb drc hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb --output /tmp/drc.json --format json

# Manual DSN export (for FreeRouting)
kicad-cli pcb export dsn hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb -o /tmp/board.dsn
```

---

## Key Points

✓ **LSET fix included** — Solves the earlier SWIG binding error  
✓ **Strict gating** — Fails hard on DRC/DFM violations; no junk files  
✓ **Full automation** — DSN export → FreeRouting → SES import → exports  
✓ **Fallbacks** — Manual routing & SES import if CLI not available  

---

## Next

- Send `fabpack_out/` files to fab
- Track board through manufacturing
- Assemble and test K1 Lightwave

Questions? See `agent/README.md` for detailed docs.
