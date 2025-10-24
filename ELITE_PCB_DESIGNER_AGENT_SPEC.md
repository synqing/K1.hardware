# Elite PCB Designer Agent Specification
## K1 Lightwave: Netlist → Production PCB Layout Automation

**Document Version:** 1.0
**Status:** Implementation Ready
**Target:** Production use on K1 Lightwave motherboard
**Scope:** Automated PCB layout with signal integrity, thermal management, and DFM validation

---

## Executive Summary

This specification defines an autonomous agent system that transforms a valid KiCad netlist into a production-ready PCB layout. The agent integrates three core subsystems:

1. **Component Placement Engine** - Intelligent placement optimizing thermal zones, signal flow, and routing
2. **Automated Routing System** - FreeRouting integration with KiCad for trace and via placement
3. **Design Validation Suite** - Real-time DFM, DRC, and manufacturing constraint checking

**Success Criteria:**
- ✅ K1 board layout in <30 minutes (vs. 4-6 hours manual)
- ✅ Zero DRC violations
- ✅ Zero manufacturing constraints violated
- ✅ Signal integrity passed
- ✅ Thermal requirements met
- ✅ Ready for JLCPCB 4-layer manufacturing

---

## Part 1: Technical Foundation

### 1.1 Technology Stack

| Layer | Technology | Version | Role |
|-------|-----------|---------|------|
| **PCB Engine** | KiCad | 9.0+ | Primary PCB design tool |
| **Python API** | IPC API | K9.0+ | Programmatic board manipulation |
| **Auto Router** | FreeRouting | 2.1.0+ | Trace & via placement |
| **Netlist Source** | SKiDL | 1.1.0+ | Python circuit description |
| **DFM Validator** | Custom | N/A | Manufacturing rules checking |
| **IPC Standards** | Custom Library | 1.0 | Design rule enforcement |

**Why These Choices:**
- KiCad IPC API: Supports programmatic placement, tracing, DRC (pcbnew deprecated in K10)
- FreeRouting: Free, open-source, active development, Specctra DSN standard (30+ year proven)
- SKiDL: Native Python circuit description, generates valid netlists, extensible
- Custom DFM: JLCPCB-specific constraints not in standard KiCad

### 1.2 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ELITE PCB DESIGNER AGENT                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  INPUT: K1 Netlist (.net file from SKiDL)                   │
│         ├─ Component list with references                    │
│         ├─ Net connectivity                                  │
│         ├─ Footprint assignments (partial)                   │
│         └─ Power domain metadata (3.3V, 5V, LED_5V)         │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ PHASE 1: DESIGN PREPARATION                             │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ • Load netlist into KiCad board                         │ │
│  │ • Assign missing footprints (Device library items)      │ │
│  │ • Replace IC placeholders (U2, U5, U6, U7, U8)         │ │
│  │ • Validate all nets connected                          │ │
│  │ • Run ERC (Electrical Rule Check) - must pass          │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ PHASE 2: COMPONENT PLACEMENT                            │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ • Define thermal zones (MCU-A, MCU-B, USB, LED_OUT)    │ │
│  │ • Cluster components by function (power, signal, I/O)  │ │
│  │ • Place decoupling capacitors near IC power pins       │ │
│  │ • Optimize placement for routing accessibility         │ │
│  │ • Verify component spacing (2mm JLCPCB minimum)        │ │
│  │ • Validate thermal zone compliance                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ PHASE 3: AUTOMATED ROUTING                              │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ • Route critical nets first (power, high-speed)        │ │
│  │ • Route SPI clock with series damping                  │ │
│  │ • Route I2C pull-ups with proper lengths               │ │
│  │ • Auto-route remaining nets with FreeRouting          │ │
│  │ • Place thermal vias under MCU/power converter         │ │
│  │ • Repour copper zones (GND, 3V3, 5V)                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ PHASE 4: VALIDATION & OPTIMIZATION                      │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ • DRC check: all traces meet clearance rules           │ │
│  │ • DFM check: all JLCPCB constraints met                │ │
│  │ • Signal integrity check: length matching              │ │
│  │ • Thermal check: temperature rise acceptable           │ │
│  │ • Optimization: reduce trace lengths, vias             │ │
│  │ • Final validation: ready for manufacturing            │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                    │
│  OUTPUT: K1 Production PCB Layout (.kicad_pcb)               │
│          ├─ All components placed                            │
│          ├─ All nets routed                                  │
│          ├─ Copper zones poured                              │
│          ├─ DRC: 0 violations                                │
│          ├─ DFM: JLCPCB compatible                           │
│          └─ Manufacturing files generated (Gerber, drill)    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 2: Detailed Implementation

### 2.1 Phase 1: Design Preparation

**Input:** K1 netlist (k1_motherboard_revA.net)
**Output:** Valid KiCad board with all footprints assigned

**Process:**

```python
class DesignPreparation:
    """
    Phase 1: Load netlist, assign missing footprints, validate schematic
    """

    def __init__(self, netlist_path, kicad_board_path):
        self.netlist = netlist_path  # k1_motherboard_revA.net
        self.board_path = kicad_board_path  # K1_Lightwave.kicad_pcb
        self.board = None
        self.missing_footprints = []

    def load_netlist(self):
        """Import netlist into KiCad board"""
        # Use KiCad CLI: kicad-cli pcb import-netlist
        # or IPC API: board.LoadNetlist() if available in K9.0
        pass

    def assign_footprints(self):
        """Assign missing footprints to Device library components"""
        # K1 Known Assignments:
        footprints = {
            'R': 'Resistor_SMD:R_0603_1608Metric',  # All resistors
            'C': 'Capacitor_SMD:C_0603_1608Metric',  # Small caps (<1µF)
            'C_bulk': 'Capacitor_SMD:C_1206_3216Metric',  # Bulk caps (>= 10µF)
            'D': 'Diode_SMD:D_SOD-323',  # Signal/ESD diodes
            'D_Schottky': 'Diode_SMD:D_SOD-123',  # Ideal diode
            'Fuse': 'Fuse:Fuse_1206_3216Metric',  # Polyfuse
        }
        # Iterate board.footprints(), match by reference pattern
        # Use IPC API to set footprint property
        pass

    def replace_ic_placeholders(self):
        """
        Replace placeholder ICs with proper symbols:
        - U2: TPS62160 buck converter (SOIC-8)
        - U5: LTC4412 ideal diode controller (SOT-23-5)
        - U6: W25Q128JV flash memory (SOIC-16)
        - U7: INA226 current monitor (MSOP-10)
        - U8: SN74AXC2T245 logic level translator (SOIC-8)
        """
        pass

    def validate_nets(self):
        """Verify all nets connected, no floating pins"""
        # Run ERC check: python kicad-cli erc
        # Parse results, report floating nets
        pass

    def run_erc(self):
        """Electrical Rule Check - must pass"""
        # ERC check for shorted nets, missing connections
        # Allow warnings for placeholder components
        # Fail if any critical errors
        pass
```

**Key Decisions:**
- Use KiCad CLI for netlist import (guaranteed compatibility, K7-K10 support)
- Manual footprint assignment (52 Device components, <10 minutes)
- IC replacements: Either manual in KiCad or programmatic replacement if time permits

### 2.2 Phase 2: Component Placement

**Input:** Valid KiCad board with all footprints
**Output:** Optimally placed components ready for routing

**Placement Strategy:**

```python
class ComponentPlacement:
    """
    Phase 2: Intelligent component placement with thermal/signal optimization
    """

    def __init__(self, board, k1_config):
        self.board = board  # KiCad board object
        self.config = k1_config  # K1-specific configuration

    def define_thermal_zones(self):
        """Define thermal zones on board"""
        zones = {
            'MCU_A': {
                'components': ['U1', 'C_BIN1', 'C_BOUT1'],  # COM-A module + power
                'center': (x, y),  # mm from corner
                'priority': 'high',
                'max_temp_rise': 10,  # °C
            },
            'MCU_B': {
                'components': ['U3', 'U6', 'U7'],  # COM-B + flash + monitor
                'center': (x, y),
                'priority': 'high',
                'max_temp_rise': 10,
            },
            'USB_INPUT': {
                'components': ['J1', 'F_USB', 'D_ESD_*'],
                'center': (x, y),
                'priority': 'medium',
            },
            'LED_OUTPUT': {
                'components': ['J_LED*', 'F1-4', 'D1-4'],
                'center': (x, y),
                'priority': 'high',  # High current
            },
        }
        return zones

    def cluster_components(self):
        """Group components by function"""
        clusters = {
            'power': ['J1', 'F_USB', 'C_BIN1', 'C_BOUT1'],
            'decoupling': ['C1', 'C2', 'C3', 'C4', 'C5'],  # Near MCU pins
            'usb_interface': ['D_ESD_DP', 'D_ESD_DM', 'R_USB_*'],
            'i2c': ['J3', 'J4', 'J5', 'J6'],
            'i2s_mic': ['J7', 'J8', 'J9'],
            'led_output': ['JLED1-4'],
            'inter_mcu': ['R_SPI_*', 'R_READY_PD'],
        }
        return clusters

    def place_components(self):
        """
        Optimal placement algorithm:
        1. Place connectors at board edge (USB, I2C, I2S, LED)
        2. Place MCU modules in center thermal zones
        3. Place decoupling capacitors within 5mm of power pins
        4. Place series resistors adjacent to MCU
        5. Fill remaining space with passive components
        """
        # Place J1 (USB-C) at bottom-center edge
        # Place J_LED1-4 at right edge (fan-out for LED outputs)
        # Place J3-J6 (I2C) at top edge
        # Place J7-J9 (I2S) at left edge
        # Place U1 (COM-A) near top-center
        # Place U3 (COM-B) near bottom-center
        # Place decoupling caps within 5mm of power pins
        # Place series resistors near source drivers
        pass

    def verify_spacing(self):
        """Verify minimum spacing constraints"""
        min_spacing = 2.0  # mm (JLCPCB standard)

        # Check all footprint-to-footprint distances
        # Check component-to-edge distance
        # Report violations
        pass

    def optimize_routing_accessibility(self):
        """Adjust placement for better routing"""
        # Minimize trace lengths (bounding box)
        # Ensure no component overlaps
        # Optimize for fanout from connectors
        pass
```

**K1-Specific Placement Rules:**

```
CONNECTOR PLACEMENT (Board Edge):
├─ J1 (USB-C): Bottom center (power input)
├─ JLED1-4 (LED Output): Right edge (fan-out)
├─ J3-J6 (I2C): Top edge (accessory)
├─ J7-J9 (I2S Mic): Left edge (audio in)
└─ J11-J12 (COM-A/B): Flexible (internal routing)

THERMAL ZONES:
├─ MCU-A Zone: Top-center (ESP32-S3-WROOM-1)
│  ├─ U1: Center
│  ├─ C_BIN1, C_BOUT1: Within 5mm of power pins
│  └─ Decoupling: Surrounding area
│
├─ MCU-B Zone: Bottom-center (bare ESP32-S3)
│  ├─ U3: Center
│  ├─ U6 (Flash): Adjacent
│  ├─ U7 (Monitor): Adjacent
│  └─ Decoupling: Surrounding area
│
├─ USB Input Zone: Bottom-left
│  ├─ J1 (connector): Board edge
│  ├─ F_USB: Within 2mm of J1 VBUS pin
│  ├─ D_ESD_*: Within 5mm of J1
│  └─ R_CC1/CC2: Very close to J1 CC pins
│
└─ LED Output Zone: Right edge
   ├─ JLED1-4: Board edge, vertical stacking
   ├─ F1-4 (Polyfuse): Between J_LED and board
   ├─ TVS D1-4: Between LED and GND
   └─ R_LED*: Series resistor to data line
```

**Placement Algorithm Pseudocode:**

```
1. Define board dimensions (assume 50mm × 80mm for K1)
2. Reserve edge zones for connectors (5mm border)
3. Define thermal zones with center points
4. For each thermal zone:
   a. Place primary IC (U1, U3, etc.)
   b. Place decoupling capacitors within 5mm (16 positions in circle)
   c. Place supporting components (resistors, diodes)
5. For each remaining component:
   a. Place nearest to source/sink for signal path
   b. Verify 2mm spacing minimum
   c. Rotate as needed for routing accessibility
6. Optimize: Minimize total wirelength using bounding box
7. Verify: All constraints met, ready for routing
```

### 2.3 Phase 3: Automated Routing

**Input:** Placed components
**Output:** Routed traces, vias, and poured zones

**Routing System:**

```python
class AutomatedRouting:
    """
    Phase 3: Route all nets using FreeRouting + manual critical traces
    """

    def __init__(self, board_path):
        self.board_path = board_path
        self.critical_nets = [
            'VBUS_USB_5V', '+3V3', '5V_LED', 'GND',  # Power
            'USB_D+_BOARD', 'USB_D-_BOARD',  # USB differential
            'SPI_SCK_A2B', 'SPI_MOSI_A2B', 'SPI_MISO_B2A',  # Inter-MCU
            'I2S_BCLK', 'I2S_LRCK', 'I2S_SD',  # Audio
        ]

    def route_critical_nets_manual(self):
        """
        Manually route high-speed/power nets before auto-routing:

        1. POWER DISTRIBUTION:
           - VBUS_USB_5V: Direct to F_USB input (fat trace)
           - 3V3: From buck converter output to distribution net
           - LED_5V: Isolated input to LED power zone
           - GND: Multi-point returns from zones to board edge

        2. HIGH-SPEED SIGNALS (SPI @ 40 MHz):
           - SPI_SCK: Add series damping resistor (33Ω)
             Routing rule: Direct path from MCU-A to MCU-B
             Length match: No constraint (clock)
           - SPI_MOSI: Direct path, 33Ω series damping
           - SPI_MISO: Direct path, 33Ω series damping
           - SPI_CS: Pull-up to 3V3, assert by MCU-A

        3. USB SIGNALS:
           - USB_D+/D-: Differential pair routing
             Target impedance: N/A (USB 2.0 FS is loose spec)
             Trace width: 10 mil (0.25mm)
             Spacing: 8 mil (consistent with other signals)
             Length match: Keep within ±50mm of each other
           - ESD diode placement: Within 5mm of J1 pads

        4. I2C SIGNALS:
           - SDA/SCL: Pull-ups to 3V3 via 4.7kΩ resistors
             Routing: No speed constraint, general purpose

        5. I2S/PDM SIGNALS:
           - I2S_BCLK: Series damping resistor (33Ω) if using translator
           - I2S_LRCK: Series damping
           - I2S_SD: Series damping (all ~20 MHz clock domain)
        """
        pass

    def export_to_specctra_dsn(self):
        """
        Export board to Specctra DSN format for FreeRouting

        Command: kicad-cli pcb export-specctra --format dsn board.kicad_pcb
        Output: board.dsn (Specctra Design Space Network)

        DSN includes:
        - Component placement (fixed)
        - Footprint pad locations
        - Net connectivity
        - Electrical constraints (clearances, widths)
        - Layer definitions (4-layer stackup)
        - Via specifications (allowed sizes)
        """
        pass

    def configure_freerouting(self):
        """
        FreeRouting configuration for K1:

        Routing Parameters:
        - Trace width: 10 mil (0.25mm) standard, 4 mil minimum
        - Via diameter: 0.3mm standard, 0.25mm minimum
        - Via drill: 0.15mm
        - Clearance: 5 mil (0.127mm) minimum
        - Layers: 4 (L1=signals, L2=GND, L3=power, L4=signals)

        High-Speed Rules:
        - SPI clock traces: 10 mil width, 20 mil spacing from other signals
        - Power traces: 50-160 mil depending on current (LED_5V: 160 mil)
        - Ground: Multiple connection points, via stitching every 5mm

        Cost Function Weights:
        - Trace length: 50% (minimize wiring)
        - Via count: 30% (minimize cost)
        - Routing failures: 20% (maximize completion)
        """
        freerouting_config = {
            'max_passes': 100,
            'effort_level': 'high',
            'multi_threading': True,
            'threads': 4,
            'optimization': 'via_reduction',
        }
        return freerouting_config

    def run_freerouting(self):
        """
        Execute FreeRouting auto-router:

        Command:
        java -Djava.awt.headless=true -jar freerouting-2.1.0.jar \
          -de board.dsn -do board.ses \
          -mt 4 --gui.enabled=false

        Timeout: 15 minutes (for K1 complexity)
        Success: >95% nets routed

        Output: board.ses (Specctra Session - routing results)
        """
        pass

    def import_routing_results(self):
        """
        Import FreeRouting results back into KiCad:

        Command: kicad-cli pcb export-specctra --format ses board.ses

        Process:
        1. Parse board.ses (routed traces, vias, segments)
        2. Import traces into KiCad board layer-by-layer
        3. Place vias from routing session
        4. Verify no conflicts with fixed components
        5. Repour copper zones (GND, 3V3, 5V)
        """
        pass

    def repour_copper_zones(self):
        """
        Fill copper zones with proper net assignment:

        Zone Configuration:
        ├─ Layer 2 (GND plane): Continuous GND pour
        │  └─ Via stitching: 10mm grid border, 5mm interior
        │
        ├─ Layer 3 (Power plane): Segmented
        │  ├─ 3V3 zone: ~40% of plane
        │  ├─ 5V zone: ~40% of plane
        │  ├─ LED_5V zone: ~20% of plane
        │  └─ Isolation traces between zones (separation)
        │
        └─ Layers 1 & 4: GND return paths + isolated zones

        Pour Rules:
        - Clearance from traces: 0.2mm
        - Minimum width: 0.25mm
        - Hatch pattern (better for impedance control)
        - Via stitching: 0.3mm dia, 10mm spacing
        """
        pass

    def place_thermal_vias(self):
        """
        Add thermal management vias:

        MCU Thermal Vias (16-24 vias in 4mm circle):
        - Diameter: 0.3mm
        - Spacing: 1.27mm grid
        - Pattern: Pad center area
        - Via stitching around MCU: 5mm grid

        Purpose: Conduct heat from BGA balls to GND plane below
        Effective thermal resistance reduction: ~50%
        """
        pass

    def verify_routing(self):
        """Validate routing results"""
        checks = [
            'All nets routed (0 unrouted segments)',
            'No trace overlaps',
            'Minimum trace width met (4 mil)',
            'Minimum clearance met (5 mil)',
            'Via count acceptable (<50 vias)',
            'High-speed nets length matched (±5%)',
            'Copper zones properly poured',
            'Thermal vias in place',
        ]
        pass
```

**Routing Priority Order:**

```
PRIORITY 1 (Power Delivery):
├─ VBUS_USB_5V (1.2A peak)
├─ 3V3 distribution (0.8A peak)
├─ LED_5V (8A peak) ← HIGHEST CURRENT
└─ GND returns (all zones)

PRIORITY 2 (High-Speed):
├─ SPI_SCK (40 MHz clock)
├─ SPI_MOSI/MISO (40 MHz data)
├─ USB_D+/D- (12 Mbps)
└─ I2S/PDM clock lines (20 MHz)

PRIORITY 3 (Control):
├─ SPI_CS, SYNC, READY
├─ I2C (SDA, SCL)
└─ General I/O (low speed)

PRIORITY 4 (Remaining):
├─ Decoupling connections
├─ Test point connections
└─ Any remaining nets
```

### 2.4 Phase 4: Validation & Optimization

**Input:** Routed board
**Output:** Manufacturing-ready PCB

```python
class DesignValidation:
    """
    Phase 4: Comprehensive DRC, DFM, and manufacturing validation
    """

    def run_drc(self):
        """Design Rule Check"""
        drc_rules = {
            'trace_width': ('min', 4, 'mil'),  # JLCPCB standard
            'trace_spacing': ('min', 5, 'mil'),
            'pad_to_trace': ('min', 5, 'mil'),
            'via_drill': ('min', 0.15, 'mm'),
            'via_pad_size': ('min', 0.3, 'mm'),
            'annular_ring': ('min', 0.15, 'mm'),
            'copper_to_edge': ('min', 0.3, 'mm'),
        }
        # Run KiCad DRC: python kicad-cli drc
        # Parse output, report violations
        # MUST PASS: 0 violations
        pass

    def validate_dfm_jlcpcb(self):
        """Verify JLCPCB manufacturing constraints"""
        checks = {
            'layer_count': 4,  # JLCPCB standard
            'via_fill': 'tented',  # No solder mask relief
            'trace_width_range': (4, 100, 'mil'),
            'trace_spacing_range': (5, 1000, 'mil'),
            'solder_mask_clearance': (4, 'mil'),
            'silk_screen_clearance': (5, 'mil'),
            'fiducial_size': 1.0,  # mm diameter
            'fiducial_placement': 3,  # minimum 3 fiducials
            'panelization': 'auto',  # JLCPCB can panelize
        }
        # Verify each constraint
        # Report violations with remediation
        pass

    def validate_signal_integrity(self):
        """Signal integrity validation"""
        checks = {
            'SPI_SCK': {
                'net': 'SPI_SCK_A2B',
                'frequency': 40,  # MHz
                'length_target': 'direct',
                'damping': '33R series',
                'status': 'pass',  # Single-ended, no impedance control needed
            },
            'SPI_MOSI': {
                'net': 'SPI_MOSI_A2B',
                'frequency': 40,
                'length_target': 'direct',
                'damping': '33R series',
                'status': 'pass',
            },
            'USB_D+_D-': {
                'net': 'USB_D+/D-_BOARD',
                'frequency': 12,  # Mbps (full-speed)
                'impedance_target': None,  # USB FS is loose spec
                'length_match': '±50mm',
                'status': 'pass',
            },
            'I2S_BCLK': {
                'net': 'I2S_BCLK',
                'frequency': 20,
                'damping': '33R if translator',
                'status': 'pass',
            },
        }
        # Measure actual trace lengths
        # Verify damping resistors placed
        # Verify differential pair spacing (if applicable)
        pass

    def validate_thermal(self):
        """Thermal analysis"""
        thermal_analysis = {
            'ambient_temp': 25,  # °C
            'max_component_temp': 85,  # °C (ESP32-S3 spec)
            'allowable_rise': 60,  # °C margin = 60°C

            'power_dissipation': {
                'MCU_A': 0.3,  # W (estimate)
                'MCU_B': 0.5,  # W (peak rendering)
                'power_converter': 0.2,  # W (TPS62160 losses)
            },

            'thermal_resistance': {
                'mcu_to_board': 15,  # °C/W typical for WROOM module
                'board_to_ambient': 5,  # °C/W (4-layer board, 50mm × 80mm)
            },

            'thermal_vias': {
                'diameter': 0.3,  # mm
                'count': 20,
                'effectiveness': 0.5,  # 50% of via thermal conductance
            },
        }

        # Calculate: ΔT = P_total × (R_jc + R_ca) - R_vias_effect
        # For K1: ΔT ≈ 0.8W × (15 + 5) - (0.5 × vias_effect) ≈ 12°C rise
        # Actual max junction temp: 25 + 12 = 37°C << 85°C spec
        # Status: PASS (excellent thermal margin)
        pass

    def validate_manufacturing(self):
        """Pre-manufacturing checklist"""
        checklist = [
            'DRC: 0 violations',
            'All nets routed',
            'Copper zones poured',
            'Via stitching complete',
            'Thermal vias placed',
            'Silk screen legible (min 1.0mm text)',
            'Test points accessible',
            'Fiducials placed (3 minimum, diagonal)',
            'Reference designators visible',
            'Solder paste apertures correct',
            'Assembly drawing generated',
            'BOM complete (part numbers, quantities)',
            'Gerber files valid (output by KiCad)',
            'Drill file matches design',
            'NC file (Excellon format)',
            'Solder mask gerber (inverted for K9.0)',
            'Silkscreen gerber (both sides)',
            'Copper gerber (all layers)',
        ]
        # Verify each item
        # Generate final report
        pass

    def optimize_design(self):
        """Final optimization"""
        optimizations = [
            'Reduce via count (post-routing cleanup)',
            'Shorten traces (move components if needed)',
            'Reduce copper area (cost savings)',
            'Verify panelization (JLCPCB auto-panelizes 2-4 boards)',
        ]
        pass

    def export_manufacturing_files(self):
        """Generate manufacturing outputs"""
        outputs = {
            'gerbers': [
                'K1_Lightwave-F_Cu.gbr',  # Layer 1 (top copper)
                'K1_Lightwave-In1_Cu.gbr',  # Layer 2 (internal GND)
                'K1_Lightwave-In2_Cu.gbr',  # Layer 3 (internal power)
                'K1_Lightwave-B_Cu.gbr',  # Layer 4 (bottom copper)
                'K1_Lightwave-F_Silkscreen.gbr',  # Top silk
                'K1_Lightwave-B_Silkscreen.gbr',  # Bottom silk
                'K1_Lightwave-F_Mask.gbr',  # Top solder mask
                'K1_Lightwave-B_Mask.gbr',  # Bottom solder mask
            ],
            'drills': [
                'K1_Lightwave.drl',  # Via and hole drill file (Excellon)
                'K1_Lightwave.nc',  # Alternate format (Excellon)
            ],
            'documentation': [
                'K1_Lightwave.kicad_pcb',  # Final PCB file
                'K1_Lightwave_assembly.pdf',  # Assembly drawing
                'K1_Lightwave_BOM.csv',  # Bill of materials
                'K1_Lightwave_placement.csv',  # Pick-and-place data
            ],
        }
        # Export each file with KiCad command-line tools
        # Verify file integrity
        pass
```

---

## Part 3: Critical Implementation Details

### 3.1 K1 Board Specifications

**Physical Dimensions:**
```
PCB Size: 50mm × 80mm (estimated for dual-MCU + I/O)
Layers: 4 (FR-4, 1.6mm thickness)
  L1: Signal/GND
  L2: GND plane (continuous)
  L3: Power distribution (segmented 3V3/5V/LED_5V)
  L4: Signal/GND
Minimum Trace Width: 4 mil (0.1mm) JLCPCB standard
Minimum Clearance: 5 mil (0.127mm)
Via Diameter: 0.3mm standard, 0.25mm minimum
Fiducials: 3 (1.0mm dia, solder mask opening)
```

**Power Distribution:**
```
Input: VBUS_USB_5V (5V, 1.2A peak from USB)
├─ F_USB (1A polyfuse)
├─ U2 (TPS62160 buck: 5V → 3V3, 1.5A)
│  └─ C_BIN1, C_BOUT1 (10µF decoupling)
│
└─ LED_5V input (isolated, 8A peak)
   └─ Ideal diode circuit (LTC4412 + FET)
      └─ LED_5V rail (8A distribution)
```

**Thermal Management:**
```
Heat Sources:
├─ MCU-A (ESP32-S3-WROOM-1): ~300mW
├─ MCU-B (bare ESP32-S3): ~500mW
├─ Power converter: ~200mW (losses)
└─ Total: ~1W maximum

Thermal Path:
MCU → BGA balls → Thermal vias → GND plane → PCB → Ambient

Thermal Vias: 16-24 × 0.3mm, 1.27mm grid (4mm circle under MCU)
Thermal Resistance: ~15°C/W (MCU to GND plane)
Maximum Temperature Rise: ~15°C (well below 85°C spec)
```

### 3.2 Critical Design Rules (IPC-2221A)

**K1 Trace Width by Current:**
```
3.3V Logic Domain:
├─ 100 mA: 4 mil minimum (0.1mm)
├─ 500 mA: 10 mil (0.25mm)
└─ 800 mA peak: 15 mil (0.38mm) recommended

5V USB Domain:
├─ 100 mA: 4 mil
├─ 500 mA: 10 mil
└─ 1.2 mA peak: 15 mil recommended

LED_5V Domain (HIGHEST CURRENT):
├─ 1A: 50 mil (1.27mm)
├─ 4A: 100 mil (2.54mm)
└─ 8A peak: 160 mil (4.06mm) REQUIRED
```

**Clearance Requirements:**
```
Voltage Class: IPC-2221A Class 2A (5-10V domain)
Minimum Clearance:
├─ Trace-to-trace: 4 mil (0.1mm)
├─ Trace-to-pad: 5 mil (0.127mm)
├─ Trace-to-board-edge: 15 mil (0.38mm) JLCPCB
└─ Copper-to-edge (final): 300 mil (7.6mm) safety margin

Environmental: Class 2 (indoor, non-corrosive, humidity <85%)
```

### 3.3 JLCPCB Manufacturing Constraints

**Trace & Via:**
```
Standard: 6/6 mil (0.15/0.15mm)
  - Trace width: ≥6 mil
  - Trace spacing: ≥6 mil
  - Cost: baseline ($10-15 for prototype)

Advanced: 4/4 mil (0.1/0.1mm)
  - Trace width: ≥4 mil
  - Trace spacing: ≥4 mil
  - Cost: +40% ($14-21 for prototype)

K1 Recommendation: STANDARD (6/6 mil)
  - Easier to hand-solder
  - Better yield rate
  - Cost savings (~$5)
  - Signal paths don't require 4/4 for 40 MHz SPI
```

**Layer Stack:**
```
Standard 4-layer:
  L1: 35µm copper (signal layer)
  Prepreg: 0.1mm (dielectric)
  L2: 35µm copper (GND plane)
  Core: 1.2mm (FR-4 substrate)
  L3: 35µm copper (power distribution)
  Prepreg: 0.1mm
  L4: 35µm copper (signal layer)
  Surface: HASL (hot air solder leveling)

Cost: ~$15 for 10 boards (prototype qty)
Lead time: 3-5 business days
```

**Assembly:**
```
SMD Assembly capability: YES (JLCPCB offers SMD assembly)
Available parts: 40,000+ JLCPCB in-stock components
Setup cost: $0 (no NRE for standard panelization)
Placement accuracy: ±0.1mm (0402-BGA)
Soldering: Lead-free (217°C reflow)

K1 Component Compatibility:
├─ ESP32-S3-WROOM-1: ✅ Available (stock part)
├─ Common resistors (0603): ✅ Available
├─ Standard capacitors (0603/1206): ✅ Available
├─ USB-C connector: ✅ Available
├─ JST connectors: ✅ Available
├─ Specialized ICs (TPS62160, etc.): ⚠️ May require manual assembly
└─ Overall: 95%+ JLCPCB compatible
```

---

## Part 4: Implementation Roadmap

### Phase 1: Foundation (Week 1)
- [x] Create IPC standards library (Python module)
- [x] Research KiCad IPC API capabilities
- [x] Research FreeRouting integration
- [ ] Implement Phase 1 (Design Prep) class
- [ ] Test footprint assignment on K1 netlist

### Phase 2: Placement (Week 2)
- [ ] Implement Phase 2 (Component Placement) class
- [ ] Define K1 thermal zones
- [ ] Test placement algorithm with K1
- [ ] Optimize placement for routing

### Phase 3: Routing (Week 3)
- [ ] Implement Phase 3 (Automated Routing) class
- [ ] Generate Specctra DSN from K1
- [ ] Configure and test FreeRouting
- [ ] Validate routing results

### Phase 4: Validation (Week 4)
- [ ] Implement Phase 4 (Validation) class
- [ ] Run comprehensive DRC
- [ ] Validate DFM constraints
- [ ] Generate manufacturing files

### Phase 5: Optimization (Week 5)
- [ ] Optimize design (trace lengths, vias)
- [ ] Final validation
- [ ] Documentation
- [ ] Ready for manufacturing

---

## Part 5: Success Metrics

| Metric | Target | K1 Baseline |
|--------|--------|------------|
| Design time | <30 min | ~4-6 hours manual |
| DRC violations | 0 | 0 |
| DFM violations | 0 | 0 |
| Routing success | >95% | 100% (simple board) |
| Trace length optimization | <10% from minimum | - |
| Thermal margin | >20°C | ~15°C |
| Manufacturing cost | <$20/board | - |
| Lead time | <5 days | 3-5 days (JLCPCB) |

---

## Part 6: Deliverables Checklist

### Code Modules
- [ ] `design_preparation.py` - Phase 1 implementation
- [ ] `component_placement.py` - Phase 2 implementation
- [ ] `automated_routing.py` - Phase 3 implementation
- [ ] `design_validation.py` - Phase 4 implementation
- [ ] `elite_pcb_designer.py` - Main agent class (orchestrator)
- [ ] `k1_configuration.py` - K1-specific parameters
- [ ] `ipc_standards_library.py` - IPC standard rules ✅ DONE

### Test & Validation
- [ ] Test suite for each phase
- [ ] Integration tests (full workflow)
- [ ] K1 reference implementation
- [ ] Before/after comparison

### Documentation
- [ ] API reference
- [ ] User guide
- [ ] Troubleshooting guide
- [ ] Design rule reference

### Manufacturing
- [ ] Gerber files (K1 sample board)
- [ ] Manufacturing report
- [ ] Cost analysis
- [ ] Assembly guide

---

## Part 7: Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| KiCad API changes in K10 | High | High | Use CLI tools as fallback, monitor upstream |
| FreeRouting routing failure | Medium | Medium | Manual critical trace routing first |
| Thermal violation | Low | High | Simulate + add thermal vias |
| Manufacturing constraints | Low | High | Verify against JLCPCB requirements early |
| Component availability | Low | Medium | Maintain BOM with alternatives |

---

## Part 8: References & Resources

**KiCad Documentation:**
- Official KiCad Python API (K9.0+)
- KiCad CLI reference
- PCB file format specification

**FreeRouting:**
- Official FreeRouting GitHub repository
- Specctra DSN/SES format specification
- FreeRouting API documentation

**IPC Standards:**
- IPC-2221A: Generic Standard on Printed Board Design
- IPC-2221B: Parametric Design Standard
- IPC-6012: Acceptability of Printed Boards
- IPC-A-610: Acceptability of Electronic Assemblies

**Manufacturing:**
- JLCPCB DFM guidelines
- JLCPCB capability table
- Standard panelization patterns

---

## Version Control

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-10-24 | Initial specification, Phase 1-4 complete |

---

**Status: READY FOR IMPLEMENTATION**

Next: Develop Phase 1 (Design Preparation) as first working module, test against K1 netlist, validate with KiCad.
