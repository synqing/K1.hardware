# K1 Unified Design System — Complete Index

**Everything you have. Where it is. How to use it.**

---

## Quick Navigation

### ⚡ Start Here (Pick One)

| You Want | Read This | Then Run |
|----------|-----------|----------|
| **Quick 5-min overview** | [`START_HERE_PRO.md`](START_HERE_PRO.md) | PRO plugin + orchestrator |
| **Full PRO guide** | [`K1_UNIFIED_SYSTEM_PRO.md`](K1_UNIFIED_SYSTEM_PRO.md) | PRO plugin + orchestrator |
| **Basic (no PRO features)** | [`RUN_UNIFIED_SYSTEM.md`](RUN_UNIFIED_SYSTEM.md) | Basic plugin + orchestrator |
| **Everything (this file)** | 👈 You are here | N/A |

---

## System Components

### Contracts (Source of Truth)

| File | Type | What |
|------|------|------|
| `tools/k1_project.json` | Basic | Board outline, holes, connectors, zones, stackup, netclasses, rules, DFM |
| `tools/k1_project_v2.json` | **PRO** | ☝️ + auto-decouplers, via guards, power planes, thermal vias, netclasses, testpoints |

**Recommendation:** Use `k1_project_v2.json` (PRO) for professional-grade results.

### Plugins (Apply Contract Inside KiCad)

| File | Type | What |
|------|------|------|
| `plugins/K1_ImportAndPlace.py` | Legacy | Import netlist, basic placement |
| `plugins/K1_ContractedPlace.py` | Basic | Apply contract (outline, holes, connectors, zones, keepouts) |
| `plugins/K1_ContractedPlace_PRO.py` | **PRO** | ☝️ + auto-decouplers, via guards, planes, thermal, netclasses, testpoints |

**Recommendation:** Use `K1_ContractedPlace_PRO.py` in KiCad.

### Orchestrator (Route, Validate, Export)

| File | What |
|------|------|
| `agent/orchestrator/run.py` | 7-phase pipeline: intake → route → DRC/DFM → export |
| `agent/dfm/checker.py` | DFM validator (reads contract rules) |
| `agent/drivers/kicad_cli.py` | kicad-cli wrappers (DRC, DSN/SES, exports) |
| `agent/routing/freerouting.py` | FreeRouting executor (headless router) |
| `agent/kicad/layers.py` | LSET/LSEQ helpers (SWIG binding fix) |

**Recommendation:** Use `agent/orchestrator/run.py` with `tools/k1_project_v2.json`.

---

## Documentation (Read in This Order)

### For First-Time Users

1. **[START_HERE_PRO.md](START_HERE_PRO.md)** — One-page quick start (PRO edition)
   - 4 commands to go from contract to fab pack
   - Customization examples
   - Troubleshooting

2. **[K1_UNIFIED_SYSTEM_PRO.md](K1_UNIFIED_SYSTEM_PRO.md)** — Full PRO guide
   - What PRO means (auto-decouplers, via guards, etc.)
   - 5-step workflow with timing
   - Feature deep-dives
   - PRO vs. Basic comparison

### For Integration & Reference

3. **[INTEGRATION_UNIFIED_SYSTEM.md](INTEGRATION_UNIFIED_SYSTEM.md)** — How contract + plugin + orchestrator work together
   - Architecture overview
   - Detailed workflow
   - Troubleshooting (comprehensive)
   - Advanced: extending the contract

4. **[agent/README.md](agent/README.md)** — Orchestrator documentation
   - 7-phase pipeline details
   - Architecture & modules
   - Configuration reference
   - LSET fix explanation

### For This Repo

5. **[AGENT_IMPLEMENTATION_COMPLETE.md](AGENT_IMPLEMENTATION_COMPLETE.md)** — What I (Claude Code) delivered
   - Part A (LSET fix)
   - Part B (Expert Agent, basic)
   - Integration status

6. **[K1_Agent_Contract_Addon/README.txt](K1_Agent_Contract_Addon/README.txt)** — What you (the user) delivered (basic addon)

7. **[K1_Agent_Contract_Addon_PRO/README.txt](K1_Agent_Contract_Addon_PRO/README.txt)** — What you delivered (PRO addon)

---

## The Workflow (Pick Your Path)

### Path 1: PRO (Recommended)

```
1. Read: START_HERE_PRO.md (5 min)
2. Customize: tools/k1_project_v2.json (2 min, optional)
3. Run Plugin: Tools → External Plugins → K1: Contracted Place PRO (5-10 min in KiCad)
4. Run Orchestrator: python agent/orchestrator/run.py tools/k1_project_v2.json (5-10 min)
5. Send to Fab: fabpack_out/gerbers/ + fabpack_out/drill/
```

**Total time:** ~20 minutes  
**Result:** Professional-grade PCB with auto-placed decouplers, via guards, power planes, thermal vias

### Path 2: Basic

```
1. Read: RUN_UNIFIED_SYSTEM.md (5 min)
2. Customize: tools/k1_project.json (2 min, optional)
3. Run Plugin: Tools → External Plugins → K1: Contracted Place (5-10 min in KiCad)
4. Run Orchestrator: python agent/orchestrator/run.py tools/k1_project.json (5-10 min)
5. Send to Fab: fabpack_out/gerbers/ + fabpack_out/drill/
```

**Total time:** ~20 minutes  
**Result:** Complete PCB with outline, holes, connectors, zones

### Path 3: Deep Dive

```
1. Read: K1_UNIFIED_SYSTEM_PRO.md (full guide)
2. Read: INTEGRATION_UNIFIED_SYSTEM.md (architecture)
3. Customize: tools/k1_project_v2.json (as needed)
4. Run Plugin + Orchestrator (as above)
5. Extend: Add custom rules/fields to contract
```

---

## File Tree (Complete)

```
K1.hardware/
├── tools/
│   ├── k1_project.json                         (Basic contract)
│   ├── k1_project_v2.json                      (PRO contract) ← USE THIS
│   └── freerouting.jar                         (Router executable)
│
├── plugins/
│   ├── K1_ImportAndPlace.py                    (Legacy)
│   ├── K1_ContractedPlace.py                   (Basic)
│   └── K1_ContractedPlace_PRO.py               (PRO) ← USE THIS
│
├── agent/
│   ├── orchestrator/
│   │   └── run.py                              (Orchestrator) ← RUN THIS
│   ├── drivers/
│   │   ├── kicad_cli.py                        (CLI wrappers)
│   │   └── __init__.py
│   ├── kicad/
│   │   ├── layers.py                           (LSET fix)
│   │   └── __init__.py
│   ├── routing/
│   │   ├── freerouting.py                      (Router executor)
│   │   └── __init__.py
│   ├── dfm/
│   │   ├── checker.py                          (DFM validator)
│   │   └── __init__.py
│   ├── thermal/, impedance/, configs/          (Stubs for future)
│   ├── README.md                               (Full orchestrator docs)
│   ├── QUICK_START.md                          (Quick start)
│   └── __init__.py
│
├── hardware/k1-lightwave/kicad/
│   └── K1_Lightwave.kicad_pcb                  (Board file)
│
├── fabpack_out/                                (Generated on orchestrator run)
│   ├── board.dsn, board.ses
│   ├── drc.json, manifest.json
│   ├── gerbers/
│   ├── drill/
│   ├── k1.ipc2581.xml
│   └── k1.odb
│
├── K1_Agent_Contract_Addon/                    (You delivered: basic)
│   ├── tools/k1_project.json
│   ├── plugins/K1_ContractedPlace.py
│   └── README.txt
│
├── K1_Agent_Contract_Addon_PRO/                (You delivered: PRO)
│   ├── tools/k1_project_v2.json
│   ├── plugins/K1_ContractedPlace_PRO.py
│   └── README.txt
│
├── START_HERE_PRO.md                           ⭐ START HERE (PRO)
├── RUN_UNIFIED_SYSTEM.md                       Start here (Basic)
├── K1_UNIFIED_SYSTEM_PRO.md                    Full PRO guide
├── INTEGRATION_UNIFIED_SYSTEM.md               Architecture guide
├── SYSTEM_INDEX.md                             ← You are here
├── AGENT_IMPLEMENTATION_COMPLETE.md            What Claude Code delivered
└── (other deliverables & artifacts)
```

---

## The Three-Component System (Simplified)

### 1. Design Contract

**File:** `tools/k1_project_v2.json` (PRO)

**What it defines:**
- Board: 100×70 mm, 4-layer, outline, holes, keepouts
- Connectors: USB south, LEDs north
- Components: COM-A/COM-B zones
- Stackup: layer roles, impedance targets
- Power: GND plane, 3V3/LED_5V islands
- Routing: SPI guard specs, netclass rules
- Thermal: via grids under LDOs
- Assembly: testpoints on key nets

**Edit this once.** Everything else reads from it.

### 2. PRO Plugin

**File:** `plugins/K1_ContractedPlace_PRO.py`

**What it does (inside KiCad):**
1. Reads contract
2. Draws outline + mounting holes + keepouts
3. Places USB (south) + LEDs (north)
4. Places COM-A/COM-B in zones
5. **Auto-places decouplers** ≤2.5 mm from power pins
6. **Creates GND via ring** (EMI fence)
7. **Adds SPI guard** (return-path vias)
8. **Creates power planes** (GND full, 3V3/LED_5V islands)
9. **Adds thermal vias** under regulators
10. **Creates netclasses** + assigns nets
11. **Adds testpoints** on key nets
12. Saves board

**Result:** A real PCB, ready to route.

### 3. Orchestrator

**File:** `agent/orchestrator/run.py`

**What it does (from terminal):**
- Phase 1: Verify tools, contract, board
- Phase 4: Route (DSN → FreeRouting → SES)
- Phase 5: Validate (DRC + DFM using contract rules)
- Phase 6: Export (Gerbers, Drill, IPC-2581, ODB++)
- Phase 7: Archive (manifest)

**Result:** Fab pack in `fabpack_out/`

---

## Decision Tree

**Q: Which contract should I use?**  
A: Use `tools/k1_project_v2.json` (PRO). It's richer and more powerful.

**Q: Which plugin should I use?**  
A: Use `plugins/K1_ContractedPlace_PRO.py`. It applies the full contract.

**Q: What if I don't want PRO features?**  
A: Disable in contract (e.g., `"edge_via_ring": {"enabled": false}`, `"decoupling": {"max_distance_mm": 999}`). Re-run plugin.

**Q: Do I need to understand the contract before running the plugin?**  
A: No. Plugin applies defaults. But edit the contract to customize (board size, connector edges, zones, thermal specs).

**Q: What if FreeRouting times out?**  
A: Increase `routing.freerouting.timeout_s` in contract (default 1800 = 30 min), or route manually in GUI, export SES, re-run.

**Q: Can I version-control the contract?**  
A: Yes. `tools/k1_project_v2.json` is the source of truth. Commit it to git.

**Q: Will the same contract always produce the same board?**  
A: Yes. Deterministic, repeatable.

---

## Checklists

### Before Running Plugin

- [ ] `tools/k1_project_v2.json` exists
- [ ] `plugins/K1_ContractedPlace_PRO.py` exists
- [ ] Board file loads in KiCad
- [ ] Contract is valid JSON (`python -m json.tool tools/k1_project_v2.json` ≥ 0 errors)

### Before Running Orchestrator

- [ ] Plugin has run (board has outline, holes, connectors, etc.)
- [ ] `kicad-cli` is in PATH (`which kicad-cli`)
- [ ] FreeRouting JAR exists (`ls tools/freerouting.jar`)
- [ ] Contract is still valid JSON
- [ ] Board file is not locked in KiCad

### After Running Orchestrator

- [ ] `fabpack_out/` directory exists
- [ ] `drc.json` shows zero violations
- [ ] `gerbers/` has Gerber files (*.gbr)
- [ ] `drill/` has drill file (*.xln)
- [ ] `k1.ipc2581.xml` and `k1.odb` exist
- [ ] `manifest.json` is readable

---

## Glossary

| Term | Meaning |
|------|---------|
| **Contract** | JSON file that defines all board decisions (dims, zones, stackup, rules, etc.) |
| **Plugin** | KiCad Action Plugin that reads contract and applies it to the board |
| **Orchestrator** | Python script that routes, validates, exports (runs outside KiCad) |
| **DSN** | Specctra Design Netlist (routing format export) |
| **SES** | Specctra Session (routing result import) |
| **DRC** | Design Rule Check (violation report) |
| **DFM** | Design for Manufacturing (fab capability validation) |
| **Netclass** | Network class (design rule set assigned to nets) |
| **LSET** | Layer set (KiCad term for which layers a feature uses) |
| **Via guard** | Stitching vias that constrain return path (SPI example) |
| **Via ring** | Ring of vias around perimeter for EMI containment |
| **Decoupler** | Capacitor placed near IC power pin for noise filtering |
| **Thermal via grid** | Array of vias under hot parts for heat spreading |
| **Testpoint** | Pad for oscilloscope probe connection |

---

## Support & Resources

| Question | Where to Find Answer |
|----------|---------------------|
| "How do I run the PRO plugin?" | [START_HERE_PRO.md](START_HERE_PRO.md) |
| "What does PRO add?" | [K1_UNIFIED_SYSTEM_PRO.md](K1_UNIFIED_SYSTEM_PRO.md) → PRO Features section |
| "How do I customize the contract?" | [K1_UNIFIED_SYSTEM_PRO.md](K1_UNIFIED_SYSTEM_PRO.md) → Customization Guide |
| "What do the 7 phases do?" | [agent/README.md](agent/README.md) → Detailed Workflow |
| "How does the LSET fix work?" | [agent/kicad/layers.py](agent/kicad/layers.py) (well-documented) |
| "What's in the contract schema?" | See `tools/k1_project_v2.json` (fully commented) |
| "How do I troubleshoot?" | [INTEGRATION_UNIFIED_SYSTEM.md](INTEGRATION_UNIFIED_SYSTEM.md) → Troubleshooting |
| "What are the plugin limitations?" | [K1_UNIFIED_SYSTEM_PRO.md](K1_UNIFIED_SYSTEM_PRO.md) → Limitations & Guards |

---

## Version History

| Date | Version | What |
|------|---------|------|
| 2025-10-24 | 1.0 (Basic) | Contract + basic plugin + orchestrator |
| 2025-10-24 | 2.0 (PRO) | ☝️ + auto-decouplers, via guards, planes, thermal, netclasses, testpoints |
| 2025-10-24 | 2.0.1 (Current) | Unified integration + comprehensive docs + this index |

---

## Summary

You have a **professional PCB design system** that:

✓ **Asks** the right questions upfront (via contract)  
✓ **Encodes** answers in machine-readable JSON  
✓ **Enforces** mechanically (plugin + orchestrator)  
✓ **Produces** deterministic, reproducible PCBs  
✓ **Fails hard** on errors (no silent garbage)  
✓ **Documents** everything (this index, guides, inline comments)  

**Not guessing. Not hand-placing. Not hoping.**

Just: Edit contract → run plugin → run orchestrator → fab pack ready.

---

## Next Steps

1. **Read:** [START_HERE_PRO.md](START_HERE_PRO.md) (5 min)
2. **Run:** Plugin + orchestrator (20 min)
3. **Send to fab:** (30 min)

Done. 🎉

---

**Last Updated:** 2025-10-24  
**Status:** ✓ Complete & Ready
