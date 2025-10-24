# Research Agent Prompt: Elite PCB Designer for KiCad

## Mission

Build a comprehensive, implementable specification for an **Elite PCB Designer Agent** that can take K1 Lightwave from netlist → production-ready PCB layout with professional-grade signal integrity, thermal management, and DFM validation.

## Phase 1: API & Technology Foundation Research

### Task 1.1: KiCad Python API Deep Dive
**Objective:** Become an expert on KiCad 9 IPC API for programmatic PCB manipulation

**Research Requirements:**
1. **IPC API vs. Legacy pcbnew Module**
   - What exactly is the IPC API? (vs. SWIG bindings)
   - Why is pcbnew deprecated? What breaks?
   - Compatibility matrix: KiCad 7, 8, 9+
   - Migration path from pcbnew → IPC API
   - Official timeline for removal

2. **Exact API Capabilities**
   - Board file loading/saving
   - Footprint manipulation (add, move, rotate)
   - Net manipulation (create, assign, connect)
   - Trace/wire routing methods
   - Via placement and configuration
   - Polygon pour creation
   - DRC rule customization
   - File export options (Gerber, ODB++, IPC-2581)

3. **Practical Implementation**
   - Write working code examples for:
     - Load .kicad_pcb and extract all components
     - Add footprint programmatically to net
     - Move component to X,Y coordinate
     - Create traces between pads
     - Place vias with grid pattern
     - Repour copper zones
   - Test with actual K1 netlist
   - Identify all error handling requirements

4. **Limitations & Workarounds**
   - What operations are NOT supported?
   - What requires GUI interaction?
   - Performance constraints?
   - Memory usage patterns?
   - Best practices for large boards?

**Deliverable:** Technical API specification with working code examples for each major operation

---

### Task 1.2: FreeRouting Integration Architecture
**Objective:** Understand exact integration points between KiCad and FreeRouting

**Research Requirements:**
1. **Specctra DSN/SES File Format**
   - What exactly is DSN? (Design Space Network)
   - What exactly is SES? (Session)
   - How to generate perfect DSN from KiCad?
   - How to import SES back into KiCad without data loss?
   - What constraints are preserved/lost?

2. **FreeRouting API vs. CLI**
   - Can FreeRouting be called programmatically?
   - Does it have a REST API or socket interface?
   - CLI command structure and options?
   - Batch processing capabilities?
   - Routing rule format and syntax?

3. **Configuration & Constraints**
   - How to specify impedance-controlled traces in DSN?
   - Differential pair definition in Specctra format?
   - Via constraints and specifications?
   - Layer definitions and stackup?
   - Electrical rules (clearances, widths)?

4. **Integration Workflow**
   - Step-by-step: KiCad → DSN → FreeRouting → SES → KiCad
   - Data loss at each conversion step?
   - How to verify routing quality?
   - Manual cleanup requirements?
   - Validation before/after routing?

5. **Alternative Routers**
   - Other auto-routers compatible with KiCad?
   - Commercial vs. open-source options?
   - Trade-offs between options?
   - Which is best for K1 dual-MCU board?

**Deliverable:** Complete FreeRouting integration specification with working workflow

---

### Task 1.3: SKiDL for Netlist Generation
**Objective:** Master SKiDL for programmatic circuit description

**Research Requirements:**
1. **SKiDL Capabilities for K1**
   - Can SKiDL generate .kicad_pcb directly? (not just netlist?)
   - Footprint assignment in SKiDL syntax
   - Component positioning in SKiDL?
   - Net constraints and priorities?
   - Electrical rules checking (ERC) integration?

2. **K1 Netlist in SKiDL**
   - Refactor current SKiDL script to be agent-readable
   - Footprint assignments as metadata
   - Thermal zone markings
   - Critical net annotations
   - Design rule specifications

3. **Programmatic Manipulation**
   - Can agent modify SKiDL script?
   - Add/remove components?
   - Change footprints?
   - Reannotate references?
   - Regenerate netlist from modified script?

**Deliverable:** SKiDL specification tailored for K1, with agent-compatible syntax

---

## Phase 2: Professional PCB Design Knowledge Research

### Task 2.1: IPC Standards Implementation
**Objective:** Create executable IPC standards library

**Research Requirements:**
1. **IPC-2221A Trace Width Formula**
   - Exact formula: I = 0.048 × ΔT^0.44 × A^0.725
   - For external vs. internal layers
   - Temperature rise constants
   - Verification with manufacturer tables
   - Python implementation with examples

2. **IPC-2221A Clearance Tables**
   - Voltage-based clearance requirements
   - All voltage levels (0-500V)
   - Environmental factors (altitude, pollution)
   - Space between traces
   - Space to board edge
   - Space to component leads
   - Create lookup table for K1 (3.3V, 5V, 12V domains)

3. **IPC-6012 Class Requirements**
   - Class 1 vs. 2 vs. 3 specifications
   - Which class for K1 (audio LED controller)?
   - Testing requirements for each class
   - Defect acceptance criteria
   - Implementation checklist

4. **IPC-A-610 Assembly Standards**
   - Solder joint quality criteria (visual)
   - Component placement tolerance
   - Pad size and shape requirements
   - Test point requirements
   - Implementation for K1 assembly

**Deliverable:** Executable Python library implementing IPC standards with K1-specific configurations

---

### Task 2.2: High-Speed Design Rules for K1
**Objective:** Define exact routing rules for K1's inter-MCU SPI link

**Research Requirements:**
1. **SPI Clock & Data Lines (20-40 MHz)**
   - Impedance target for SPI signals?
   - Differential pair impedance? (Single-ended, not differential)
   - Length matching tolerance (5mm for SPI)?
   - Crosstalk risk between SPI lines?
   - Return path requirements?

2. **USB Signals (if implemented)**
   - USB 2.0 full-speed: 12 Mbps (low-speed for routing)
   - Differential impedance: 90Ω ±10%
   - Trace width and spacing for 90Ω target
   - Length matching for D+/D- pair
   - ESD diode placement requirements

3. **Clock Distribution (20 MHz reference)**
   - Clock slew rate requirements
   - Skew tolerance for distributed clocks
   - Via placement near clock source
   - Clock trace width
   - Guard traces needed?

4. **Impedance Calculator for K1**
   - K1 stackup: 4-layer, FR-4, 1.6mm
   - IPC-2221 calculations
   - Differential pair spacing for 90Ω (if needed)
   - Single-ended 50Ω targets for high-speed
   - Verification methodology

**Deliverable:** K1-specific high-speed design rules with impedance calculations

---

### Task 2.3: Thermal Management Algorithm
**Objective:** Implement thermal analysis for K1 components

**Research Requirements:**
1. **Component Thermal Specs**
   - ESP32-S3-WROOM thermal resistance (θJA)
   - Power dissipation at peak load
   - Maximum junction temperature (85°C typical)
   - Thermal via effectiveness
   - Copper area thermal contribution

2. **Thermal Via Strategy**
   - Optimal via diameter and spacing
   - Via fill vs. tented vs. open
   - Number of vias needed per component
   - Placement grid pattern
   - Thermal resistance calculations

3. **Heat Dissipation Analysis**
   - Simulate K1 at max power (500mW MCU estimate)
   - Ambient temperature assumptions (25°C)
   - Thermal margin target (10°C)
   - Copper plane effectiveness
   - Component arrangement impact

4. **K1-Specific Thermal Zones**
   - High heat: MCU, power converters
   - Moderate heat: LED drivers, decoupling caps
   - Cool zone: passive components, ESD diodes
   - Placement constraints by thermal zone

**Deliverable:** Working thermal analyzer with K1-specific parameters and simulations

---

### Task 2.4: Signal Integrity Best Practices
**Objective:** Document SI rules for K1 design

**Research Requirements:**
1. **Crosstalk Prevention**
   - Rules for SPI bus (SCK, MOSI, MISO, CS)
   - Spacing requirements between high-speed lines
   - Return path management
   - Ground plane stitching via density

2. **Via Stitching Strategy**
   - Purpose: EMI containment, return path
   - Spacing for different frequency ranges
   - K1 frequency content (20-40 MHz SPI clock)
   - Via diameter and placement grid
   - Border via stitching (Faraday cage effect)

3. **Layer Stackup Design**
   - K1 recommended: L1 (signals), L2 (ground), L3 (power), L4 (signals/ground)
   - Ground plane continuity
   - Power plane segmentation (3.3V vs. 5V)
   - Dielectric thickness for impedance control
   - Manufacturing feasibility

4. **Differential Pair Routing (if used)**
   - Trace width, spacing for 90Ω differential (if applicable)
   - Length matching tolerance
   - Via transitions
   - Crosstalk with adjacent traces

**Deliverable:** K1 signal integrity specification with routing rules

---

## Phase 3: Manufacturing & Cost Research

### Task 3.1: JLCPCB Constraint Codification
**Objective:** Encode all JLCPCB DFM constraints into agent rules

**Research Requirements:**
1. **Trace & Via Capabilities**
   - Standard (6/6 mil) vs. Advanced (4/4 mil) costs
   - Via drill sizes: 0.3mm, 0.25mm minimum
   - Annular ring: 0.15mm minimum
   - Aspect ratio limits: via length / diameter
   - Blind/buried via cost multipliers

2. **Layer Count Economics**
   - Cost per layer
   - Standard stackups: 1, 2, 4, 6, 8 layers
   - 4-layer vs. 2-layer trade-offs for K1
   - Impedance control requirements
   - Manufacturing complexity

3. **Assembly Constraints**
   - Component spacing minimums (2mm typical)
   - Fine-pitch component handling (BGA pitch 0.5mm)
   - Fiducial placement requirements (3 minimum, diagonal)
   - Test point accessibility
   - Tooling hole requirements

4. **Cost Optimization Vectors**
   - Trace width impact: 8 mil vs. 6 mil cost
   - Layer count: 2 vs. 4 layer savings
   - Panelization: 1x1 vs. 2x2 vs. 4x4 savings percentages
   - Component count impact
   - Assembly yield improvements

**Deliverable:** JLCPCB constraint database with cost model for K1

---

### Task 3.2: DFM Validation Rules
**Objective:** Create comprehensive DFM checker for K1

**Research Requirements:**
1. **Fabrication DFM**
   - Minimum trace width and spacing
   - Via diameter and hole size
   - Annular ring adequacy
   - Clearance to board edge
   - Copper to edge safety margins
   - Solder mask clearances
   - Silkscreen legibility (line width, text size)

2. **Assembly DFM (DFA)**
   - Component spacing (no overlaps, toolhead clearance)
   - Pad size vs. component pins
   - Solder paste opening dimensions
   - Test point accessibility
   - Fiducial placement and orientation
   - Reference designator visibility

3. **Reflow & Thermal**
   - Solder paste volume adequacy
   - Thermal shock compatibility
   - Lead-free solder (217°C melting point) considerations
   - Board flex during reflow
   - Warping prevention

4. **JLCPCB-Specific Checks**
   - Use JLCPCB DFM checker API (if available)
   - Common failure modes
   - Cost optimization recommendations
   - Assembly process compatibility

**Deliverable:** DFM checker implementation with JLCPCB rules for K1

---

### Task 3.3: Design Review Checklist
**Objective:** Create automated design review process

**Research Requirements:**
1. **Pre-Layout Validation**
   - Schematic ERC: all nets connected?
   - Footprint availability and correctness
   - Component part numbers verified
   - Pin-to-pin electrical compatibility
   - Power requirements validation

2. **Post-Placement Validation**
   - Component thermal zones adhered?
   - Spacing violations?
   - 3D model enclosure fit?
   - Signal path logic flow?
   - Decoupling proximity?

3. **Post-Routing Validation**
   - DRC: zero errors?
   - All nets routed (no unrouted segments)?
   - Length matching verified?
   - Via stitching complete?
   - Copper planes repoured?

4. **Pre-Fabrication Validation**
   - Gerber files correct?
   - Drill file matches design?
   - Silkscreen complete and legible?
   - BOM accuracy?
   - Pick-and-place data valid?
   - Fiducial placement correct?

**Deliverable:** Automated design review checklist with validation scripts for K1

---

## Phase 4: Agent Implementation Research

### Task 4.1: Component Placement Algorithm Research
**Objective:** Understand best practices for programmatic component placement

**Research Requirements:**
1. **Professional Placement Methodologies**
   - Thermal zone creation
   - Signal flow grouping
   - Component family clustering
   - Mechanical constraints
   - Decoupling proximity rules

2. **Genetic Algorithm for Placement**
   - Fitness function: thermal, routing, testability
   - Mutation operators: move, rotate, swap
   - Crossover strategy
   - Convergence criteria
   - Population size and generation count

3. **Constraint Satisfaction**
   - Hard constraints (cannot violate)
   - Soft constraints (prefer but flexible)
   - Constraint propagation algorithms
   - Backtracking for infeasible placements
   - Optimization under constraints

4. **K1-Specific Placement**
   - Thermal zones: MCU-A audio, MCU-B LED, USB input, LED output
   - Power distribution path minimization
   - SPI signal path optimization
   - I2C clustering
   - Decoupling distribution

**Deliverable:** Component placement algorithm specification with K1 implementation

---

### Task 4.2: Routing Algorithm Research
**Objective:** Understand FreeRouting workflow for K1

**Research Requirements:**
1. **Specctra Format Deep Dive**
   - DSN file structure and syntax
   - Constraint definition format
   - Net and pin definitions
   - Via specifications
   - Layer definitions and routing grid

2. **Routing Strategy**
   - Critical nets first (power, high-speed)
   - High-current trace routing
   - SPI signal routing (clock, MOSI, MISO, CS)
   - Ground/return path optimization
   - Minimize routing conflicts

3. **FreeRouting Configuration**
   - Routing parameters (effort level, optimization)
   - Cost function weights
   - Timing constraints
   - Signal integrity constraints
   - Rip-up and retry strategy

4. **Post-Routing Validation**
   - Length matching verification
   - Impedance measurement points
   - Crosstalk analysis
   - Return path continuity
   - DRC validation

**Deliverable:** Complete FreeRouting workflow specification for K1

---

### Task 4.3: Agent Architecture Deep Dive
**Objective:** Design optimal architecture for Elite PCB Designer Agent

**Research Requirements:**
1. **Module Dependencies & Data Flow**
   - How do placement, routing, validation interact?
   - Data structures for board representation?
   - File I/O at each stage?
   - Error handling strategy?
   - Rollback/undo mechanism?

2. **Decision Tree & Heuristics**
   - When to place vs. when to defer?
   - How to handle routing conflicts?
   - When to restart routing?
   - Convergence indicators?
   - Human intervention points?

3. **Performance Optimization**
   - Large board handling (100+ components)
   - Time budget per phase
   - Parallel processing opportunities?
   - Caching strategies?
   - Memory constraints?

4. **Extensibility & Plugins**
   - Custom DRC rules
   - Custom optimization algorithms
   - Support for different boards
   - Third-party tool integration

**Deliverable:** Detailed architecture specification with data flow diagrams

---

## Phase 5: Validation & Best Practices

### Task 5.1: Test Cases & Benchmarks
**Objective:** Define test strategy for agent implementation

**Research Requirements:**
1. **K1 Test Design**
   - Use actual K1 netlist as primary test case
   - Expected placement quality metrics
   - Expected routing success rate
   - Design time target: < 30 minutes
   - DRC compliance: 100% pass

2. **Regression Tests**
   - Standard test boards (reference designs)
   - Known good designs from manufacturers
   - Industry benchmark designs
   - Stress tests (high component density)
   - Failure case testing

3. **Validation Metrics**
   - Placement density (utilization %)
   - Routing success rate
   - Trace length distribution
   - Thermal zone compliance
   - DFM rule violations
   - Design time
   - Manual intervention count

**Deliverable:** Test specification with K1 reference implementation

---

### Task 5.2: Documentation & User Guides
**Objective:** Create user-facing documentation

**Research Requirements:**
1. **API Documentation**
   - Function signatures
   - Parameter specifications
   - Return value descriptions
   - Error codes and handling
   - Usage examples

2. **Design Guides**
   - How to prepare netlist for agent
   - Configuration file format
   - Design rule specification
   - Constraint definition
   - Best practices for K1-like boards

3. **Troubleshooting Guide**
   - Common failures and solutions
   - Design rule conflict resolution
   - Routing failure recovery
   - Thermal zone violations
   - Manufacturing constraint issues

**Deliverable:** Complete user documentation with examples

---

## Deliverables Checklist

- [ ] KiCad Python API specification with working code
- [ ] FreeRouting integration workflow documentation
- [ ] IPC standards implementation library
- [ ] K1-specific high-speed design rules
- [ ] Thermal analyzer implementation
- [ ] JLCPCB constraint database
- [ ] DFM validation rules
- [ ] Component placement algorithm specification
- [ ] Routing algorithm workflow
- [ ] Agent architecture specification
- [ ] Test specification with K1 reference
- [ ] Complete user documentation

## Success Criteria

1. **Technical Completeness**
   - All KiCad API operations documented
   - FreeRouting integration workflow tested
   - IPC standards correctly implemented
   - JLCPCB constraints verified against real designs

2. **Professional Quality**
   - Designs pass professional designer review
   - Manufacturing cost competitive with manual design
   - No design rule violations
   - Assembly compatibility verified

3. **Implementation Readiness**
   - Code is production-ready
   - Edge cases handled
   - Performance acceptable
   - Extensible for future improvements

---

**Timeline:** 4-6 weeks for comprehensive research and implementation
**Team:** 1-2 senior PCB designers + 1 software engineer
**Tools:** KiCad, FreeRouting, Python, IPC standards documents
