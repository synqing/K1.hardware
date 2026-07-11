# Phase 1 Design Preparation - Quick Usage Guide

## Prerequisites

```bash
# Required software
- Python 3.8+
- KiCad 7.0+ (with kicad-cli)

# Check installations
python3 --version
kicad-cli --version
```

## Quick Start (5 minutes)

### 1. Run Test on K1 Lightwave

```bash
cd /path/to/K1.hardware
python3 test_design_preparation.py
```

**Expected Output:**
- ✅ 42 footprints assigned automatically
- ✅ 5 IC replacements documented
- ✅ 69 nets validated
- ✅ ERC passed
- 📄 Report saved to `design_preparation_report.json`

### 2. View Results

```bash
# View JSON report
cat design_preparation_report.json | python3 -m json.tool

# Or open in text editor
code design_preparation_report.json
```

### 3. Apply Footprints (Manual)

Open KiCad PCB Editor:
```bash
# Using footprint assignments from report
# For each component in report:
# 1. Select component on PCB
# 2. Press 'E' (edit)
# 3. Set footprint from report
# 4. Save
```

---

## Command-Line Usage

### Basic Execution

```bash
python3 design_preparation.py \
  hardware/k1-lightwave/k1_motherboard_revA.net \
  hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb
```

### Full Options

```bash
python3 design_preparation.py \
  hardware/k1-lightwave/k1_motherboard_revA.net \
  hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb \
  --output hardware/k1-lightwave/kicad/K1_Lightwave_updated.kicad_pcb \
  --report phase1_report.json \
  --kicad-cli /opt/homebrew/bin/kicad-cli \
  --verbose
```

**Parameters:**
- `netlist` - Required: Path to .net file
- `board` - Required: Path to .kicad_pcb file
- `--output` - Optional: Output PCB path (default: overwrites input)
- `--report` - Optional: Save JSON report
- `--kicad-cli` - Optional: Path to kicad-cli (default: /opt/homebrew/bin/kicad-cli)
- `--verbose` - Optional: Enable debug logging

---

## Python Module Usage

### Basic Example

```python
from pathlib import Path
from design_preparation import DesignPreparation

# Setup paths
netlist = Path("hardware/k1-lightwave/k1_motherboard_revA.net")
board = Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")

# Create instance
prep = DesignPreparation(netlist, board)

# Run Phase 1
success = prep.execute()

# Check results
print(f"Success: {success}")
print(f"Footprints: {len(prep.results['footprints_assigned'])}")
print(f"ERC: {prep.results['erc_passed']}")
```

### Access Individual Steps

```python
# Run steps individually
prep = DesignPreparation(netlist, board)

# Step 1: Load netlist
prep.load_netlist()

# Step 2: Assign footprints
assignments = prep.assign_footprints()
print(f"Assigned: {assignments}")

# Step 3: Document IC replacements
replacements = prep.replace_ic_placeholders()

# Step 4: Validate nets
valid, message = prep.validate_nets()
print(f"Nets: {message}")

# Step 5: Run ERC
passed, message = prep.run_erc()
print(f"ERC: {message}")
```

### Custom Footprint Rules

```python
from design_preparation import DesignPreparation, FootprintAssignment

# Create custom instance
prep = DesignPreparation(netlist, board)

# Add custom footprint rule
custom_rule = FootprintAssignment(
    pattern=r'^U_CUSTOM\d+$',
    footprint='Package_SO:SOIC-14_3.9x8.7mm_P1.27mm',
    description='Custom ICs',
    value_filter=None
)

# Insert at beginning of rules
prep.FOOTPRINT_RULES.insert(0, custom_rule)

# Run with custom rules
prep.execute()
```

---

## Interpreting Results

### JSON Report Structure

```json
{
  "netlist_loaded": true,           // Netlist import success
  "footprints_assigned": {          // Component -> Footprint map
    "R1": "Resistor_SMD:R_0603_1608Metric",
    "C1": "Capacitor_SMD:C_0603_1608Metric"
  },
  "ic_replacements_needed": {       // IC placeholders to replace
    "U2": {
      "current": "Device:C (placeholder)",
      "target": "Regulator_Switching:TPS62160",
      "footprint": "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
      "description": "Buck converter 5V->3.3V, 1.5A"
    }
  },
  "nets_valid": true,               // Net connectivity check
  "erc_passed": true,               // Electrical rule check
  "errors": [],                     // Critical errors
  "warnings": []                    // Non-critical warnings
}
```

### Exit Codes

- `0` - Success (ERC passed, no errors)
- `1` - Failure (errors encountered)

### Log Levels

**INFO** - Normal progress
```
2025-10-24 04:49:27 - INFO - Loading netlist...
2025-10-24 04:49:27 - INFO - Found 52 components
```

**WARNING** - Non-critical issues
```
2025-10-24 04:49:28 - WARNING - 5 IC placeholders need manual replacement
```

**ERROR** - Critical failures
```
2025-10-24 04:49:28 - ERROR - Netlist import failed: file not found
```

---

## Common Issues & Solutions

### Issue 1: Netlist Import Fails

**Symptom:**
```
ERROR - Netlist import failed:
```

**Solution:**
- This is expected on some KiCad versions
- Module continues with analysis
- Footprint assignments still generated
- Apply manually or use KiCad Python API

### Issue 2: KiCad CLI Not Found

**Symptom:**
```
ERROR - kicad-cli not found
```

**Solution:**
```bash
# Find kicad-cli
which kicad-cli

# If not found, install KiCad or specify path
python3 design_preparation.py \
  ... \
  --kicad-cli /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
```

### Issue 3: ERC Not Running

**Symptom:**
```
WARNING - Schematic file not found for ERC
```

**Solution:**
- ERC requires .kicad_sch file (not just .net)
- Place schematic in same directory as netlist
- Or skip ERC (not critical for Phase 1)

### Issue 4: Missing Footprints

**Symptom:**
```
WARNING - 10 components still need footprints
```

**Solution:**
- Check component references against rules
- Add custom footprint rules
- Some components (ICs) require manual assignment

---

## Next Steps After Phase 1

### 1. Review Footprint Assignments

```bash
# Extract just the assignments
jq '.footprints_assigned' design_preparation_report.json
```

### 2. Apply Footprints to PCB

**Option A: Manual (KiCad GUI)**
- Open PCB in KiCad
- Update each footprint from report
- Save

**Option B: Scripted (KiCad Python API)**
```python
import pcbnew

board = pcbnew.LoadBoard("K1_Lightwave.kicad_pcb")
assignments = {...}  # From report

for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref in assignments:
        fp.SetFPID(pcbnew.FPID(assignments[ref]))

board.Save("K1_Lightwave_updated.kicad_pcb")
```

### 3. Replace IC Placeholders

**In KiCad Schematic Editor:**
1. Open `K1_Lightwave.kicad_sch`
2. For each IC in `ic_replacements_needed`:
   - Delete placeholder component
   - Place target component
   - Reconnect nets
3. Regenerate netlist
4. Re-run Phase 1

### 4. Proceed to Phase 2

Once all footprints assigned:
```bash
# Phase 2: Component Placement (coming soon)
python3 component_placement.py \
  hardware/k1-lightwave/kicad/K1_Lightwave_phase1.kicad_pcb
```

---

## Validation Checklist

Before proceeding to Phase 2:

- [ ] All passive components have footprints (R, C, D, F)
- [ ] All connectors have footprints (J*)
- [ ] IC placeholders documented for replacement
- [ ] Net validation passed (no floating nets)
- [ ] ERC passed (0 errors)
- [ ] Board file opens in KiCad without errors

---

## Advanced Usage

### Batch Processing

```python
# Process multiple designs
designs = [
    ("board1.net", "board1.kicad_pcb"),
    ("board2.net", "board2.kicad_pcb"),
]

results = []
for netlist, board in designs:
    prep = DesignPreparation(netlist, board)
    success = prep.execute()
    results.append((board, success, prep.results))

# Summary
for board, success, res in results:
    print(f"{board}: {'PASS' if success else 'FAIL'} - "
          f"{len(res['footprints_assigned'])} footprints")
```

### CI/CD Integration

```yaml
# .github/workflows/phase1.yml
name: Phase 1 - Design Preparation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install KiCad
        run: |
          sudo add-apt-repository ppa:kicad/kicad-7.0-releases
          sudo apt-get update
          sudo apt-get install kicad

      - name: Run Phase 1
        run: |
          python3 design_preparation.py \
            hardware/k1-lightwave/k1_motherboard_revA.net \
            hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb \
            --report phase1_report.json

      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: phase1-report
          path: phase1_report.json

      - name: Check Success
        run: |
          # Fail if errors > 0
          python3 -c "
          import json
          with open('phase1_report.json') as f:
              report = json.load(f)
          exit(len(report['errors']))
          "
```

---

## Troubleshooting

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

prep = DesignPreparation(netlist, board)
prep.logger.setLevel(logging.DEBUG)
prep.execute()
```

### Verify Netlist Format

```bash
# Check netlist is valid KiCad format
head -20 k1_motherboard_revA.net

# Should start with:
# (export
#   (version "D")
#   (design
```

### Test KiCad CLI

```bash
# Test netlist import directly
kicad-cli pcb import netlist \
  --input-file k1_motherboard_revA.net \
  --pcb K1_Lightwave.kicad_pcb \
  --output test_output.kicad_pcb
```

---

## Performance Tips

1. **Large Designs (>500 components)**
   - Increase timeout: Modify `timeout` parameter in subprocess calls
   - Process in sections: Split netlist by functional blocks

2. **Slow ERC**
   - Skip ERC for iteration: Comment out `run_erc()` call
   - Run ERC separately in KiCad GUI

3. **Memory Usage**
   - For huge designs (>1000 components), process footprints by category
   - Use streaming JSON parser for reports

---

## Getting Help

**Documentation:**
- `ELITE_PCB_DESIGNER_AGENT_SPEC.md` - Full specification
- `PHASE1_IMPLEMENTATION_SUMMARY.md` - Detailed results
- `design_preparation.py` - Inline docstrings

**Logs:**
- Console output shows real-time progress
- JSON report contains complete results
- Add `--verbose` for detailed logging

**Common Questions:**
- Q: Why did netlist import fail?
  - A: Some KiCad CLI versions have limited support. Module continues with analysis.

- Q: How do I apply footprint assignments?
  - A: Either manually in KiCad or using KiCad Python API (pcbnew).

- Q: Can I customize footprint rules?
  - A: Yes! Add rules to `FOOTPRINT_RULES` list in DesignPreparation class.

---

**Last Updated:** 2025-10-24
**Version:** 1.0
**Compatible:** KiCad 7.0+, Python 3.8+
