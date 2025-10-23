# Router Orchestrator (FreeRouting + DSN/SES)

## Purpose
Orchestrates **automated PCB routing** using FreeRouting DSN/SES loop. Handles critical nets, diff pairs, and design rule compliance.

## When Auto-Activate
**Keywords:** `routing`, `autoroute`, `FreeRouting`, `DSN`, `SES`, `trace routing`, `layer assignment`

## Core Workflow

### 1. Export DSN (Design Space)
```python
def export_dsn(board_file: str) -> str:
    """Export board to FreeRouting DSN format"""
    os.system(f"kicad-cli pcb export dsn {board_file} output.dsn")
    return "output.dsn"
```

### 2. Run FreeRouting
```python
def run_freerouting(dsn_file: str) -> str:
    """Execute FreeRouting autorouter headless"""
    # FreeRouting: java -jar freerouting.jar input.dsn
    os.system(f"java -Djava.awt.headless=true -jar freerouting.jar {dsn_file}")
    return f"{dsn_file.split('.')[0]}.ses"
```

### 3. Import SES (Session)
```python
def import_ses(board_file: str, ses_file: str) -> None:
    """Import routed SES back into KiCad"""
    os.system(f"kicad-cli pcb import ses {ses_file} -o {board_file}")
```

### 4. Verify & Iterate
- Run DRC check
- If violations: identify bottleneck nets, adjust rules, re-route
- Loop until clean

## Outputs
- **k1_lightwave_routed.kicad_pcb** — Fully routed board

---

## Integration
- **Verifier** runs DRC on routed board
- **Publisher** generates final Gerbers

## Example Output
```
✅ Routing complete:
  - Traces: 2,847 connections routed
  - Via count: 156
  - DRC violations: 0 ✅
  - Routing time: 2m 34s

→ Ready for Verification (next step)
```
