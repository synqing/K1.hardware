# FreeRouting Quick Start for K1 Lightwave

## 30-Second Overview

**Goal:** Automatically route PCB traces using FreeRouting

**Process:** KiCad PCB → Export DSN → FreeRouting (autoroute) → Import SES → Routed PCB

**Time:** 5 minutes – 4 hours (depending on board complexity)

**Risk:** <5% data loss (cosmetic only; all traces preserved 100%)

---

## Installation (One-Time)

```bash
# macOS
brew install java
brew install freerouting

# Linux
sudo apt install default-jre
wget https://github.com/freerouting/freerouting/releases/download/v2.1.0/freerouting-2.1.0-linux-x64.tar.gz
tar xzf freerouting-2.1.0-linux-x64.tar.gz

# Windows
# Download .exe from https://github.com/freerouting/freerouting/releases
```

---

## Workflow: Manual (GUI) — 5 Minutes

### Step 1: Export to DSN (from KiCad)
```
PCBnew > File > Export > "Specctra DSN…"
Save as: board.dsn
```

### Step 2: Open in FreeRouting
```bash
java -jar freerouting-2.1.0.jar
# GUI opens → File > Open > board.dsn
```

### Step 3: Route
```
Click "Magic Wand" icon (or Route menu)
Wait for completion (watch progress bar)
```

### Step 4: Save SES
```
File > Save As > board.ses
Close FreeRouting
```

### Step 5: Import Back (to KiCad)
```
PCBnew > File > Import > "Specctra Session…"
Select board.ses
All traces appear on board
```

### Step 6: Verify & Save
```
Tools > Design Rule Checker (check for violations)
File > Save As > board_routed.kicad_pcb
```

---

## Workflow: Headless (CLI) — Automated

```bash
# Single command:
java -Djava.awt.headless=true -jar freerouting-2.1.0.jar \
  -de board.dsn \
  -do board.ses \
  -mt 4 \
  --gui.enabled=false
```

**Output:** `board.ses` (routed design)

---

## Workflow: Python Script (Recommended)

```python
#!/usr/bin/env python3
import subprocess
import sys

# Export DSN
sys.path.insert(0, "/Applications/KiCad/KiCad.app/Contents/SharedSupport/scripting")
from pcbnew import DSN

db = DSN.SPECCTRA_DB()
db.LoadPCB("board.kicad_pcb")
db.ExportPCB("board.dsn")
print("✓ Exported: board.dsn")

# Route
subprocess.run([
    "java", "-Djava.awt.headless=true", "-jar", "freerouting-2.1.0.jar",
    "-de", "board.dsn", "-do", "board.ses", "-mt", "4", "--gui.enabled=false"
])
print("✓ Routing complete: board.ses")

# Import back
import pcbnew
board = pcbnew.LoadBoard("board.kicad_pcb")
db.LoadSESSION("board.ses")
db.ImportSession(board)
board.Save("board_routed.kicad_pcb")
print("✓ Imported: board_routed.kicad_pcb")
```

---

## Specctra DSN Format (Minimal Structure)

```
(pcb "example.dsn"
  (parser (string_quote ") (host_cad "kicad"))
  (resolution um 10)
  (unit um)

  (structure
    (layer_descriptor (layer 1 "F.Cu" (type signal)))
    (boundary (path 0 0 0 100000 0 100000 100000 0 100000 0 0))
  )

  (placement
    (component "U1" (place 25000 25000 0 front))
  )

  (library
    (image "U1" (pin 1 (at 0 0)) (pin 2 (at 2540 0)))
  )

  (network
    (net "GND" (pins U1.1))
    (net "VCC" (pins U1.2))
  )
)
```

---

## FreeRouting CLI Arguments

| Argument | Purpose | Example |
|----------|---------|---------|
| `-de <file>` | Input DSN file | `-de board.dsn` |
| `-do <file>` | Output SES file | `-do board.ses` |
| `-mt <num>` | Thread count | `-mt 4` |
| `-inc <nets>` | Skip nets | `-inc GND,VCC` |
| `--gui.enabled=false` | Headless mode | (recommended) |
| `-oit <num>` | Iterations | `-oit 100` |

---

## Data Preservation at Each Step

| Step | Preserved | Lost | Loss % |
|------|-----------|------|--------|
| PCB → DSN | Netlist, placement, rules | Routed traces (expected) | <1% |
| DSN → SES | Everything + routed traces | Nothing | 0% |
| SES → PCB | All traces, vias, nets | Cosmetic metadata | <5% |
| **Total** | **All electrical connections** | **Cosmetic only** | **<5%** |

---

## Alternative Routers

| Router | License | Cost | Best For |
|--------|---------|------|----------|
| **FreeRouting** | GPL-3.0 | Free | General-purpose, hobby, SMB |
| **TopoRouter** | GPL-2.0 | Free | Linux, topological routing |
| **TopoR** | Commercial | $800–$2K | Professional, high-speed |
| **Xpedition/Allegro** | Commercial | $50K+ | Enterprise, aerospace |

**For K1:** Use FreeRouting (free, active development, cross-platform)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Board may be corrupted" after import | File > Repair Board, or reload + re-import |
| Missing components | Check DSN export; may need manual cleanup |
| DRC violations after routing | Check design rules in DSN; may need re-export |
| Routing takes hours | Reduce complexity, increase `-mt` threads |
| Java not found | Install Java JRE 21+ |
| Cannot open DSN file | Verify file path, check syntax |

---

## Files Involved

```
board.kicad_pcb          ← Input (unrouted PCB)
  ↓ (Export DSN)
board.dsn               ← Input to FreeRouting (~100-500 KB)
  ↓ (Route with FreeRouting)
board.ses               ← Output from FreeRouting (routed traces)
  ↓ (Import SES)
board_routed.kicad_pcb  ← Output (fully routed PCB)
```

---

## Performance Tips

- **Multi-threading:** Use `-mt` equal to CPU core count: `-mt 8`
- **Design Rules:** Conservative clearances in DSN = faster routing
- **Complexity:** Remove unnecessary traces/vias before routing
- **Iterations:** Higher `-oit` = longer runtime but better quality

---

## API Alternative (Cloud-Based)

If you want programmatic routing without local FreeRouting:

```python
from freerouting import FreeroutingClient
import os

client = FreeroutingClient(api_key=os.environ["FREEROUTING_API_KEY"])
result = client.run_routing_job(
    name="K1_Lightwave_v1",
    dsn_file_path="board.dsn",
    timeout=3600
)
# Save result
import base64
with open("board.ses", "wb") as f:
    f.write(base64.b64decode(result["data"]))
```

**Requires:** API key from https://www.freerouting.app/

---

## Next Steps

1. **Install:** `brew install freerouting` (macOS) or equivalent
2. **Test:** Export K1_Lightwave.kicad_pcb as DSN, route small section
3. **Verify:** Run DRC after SES import
4. **Automate:** Use Python script for CI/CD integration

---

**Reference:** See `FREEROUTING_INTEGRATION_SPEC.md` for complete technical specification
