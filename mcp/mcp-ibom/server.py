#!/usr/bin/env python3
"""
MCP server for Interactive HTML BOM (iBOM) generator.
CLI: generate_interactive_bom --no-browser --dest-dir <out> <board.kicad_pcb>

Docs: https://github.com/openscopeproject/InteractiveHtmlBom
"""
import os, subprocess
from pathlib import Path
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ibom")

def _run(cmd: List[str]) -> Dict[str, Any]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return {"cmd": " ".join(cmd), "returncode": p.returncode, "ok": p.returncode == 0, "stdout": p.stdout, "stderr": p.stderr}

@mcp.tool()
def generate(board_kicad_pcb: str, out_dir: str = "docs/ibom", name_format: str = "ibom", extra_fields: str = "LCSC,MPN,Manufacturer") -> Dict[str, Any]:
    """Create a self-contained HTML iBOM for PnP/assembly."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    cmd = [
        "generate_interactive_bom", "--no-browser",
        "--dest-dir", out_dir, "--name-format", name_format,
        "--extra-fields", extra_fields, board_kicad_pcb
    ]
    res = _run(cmd)
    res.update({"output_dir": str(Path(out_dir).resolve())})
    return res

if __name__ == "__main__":
    mcp.run()
