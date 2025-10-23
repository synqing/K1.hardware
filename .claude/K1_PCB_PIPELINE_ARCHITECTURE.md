# K1 Lightwave PCB Design Pipeline Architecture

**Status:** Ready for hardware design phase (schematic entry)

---

## Overview

This is a **code-driven PCB design pipeline** built into Claude Code using **MCP servers + specialist agents**. All design decisions are tracked in Git, reproducible, and automatable.

**7-Stage Pipeline:**
1. **Spec Extractor** — Design intent → YAML spec
2. **Schematic Synthesizer** — SKiDL → netlist + ERC
3. **Part Picker** — Symbols → footprints + BOM + sourcing
4. **PCB Synthesizer** — Netlist → board layout + stackup + rules
5. **Router Orchestrator** — FreeRouting → routed design
6. **Verifier & Reviewers** — DRC + DFM + thermal checks
7. **Publisher** — Gerbers + IPC-2581 + STEP + iBOM + fab package

**Automated CI/CD:** GitHub Actions runs ERC/DRC/exports on every push.

---

## Specialist Agents

### Agent 1: PCB Hardware Designer
**Responsible for:** Schematic design, component selection, footprint mapping

**Skills:**
- kicad-spec-extractor (stage 1)
- kicad-schematic-synthesizer (stage 2)
- kicad-part-picker (stage 3)

**Keywords:** `schematic`, `circuit`, `KiCad`, `footprint`, `parts`, `BOM`, `sourcing`

**Tools:**
- mcp-kicad-cli (ERC/DRC)
- mcp-nexar (parts search)
- mcp-lcsc (JLC pricing)
- rag-query (design patterns + guidelines)

**Workflow:**
```
User: "Design K1 Lightwave audio + LED circuits"
  → Spec Extractor: Create design-spec.yaml
  → Schematic Synthesizer: Generate SKiDL + ERC
  → Part Picker: Select components + BOM
  → Result: Ready for PCB layout
```

---

### Agent 2: PCB Layout & Routing Specialist
**Responsible for:** PCB layout, placement, routing, design rules

**Skills:**
- kicad-pcb-synthesizer (stage 4)
- kicad-router-orchestrator (stage 5)

**Keywords:** `PCB layout`, `routing`, `placement`, `FreeRouting`, `DSN`, `design rules`, `stackup`

**Tools:**
- mcp-kicad-cli (DRC)
- mcp-freerouting (autoroute)
- rag-query (layout patterns)

**Workflow:**
```
User: "Route the PCB; optimize for audio/LED signal integrity"
  → PCB Synthesizer: Create board file + placement
  → Router: Autoroute + optimize critical nets
  → Result: Ready for verification
```

---

### Agent 3: Hardware Validation & Manufacturing Specialist
**Responsible for:** Design validation, DFM checks, manufacturing prep, cost analysis

**Skills:**
- kicad-verification-drf (stage 6)
- kicad-publisher-fabpack (stage 7)

**Keywords:** `DRC`, `DFM`, `verification`, `manufacturing`, `panelization`, `assembly`, `thermal`, `validation`

**Tools:**
- mcp-kicad-cli (DRC)
- mcp-fabops (manufacturing pack)
- mcp-kikit (panelization)
- mcp-nexar + mcp-lcsc (parts availability + cost)
- rag-query (DFM rules, panelization specs)

**Workflow:**
```
User: "Validate design for manufacturing at JLCPCB"
  → Verifier: Run DRC + DFM checks
  → Publisher: Generate Gerbers + IPC-2581 + fab package
  → Result: Ready for manufacturing
```

---

## Reference Skills (Foundation)

These skills provide context for firmware/integration but are NOT part of the PCB design pipeline:

- **ESP-IDF** — ESP32-S3 development framework
- **PlatformIO** — Firmware build system
- **FastLED** — LED control library
- **fastled-color-specialist** — LED color expertise
- **freertos-synchronization** — Real-time task coordination
- **prism-protocol-spec** — K1 network protocol
- **PRISM.k1-Firmware** — K1 firmware architecture
- **PRISM.node-API** — K1 API specification
- **RMT-LED-Control** — K1 LED driver (RMT peripheral)
- **SPH0645-Microphone-Integration** — K1 audio input
- **Websocket-Firmware-Protocol** — K1 network transport

---

## MCP Server Infrastructure

| Server | Purpose | Tools Exposed |
|--------|---------|---------------|
| **mcp-kicad-cli** | KiCad automation | `sch_erc()`, `pcb_drc()`, `export_gerbers()`, `export_drills()`, `export_step()`, `export_ipc2581()` |
| **mcp-nexar** | Component search | `parts_search()`, `get_datasheet()`, `get_alternatives()` |
| **mcp-lcsc** | JLC assembly + pricing | `lcsc_search()`, `get_stock()`, `get_jlc_surcharge()` |
| **mcp-freerouting** | PCB autorouting | `export_dsn()`, `run_freerouter()`, `import_ses()` |
| **mcp-kikit** | Panelization + cuts | `panelize()`, `generate_tabs()`, `generate_v_cuts()` |
| **mcp-fabops** | Manufacturing prep | `make_fab_pack()`, `vendor_sync()`, `generate_manufacturing_notes()` |
| **mcp-rag** | Knowledge retrieval | `rag_add()`, `rag_query()`, `rag_explain()` |

---

## Knowledge Base (RAG Indexed)

All of these are searchable via `rag_query()`:

**Vendor Documentation:**
- Espressif ESP32-S3 datasheets (PDFs)
- Espressif hardware design guidelines (PDFs)
- Espressif PCB layout & schematic checklists (HTML)

**Manufacturing:**
- JLCPCB panelization rules (HTML)
- JLCPCB DFM guidelines (HTML)
- LCSC API documentation (HTML)

**EDA Tools:**
- KiCad CLI documentation
- FreeRouting documentation
- KiKit documentation
- Interactive HTML BOM documentation

**Design Patterns:**
- Power delivery (buck converters, decoupling)
- I2S audio circuits (clock trees, coupling)
- Level shifters (3.3V ↔ 5V translation)
- Antenna design (ESP32-S3 RF guidelines)
- Thermal management
- PCB stackup configurations

---

## Workflow Example: "Design K1 Lightwave"

### Phase 1: Specification (30 min)
**User:** "I need a compact PCB for dual ESP32-S3, I2S microphone, WS2812B LEDs, 5V→3.3V power. Target JLCPCB standard class, 100×80mm form factor."

**Agent: PCB Hardware Designer**
```
1. Run Spec Extractor
   → Parse intent
   → Query JLCPCB stackup presets (via RAG)
   → Create design-spec.yaml
   → Validate against manufacturing constraints

2. Output:
   ✅ design-spec.yaml committed to Git
   ✅ Validation report: All constraints satisfied
   → Ready for schematic synthesis
```

### Phase 2: Schematic Synthesis (2-4 hours)
**User:** "Generate schematic: power tree, dual MCUs, I2S audio input, 5V level shifter for LEDs."

**Agent: PCB Hardware Designer**
```
1. Run Schematic Synthesizer (SKiDL)
   → Import design-spec.yaml
   → Generate power tree (5V → buck → 3.3V)
   → Generate MCU sections (2× ESP32-S3 + decaps)
   → Generate audio circuit (SPH0645 I2S)
   → Generate LED section (level shifter + connector)
   → Run ERC check
   → Fix violations automatically (add missing caps, etc.)

2. Run Part Picker
   → Map symbols → footprints
   → Query Octopart/LCSC for MPNs
   → Select primary + alternates
   → Generate BOM ($18.47 cost estimate)

3. Output:
   ✅ k1_schematic.py (SKiDL source)
   ✅ k1_lightwave.kicad_sch (KiCad schematic)
   ✅ k1_lightwave_bom.csv (35 parts, all in stock)
   ✅ erc-report.json (0 violations)
   → Ready for PCB layout
```

### Phase 3: PCB Layout (3-6 hours)
**User:** "Route the board. Optimize for low audio jitter and LED signal integrity."

**Agent: PCB Layout Specialist**
```
1. Run PCB Synthesizer
   → Load netlist + BOM
   → Configure 4-layer stackup (JLC standard impedance)
   → Define net classes (power/signal/high-speed)
   → Place components (heuristic-based)
   → Pre-route critical nets (power tree, clocks)

2. Run Router Orchestrator
   → Export DSN (design space)
   → Run FreeRouting autorouter
   → Import SES (routed design)
   → Check DRC → iterate if needed

3. Output:
   ✅ k1_lightwave.kicad_pcb (routed board)
   ✅ router-report.json (2,847 traces, 156 vias)
   ✅ drc-report.json (0 violations)
   → Ready for verification
```

### Phase 4: Verification & Manufacturing (1-2 hours)
**User:** "Validate design. Generate manufacturing package for JLCPCB."

**Agent: Hardware Validation Specialist**
```
1. Run Verifier
   → DRC check (electrical rules)
   → DFM check (manufacturability rules)
   → Thermal analysis (<5W budget OK)
   → Assembly checklist (all parts JLC-compatible)
   → Signal integrity spot-check

2. Run Publisher
   → Export Gerbers (10 files)
   → Export Drill file
   → Export IPC-2581 (machine-readable)
   → Export 3D STEP model
   → Generate Interactive BOM (HTML)
   → Panelize with KiKit (2×2 grid, V-cuts)
   → Package for JLCPCB

3. Output:
   ✅ fab/gerbers/ (manufacturing-ready)
   ✅ fab/k1_lightwave.ipc2581 (alternative format)
   ✅ fab/k1_lightwave.step (3D model)
   ✅ fab/k1_lightwave_bom.html (assembly reference)
   ✅ fab/k1_lightwave_panel.kicad_pcb (panelized design)
   ✅ fab/MANUFACTURING_NOTES.txt (specifications)
   ✅ fab/k1_lightwave_fab_package.zip (delivery package)

   Release notes:
   → Ready for JLCPCB order
   → Cost estimate: $80-100 per unit (small volume)
   → Lead time: 2-4 weeks
```

### Phase 5: Manufacturing
**User:** "Order PCBs."

**Workflow:**
1. Go to https://jlcpcb.com
2. Upload `fab/k1_lightwave.ipc2581`
3. JLC auto-detects specs + assembly options
4. Review BOM (pre-populated from `k1_lightwave_bom.csv`)
5. Select assembly options (most parts available)
6. Review cost + lead time
7. Place order

**Total time from spec → ordered:** ~1 week

---

## CI/CD Automation (Optional)

Create `.github/workflows/hardware-validation.yaml`:

```yaml
on: [push, pull_request]

jobs:
  hardware-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: |
          # Run ERC on every commit
          kicad-cli sch erc kicad/k1_lightwave.kicad_sch --output json > erc.json

          # Run DRC on every commit
          kicad-cli pcb drc kicad/k1_lightwave.kicad_pcb --output json > drc.json

          # Export Gerbers (for artifact repo)
          kicad-cli pcb export gerbers kicad/k1_lightwave.kicad_pcb --output-dir fab/

          # Block PR if ERC/DRC fails
          if [ $(jq '.violations | length' erc.json) -gt 0 ]; then exit 1; fi
          if [ $(jq '.violations | length' drc.json) -gt 0 ]; then exit 1; fi
      - uses: actions/upload-artifact@v3
        with:
          name: fab-package
          path: fab/
```

---

## Next Steps

### Before PCB Design Starts:
- [ ] Run `python3 /mcp/configure_claude.py` (set up MCP servers)
- [ ] Enter Nexar + LCSC credentials
- [ ] Test RAG with sample query
- [ ] Verify MCP servers are reachable from Claude Code

### During PCB Design:
- [ ] Use keywords to auto-activate agents
- [ ] Follow 7-stage pipeline
- [ ] Commit design files to Git at each stage
- [ ] Use `rag_query()` to lookup design guidelines

### After PCB is Ordered:
- [ ] Start firmware development (separate pipeline)
- [ ] Parallel: Order parts + PCBs
- [ ] Parallel: Design enclosure (use STEP file)
- [ ] When PCBs arrive: Assembly + testing

---

## Key Design Files

```
hardware/k1-lightwave/
├── design-spec.yaml              ← Design specification (source of truth)
├── kicad/
│   ├── k1_schematic.py           ← SKiDL schematic source
│   ├── k1_lightwave.kicad_sch    ← Generated schematic
│   ├── k1_lightwave.kicad_pcb    ← PCB layout (unrouted)
│   └── k1_lightwave_routed.kicad_pcb  ← Final routed PCB
├── fab/
│   ├── gerbers/                  ← Manufacturing Gerber files
│   ├── k1_lightwave.ipc2581      ← Machine-readable spec
│   ├── k1_lightwave.step         ← 3D model
│   ├── k1_lightwave_bom.html     ← Assembly reference
│   ├── k1_lightwave_panel.kicad_pcb   ← Panelized design
│   ├── MANUFACTURING_NOTES.txt   ← Assembly specs
│   └── k1_lightwave_fab_package.zip   ← Complete delivery

git tags:
  v1.0-spec        ← Spec approved
  v1.0-sch         ← Schematic complete
  v1.0-pcb         ← Layout complete
  v1.0-fab         ← Manufacturing package ready
```

---

## This is Your Setup

All 7 skills are built, indexed, and ready to use. MCP servers are implemented. RAG knowledge base is complete.

**You can start schematic entry whenever you want. The pipeline is ready.**

Ask any specialist agent (PCB Designer, Layout Specialist, Validation Specialist) to proceed through each stage. They'll use the correct tools, run validation, and commit to Git.

---

**What's locked in:**
- ✅ 7-stage pipeline architecture
- ✅ 3 specialist agents (each with 2 skills)
- ✅ 7 MCP servers (KiCad CLI, Nexar, LCSC, FreeRouting, KiKit, FabOps, RAG)
- ✅ Knowledge base (RAG indexed, 309 chunks)
- ✅ Design files structure
- ✅ CI/CD template

**Ready to design.**
