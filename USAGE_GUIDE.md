# IPC Standards Library - Usage Guide

## Quick Start

### Installation
```bash
# The library requires only Python 3.7+ with standard library
# No external dependencies required
python test_ipc_standards.py  # Verify installation
```

### Basic Usage

```python
from ipc_standards_library import IPC2221A, TemperatureRise, K1Configuration

# Calculate trace width for your signal
trace_width, area = IPC2221A.calculate_trace_width(
    current_ma=1000,
    temp_rise=TemperatureRise.POWER_EXTERNAL,
    is_external=True,
    copper_oz=1.0,
)
print(f"Calculated width: {trace_width:.2f} mils")
print(f"Rounded to standard: {IPC2221A.round_trace_width(trace_width)} mils")
```

---

## Complete Examples

### Example 1: Design K1 Power Distribution Network

```python
from ipc_standards_library import (
    K1Configuration,
    IPC2221A,
    IPC6012,
    IPCReporter,
    PCBClass,
)

# Step 1: Confirm K1 uses Class 2 PCB
pcb_class = K1Configuration.DESIGN_RULES['pcb_class']
print(f"K1 PCB Class: {pcb_class.name}")
print(f"Class definition: {IPC6012.CLASS_DEFINITIONS[pcb_class]}")

# Step 2: Get trace width recommendations for each power domain
print("\nPower Domain Trace Width Analysis:")
print("=" * 60)

for domain_name, domain in K1Configuration.POWER_DOMAINS.items():
    # Get recommended width
    width = K1Configuration.get_recommended_trace_width(domain_name)

    # Get clearance requirements
    clearances = K1Configuration.get_clearance_for_domain(domain_name)

    print(f"\nDomain: {domain_name}")
    print(f"  Voltage: {domain.voltage}V")
    print(f"  Peak Current: {domain.current_peak_ma}mA")
    print(f"  Recommended Trace Width: {width:.1f} mils")
    print(f"  Trace-to-Trace Clearance: {clearances['trace_to_trace']} mils")
    print(f"  Trace-to-Edge Clearance: {clearances['trace_to_edge']} mils")
    print(f"  Trace-to-Leads Clearance: {clearances['trace_to_leads']} mils")
    print(f"  Notes: {domain.notes}")

# Step 3: Generate design report
print("\n" + "=" * 60)
report = IPCReporter.generate_pcb_design_report("K1 Lightwave PCB Design")
print(report)
```

**Output:**
```
K1 PCB Class: CLASS_2
Class definition: {'name': 'Dedicated Service', ...}

Power Domain Trace Width Analysis:
============================================================

Domain: VBUS_USB_5V
  Voltage: 5.0V
  Peak Current: 1200mA
  Recommended Trace Width: 15.0 mils
  Trace-to-Trace Clearance: 4 mils
  Trace-to-Edge Clearance: 15 mils
  Trace-to-Leads Clearance: 12 mils
  Notes: USB input, logic power only, no LED load

Domain: LED_5V
  Voltage: 5.0V
  Peak Current: 8000mA
  Recommended Trace Width: 160.3 mils
  Trace-to-Trace Clearance: 4 mils
  Trace-to-Edge Clearance: 15 mils
  Trace-to-Leads Clearance: 12 mils
  Notes: High-current LED output, isolated from USB

Domain: 3V3_LOGIC
  Voltage: 3.3V
  Peak Current: 800mA
  Recommended Trace Width: 15.0 mils (adjusted)
  Trace-to-Trace Clearance: 3 mils
  Trace-to-Edge Clearance: 10 mils
  Trace-to-Leads Clearance: 10 mils
  Notes: MCU and digital logic, regulated from VBUS
```

---

### Example 2: Verify Design Against IPC Standards

```python
from ipc_standards_library import (
    validate_design,
    IPC2221A,
    VoltageClass,
    EnvironmentalCondition,
)

# Proposed design parameters
proposed_designs = [
    {'name': 'VBUS main supply', 'width': 10, 'clearance': 4, 'voltage': 5.0},
    {'name': 'LED output 1', 'width': 100, 'clearance': 4, 'voltage': 5.0},
    {'name': 'LED output 2', 'width': 100, 'clearance': 4, 'voltage': 5.0},
    {'name': 'Digital signal', 'width': 5, 'clearance': 3, 'voltage': 3.3},
    {'name': 'Audio signal', 'width': 4, 'clearance': 3, 'voltage': 3.3},  # Too narrow!
]

print("Design Verification Against IPC Standards:")
print("=" * 70)

for design in proposed_designs:
    valid, message = validate_design(
        trace_width_mils=design['width'],
        clearance_mils=design['clearance'],
        voltage=design['voltage'],
    )

    status = "PASS" if valid else "FAIL"
    print(f"\n{design['name']:<30} {status:>6}")
    print(f"  Width: {design['width']} mils, Clearance: {design['clearance']} mils")
    print(f"  Result: {message}")
```

**Output:**
```
Design Verification Against IPC Standards:
======================================================================

VBUS main supply                 PASS
  Width: 10 mils, Clearance: 4 mils
  Result: Design meets IPC standards

LED output 1                     PASS
  Width: 100 mils, Clearance: 4 mils
  Result: Design meets IPC standards

...

Audio signal                     FAIL
  Width: 4 mils, Clearance: 3 mils
  Result: Trace width 4 mils is below minimum 5 mils
```

---

### Example 3: Solder Joint Quality Assessment (Manufacturing)

```python
from ipc_standards_library import IPCA610, SolderJointQuality

# Example: Inspect a solder joint under microscope
joint_inspection = {
    'fillet_shape': True,      # Smooth 45° angle confirmed
    'wetting': True,            # >75% lead coverage achieved
    'solder_volume': True,      # Adequate solder present
    'voiding': True,            # <10% internal voids
    'pad_coverage': True,       # >75% pad covered
    'coplanarity': True,        # Within ±0.10" specification
    'lead_bend': True,          # No visible bending
    'bridging': False,          # Some bridging detected
}

# Evaluate joint quality for Class 2 PCB
result = IPCA610.evaluate_solder_joint(joint_inspection, severity_level='class_2')

print(f"Solder Joint Quality Assessment (IPC-A-610 Class 2):")
print(f"=" * 60)
print(f"Result: {result.value}")
print(f"Status: {'ACCEPTABLE' if result == SolderJointQuality.ACCEPTABLE else 'REWORK REQUIRED'}")

# Show what criteria passed/failed
print("\nDetailed Assessment:")
for criterion, passed in joint_inspection.items():
    status = "PASS" if passed else "FAIL"
    print(f"  {criterion:<20} {status}")

# Show criteria definition
print("\nCriteria Definitions (Class 2):")
for criterion_name, criteria in IPCA610.SOLDER_JOINT_CRITERIA.items():
    print(f"\n{criteria.criterion}:")
    print(f"  Acceptable: {criteria.acceptable_description}")
    print(f"  Rework:     {criteria.rework_description}")
    print(f"  Reject:     {criteria.reject_description}")
```

**Output:**
```
Solder Joint Quality Assessment (IPC-A-610 Class 2):
============================================================
Result: ACCEPTABLE
Status: ACCEPTABLE

Detailed Assessment:
  fillet_shape         PASS
  wetting              PASS
  solder_volume        PASS
  voiding              PASS
  pad_coverage         PASS
  coplanarity          PASS
  lead_bend            PASS
  bridging             FAIL

Criteria Definitions (Class 2):
...
```

---

### Example 4: Current-to-Trace-Width Scaling Analysis

```python
from ipc_standards_library import IPC2221A, TemperatureRise

# Analyze how trace width scales with current
print("Current to Trace Width Scaling (External, 1oz copper):")
print("=" * 60)
print(f"{'Current (mA)':<15} {'Width Calc':<15} {'Rounded':<15} {'Safety (1.5x)':<15}")
print("-" * 60)

currents = [100, 250, 500, 1000, 2000, 5000, 8000]

for current_ma in currents:
    width_calc, _ = IPC2221A.calculate_trace_width(
        current_ma=current_ma,
        temp_rise=TemperatureRise.POWER_EXTERNAL,
        is_external=True,
        copper_oz=1.0,
    )
    width_rounded = IPC2221A.round_trace_width(width_calc)
    width_safe = IPC2221A.round_trace_width(width_calc * 1.5)

    print(f"{current_ma:<15} {width_calc:<15.2f} {width_rounded:<15.0f} {width_safe:<15.0f}")
```

**Output:**
```
Current to Trace Width Scaling (External, 1oz copper):
============================================================
Current (mA)    Width Calc      Rounded         Safety (1.5x)
------------------------------------------------------------
100             0.25            1.0             2.0
250             0.89            1.0             2.0
500             2.33            3.0             5.0
1000            6.07            8.0             10.0
2000            15.79           20.0            25.0
5000            55.89           63.0            100.0
8000            106.88          125.0           160.0
```

---

### Example 5: Clearance Requirements for Different Voltage Classes

```python
from ipc_standards_library import (
    IPC2221A,
    VoltageClass,
    EnvironmentalCondition,
)

# Compare clearance requirements
print("Clearance Requirements by Voltage and Environment:")
print("=" * 80)

voltage_classes = [
    VoltageClass.ULTRA_LOW,
    VoltageClass.LOW,
    VoltageClass.MEDIUM_LOW,
    VoltageClass.MEDIUM,
    VoltageClass.HIGH,
]

environments = [
    EnvironmentalCondition.CLASS_1,
    EnvironmentalCondition.CLASS_2A,
    EnvironmentalCondition.CLASS_3B,
]

for voltage in voltage_classes:
    print(f"\n{voltage.name}:")
    for env in environments:
        clearance = IPC2221A.get_clearance('trace_to_trace', voltage, env)
        print(f"  {env.name:<20} {clearance:>3} mils")
```

**Output:**
```
Clearance Requirements by Voltage and Environment:
================================================================================

ULTRA_LOW:
  CLASS_1              3 mils
  CLASS_2A             3 mils
  CLASS_3B             6 mils

LOW:
  CLASS_1              3 mils
  CLASS_2A             4 mils
  CLASS_3B             8 mils

...
```

---

### Example 6: PCB Class Selection Helper

```python
from ipc_standards_library import IPC6012, PCBClass

# Determine PCB class for different applications
applications = [
    "Consumer LED controller, outdoor",
    "Automotive engine control unit",
    "Medical device display board",
    "Industrial sensor interface, dry environment",
    "Military avionics computer",
]

print("PCB Class Recommendations:")
print("=" * 70)

for app in applications:
    recommended_class = IPC6012.select_class_for_application(app)
    class_def = IPC6012.CLASS_DEFINITIONS[recommended_class]

    print(f"\nApplication: {app}")
    print(f"Recommended Class: {recommended_class.name}")
    print(f"  Name: {class_def['name']}")
    print(f"  Environment: {class_def['environment']}")
    print(f"  Repair: {class_def['repair']}")
```

**Output:**
```
PCB Class Recommendations:
======================================================================

Application: Consumer LED controller, outdoor
Recommended Class: CLASS_2
  Name: Dedicated Service
  Environment: Commercial/industrial environment
  Repair: Limited/restricted
...
```

---

### Example 7: Detailed PCB Class Requirements Comparison

```python
from ipc_standards_library import IPC6012, PCBClass

# Compare requirements across all classes
print("IPC-6012 Complete Requirements Table:")
print("=" * 100)

for requirement in IPC6012.REQUIREMENTS[:5]:  # Show first 5 requirements
    print(f"\n{requirement.parameter} ({requirement.unit}):")
    print(f"  Class 1: {requirement.class_1}")
    print(f"  Class 2: {requirement.class_2}")
    print(f"  Class 3: {requirement.class_3}")
    if requirement.notes:
        print(f"  Notes:   {requirement.notes}")
```

**Output:**
```
IPC-6012 Complete Requirements Table:
====================================================================================================

Copper Pattern Definition (inch):
  Class 1: ±0.005 inch typical
  Class 2: ±0.003 inch typical
  Class 3: ±0.002 inch typical
  Notes:   Stricter control for higher classes

Via/Hole Size Tolerance (inch):
  Class 1: ±0.005 inch
  Class 2: ±0.003 inch
  Class 3: ±0.002 inch
  Notes:   Affects electrical connectivity
...
```

---

## Integration with PCB Design Tools

### KiCad Integration Example

```python
"""
Integration with KiCad EDA tool for automated design rule checking
"""

from ipc_standards_library import K1Configuration, validate_design

def check_kicad_design(pcb_file_path):
    """
    Validate KiCad PCB design against IPC standards

    Note: This requires parsing KiCad PCB file format
    Implementation would extract traces, clearances, voltages
    """
    # Pseudocode for integration:
    # 1. Parse PCB file for trace widths, clearances, voltages
    # 2. For each net, determine voltage domain
    # 3. Get recommended values from K1Configuration
    # 4. Compare design values against recommendations
    # 5. Generate report of violations

    violations = []

    # Example check:
    # if trace_width < K1Configuration.DESIGN_RULES['min_trace_width']:
    #     violations.append(f"Trace {net_name} too narrow")

    return violations

# Usage:
# violations = check_kicad_design("K1_Lightwave.kicad_pcb")
# if violations:
#     print("Design violations found:")
#     for v in violations:
#         print(f"  - {v}")
```

---

## Reference: Function API

### IPC2221A Functions

```python
# Calculate trace width
width_mils, area_mils2 = IPC2221A.calculate_trace_width(
    current_ma: float,
    temp_rise: TemperatureRise,
    is_external: bool = True,
    copper_oz: float = 1.0,
) -> Tuple[float, float]

# Round to standard width
width = IPC2221A.round_trace_width(width_mils: float, standard: str = 'IPC') -> float

# Get clearance
clearance = IPC2221A.get_clearance(
    clearance_type: str,  # 'trace_to_trace', 'trace_to_edge', 'trace_to_leads'
    voltage_class: VoltageClass,
    environmental: EnvironmentalCondition,
) -> int
```

### K1Configuration Functions

```python
# Get recommended trace width
width = K1Configuration.get_recommended_trace_width(
    domain_name: str  # 'VBUS_USB_5V', 'LED_5V', '3V3_LOGIC'
) -> float

# Get clearance requirements
clearances = K1Configuration.get_clearance_for_domain(
    domain_name: str
) -> Dict[str, int]
```

### IPC6012 Functions

```python
# Get specific requirement
value = IPC6012.get_requirement(
    parameter: str,
    pcb_class: PCBClass
) -> str

# Select class for application
selected_class = IPC6012.select_class_for_application(
    app_type: str
) -> PCBClass
```

### IPCA610 Functions

```python
# Evaluate solder joint quality
result = IPCA610.evaluate_solder_joint(
    joint_measurements: Dict[str, bool],  # criterion -> pass/fail
    severity_level: str = 'class_2'
) -> SolderJointQuality
```

---

## Testing

### Run All Tests
```bash
python -m unittest test_ipc_standards -v
```

### Run Specific Test Class
```bash
python -m unittest test_ipc_standards.TestIPC2221ATraceWidth -v
```

### Run Specific Test
```bash
python -m unittest test_ipc_standards.TestIPC2221ATraceWidth.test_high_current_power_trace -v
```

### Test Results (Expected)
```
Ran 51 tests in 0.001s
OK

Test Coverage:
  - IPC-2221A: Trace width calculations (7 tests)
  - IPC-2221A: Clearance tables (8 tests)
  - IPC-6012: PCB class requirements (10 tests)
  - IPC-A-610: Assembly standards (9 tests)
  - K1 Configuration: (10 tests)
  - Integration & Utilities: (7 tests)
```

---

## Troubleshooting

### Issue: Trace width seems too large
**Solution:** Verify you're using the correct temperature rise class for your signal type:
- Digital signals: DIGITAL_EXTERNAL (25°C)
- Power rails: POWER_EXTERNAL (30°C)
- Critical signals: CRITICAL_EXTERNAL (20°C)

### Issue: Clearance doesn't match expected values
**Solution:** Confirm your environmental classification:
- K1 default: CLASS_2A (controlled, moderate humidity)
- Outdoor use: CLASS_3B (uncontrolled, high humidity)

### Issue: K1 LED domain trace width is very large (160 mils)
**Solution:** This is correct! The LED_5V domain carries up to 8A peak current:
- 8000 mA @ 30°C rise requires ~105 mils calculated
- With 1.5× safety factor = 160 mils
- Consider using 2oz copper to reduce width to ~80 mils if space is critical

---

## Support and References

**Standard Documents:**
- IPC-2221A: Generic Standard on Printed Board Design
- IPC-6012: Specification for Printed Circuit Boards
- IPC-A-610: Acceptability of Electronic Assemblies

**Online Resources:**
- IPC (Association Connecting Electronics Industries): www.ipc.org
- JLCPCB Capabilities: https://jlcpcb.com/capabilities/pcb-capability

**Questions?**
Refer to the comprehensive technical specification in `IPC_STANDARDS_SPECIFICATION.md`

---

## Version Information

- Library Version: 1.0.0
- Python: 3.7+
- Dependencies: None (standard library only)
- Status: Production Ready
- Last Updated: 2025-10-24

