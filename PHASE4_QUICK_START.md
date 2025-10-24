# Phase 4: Design Validation - Quick Start Guide

**Get started with K1 Lightwave PCB validation in 5 minutes**

---

## Installation

```bash
# Prerequisites: Python 3.12+, KiCad 7.0+
pip install pcbnew  # KiCad Python API

# Optional: Install test dependencies
pip install pytest pytest-cov
```

---

## Quick Validation

### Option 1: K1 Lightwave Script (Recommended)

```bash
# Run K1-specific validation
python validate_k1_lightwave.py

# Output:
# ✅ VALIDATION PASSED - BOARD IS MANUFACTURING READY!
# 📦 Manufacturing files ready in: validation_output/manufacturing/
```

### Option 2: Python API

```python
from design_validation import DesignValidation

# Validate any board
validator = DesignValidation("path/to/board.kicad_pcb")
success = validator.execute()

print(f"Ready: {success}")
```

### Option 3: Command Line

```bash
python design_validation.py \
    hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb \
    --output-dir validation_output
```

---

## What Gets Validated?

1. ✅ **DRC** - Design rules (0 violations required)
2. ✅ **DFM** - Manufacturing constraints (JLCPCB)
3. ✅ **Signal Integrity** - SPI, USB, I2C routing
4. ✅ **Thermal** - Junction temperature <80°C
5. ✅ **Manufacturing Ready** - 14-item checklist
6. ✅ **Files** - Gerber/drill generation

---

## Output Files

```
validation_output/
├── validation_report.txt         # Human-readable report
├── validation_summary.json       # Machine-readable data
└── manufacturing/                # Ready for JLCPCB
    ├── K1_Lightwave-F_Cu.gbr
    ├── K1_Lightwave-In1_Cu.gbr   # GND plane
    ├── K1_Lightwave-In2_Cu.gbr   # Power plane
    ├── K1_Lightwave-B_Cu.gbr
    ├── *.gbr (8 Gerber files)
    └── K1_Lightwave.drl
```

---

## K1 Lightwave Expected Results

```
DRC: 0 violations ✅
DFM: 0 violations ✅
Signal Integrity: PASS ✅
Thermal: T_junction = 40°C (45°C margin) ✅
Manufacturing Ready: YES ✅

Cost: ~$15-20 per board (JLCPCB)
Lead Time: 3-5 business days
```

---

## Custom Thermal Parameters

```python
from design_validation import ThermalValidator, ThermalParameters

# Override K1 defaults
params = ThermalParameters(
    ambient_temp_c=25.0,
    power_mcu_a_w=0.5,      # Your MCU power
    power_mcu_b_w=1.0,
    max_junction_temp_c=125.0
)

validator = ThermalValidator(board_path, params)
result = validator.validate_thermal_design()
print(f"T_junction: {result.details['t_junction_c']}°C")
```

---

## Troubleshooting

### DRC fails to execute
```bash
# Install KiCad 7.0+
brew install kicad  # macOS
# or use KiCad installer

# Verify installation
kicad-cli --version
```

### Board file not found
```python
# Use absolute path
from pathlib import Path
board_path = Path("/full/path/to/board.kicad_pcb").resolve()
```

### Python module errors
```bash
# Install dependencies
pip install pcbnew pytest

# Verify KiCad API
python -c "import pcbnew; print(pcbnew.Version())"
```

---

## Next Steps

1. ✅ Run validation on your board
2. ✅ Review validation_report.txt
3. ✅ Fix any issues if validation fails
4. ✅ Upload manufacturing/ to JLCPCB
5. ✅ Order boards!

---

## Complete Documentation

- **README**: [PHASE4_DESIGN_VALIDATION_README.md](PHASE4_DESIGN_VALIDATION_README.md)
- **Summary**: [PHASE4_IMPLEMENTATION_SUMMARY.md](PHASE4_IMPLEMENTATION_SUMMARY.md)
- **Spec**: [ELITE_PCB_DESIGNER_AGENT_SPEC.md](ELITE_PCB_DESIGNER_AGENT_SPEC.md)

---

## Support

Questions? Issues? Open a GitHub issue or contact the PRISM K1 hardware team.

**🚀 Happy designing!**
