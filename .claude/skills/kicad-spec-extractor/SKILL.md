# KiCad Design Spec Extractor

## Purpose
Converts high-level design intent into a **single source of truth** design specification (YAML/JSON) that drives all downstream PCB pipeline stages. This skill ensures reproducibility and allows agents to reason about design constraints.

## When Auto-Activate
**Keywords (trigger this skill):**
- `design spec`, `board spec`, `constraints`, `stackup`, `design rules`
- `design intent`, `architecture`, `board goals`, `form factor`
- `layer count`, `impedance`, `manufacturing preset`

## Core Workflow

### 1. Parse User Intent
Extract from user prompt or existing design docs:
- **Board type** (audio-reactove LED driver, mixed-signal, RF, etc.)
- **Size/form factor** constraints
- **Layer count** desired (2/4/6 layers)
- **Major components** (MCUs, power ICs, signal chains)
- **IO pin mapping** (connectors, power, data)
- **Electrical constraints** (diff pairs, impedance, EMI)
- **Manufacturer target** (JLCPCB standard, custom, etc.)

### 2. Build Structured Spec
Create/update `hardware/k1-lightwave/design-spec.yaml`:

```yaml
design:
  name: "K1 Lightwave Controller"
  description: "Dual ESP32-S3 audio-reactive LED driver"
  version: "1.0"

form_factor:
  dimensions_mm: [100, 80, 40]  # L×W×H
  connector_positions: "edges"
  mounting: "DIN rail compatible"

electrical:
  main_voltage: 5.0  # V
  logic_voltage: 3.3  # V
  max_current: 2.0  # A @ 5V
  power_budget: [1.5, 0.5, 1.0]  # MCU, audio, LED W

components:
  primary:
    - part: "ESP32-S3-WROOM-1"
      quantity: 2
      purpose: "MCU for audio + LED orchestration"
      notes: "Separate tasks: audio capture, LED sync"
  secondary:
    - part: "SPH0645"
      quantity: 1
      purpose: "MEMS microphone, I2S digital out"
    - part: "SN74AHCT125"
      quantity: 1
      purpose: "3.3V→5V level shifter for WS2812B"

pcb:
  layer_count: 4
  substrate: "FR-4, 1.6mm"
  copper_weight: "1oz/35µm"
  min_trace_width: 0.15  # mm
  min_clearance: 0.15  # mm
  via_drill: 0.3  # mm

stackup:
  preset: "jlcpcb_4layer_standard"  # References standard impedance tables
  notes: "Use JLC standard impedance for 50Ω critical traces"

constraints:
  diff_pairs: ["LVDS", "USB"]  # If applicable
  high_speed_nets: ["I2S_CLK", "SPI_CLK"]
  power_plane_voltage: [5.0, 3.3]
  keep_out_zones:
    antenna: "10mm around ESP32 antenna"
    thermal: "5W nominal @ 50°C ambient"

manufacturer:
  target: "jlcpcb"
  class: "standard"  # PCB class (e.g., standard, advanced)
  panel_size_limit: "500×300 mm"

design_rules:
  erc_checks: ["all"]  # Run full ERC
  drc_checks: ["clearance", "via_size", "trace_width", "power_integrity"]
  manufacturability_checks: true
```

### 3. Validate Spec
- **Completeness check**: All required fields present?
- **Feasibility check**: Constraints realistic (e.g., 0.05mm trace is not JLC standard)?
- **Consistency check**: Power budget sum ≤ input power?
- **Cross-reference**: Major parts available in Octopart/LCSC?

### 4. Commit to Git
Store spec in repo with human-readable diff:
```bash
git add hardware/k1-lightwave/design-spec.yaml
git commit -m "Update design spec: 4-layer stackup, ESP32-S3×2, I2S + WS2812B"
```

---

## Tool Calls

**MCP Tools:**
- `rag_query()` — Find stackup templates for chosen manufacturer
- `parts_search()` (Nexar) — Validate component availability
- `lcsc_search()` — Cross-check parts at JLC pricing

**Python Helpers:**
- YAML parser (validate structure)
- Constraint solver (e.g., can 0.15mm traces fit in 4-layer stackup?)

---

## Outputs

1. **design-spec.yaml** — Versioned, Git-tracked source of truth
2. **spec-validation-report.md** — Human-readable audit (warnings, feasibility notes)
3. **constraint-summary.json** — Parsed constraints for downstream agents (DRC, router)

---

## Example Usage

**User Input:**
> "I need a 4-layer PCB for K1 Lightwave. Dual ESP32-S3, digital microphone (I2S), WS2812B LEDs via level shifter. Compact form factor (~100×80mm). Target JLCPCB standard class. Low EMI."

**Skill Output:**
```
✅ Spec extracted and validated:
  - Form factor: 100×80×40 mm
  - Layers: 4 (FR-4 1.6mm, 1oz copper)
  - Stackup: JLC standard impedance for 50Ω
  - Components: ESP32-S3×2, SPH0645, SN74AHCT125, etc.
  - Constraints: I2S/SPI high-speed, antenna keepout, 5W thermal budget
  - All parts available at LCSC ✅

✏️ Committed: hardware/k1-lightwave/design-spec.yaml (v1.0)

→ Ready for Schematic Synthesizer (next step)
```

---

## Error Handling

| Issue | Resolution |
|-------|-----------|
| **Conflicting constraints** (e.g., 0.05mm trace in 4-layer) | Flag, suggest layer increase or spacing revision |
| **Component unavailable** | Suggest alternatives from Octopart/LCSC |
| **Power budget exceeded** | Show headroom deficit; recommend larger supply or higher MCU |
| **Form factor unrealistic** | Cross-check dimensions against component footprints |

---

## Integration with Downstream Agents

- **Schematic Synthesizer** reads `design-spec.yaml` to auto-generate SKiDL imports + ERC rules
- **PCB Synthesizer** reads stackup preset + DRC rules from spec
- **Verifier** uses constraint list to check manufacturability
- **Publisher** reads form factor to generate panelization hints

---

## Notes

- Spec is **NOT** the final schematic; it's the **contract** that schematic synthesis must fulfill.
- Stackup presets should be **manufacturer-specific** (link to JLC/PCBWay official tables).
- Constraint solver should be **conservative** (flag borderline feasibility).
- Human review of spec is **always required** before synthesis begins.
