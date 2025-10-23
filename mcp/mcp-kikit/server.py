#!/usr/bin/env python3
"""
MCP server for KiKit panelization and JLC fab pack.
Typical calls:
- panelize (grid + vcuts/mousebites + rails)
- fab_jlcpcb (--assembly --field LCSC)

Docs: https://github.com/yaqwsx/KiKit
"""
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("kikit")

def _run(cmd: List[str]) -> Dict[str, Any]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return {"cmd": " ".join(cmd), "returncode": p.returncode, "ok": p.returncode == 0, "stdout": p.stdout, "stderr": p.stderr}

@mcp.tool()
def panelize_grid(input_pcb: str,
                  output_pcb: str,
                  rows: int = 4,
                  cols: int = 8,
                  space_mm: str = "2mm",
                  tabs: str = "full",
                  cuts: str = "vcuts; clearance: 0.4mm",
                  rails_mm: str = "5mm") -> Dict[str, Any]:
    """Create a grid panel with rails and V-cuts/mousebites."""
    Path(output_pcb).parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "kikit", "panelize",
        "--layout", f"grid; rows: {rows}; cols: {cols}; space: {space_mm}",
        "--tabs", tabs,
        "--cuts", cuts,
        "--framing", f"railstb; width: {rails_mm}",
        input_pcb, output_pcb
    ]
    res = _run(cmd)
    res.update({"output": str(Path(output_pcb).resolve())})
    return res

@mcp.tool()
def fab_jlcpcb(board_or_panel: str,
               out_dir: str = "fab/jlc",
               assembly: bool = True,
               schematic: Optional[str] = None,
               field: str = "LCSC",
               autoname: bool = True,
               missing_error: bool = True) -> Dict[str, Any]:
    """Create JLCPCB-ready fab pack (gerbers.zip, bom.csv, pos.csv)."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    cmd = ["kikit", "fab", "jlcpcb"]
    if assembly:
        cmd.append("--assembly")
    if schematic:
        cmd += ["--schematic", schematic]
    if field:
        cmd += ["--field", field]
    if autoname:
        cmd.append("--autoname")
    if missing_error:
        cmd.append("--missingError")
    cmd += [board_or_panel, out_dir]
    res = _run(cmd)
    res.update({"output_dir": str(Path(out_dir).resolve())})
    return res

if __name__ == "__main__":
    mcp.run()
