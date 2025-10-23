#!/usr/bin/env python3
"""
MCP server exposing KiCad CLI tools:
- ERC/DRC JSON reports
- BOM / netlist export
- Gerbers, Drill, STEP, IPC-2581, GLB

Docs: https://docs.kicad.org/cli/
"""
import json, os, subprocess, sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP

KICAD = os.environ.get("KICAD_CLI", "kicad-cli")
mcp = FastMCP("kicad-cli")

def _run(cmd: List[str], cwd: Optional[str] = None, ok_codes: List[int] = [0,5]) -> Dict[str, Any]:
    """Run a subprocess and return structured result. KiCad returns 5 for 'violations found'."""
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return {
        "cmd": " ".join(cmd),
        "cwd": cwd or os.getcwd(),
        "returncode": proc.returncode,
        "ok": proc.returncode in ok_codes,
        "stdout": proc.stdout,
        "stderr": proc.stderr
    }

def _ensure_parent(p: str):
    Path(p).parent.mkdir(parents=True, exist_ok=True)

@mcp.tool()
def sch_erc(schematic: str, out: str = "erc.json", format: str = "json", exit_code_violations: bool = True) -> Dict[str, Any]:
    """Run ERC on a .kicad_sch. Returns path + counts if JSON."""
    _ensure_parent(out)
    cmd = [KICAD, "sch", "erc", "--format", format, "-o", out, schematic]
    if exit_code_violations:
        cmd.insert(3, "--exit-code-violations")
    res = _run(cmd)
    summary = {}
    if Path(out).exists() and format == "json":
        try:
            data = json.loads(Path(out).read_text())
            summary = {
                "errors": data.get("error_count"),
                "warnings": data.get("warning_count"),
                "exclusions": data.get("excluded_count")
            }
        except Exception:
            pass
    res.update({"output": str(Path(out).resolve()), "summary": summary})
    return res

@mcp.tool()
def sch_export_bom(schematic: str, out_csv: str = "bom.csv", fields: str = "*") -> Dict[str, Any]:
    """Export CSV BOM from schematic."""
    _ensure_parent(out_csv)
    cmd = [KICAD, "sch", "export", "bom", "--fields", fields, "-o", out_csv, schematic]
    res = _run(cmd)
    res.update({"output": str(Path(out_csv).resolve())})
    return res

@mcp.tool()
def sch_export_netlist(schematic: str, out_net: str = "project.net", fmt: str = "kicadsexpr") -> Dict[str, Any]:
    """Export netlist from schematic (kicadsexpr|kicadxml|cadstar|orcadpcb2|spice|spicemodel)."""
    _ensure_parent(out_net)
    cmd = [KICAD, "sch", "export", "netlist", "-f", fmt, "-o", out_net, schematic]
    res = _run(cmd)
    res.update({"output": str(Path(out_net).resolve())})
    return res

@mcp.tool()
def pcb_drc(board: str, out: str = "drc.json", format: str = "json", exit_code_violations: bool = True) -> Dict[str, Any]:
    """Run DRC on a .kicad_pcb. Return JSON path + basic counts."""
    _ensure_parent(out)
    cmd = [KICAD, "pcb", "drc", "--format", format, "-o", out, board]
    if exit_code_violations:
        cmd.insert(3, "--exit-code-violations")
    res = _run(cmd)
    summary = {}
    if Path(out).exists() and format == "json":
        try:
            data = json.loads(Path(out).read_text())
            summary = {
                "violations": data.get("violation_count", 0),
                "unconnected": data.get("unconnected_count", 0)
            }
        except Exception:
            pass
    res.update({"output": str(Path(out).resolve()), "summary": summary})
    return res

@mcp.tool()
def pcb_export_gerbers(board: str, out_dir: str = "fab/gerbers") -> Dict[str, Any]:
    """Export one-file-per-layer Gerbers."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    cmd = [KICAD, "pcb", "export", "gerbers", board, "-o", out_dir]
    res = _run(cmd)
    res.update({"output": str(Path(out_dir).resolve())})
    return res

@mcp.tool()
def pcb_export_drill(board: str, out_dir: str = "fab/drill") -> Dict[str, Any]:
    """Export drill files."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    cmd = [KICAD, "pcb", "export", "drill", board, "-o", out_dir]
    res = _run(cmd)
    res.update({"output": str(Path(out_dir).resolve())})
    return res

@mcp.tool()
def pcb_export_step(board: str, out_file: str = "mechanical/board.step") -> Dict[str, Any]:
    """Export STEP 3D model."""
    _ensure_parent(out_file)
    cmd = [KICAD, "pcb", "export", "step", board, "-o", out_file]
    res = _run(cmd)
    res.update({"output": str(Path(out_file).resolve())})
    return res

@mcp.tool()
def pcb_export_ipc2581(board: str, out_file: str = "fab/board.ipc") -> Dict[str, Any]:
    """Export IPC-2581 manufacturing data."""
    _ensure_parent(out_file)
    cmd = [KICAD, "pcb", "export", "ipc2581", board, "-o", out_file]
    res = _run(cmd)
    res.update({"output": str(Path(out_file).resolve())})
    return res

@mcp.tool()
def pcb_export_glb(board: str, out_file: str = "mechanical/board.glb") -> Dict[str, Any]:
    """Export GLB 3D model."""
    _ensure_parent(out_file)
    cmd = [KICAD, "pcb", "export", "glb", board, "-o", out_file]
    res = _run(cmd)
    res.update({"output": str(Path(out_file).resolve())})
    return res

if __name__ == "__main__":
    mcp.run()
