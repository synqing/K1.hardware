# KiCad Schematic Synthesizer (SKiDL + ERC)

## Purpose
Converts a design spec into a **complete, ERC-checked schematic netlist** using SKiDL (programmatic schematic language). Ensures connectivity is code-driven, version-controlled, and deterministic.

## When Auto-Activate
**Keywords (trigger this skill):**
- `schematic`, `netlist`, `SKiDL`, `generate schematic`, `ERC`
- `circuit synthesis`, `connectivity`, `power tree`, `signal hierarchy`
- `symbol assignment`, `pin assignment`, `hierarchical schematic`

## Core Workflow

### 1. Read Design Spec
Load `hardware/k1-lightwave/design-spec.yaml`:
- Extract component list (MPNs, quantities, purposes)
- Extract electrical constraints (power rails, signal classes, diff pairs)
- Extract pin assignments (connectors, IO mapping)

### 2. Generate SKiDL Schematic
Create `hardware/k1-lightwave/kicad/k1_schematic.py` (or equiv):

```python
# k1_schematic.py — PCB netlist generator
from skidl import *

set_default_tool(KICAD)

# Configuration (from design-spec.yaml)
SPEC = load_yaml("../design-spec.yaml")

# Power tree (first priority: clean power distribution)
def power_tree():
    """Main power supply and regulators"""
    with Group("Power Distribution"):
        # Input connector (5V barrel jack / USB-C)
        J_POWER = Connector(
            name="J_POWER",
            part="USB_C_Receptacle_USB3.1_16P",
            description="5V input, 2A budget"
        )

        # Bulk decoupling (low-ESR ceramic)
        C_BULK1 = C(value="100µF", voltage="10V", description="Bulk cap near inlet")
        C_BULK2 = C(value="100µF", voltage="10V", description="Second bulk cap")
        Net("+5V") += [J_POWER[1], C_BULK1[1], C_BULK2[1]]
        Net("GND") += [J_POWER[5], C_BULK1[2], C_BULK2[2]]

        # 3.3V LDO (for logic and MCUs)
        U_VREG = IC(
            part="TPS54302",  # or AMS1117 (lower cost, higher dropout)
            pin_assignments={
                "IN": "+5V",
                "EN": "+5V",
                "FB": "VREF",
                "OUT": "+3V3",
                "GND": "GND"
            }
        )

        # Feedback divider for LDO
        R_FB_TOP = R(value="100k", tolerance="1%")
        R_FB_BOT = R(value="30k", tolerance="1%")
        Net("VREF") += [R_FB_TOP[1], R_FB_BOT[1], U_VREG.FB]

        # Output filter (low-ESR ceramic + electrolytic)
        C_3V3_BULK = C(value="47µF", voltage="10V")
        C_3V3_CERAMIC = C(value="100nF", voltage="10V")
        Net("+3V3") += [U_VREG.OUT, C_3V3_BULK[1], C_3V3_CERAMIC[1]]

# MCU cores (2× ESP32-S3)
def mcu_section():
    """MCU block: ESP32-S3 ×2 (audio + LED orchestration)"""
    with Group("MCU — Audio Core"):
        U_MCU_AUDIO = IC(
            part="ESP32-S3-WROOM-1",
            description="MCU: I2S audio capture"
        )
        decap_by_pin(U_MCU_AUDIO, "+3V3", "GND", [100, 10, 10], "nF")  # Auto-place caps

        # Crystal (external clock if needed; ESP32-S3 has internal)
        # (optional; skip for now if using internal clock)

        # Strapping pins (pulled to rail or GND for boot mode)
        # GPIO0=high for normal boot, GPIO45=high for SPI mode, etc.

    with Group("MCU — LED Core"):
        U_MCU_LED = IC(
            part="ESP32-S3-WROOM-1",
            description="MCU: WS2812B LED orchestration"
        )
        decap_by_pin(U_MCU_LED, "+3V3", "GND", [100, 10, 10], "nF")

# Audio input stage
def audio_section():
    """Audio capture: digital microphone (I2S) + clock tree"""
    with Group("Audio Input"):
        # Digital MEMS mic (I2S out)
        U_MIC = IC(
            part="SPH0645",
            description="MEMS digital microphone"
        )

        # I2S clock generator (if needed; ESP32-S3 can generate)
        # Or use MCU-generated clock

        # I2S routing to MCU_AUDIO
        # I2S_BCLK, I2S_LRCLK, I2S_DOUT → GPIO pins on MCU_AUDIO

# LED output stage
def led_section():
    """LED output: level shifter + connector"""
    with Group("LED Output"):
        # 3.3V → 5V level shifter (for WS2812B DATA line)
        U_LVSHIFT = IC(
            part="SN74AHCT125",  # 4-ch buffer, 3.3V input → 5V output
            description="Level shifter: 3.3V logic → 5V WS2812B"
        )

        # Decoupling for shifter
        decap_by_pin(U_LVSHIFT, "+5V", "GND", [100], "nF")

        # WS2812B connector (JST-XH 3-pin: GND, 5V, DATA)
        J_LED = Connector(
            name="J_LED",
            part="JST_XH_3pin",
            description="WS2812B output (GND, 5V, DATA)"
        )

        Net("GND") += [J_LED[1], U_LVSHIFT.GND]
        Net("+5V") += [J_LED[2], U_LVSHIFT.VCC]
        Net("LED_DATA_5V") += [J_LED[3], U_LVSHIFT.output]

# Top-level assembly
def generate_schematic():
    """Assemble all sections"""
    reset_connection_stack()

    # Power first (voltage stable before signal)
    power_tree()

    # Then MCUs + clocking
    mcu_section()

    # Then signal paths (audio, LED)
    audio_section()
    led_section()

    # Generate KiCad schematic file
    generate_netlist(file="k1_schematic.net")
    generate_kicad_sch_file(file="k1_lightwave.kicad_sch")

if __name__ == "__main__":
    generate_schematic()
    print("✅ Schematic generated: k1_lightwave.kicad_sch")
```

### 3. Run ERC (Electrical Rules Check)
```bash
kicad-cli sch erc k1_lightwave.kicad_sch --output json > erc-report.json
```

### 4. Parse ERC & Auto-Fix
Read `erc-report.json` and:
- **Power pin errors** → Add missing power connections or ground planes
- **Floating nets** → Connect unconnected signals or mark NC (no-connect)
- **Unassigned footprints** → Warn (footprint step is next)
- **High-voltage/current errors** → Suggest wire gauge or trace width

**Auto-fixes are conservative:** Only fix obvious mistakes; flag ambiguous issues for human review.

### 5. Iterate Until ERC=0
Loop steps 2–4 until no ERC violations:
```
ERC pass 1: 12 violations → Fix 10 auto → Manual review 2
ERC pass 2: 2 violations → Fix 1 → Manual review 1
ERC pass 3: 0 violations ✅
```

### 6. Commit & Document
```bash
git add hardware/k1-lightwave/kicad/k1_schematic.py
git add hardware/k1-lightwave/kicad/k1_lightwave.kicad_sch
git commit -m "Schematic synthesis: dual ESP32-S3, audio I2S, LED level shifter (ERC=0)"
```

---

## Tool Calls

**MCP Tools:**
- `sch_erc()` (kicad-cli) — Run headless ERC
- `rag_query()` — Fetch design patterns (power tree, I2S clock, level shifter best practices)
- `parts_search()` (Nexar) — Validate MPN footprints + alternatives

**Python Libraries:**
- SKiDL (https://skidl.readthedocs.io/)
- json/yaml (parse ERC report + spec)

---

## Outputs

1. **k1_schematic.py** — Versioned, code-driven source of truth for connectivity
2. **k1_lightwave.kicad_sch** — KiCad schematic file (auto-generated, human-readable)
3. **erc-report.json** — Structured ERC violations (empty on success)
4. **schematic-summary.md** — Human-readable audit (power tree, signal paths, pin count)

---

## Example Output

```
✅ Schematic synthesized:
  - Components: 2× ESP32-S3, 1× SPH0645, 1× SN74AHCT125, ~20 passive parts
  - Power tree: 5V → 3.3V LDO (TPS54302) w/ bulk caps + feedthrough
  - Signal paths: I2S (audio), WS2812B (LEDs), USB-C (power + debug)
  - Net count: 47
  - ERC violations: 0 ✅
  - Unassigned footprints: 0 ✅

✏️ Committed: kicad/k1_schematic.py + k1_lightwave.kicad_sch

→ Ready for Footprint Mapping & Part Binding (next step)
```

---

## Design Patterns (Built-In)

- **Power tree**: Input → bulk caps → regulator → bypass caps → load
- **I2S clock tree**: MCU generates BCLK/LRCLK → microphone consumes
- **Level shifter**: Always add 100nF bypass to supply pin
- **Decoupling**: 1× 100µF + 10µF + 10nF per IC power pin (ceramic preferred, low ESR)

---

## Integration with Downstream Agents

- **Part Picker** reads `k1_lightwave.kicad_sch` to extract symbols → maps footprints
- **PCB Synthesizer** reads netlist to generate board connectivity
- **Verifier** uses net list to validate DRC + manufacturability

---

## Notes

- SKiDL scripts are **deterministic**: same inputs → same schematic (ideal for CI/CD)
- ERC checks catch **electrical mistakes early** (wrong voltage, unconnected power)
- Auto-fixes are **conservative**: human always reviews before committing
- Schematic is **the source of truth** (not the KiCad GUI file)
