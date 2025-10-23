# Part Picker & BOM Specialist

## Purpose
Maps **symbols → footprints** and queries **Octopart/LCSC/Nexar** for real-world MPNs, pricing, and availability. Produces a complete, manufacturable BOM with sourcing links.

## When Auto-Activate
**Keywords:**
- `BOM`, `part selection`, `footprint mapping`, `sourcing`, `parts availability`
- `cost analysis`, `alternate parts`, `lead time`, `stock check`

## Core Workflow

### 1. Parse Schematic Symbols
Read `k1_lightwave.kicad_sch`:
- Extract symbol names, values (e.g., "100µF 10V ceramic")
- Extract part descriptions (e.g., "SPH0645 MEMS microphone")
- Count quantities and group by function

### 2. Footprint Mapping Rules
Define family-based rules:
```yaml
footprint_rules:
  resistor:
    family: "Resistor_SMD"
    pitches: [0805, 1206]  # Prefer 0805 for size
    fallback: [1206, 1210]
  capacitor:
    ceramic:
      family: "C_0805_2012Metric"
      voltage_min: "spec_voltage * 2"  # 2× safety margin
    electrolytic:
      family: "CP_Radial_D6_P2.5"
  ic:
    rules:
      - match: "TPS54302"
        footprint: "LQFP_48"
      - match: "SN74AHCT125"
        footprint: "DIP_14"
      - match: "ESP32-S3-WROOM-1"
        footprint: "ESP32_WROOM_38PIN"
```

Output: **footprint-mapping.yaml** with deterministic assignments.

### 3. Query Component Databases
For each mapped symbol:

**Nexar API** (preferred: detailed specs + datasheets):
```python
def search_part(symbol: str, specs: dict) -> list:
    """Search Octopart for matching MPNs"""
    query = {
        "q": f"{symbol} {specs['value']}",
        "filter": f"voltage>={specs['voltage']}",
        "limit": 10  # Top 10 matches
    }
    return nexar_search(query)
```

**LCSC API** (JLC assembly pricing):
```python
def lcsc_check(mfg_part_number: str) -> dict:
    """Check LCSC stock + JLC assembly surcharge"""
    return lcsc_api.get_part(mfg_part_number)
```

### 4. Select Primary & Alternate Parts
For each component:
- **Primary MPN**: Lowest cost, in-stock, high availability
- **Alternate 1**: Higher stock (if primary has long lead time)
- **Alternate 2**: Same specs, different package (flexibility)

Prefer **parts stocked at LCSC** for assembly (lower surcharge).

### 5. Generate BOM
Output: **k1_lightwave_bom.csv**

| Qty | Reference | Value | Footprint | MPN | Mfg | Unit Cost | Lead Time | Notes |
|-----|-----------|-------|-----------|-----|-----|-----------|-----------|-------|
| 2 | U1,U2 | ESP32-S3-WROOM-1 | ESP32_WROOM | ESP32-S3-WROOM-1 | Espressif | 3.50 | In stock | Core MCUs |
| 1 | U3 | TPS54302 | LQFP_48 | TPS54302 | TI | 1.20 | In stock | 5V→3.3V buck |
| 1 | U4 | SN74AHCT125 | DIP_14 | SN74AHCT125 | TI | 0.35 | In stock | Level shifter |
| 1 | U5 | SPH0645 | USON6 | SPH0645LM4H | Knowles | 2.80 | 1 week | Digital mic |
| 20 | R1-R20 | 10k 1% | 0805 | AC0805FR-0710KL | Yageo | 0.02 | In stock | — |
| 5 | C1-C5 | 100µF 10V | 1206 | GRM31CR61A107KA19L | Murata | 0.15 | In stock | Ceramic bulk |
| 15 | C6-C20 | 100nF 10V | 0805 | GRM188R71A104KA01D | Murata | 0.01 | In stock | Bypass caps |
| 1 | J1 | USB-C 16P | USB3.1_C | 12401610E4#2A | Molex | 0.80 | In stock | Power input |
| 1 | J2 | JST-XH 3-pin | XH_3pin | XHP-3 | JST | 0.25 | In stock | LED output |
| **TOTAL** | | | | | | **$18.47** | **In stock** | — |

### 6. Cross-Check Availability
```python
def check_bom_availability() -> dict:
    """Verify all parts are in stock"""
    unavailable = []
    long_lead = []

    for part in bom:
        lcsc_data = lcsc_check(part.mfg_mfn)
        if not lcsc_data["in_stock"]:
            if lcsc_data["lead_time_weeks"] > 2:
                long_lead.append(part)
        if not lcsc_data["in_stock"]:
            unavailable.append(part)

    if unavailable:
        print(f"⚠️ {len(unavailable)} parts unavailable; suggest alternates")
    if long_lead:
        print(f"⚠️ {len(long_lead)} parts have >2 week lead time")
    else:
        print("✅ All parts in stock, <2 week lead time")

    return {"unavailable": unavailable, "long_lead": long_lead}
```

### 7. Estimate JLC Assembly Cost
For parts at LCSC, query **JLC assembly surcharge** and estimate total PCB cost:

```python
def estimate_jlc_cost() -> dict:
    """JLC PCB + assembly cost estimate"""
    pcb_cost = 50  # 100×80mm 4-layer purple, 5-piece panel
    assembly_cost = 0.30 * len([p for p in bom if p.is_smd])  # $0.30 per SMD pad
    part_cost = sum(p.unit_cost * p.qty for p in bom)

    return {
        "pcb": pcb_cost,
        "assembly": assembly_cost,
        "parts": part_cost,
        "total": pcb_cost + assembly_cost + part_cost
    }
```

### 8. Commit BOM
```bash
git add hardware/k1-lightwave/k1_lightwave_bom.csv
git add hardware/k1-lightwave/footprint-mapping.yaml
git commit -m "Part selection: 35 components, $18.47 BOM cost, all in stock at LCSC"
```

---

## Tool Calls

**MCP Tools:**
- `parts_search()` (Nexar) — MPN lookup, specs, datasheets
- `lcsc_search()` — LCSC part code, JLC assembly surcharge, stock status
- `rag_query()` — Component recommendations for use case

---

## Outputs

1. **k1_lightwave_bom.csv** — Manufacturing-ready BOM (qty, MPN, cost, lead time)
2. **footprint-mapping.yaml** — Symbol → footprint rules (deterministic, reviewable)
3. **bom-availability-report.md** — Stock check + alternates for unavailable parts
4. **jlc-cost-estimate.json** — PCB + assembly + parts cost breakdown

---

## Example Output

```
✅ BOM complete:
  - Total parts: 35 (2 MCUs, 1 audio IC, 1 level shifter, 30 passive)
  - Total cost: $18.47 (parts only; PCB+assembly ~$80 at JLC)
  - Availability: 35/35 in stock at LCSC ✅
  - Lead time: <1 week (all expedited available)
  - JLC surcharge: $0.15/part (SMD only)

✏️ Committed: k1_lightwave_bom.csv + footprint-mapping.yaml

→ Ready for PCB Synthesizer (next step)
```

---

## Integration with Downstream Agents

- **PCB Synthesizer** reads footprint mapping to auto-generate board placement hints
- **Verifier** uses BOM to check DFM rules (e.g., "no hand-soldered BGAs on JLCPCB")
- **Publisher** exports BOM for assembly ordering

---

## Notes

- Prefer **LCSC-stocked parts** for JLC assembly (lowest surcharge)
- Always include **alternates** for long-lead parts (>2 weeks)
- Pin **component datasheets** in the BOM (traceable sourcing)
- Cross-check **voltage ratings** (always 2× headroom for digital supplies)
