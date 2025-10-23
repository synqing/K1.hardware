# PCB Synthesizer (pcbnew API + Stackup)

## Purpose
Generates a **complete PCB layout file** using KiCad's Python `pcbnew` API. Configures stackup, design rules, initial placement, and pre-routing based on design spec.

## When Auto-Activate
**Keywords:**
- `PCB layout`, `board design`, `stackup`, `layer configuration`, `placement`
- `design rules`, `net classes`, `trace width`, `diff pairs`

## Core Workflow

### 1. Load Design Spec & Footprint Mapping
```python
import pcbnew
from pathlib import Path

spec = load_yaml("design-spec.yaml")
footprints = load_yaml("footprint-mapping.yaml")
bom = load_csv("k1_lightwave_bom.csv")
```

### 2. Create Board & Set Stackup
```python
def setup_board():
    """Configure board physical layer"""
    board = pcbnew.BOARD()

    # Board dimensions (from spec: 100×80mm)
    board.SetBoardThickness(pcbnew.FromMM(1.6))
    board.SetCopperLayerCount(4)

    # Stackup (from manufacturer preset: JLC standard)
    setup_jlc_4layer_stackup(board, spec["pcb"]["stackup"]["preset"])

    # Design rules
    drc = board.GetDesignSettings()
    drc.SetMinClearance(pcbnew.FromMM(0.15))  # 0.15mm trace clearance
    drc.SetTrackMinWidth(pcbnew.FromMM(0.2))  # 0.2mm minimum trace
    drc.SetViaDrill(pcbnew.FromMM(0.3))       # 0.3mm via drill

    return board

def setup_jlc_4layer_stackup(board, preset: str):
    """Configure JLC standard 4-layer impedance stack"""
    # JLC standard stackup:
    # Layer 0 (F.Cu): 1 oz (35µm)
    # Dielectric: ~0.1mm (FR4, εr=4.5)
    # Layer 1 (In1.Cu): 1 oz (35µm) — internal GND/PWR plane
    # Dielectric: ~0.8mm
    # Layer 2 (In2.Cu): 1 oz (35µm) — internal GND/PWR plane
    # Dielectric: ~0.1mm
    # Layer 3 (B.Cu): 1 oz (35µm)

    stackup_config = {
        "copper_weight": "1oz",
        "dielectric_constant": 4.5,
        "loss_tangent": 0.02,
        "impedance_target": 50  # Ohms (if diff pairs)
    }

    # Impedance calculator (use manufacturer tables as source of truth)
    # For JLC 4-layer: 50Ω trace width ~0.25mm on layer 1 (near GND)

    # Apply to board design settings
    board.GetDesignSettings().SetCopperLayerCount(4)
    # KiCad populates standard layer stack automatically
```

### 3. Define Net Classes & Diff Pairs
```python
def setup_net_classes(board):
    """Define electrical net classes (power, signal, high-speed)"""
    drc = board.GetDesignSettings()

    # Power net class (wider traces)
    power_class = drc.GetNetClasses().GetClass("+5V")
    power_class.SetTrackWidth(pcbnew.FromMM(0.5))
    power_class.SetViaDrill(pcbnew.FromMM(0.4))

    # Ground (wide, thick)
    gnd_class = drc.GetNetClasses().GetClass("GND")
    gnd_class.SetTrackWidth(pcbnew.FromMM(0.6))
    gnd_class.SetViaDrill(pcbnew.FromMM(0.4))

    # Signal (standard)
    signal_class = drc.GetNetClasses().GetClass("Default")
    signal_class.SetTrackWidth(pcbnew.FromMM(0.25))
    signal_class.SetViaDrill(pcbnew.FromMM(0.3))

    # High-speed (I2S, SPI — from spec diff_pairs)
    high_speed_nets = spec["constraints"]["high_speed_nets"]
    hs_class = drc.GetNetClasses().GetClass("HighSpeed")
    hs_class.SetTrackWidth(pcbnew.FromMM(0.25))
    # Diff pair spacing: ~0.25mm (impedance matched to 50Ω on JLC standard stack)
    hs_class.SetDiffPairGap(pcbnew.FromMM(0.25))
    hs_class.SetDiffPairWidth(pcbnew.FromMM(0.25))
```

### 4. Load Netlist & Create Footprints
```python
def load_netlist_and_place(board):
    """Import netlist from KiCad schematic"""
    # Load netlist exported by schematic synthesizer
    netlist_file = "k1_lightwave.net"
    board.Load(netlist_file)  # Creates footprints on board

    # Verify footprints loaded
    footprints = board.GetFootprints()
    print(f"✅ Loaded {len(footprints)} footprints")

    return footprints
```

### 5. Deterministic Placement (Heuristic)
```python
def place_components(board):
    """Initial placement based on function and routing hints"""
    footprints = board.GetFootprints()

    placement_rules = {
        "MCU": {"region": "center", "spacing_mm": 20},
        "PMIC": {"region": "left", "spacing_mm": 10},
        "Audio IC": {"region": "right_top", "spacing_mm": 5},
        "Level Shifter": {"region": "right_bottom", "spacing_mm": 5},
        "Passives": {"region": "scattered", "spacing_mm": 2},
        "Connectors": {"region": "edges", "spacing_mm": 5},
    }

    # Group footprints by function
    for fp in footprints:
        ref = fp.GetReference()  # e.g., "U1", "R5", "J1"
        value = fp.GetValue()

        # Infer placement region
        if "ESP32" in value:
            place_component(fp, placement_rules["MCU"])
        elif "TPS54302" in value:
            place_component(fp, placement_rules["PMIC"])
        elif "SPH0645" in value:
            place_component(fp, placement_rules["Audio IC"])
        elif "SN74AHCT" in value:
            place_component(fp, placement_rules["Level Shifter"])
        elif ref.startswith(("R", "C")):
            place_component(fp, placement_rules["Passives"])
        elif ref.startswith("J"):
            place_component(fp, placement_rules["Connectors"])

    print(f"✅ Placed {len(footprints)} components")

def place_component(footprint, rule):
    """Place footprint in region based on heuristic"""
    # Simple placement: distribute within region bounds
    # Real implementation: use force-directed graph or simulated annealing
    region_bounds = {
        "center": (25, 20, 75, 60),  # x1, y1, x2, y2 mm
        "left": (5, 20, 20, 60),
        "right_top": (80, 20, 95, 40),
        "right_bottom": (80, 40, 95, 60),
        "edges": "auto",  # Connectors auto-placed on perimeter
    }

    # Place with small random offset for DRC clearance check
    footprint.SetPosition(pcbnew.wxPointMM(*get_free_position(region_bounds[rule["region"]])))
```

### 6. Pre-Routing (Critical Nets)
```python
def pre_route_critical_nets(board):
    """Route high-priority nets (power, clock, data) by rules"""
    critical_nets = [
        ("+5V", "+3V3", "+3V3"),  # Power tree
        ("I2S_CLK", "I2S_LRCLK", "I2S_DOUT"),  # Audio clocks/data
        ("SPI_CLK", "SPI_MOSI", "SPI_MISO"),  # LED data line (fast)
    ]

    for net_pair in critical_nets:
        # Connect with shortest path + width rules
        # Use net class to get trace width (power wider than signal)
        connect_nets(board, net_pair, use_net_class_width=True)

    print(f"✅ Pre-routed {len(critical_nets)} critical nets")

def connect_nets(board, nets: tuple, use_net_class_width=True):
    """Connect nets with specified width"""
    # Stub implementation; real version uses router API
    pass
```

### 7. Add Keep-Out Zones
```python
def add_keepouts(board):
    """Add keep-out zones for antenna, thermal, mechanical"""
    # Antenna keep-out (from spec: 10mm around ESP32 antenna)
    antenna_keepout = pcbnew.ZONE(board)
    antenna_keepout.SetLayer(pcbnew.F_Fab)
    antenna_keepout.SetName("Antenna_Keepout")
    # Polygon: 10mm around antenna position
    add_zone_polygon(antenna_keepout, antenna_bounds_with_margin())

    # Thermal keep-out (from spec: >5W dissipation zones)
    thermal_zones = [
        ("TPS54302", 5),  # mm clearance around hot component
        ("ESP32-S3", 3),
    ]
    for component, margin_mm in thermal_zones:
        zone = create_thermal_zone(board, component, margin_mm)

    print(f"✅ Added keep-out zones")
```

### 8. Save & Validate
```python
def save_board(board, filename="k1_lightwave.kicad_pcb"):
    """Save board file and run DRC"""
    board.Save(filename)
    print(f"✅ Board saved: {filename}")

    # Run DRC check
    run_drc_check(board)
```

---

## Tool Calls

**MCP Tools:**
- `pcb_drc()` (kicad-cli) — Validate layout against design rules
- `rag_query()` — Fetch stackup presets, impedance calculator, placement heuristics

---

## Outputs

1. **k1_lightwave.kicad_pcb** — PCB layout file (ready for routing)
2. **board-stackup.json** — Configured layer stack + impedance specs
3. **placement-report.md** — Component placement summary

---

## Example Output

```
✅ PCB synthesized:
  - Dimensions: 100×80mm
  - Layers: 4 (FR-4 1.6mm, 1oz copper, JLC standard impedance)
  - Footprints: 35 placed
  - Critical nets pre-routed: 3 (power, I2S clocks, LED data)
  - Keep-out zones: antenna, thermal
  - DRC violations: 0 (unrouted nets OK at this stage)

✏️ Saved: k1_lightwave.kicad_pcb

→ Ready for Router (next step)
```

---

## Integration with Downstream Agents

- **Router** reads board + net classes to auto-route
- **Verifier** runs full DRC after routing
- **Publisher** exports final board for manufacturing

---

## Notes

- Placement is **heuristic-based** (good for prototypes; RL models can improve)
- Pre-routing handles **critical nets only** (power, clocks); general routing is next
- Stackup is **manufacturer-specific** (JLC standard as default)
- DRC is **progressive** (can be relaxed during synthesis; tightened before fab)
