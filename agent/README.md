# K1 Expert PCB Design Agent

**Complete, end-to-end PCB design automation for the K1 Lightwave LED controller.**

## What it does

The K1 Expert Agent orchestrates a **7-phase pipeline** from netlist to fab pack:

1. **Project Intake** — Verify tools (kicad-cli, FreeRouting JAR), board file, output directory
2. **Netlist & Footprint Resolution** — Verify board is populated (handled by K1: Import Netlist + Place plugin)
3. **Board Prep & Placement** — Checkpoint; board should have footprints with assigned nets
4. **Routing** — DSN export → FreeRouting headless → SES import
5. **Validation** — DRC (JSON) + DFM checks (JLC rules, copper-to-edge, thermal, high-speed)
6. **Exports** — Gerbers, Drill, IPC-2581, ODB++, iBOM (as available)
7. **Archive** — Fab pack ZIP with manifest

**Key principle:** Fail hard on any error. Collect all violations in phase 5, report once, then stop.

---

## Quick Start (5 minutes)

### Prerequisites

- **KiCad 9.0+** (with kicad-cli support)
- **FreeRouting JAR** (`tools/freerouting.jar`) — optional; manual routing fallback if missing
- **Python 3.8+**

### Setup

1. **Verify the K1 board is populated:**

   Open the board in KiCad:
   ```bash
   kicad-cli pcb export gerbers hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb -o /tmp/test
   # Should succeed if footprints are present
   ```

2. **Configure the agent** (already done; see `agent/configs/k1_project.json`):

   ```json
   {
     "board_file": "hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb",
     "output_dir": "fabpack_out",
     "freerouting_jar": "tools/freerouting.jar",
     ...
   }
   ```

3. **Run the orchestrator:**

   ```bash
   python agent/orchestrator/run.py agent/configs/k1_project.json
   ```

   Output:
   ```
   ======================================================================
   K1 Expert PCB Design Agent - Orchestrator
   ======================================================================
   
   PHASE 1: Project Intake & Verification
   ...
   PHASE 4: Routing
   ...
   PHASE 5: Validation (DRC + DFM)
   ...
   PHASE 6: Exports (Fab Pack)
   ...
   PHASE 7: Archive & Manifest
   ...
   
   ✓ ALL PHASES COMPLETE - FAB PACK READY
   Outputs: fabpack_out/
   ```

---

## Detailed Workflow

### Phase 1: Project Intake

The orchestrator loads the config file and verifies:

- ✓ `kicad-cli` is available
- ✓ Board file exists and has reasonable size (>10 KB = populated)
- ✓ Output directory can be created
- ✓ FreeRouting JAR is present (optional; fallback to manual routing)

**If it fails here:** Check your KiCad installation (`kicad-cli --version`).

### Phase 2–3: Netlist & Placement

**These phases assume the K1: Import Netlist + Place plugin has already run.**

The plugin is responsible for:

1. Importing the netlist from Eeschema (or SKiDL)
2. Creating missing footprints
3. Assigning pad nets
4. Placing components on the board (rule-based: anchor modules, regulators near ingress, decouplers nearby)

If you haven't run it yet:

- Open KiCad PCB Editor
- Menu: **Tools → Scripting Console**
- Load and run the K1 plugin (from a previous delivery)
- The board will be populated and netted

### Phase 4: Routing

```
DSN export (kicad-cli)
    ↓
FreeRouting (java -jar freerouting.jar)
    ↓
SES import (kicad-cli or GUI fallback)
    ↓
Board updated with routed tracks
```

**If FreeRouting times out (>1800s):**

- Reduce the timeout in config (not recommended for complex boards)
- Or run FreeRouting GUI manually:
  - Open `fabpack_out/board.dsn` in FreeRouting GUI
  - Route the board
  - Export session to `fabpack_out/board.ses`
  - Re-run the orchestrator

**If SES import fails via CLI:**

- The script prints a fallback: do one-click in the GUI (File → Import → Specctra Session)
- Save the board
- Re-run the orchestrator

### Phase 5: Validation

**DRC (Design Rule Check):**

- Runs `kicad-cli pcb drc` and parses JSON output
- Counts violations and unconnected items
- Fails if either > 0

**DFM (Design for Manufacturing):**

- JLC Standard profile (6/6 mil trace/space, 0.3 mm via drill, 0.4 mm copper-to-edge)
- K1-specific: SPI length matching, USB impedance (if enabled)
- Thermal checks: decap placement, via arrays

**Collect all issues:**

If any DRC violations or DFM failures are found, the orchestrator:

1. Writes a detailed report to `fabpack_out/validation_failures.txt`
2. Prints the summary to stdout
3. Exits with code 1

**To fix and retry:**

- Edit the board in KiCad
- Manually adjust traces, vias, or decouplers
- Run DRC in KiCad to verify clean
- Re-run the orchestrator

### Phase 6: Exports

Generates fab-ready files:

- **Gerbers** (F.Cu, B.Cu, F.Mask, B.Mask, F.SilkS, Edge.Cuts, drill)
- **IPC-2581 XML** (industry standard, compatible with most fabs)
- **ODB++** (advanced format for high-mix fabs)

These are written to `fabpack_out/`.

### Phase 7: Archive

Creates a manifest (`manifest.json`) with:

- Timestamp
- Board file path
- DRC/DFM status
- All artifact paths
- Stackup and netclass config

Ready to send to fab or archive.

---

## Architecture

```
agent/
├── __init__.py
├── README.md (this file)
├── drivers/
│   ├── __init__.py
│   ├── kicad_cli.py       # Wrappers for kicad-cli (DRC, exports, DSN/SES)
│   ├── kicad_ipc.py       # (TODO) IPC client for in-editor control
│   └── plugin_bridge.py   # (TODO) Action Plugin executor
├── kicad/
│   ├── __init__.py
│   ├── layers.py          # LSET/LSEQ helpers (FIXES THE SWIG ERROR)
│   ├── eeschema.py        # (TODO) Netlist ops
│   ├── pcb.py             # (TODO) Board ops (footprints, nets, zones)
│   └── rules.py           # (TODO) Netclasses, constraints, DRC rules
├── routing/
│   ├── __init__.py
│   ├── dsn_ses.py         # (TODO) DSN/SES helpers
│   └── freerouting.py     # Headless router calls with retry logic
├── dfm/
│   ├── __init__.py
│   └── checker.py         # DFM rule validator (JLC, K1-specific, thermal)
├── thermal/
│   ├── __init__.py
│   └── model.py           # (TODO) Thermal analysis, via arrays
├── impedance/
│   ├── __init__.py
│   └── stackup.py         # (TODO) Impedance calculations (USB, SPI)
├── orchestrator/
│   ├── __init__.py
│   └── run.py             # 7-phase pipeline orchestrator (ENTRY POINT)
└── configs/
    ├── __init__.py
    └── k1_project.json    # K1 project config (board, stackup, netclasses, DFM)
```

### Key Files

| File | Purpose |
|------|---------|
| `agent/kicad/layers.py` | **FIXES THE LSET ERROR** — Safe LSET/LSEQ creation |
| `agent/drivers/kicad_cli.py` | kicad-cli wrapper (DRC, DSN/SES exports) |
| `agent/routing/freerouting.py` | FreeRouting JAR executor |
| `agent/orchestrator/run.py` | **ENTRY POINT** — Runs the 7-phase pipeline |
| `agent/dfm/checker.py` | DFM validation (JLC rules, thermal, high-speed) |
| `agent/configs/k1_project.json` | Board config, stackup, netclasses, DFM profile |

---

## The LSET Fix (Part A)

The immediate error you hit was:

```
pcbnew.new_LSET(...) — wrong number/type of arguments
```

**Root cause:** SWIG binding for LSET doesn't accept strings or raw ints. Needs PCB_LAYER_ID enums.

**Solution:** Use the helpers in `agent/kicad/layers.py`:

```python
from agent.kicad.layers import lset, lset_from_names, all_cu_layers

# Option 1: Enum constants
cu = lset(pcbnew.F_Cu, pcbnew.B_Cu)

# Option 2: Layer name strings (mapped via board)
cu = lset_from_names(board, "F.Cu", "B.Cu")

# Option 3: All copper layers
cu = all_cu_layers()

# Use it
zone.SetLayerSet(cu)
```

**Never do this:**

```python
pcbnew.LSET("F.Cu", "B.Cu")  # ✗ Strings not accepted
pcbnew.new_LSET(0, 2)        # ✗ Raw ints not accepted
```

---

## Execution Modes

### Local Interactive (Recommended for Development)

1. Run the K1: Import Netlist + Place plugin in KiCad (one-time setup, 5 min)
2. Run the orchestrator:
   ```bash
   python agent/orchestrator/run.py agent/configs/k1_project.json
   ```
3. Watch the 7-phase pipeline
4. If routing fails, do SES import in GUI, re-run

### CI Headless (Future)

- Pre-populate board with plugin (one-time)
- Commit board file to repo
- CI runs: `python agent/orchestrator/run.py config.json`
- Exports fab pack as artifact

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Phase 1 fails: "kicad-cli not available" | KiCad not in PATH | `which kicad-cli` or add to PATH |
| Phase 1 fails: "Board looks unpopulated" | K1 plugin not run yet | Run K1: Import Netlist + Place plugin in KiCad |
| Phase 4 fails: "FreeRouting JAR not found" | JAR missing from tools/ | Download from [freerouting.org](https://freerouting.org) or skip routing |
| Phase 4 hangs: "Timeout after 1800s" | Large board / slow machine | Increase `freerouting_timeout` in config or route manually |
| Phase 4 fails: "SES import via CLI failed" | KiCad build lacks CLI SES support | Follow the printed fallback (GUI one-click) |
| Phase 5 fails: "DRC violations" | Design rule violations | Fix in KiCad, re-run orchestrator |
| Phase 5 fails: "DFM violations" | Manufacturing constraint violations | See `validation_failures.txt` for details; adjust config or board |

---

## Configuration Reference

See `agent/configs/k1_project.json` for full options:

```json
{
  "board_file": "path/to/board.kicad_pcb",
  "output_dir": "fabpack_out",
  "freerouting_jar": "tools/freerouting.jar",
  "freerouting_timeout": 1800,
  "stackup": { ... },
  "dfm_profile": "jlc_standard",
  "netclasses": [ ... ],
  "constraints": {
    "spi": { "enabled": true, ... },
    "usb": { "enabled": false, ... }
  },
  "thermal": { ... }
}
```

---

## Next Steps

- [ ] Run K1: Import Netlist + Place plugin (if not done)
- [ ] Run `python agent/orchestrator/run.py agent/configs/k1_project.json`
- [ ] Check `fabpack_out/` for Gerbers, Drill, IPC-2581
- [ ] Upload to JLCPCB or your fab of choice

---

## Support & Debugging

**Full logs:** Check stdout from orchestrator run. Each phase prints details.

**Artifacts:** All outputs in `fabpack_out/`:
- `drc.json` — DRC report
- `validation_failures.txt` — DFM failures (if any)
- `manifest.json` — Metadata & artifact manifest
- `*.gbr` — Gerber files
- `*.xln` — Drill files
- `*.ipc2581` — IPC-2581 XML
- `*.odb` — ODB++ package

---

## Version

Agent version: **1.0.0**

KiCad version required: **9.0+**

Last updated: **2025-10-24**
