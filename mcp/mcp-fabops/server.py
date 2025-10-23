#!/usr/bin/env python3
"""
MCP 'fabops' server — Fabrication Operations
Two powerful composite tools:
1. make_fab_pack: KiCad → KiKit (panel+JLC fab) → iBOM → STEP/GLB in one call
2. vendor_sync: Fill missing LCSC C-numbers from LCSC OpenAPI (+ Nexar assist), write back to schematic

Relies on documented CLIs/APIs:
- KiCad CLI: ERC/DRC, exports (Gerber, Drill, STEP, GLB, IPC-2581)
- KiKit: panelize + fab jlcpcb --assembly --field LCSC --missingError
- InteractiveHtmlBom: generate_interactive_bom --no-browser
- Nexar: OAuth2 GraphQL supply data (fallback MPN guesser)
- LCSC OpenAPI: signed endpoints (key, nonce, timestamp, signature=SHA1, 60s TTL)

Docs:
- KiCad CLI: https://docs.kicad.org/
- KiKit: https://github.com/yaqwsx/KiKit
- iBOM: https://github.com/openscopeproject/InteractiveHtmlBom
- Nexar: https://docs.nexar.com/
- LCSC: https://www.lcsc.com/
"""
from __future__ import annotations
import csv, json, os, random, string, time, hashlib, subprocess, sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import requests
from mcp.server.fastmcp import FastMCP

# Optional: kicad-skip for safe schematic editing (S-expression aware)
try:
    from skip.schem import Schematic  # type: ignore
    HAVE_SKIP = True
except Exception:
    HAVE_SKIP = False

mcp = FastMCP("fabops")

# --- Environment / external tools ---

KICAD = os.environ.get("KICAD_CLI", "kicad-cli")

# LCSC OpenAPI (required for vendor_sync)
LCSC_BASE = "https://ips.lcsc.com"
LCSC_KEY = os.environ.get("LCSC_API_KEY", "")
LCSC_SECRET = os.environ.get("LCSC_API_SECRET", "")

# Nexar (optional assist for MPN guessing)
NEXAR_ID = os.environ.get("NEXAR_CLIENT_ID", "")
NEXAR_SECRET = os.environ.get("NEXAR_CLIENT_SECRET", "")
NEXAR_SCOPE = os.environ.get("NEXAR_SCOPE", "supply.domain")
NEXAR_TOKEN_URL = "https://identity.nexar.com/connect/token"
NEXAR_GQL_URL = "https://api.nexar.com/graphql"
_token_cache: Dict[str, Any] = {"token": None, "exp": 0.0}

# --- Helpers ---

def _run(cmd: List[str], cwd: Optional[str] = None, ok_codes: List[int] = [0, 5]) -> Dict[str, Any]:
    """Run subprocess. KiCad CLI returns 5 when violations found."""
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return {
        "cmd": " ".join(cmd),
        "cwd": cwd or os.getcwd(),
        "returncode": p.returncode,
        "ok": p.returncode in ok_codes,
        "stdout": p.stdout[:500],  # truncate for readability
        "stderr": p.stderr[:500]
    }

def _ensure_dir(p: str) -> None:
    Path(p).mkdir(parents=True, exist_ok=True)

# --- KiCad CLI wrappers ---

def kicad_sch_bom(schematic: str, out_csv: str, fields: str = "*") -> Dict[str, Any]:
    _ensure_dir(Path(out_csv).parent.as_posix())
    return _run([KICAD, "sch", "export", "bom", "--fields", fields, "-o", out_csv, schematic])

def kicad_pcb_drc(board: str, out_json: str) -> Dict[str, Any]:
    _ensure_dir(Path(out_json).parent.as_posix())
    return _run([KICAD, "pcb", "drc", "--format", "json", "--exit-code-violations", "-o", out_json, board])

def kicad_pcb_export_step(board: str, out_step: str) -> Dict[str, Any]:
    _ensure_dir(Path(out_step).parent.as_posix())
    return _run([KICAD, "pcb", "export", "step", board, "-o", out_step])

def kicad_pcb_export_glb(board: str, out_glb: str) -> Dict[str, Any]:
    _ensure_dir(Path(out_glb).parent.as_posix())
    return _run([KICAD, "pcb", "export", "glb", board, "-o", out_glb])

# --- KiKit wrappers ---

def kikit_panelize_grid(input_pcb: str, output_pcb: str, rows: int, cols: int,
                        space: str, tabs: str, cuts: str, rails_width: str) -> Dict[str, Any]:
    _ensure_dir(Path(output_pcb).parent.as_posix())
    cmd = [
        "kikit", "panelize",
        "--layout", f"grid; rows: {rows}; cols: {cols}; space: {space}",
        "--tabs", tabs,
        "--cuts", cuts,
        "--framing", f"railstb; width: {rails_width}",
        input_pcb, output_pcb
    ]
    return _run(cmd)

def kikit_fab_jlcpcb(board_or_panel: str, out_dir: str, schematic: Optional[str],
                     assembly: bool, field: str, autoname: bool, missing_error: bool) -> Dict[str, Any]:
    _ensure_dir(out_dir)
    cmd = ["kikit", "fab", "jlcpcb"]
    if assembly: cmd.append("--assembly")
    if schematic: cmd += ["--schematic", schematic]
    if field: cmd += ["--field", field]
    if autoname: cmd.append("--autoname")
    if missing_error: cmd.append("--missingError")
    cmd += [board_or_panel, out_dir]
    return _run(cmd)

# --- iBOM wrapper ---

def ibom_generate(board_or_panel: str, out_dir: str, name_format: str, extra_fields: str) -> Dict[str, Any]:
    _ensure_dir(out_dir)
    cmd = [
        "generate_interactive_bom", "--no-browser",
        "--dest-dir", out_dir, "--name-format", name_format,
        "--extra-fields", extra_fields, board_or_panel
    ]
    return _run(cmd)

# --- Nexar client ---

def _nexar_token() -> Optional[str]:
    now = time.time()
    if _token_cache["token"] and now < _token_cache["exp"]:
        return _token_cache["token"]
    if not (NEXAR_ID and NEXAR_SECRET):
        return None
    try:
        r = requests.post(NEXAR_TOKEN_URL, data={
            "grant_type": "client_credentials",
            "client_id": NEXAR_ID, "client_secret": NEXAR_SECRET,
            "scope": NEXAR_SCOPE
        }, timeout=30)
        r.raise_for_status()
        data = r.json()
        _token_cache["token"] = data["access_token"]
        _token_cache["exp"] = now + max(60, data.get("expires_in", 3600) - 30)
        return _token_cache["token"]
    except Exception:
        return None

def nexar_guess_mpn(free_text: str) -> Optional[str]:
    """Guess MPN from free-text (Value, Footprint, Description, etc.)"""
    tok = _nexar_token()
    if not tok: return None
    q = """
    query ($q:String!, $limit:Int!) {
      supSearch(q:$q, limit:$limit) {
        results { part { mpn } }
      }
    }
    """
    try:
        r = requests.post(NEXAR_GQL_URL, json={"query": q, "variables": {"q": free_text, "limit": 1}},
                          headers={"Authorization": f"Bearer {tok}"}, timeout=45)
        r.raise_for_status()
        data = r.json()
        return data["data"]["supSearch"]["results"][0]["part"]["mpn"]
    except Exception:
        return None

# --- LCSC client ---

def _nonce(n: int = 16) -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

def _lcsc_auth() -> Dict[str, str]:
    ts = str(int(time.time()))
    n = _nonce(16)
    sig_src = f"key={LCSC_KEY}&nonce={n}&secret={LCSC_SECRET}&timestamp={ts}"
    sig = hashlib.sha1(sig_src.encode("utf-8")).hexdigest()
    return {"key": LCSC_KEY, "nonce": n, "timestamp": ts, "signature": sig}

def lcsc_keyword_search(keyword: str, page_size: int = 30, in_stock: bool = True) -> Dict[str, Any]:
    """Search LCSC by keyword (C-number best). 60s signature TTL."""
    params = {"keyword": keyword, "page_size": page_size, "is_available": str(in_stock).lower(),
              **_lcsc_auth()}
    r = requests.get(f"{LCSC_BASE}/rest/wmsc2agent/search/product", params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def lcsc_item_info(product_number: str) -> Dict[str, Any]:
    r = requests.get(f"{LCSC_BASE}/rest/wmsc2agent/product/info/{product_number}",
                     params=_lcsc_auth(), timeout=30)
    r.raise_for_status()
    return r.json()

# --- Schematic editing ---

def _write_lcsc_fields_to_schematic(schematic_path: str, patches: Dict[str, str]) -> Tuple[bool, str]:
    """Write LCSC C-numbers to schematic using kicad-skip (S-expression safe)."""
    if not HAVE_SKIP:
        return False, "kicad-skip not installed (pip install kicad-skip)."
    try:
        sch = Schematic(schematic_path)
        changed = 0
        for sym in sch.symbols:
            ref = sym.get("Reference", None)
            if not ref or ref not in patches:
                continue
            sym.setProperty("LCSC", patches[ref])
            changed += 1
        if changed:
            sch.save(schematic_path)
        return True, f"Updated {changed} symbols with LCSC fields."
    except Exception as e:
        return False, f"kicad-skip error: {e}"

# --- CSV helpers ---

def _read_bom_csv(csv_path: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({k.strip(): (v or "").strip() for k, v in r.items()})
    return rows

def _pick(row: Dict[str, str], names: List[str]) -> Optional[str]:
    for n in names:
        if n in row and row[n]:
            return row[n]
    return None

# =============================================================================
# Power-Domain Guard (K1-specific)
# =============================================================================

def kicad_sch_export_netlist(schematic: str, out_net: str = "tmp_sch.net") -> Dict[str, Any]:
    """Export schematic to netlist for power-domain analysis."""
    _ensure_dir(Path(out_net).parent.as_posix())
    return _run([KICAD, "sch", "export", "netlist", "-f", "kicadsexpr", "-o", out_net, schematic])

@mcp.tool()
def check_power_domains(schematic_kicad_sch: str,
                        usb_5v_name: str = "VBUS_USB_5V",
                        led_5v_name: str = "LED_5V") -> Dict[str, Any]:
    """Fail if any component pin is tied to both 5V nets, or if net names collide.
    K1-specific: Prevents shorts between USB 5V (controller) and LED 5V (external).
    """
    out_net = Path("fab/tmp_sch.net")
    res = kicad_sch_export_netlist(schematic_kicad_sch, out_net.as_posix())
    if not res["ok"]:
        return {"ok": False, "error": f"Netlist export failed: {res['stderr']}"}

    data = Path(out_net).read_text(encoding="utf-8", errors="ignore")
    same_name = usb_5v_name == led_5v_name

    # Naive but effective: collect component refs under each net and intersect
    import re
    def refs_for(netname):
        block = re.findall(rf'\(net \(code \d+\) \(name "{re.escape(netname)}"\)(.*?)\)\s*\)', data, flags=re.S)
        pins = re.findall(r'\(node \(ref ([^)]+)\) \(pin ([^)]+)\)\)', block[0]) if block else []
        return set(r for (r, p) in pins)

    usb_refs = refs_for(usb_5v_name)
    led_refs = refs_for(led_5v_name)
    cross = usb_refs.intersection(led_refs)

    ok = (not same_name) and (len(cross) == 0)
    return {
        "ok": ok,
        "shared_refs": sorted(list(cross)),
        "usb_5v_refs": len(usb_refs),
        "led_5v_refs": len(led_refs),
        "error": f"Power-domain violation: {', '.join(cross)} tied to both nets" if not ok else None
    }

# =============================================================================
# TOOL 1: make_fab_pack
# =============================================================================

@mcp.tool()
def make_fab_pack(
    board_kicad_pcb: str,
    schematic_kicad_sch: str,
    out_root: str = "fab/out",
    rows: int = 4,
    cols: int = 8,
    space: str = "2mm",
    tabs: str = "full",
    cuts: str = "vcuts; clearance: 0.4mm",
    rails_width: str = "5mm",
    field: str = "LCSC",
    autoname: bool = True,
    missing_error: bool = True,
    gen_step: bool = True,
    gen_glb: bool = True,
    gen_ibom: bool = True,
    ibom_extra_fields: str = "LCSC,MPN,Manufacturer"
) -> Dict[str, Any]:
    """
    One-command fabrication pack:
    1) DRC JSON (non-fatal)
    2) Panelize with KiKit (grid + V-cuts/rails)
    3) JLC fab pack (Gerbers, BOM, POS) with assembly
    4) iBOM HTML (from panel)
    5) STEP & GLB 3D exports

    Returns: paths & logs for all artifacts.
    """
    out_root = Path(out_root)
    panel_dir = out_root / "panel"
    fab_dir = out_root / "jlc"
    mech_dir = out_root / "mechanical"
    report_dir = out_root / "reports"
    ibom_dir = Path("docs/ibom")

    for d in (panel_dir, fab_dir, mech_dir, report_dir, ibom_dir):
        _ensure_dir(d.as_posix())

    # 0) Power-domain guard (K1-specific: prevent USB 5V ↔ LED 5V shorts)
    guard = check_power_domains(schematic_kicad_sch)
    if not guard.get("ok", False):
        return {
            "ok": False,
            "error": guard.get("error", "Power-domain violation detected"),
            "guard_result": guard
        }

    # 1) DRC JSON (informational)
    drc_json = (report_dir / "drc.json").as_posix()
    drc_res = kicad_pcb_drc(board_kicad_pcb, drc_json)

    # 2) Panelize
    panel_pcb = (panel_dir / (Path(board_kicad_pcb).stem + "_panel.kicad_pcb")).as_posix()
    pnl_res = kikit_panelize_grid(board_kicad_pcb, panel_pcb, rows, cols, space, tabs, cuts, rails_width)

    # 3) JLC fab pack
    fab_res = kikit_fab_jlcpcb(panel_pcb, fab_dir.as_posix(), schematic_kicad_sch,
                               assembly=True, field=field, autoname=autoname, missing_error=missing_error)

    # 4) iBOM
    ibom_res = {}
    if gen_ibom:
        ibom_res = ibom_generate(board_kicad_pcb, ibom_dir.as_posix(), "ibom", ibom_extra_fields)

    # 5) 3D exports (from single board, not panel)
    step_res = {}
    glb_res = {}
    if gen_step:
        step_res = kicad_pcb_export_step(board_kicad_pcb, (mech_dir / "board.step").as_posix())
    if gen_glb:
        glb_res = kicad_pcb_export_glb(board_kicad_pcb, (mech_dir / "board.glb").as_posix())

    return {
        "ok": pnl_res["ok"] and fab_res["ok"] and (not gen_ibom or ibom_res.get("ok", True)),
        "artifacts": {
            "panel_pcb": panel_pcb,
            "jlc_dir": fab_dir.as_posix(),
            "gerbers_zip": f"{fab_dir}/gerbers.zip",
            "bom_csv": f"{fab_dir}/bom.csv",
            "pos_csv": f"{fab_dir}/pos.csv",
            "drc_json": drc_json,
            "ibom_html": f"{ibom_dir.as_posix()}/ibom.html" if gen_ibom else None,
            "step_file": (mech_dir / "board.step").as_posix() if gen_step else None,
            "glb_file": (mech_dir / "board.glb").as_posix() if gen_glb else None
        },
        "logs": {
            "drc": drc_res,
            "panelize": pnl_res,
            "fab": fab_res,
            "ibom": ibom_res,
            "step": step_res,
            "glb": glb_res
        }
    }

# =============================================================================
# TOOL 2: vendor_sync
# =============================================================================

@mcp.tool()
def vendor_sync(
    schematic_kicad_sch: str,
    board_kicad_pcb: Optional[str] = None,
    out_manifest: str = "fab/lcsc_manifest.json",
    lcsc_field: str = "LCSC",
    mpn_fields: str = "MPN,Manufacturer Part Number,Mfr Part#,Part Number,mpn,Mpn",
    apply_changes: bool = True,
    run_fab: bool = False,
    jlc_out_dir: str = "fab/jlc"
) -> Dict[str, Any]:
    """
    Sync missing LCSC C-numbers:
    1) Export BOM CSV (all fields)
    2) For empty LCSC cells, search LCSC by MPN (or Nexar-guessed MPN)
    3) Write C-numbers back to schematic (kicad-skip if available)
    4) Optionally run kikit fab jlcpcb --assembly ... --missingError

    Returns: manifest JSON + summary.
    """
    # 1) Export BOM
    tmp_csv = Path(out_manifest).with_suffix(".tmp_bom.csv").as_posix()
    bom_res = kicad_sch_bom(schematic_kicad_sch, tmp_csv, fields="*")
    if not Path(tmp_csv).exists():
        return {"ok": False, "error": f"BOM export failed: {bom_res['stderr']}", "bom_csv": tmp_csv}

    rows = _read_bom_csv(tmp_csv)
    mpn_keys = [s.strip() for s in mpn_fields.split(",") if s.strip()]

    patches: Dict[str, str] = {}
    resolved: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []

    if not (LCSC_KEY and LCSC_SECRET):
        return {
            "ok": False,
            "error": "LCSC_API_KEY/SECRET not set; cannot resolve C-numbers.",
            "bom_csv": tmp_csv
        }

    for r in rows:
        ref = r.get("Reference", "")
        if not ref:
            continue
        if r.get(lcsc_field, ""):
            continue

        # Find MPN or guess it
        mpn = _pick(r, mpn_keys)
        if not mpn:
            guess_text = " ".join([
                r.get("Value", ""), r.get("Footprint", ""), r.get("Datasheet", ""), r.get("Description", "")
            ]).strip()
            mpn = nexar_guess_mpn(guess_text) if guess_text else None

        if not mpn:
            skipped.append({"ref": ref, "reason": "No MPN available for LCSC search"})
            continue

        # Search LCSC
        try:
            lcsc_res = lcsc_keyword_search(mpn, page_size=10, in_stock=True)
            # Extract C-number from response (shape varies; try common keys)
            cnum = None
            data = lcsc_res.get("result") or lcsc_res.get("data") or lcsc_res
            if isinstance(data, dict):
                for key in ("list", "items", "products", "data", "results"):
                    if key in data and isinstance(data[key], list) and data[key]:
                        cand = data[key][0]
                        cnum = cand.get("lcsc_part_number") or cand.get("product_number") or cand.get("number") or cand.get("sku")
                        break
            elif isinstance(data, list) and data:
                cand = data[0]
                cnum = cand.get("lcsc_part_number") or cand.get("product_number") or cand.get("number") or cand.get("sku")

            if cnum:
                patches[ref] = cnum
                resolved.append({"ref": ref, "mpn": mpn, "lcsc": cnum, "source": "LCSC search"})
            else:
                skipped.append({"ref": ref, "mpn": mpn, "reason": "No product found in LCSC response"})
        except Exception as e:
            skipped.append({"ref": ref, "mpn": mpn, "reason": f"LCSC search error: {str(e)[:100]}"})

    # 3) Write back
    write_msg = "no changes"
    if apply_changes and patches:
        ok, write_msg = _write_lcsc_fields_to_schematic(schematic_kicad_sch, patches)

    # 4) Optional fab pack
    fab_res = {}
    if run_fab and board_kicad_pcb:
        fab_res = kikit_fab_jlcpcb(board_kicad_pcb, jlc_out_dir, schematic_kicad_sch,
                                   assembly=True, field=lcsc_field, autoname=True, missing_error=True)

    # 5) Persist manifest
    manifest = {
        "schematic": schematic_kicad_sch,
        "field": lcsc_field,
        "resolved": resolved,
        "skipped": skipped,
        "patches": patches,
        "apply_changes": apply_changes,
        "write_result": write_msg,
        "fab": fab_res if fab_res else None,
        "bom_csv": tmp_csv
    }
    _ensure_dir(Path(out_manifest).parent.as_posix())
    Path(out_manifest).write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return {
        "ok": True,
        "manifest": Path(out_manifest).resolve().as_posix(),
        "summary": {
            "resolved": len(resolved),
            "skipped": len(skipped),
            "applied": bool(patches) and apply_changes,
            "write_msg": write_msg
        }
    }

if __name__ == "__main__":
    mcp.run()
