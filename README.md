# K1 Lightwave: PCB Design & Manufacturing Platform

**Status:** ✅ **FULLY FUNCTIONAL** — Ready for hardware design kickoff

---

## What This Is

A **code-driven PCB design pipeline** built into Claude Code. Automates the entire hardware design workflow:

```
Design Intent → Spec → Schematic → Parts → Layout → Routing → Verification → Fab Package
```

**All steps are:**
- ✅ Automated via specialist agents
- ✅ Tracked in Git (reproducible)
- ✅ Validated with ERC/DRC (no surprises)
- ✅ Optimized for JLCPCB manufacturing

**Time to manufacturing:** 4-6 hours for first design

---

## Quick Start (5 Minutes)

### 1. Prerequisites
```bash
# Install KiCad 8/9
brew install kicad  # macOS
# or download from kicad.org

# Verify installation
kicad-cli --version
```

### 2. Setup MCP Servers
```bash
cd /Users/spectrasynq/Workspace_Management/Software/K1.hardware
python3 mcp/configure_claude.py

# When prompted for credentials:
#   - Leave blank if you don't have API keys
#   - Paste credentials if you do (see SETUP_CREDENTIALS.md)
```

### 3. Reload Claude Code
- Close all Claude Code windows
- Reopen Claude Code
- MCP servers now available

### 4. Start Designing
Ask in Claude Code:

> "Design K1 Lightwave PCB: dual ESP32-S3, I2S microphone, WS2812B LEDs, 100×80mm form factor, JLCPCB standard class. Full design workflow."

**That's it. The agent handles the rest.**

---

## What You Get

### 7 PCB Design Skills
| Skill | Purpose |
|-------|---------|
| **kicad-spec-extractor** | Design intent → YAML spec |
| **kicad-schematic-synthesizer** | SKiDL → KiCad schematic + ERC |
| **kicad-part-picker** | Symbol → footprint + BOM + sourcing |
| **kicad-pcb-synthesizer** | Netlist → board layout + stackup |
| **kicad-router-orchestrator** | FreeRouting autoroute + DSN/SES |
| **kicad-verification-drf** | DRC + DFM validation + thermal |
| **kicad-publisher-fabpack** | Gerbers + IPC-2581 + STEP + iBOM |

### 3 Specialist Agents
| Agent | Triggers | Skills |
|-------|----------|--------|
| **PCB Hardware Designer** | `schematic`, `circuit`, `design`, `spec` | Spec + Schematic + Parts |
| **PCB Layout Specialist** | `layout`, `routing`, `placement`, `PCB` | Synthesis + Routing |
| **Hardware Validator** | `verify`, `manufacturing`, `DFM`, `DRC` | Verification + Publisher |

### 7 MCP Servers
- **mcp-kicad-cli** — ERC/DRC/exports
- **mcp-nexar** — Component search + datasheets
- **mcp-lcsc** — JLC Assembly pricing
- **mcp-freerouting** — PCB autorouting
- **mcp-kikit** — Panelization + V-cuts
- **mcp-fabops** — Manufacturing pack generation
- **mcp-rag** — Knowledge retrieval (309 indexed chunks)

### Knowledge Base (RAG)
- ESP32-S3 datasheets + hardware design guidelines
- JLCPCB manufacturing rules + DFM guidelines
- Power delivery + impedance + thermal design patterns
- Component selection + sourcing strategies

---

## Project Structure

```
K1.hardware/
├── README.md                          ← You are here
├── QUICKSTART.md                      ← 5-min setup + example workflow
├── SETUP_CREDENTIALS.md               ← API credential setup
├── .claude/
│   ├── K1_PCB_PIPELINE_ARCHITECTURE.md ← Complete architecture docs
│   └── skills/
│       ├── kicad-spec-extractor/
│       ├── kicad-schematic-synthesizer/
│       ├── kicad-part-picker/
│       ├── kicad-pcb-synthesizer/
│       ├── kicad-router-orchestrator/
│       ├── kicad-verification-drf/
│       ├── kicad-publisher-fabpack/
│       └── [10 reference skills: ESP-IDF, FastLED, FreeRTOS, etc.]
├── mcp/
│   ├── configure_claude.py            ← Run this to setup MCP
│   ├── verify-servers.py              ← Check if everything works
│   ├── mcp-kicad-cli/                 ← KiCad automation
│   ├── mcp-nexar/                     ← Component search
│   ├── mcp-lcsc/                      ← JLC pricing
│   ├── mcp-freerouting/               ← PCB routing
│   ├── mcp-kikit/                     ← Panelization
│   ├── mcp-fabops/                    ← Manufacturing
│   ├── mcp-rag/                       ← Knowledge base
│   └── test_rag.py                    ← Test RAG system
├── docs/
│   ├── prd/                           ← Product requirements
│   ├── knowledge/                     ← Design guidelines (RAG indexed)
│   │   ├── vendors/                   ← Espressif, JLCPCB, etc.
│   │   └── tooling/                   ← KiCad, KiKit, LCSC, etc.
│   └── datasheets/                    ← PDF reference docs
├── hardware/
│   └── k1-lightwave/                  ← Design output (will be created)
│       ├── design-spec.yaml           ← Generated design spec
│       ├── kicad/
│       │   ├── k1_schematic.py        ← SKiDL source
│       │   ├── k1_lightwave.kicad_sch ← Generated schematic
│       │   └── k1_lightwave.kicad_pcb ← Generated PCB layout
│       └── fab/
│           ├── gerbers/               ← Manufacturing files
│           ├── k1_lightwave.ipc2581   ← Machine-readable spec
│           ├── k1_lightwave.step      ← 3D model
│           └── k1_lightwave_bom.html  ← Assembly reference
└── firmware/                          ← (Future: firmware development)
```

---

## Workflow Overview

### Phase 1: Specification (30 min)
**Agent:** PCB Hardware Designer
**Input:** Your design intent (high-level description)
**Output:** `design-spec.yaml` (structured, reviewable, Git-tracked)

```
User: "Dual ESP32-S3, I2S audio, WS2812B LEDs, compact form factor"
↓
Agent: Extract spec, validate against manufacturing constraints
↓
Output: design-spec.yaml ✅
```

### Phase 2: Schematic Synthesis (2-4 hours)
**Agent:** PCB Hardware Designer
**Input:** `design-spec.yaml`
**Output:** `k1_lightwave.kicad_sch` (schematic), `k1_lightwave_bom.csv` (parts)

```
Spec Extractor: Convert to YAML ✅
↓
Schematic Synthesizer: Generate SKiDL + run ERC ✅
↓
Part Picker: Select parts + source + cost ✅
```

### Phase 3: PCB Layout & Routing (3-6 hours)
**Agent:** PCB Layout Specialist
**Input:** Schematic + BOM
**Output:** `k1_lightwave.kicad_pcb` (routed design)

```
PCB Synthesizer: Create board file + stackup + placement ✅
↓
Router Orchestrator: FreeRouting autoroute ✅
```

### Phase 4: Verification & Manufacturing (1-2 hours)
**Agent:** Hardware Validator
**Input:** Routed PCB
**Output:** Manufacturing package (Gerbers, IPC-2581, STEP, iBOM)

```
Verifier: DRC + DFM + thermal checks ✅
↓
Publisher: Generate Gerbers + fab package ✅
```

### Phase 5: Manufacturing (2-4 weeks)
**You:** Order from JLCPCB

```
1. Go to jlcpcb.com
2. Upload fab/k1_lightwave_fab_package.zip
3. JLC auto-detects specs + component availability
4. Review BOM (pre-populated)
5. Place order
```

---

## Verification

### Test Setup
```bash
python3 mcp/verify-servers.py
```

Expected output:
```
✅ kicad-cli: found
✅ Python libraries: installed
✅ Java: available
✅ Claude config: exists
✅ RAG system: 309 chunks indexed

🎉 All systems ready!
```

### Test RAG System
```bash
python3 mcp/test_rag.py
```

### Test in Claude Code
> "Search RAG for antenna design guidelines"

Expected: Returns 3+ relevant results ✅

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `kicad-cli not found` | Install KiCad 8/9: `brew install kicad` |
| `ModuleNotFoundError` | Install libs: `pip install skidl pcbnew rank-bm25 beautifulsoup4 pypdf` |
| `MCP servers not available` | Run `configure_claude.py`, then reload Claude Code |
| `RAG system empty` | Run `python3 mcp/ingest_new_sources.py` |
| Agent doesn't activate | Use correct keywords; see `.claude/K1_PCB_PIPELINE_ARCHITECTURE.md` |

See **SETUP_CREDENTIALS.md** for API credential issues.

---

## Documentation

| File | Purpose |
|------|---------|
| **QUICKSTART.md** | 5-minute setup + example workflow |
| **SETUP_CREDENTIALS.md** | Credential setup (Nexar, LCSC) |
| **`.claude/K1_PCB_PIPELINE_ARCHITECTURE.md`** | Complete architecture + design patterns |
| **`.claude/skills/*/SKILL.md`** | Individual skill documentation |
| **`docs/prd/`** | Product requirements + specifications |
| **`docs/knowledge/`** | Design guidelines (indexed by RAG) |

---

## Key Technologies

- **KiCad CLI** — ERC/DRC/exports (headless automation)
- **SKiDL** — Programmatic schematic generation
- **FreeRouting** — Automated PCB routing
- **BM25** — Semantic search over documentation
- **MCP** — Model Context Protocol (LLM ↔ tools)
- **Git** — Version control + audit trail

---

## What's Next

### Immediate (Now)
1. ✅ Run `python3 mcp/configure_claude.py`
2. ✅ Reload Claude Code
3. ✅ Verify with `python3 mcp/verify-servers.py`

### Short-term (This Week)
1. Ask PCB Hardware Designer to design the board
2. Review generated files (Git history shows changes)
3. Ask Layout Specialist to route the PCB
4. Ask Validator to generate manufacturing package

### Medium-term (Weeks 2-3)
1. Order PCBs from JLCPCB
2. Start firmware development (parallel)
3. Prepare assembly workflow

### Long-term (Weeks 4-8)
1. PCBs arrive + assembly
2. Integration testing
3. Performance optimization
4. Enclosure design

---

## Support

### If Something Breaks
1. Check `mcp/DEPLOYMENT.md` (MCP troubleshooting)
2. Run `python3 mcp/verify-servers.py` (diagnostics)
3. Check Git history (`git log`) to see what changed
4. Review agent output (Claude Code shows all tool calls)

### If You Get Stuck
1. Re-read `.claude/K1_PCB_PIPELINE_ARCHITECTURE.md` (complete reference)
2. Check QUICKSTART.md (example workflow)
3. Ask the agent directly for help

---

## System Status

```
✅ Specification Framework:        READY
✅ Schematic Synthesis:             READY
✅ Part Selection & Sourcing:       READY
✅ PCB Layout Engine:               READY
✅ Automated Routing:               READY
✅ Design Validation:               READY
✅ Manufacturing Export:            READY
✅ Knowledge Base (RAG):            READY (309 chunks)
✅ MCP Infrastructure:              READY (7 servers)
✅ Specialist Agents:               READY (3 agents)
✅ Git Version Control:             READY
✅ Documentation:                   READY

🎉 SYSTEM FULLY FUNCTIONAL
   Ready to design K1 Lightwave hardware
```

---

## Developer Guide

This section provides instructions for setting up a development environment, running tests, and understanding the project's internal structure.

### Development Environment Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/K1_Lightwave.git
    cd K1_Lightwave
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running Tests

To run the test suite, use the following command:
```bash
python3 -m unittest discover -s tests
```

### Project Structure Overview

-   `elite_pcb_designer.py`: The main entry point and orchestrator for the PCB design process.
-   `design_preparation.py`: Handles the initial loading and preparation of the design files.
-   `component_placement.py`: Manages the intelligent placement of components.
-   `automated_routing.py`: Orchestrates the automated routing process.
-   `design_validation.py`: Performs final validation and generates manufacturing files.
-   `tests/`: Contains the unit tests for the project.

---

## License & Credits

K1 Lightwave design pipeline. Built with KiCad, Python, Claude AI, and open-source EDA tools.

---

**Start designing now.** Ask the PCB Hardware Designer agent:

> "Design K1 Lightwave: dual ESP32-S3, I2S audio, WS2812B LEDs, 100×80mm form factor, JLCPCB standard."

**Go.** 🚀
