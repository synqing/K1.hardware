#!/usr/bin/env python3
"""
MCP server for KiBot — run reproducible fab/doc CI jobs locally.
Example:
  kibot_run(project_dir=".", config_yaml="config.kibot.yaml", board="board.kicad_pcb", schematic="project.kicad_sch", out_dir="_artifacts")

Docs: https://kibot.readthedocs.io/
"""
import subprocess, os
from pathlib import Path
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("kibot")

def _run(cmd: List[str], cwd: Optional[str] = None) -> Dict[str, Any]:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return {
        "cmd": " ".join(cmd),
        "cwd": cwd or os.getcwd(),
        "returncode": p.returncode,
        "ok": p.returncode == 0,
        "stdout": p.stdout,
        "stderr": p.stderr
    }

@mcp.tool()
def kibot_run(project_dir: str,
              config_yaml: str,
              out_dir: str = "_artifacts",
              schematic: Optional[str] = None,
              board: Optional[str] = None) -> Dict[str, Any]:
    """Run KiBot with given config, writing outputs to out_dir."""
    Path(project_dir, out_dir).mkdir(parents=True, exist_ok=True)
    cmd = ["kibot", "-c", config_yaml, "-d", out_dir]
    if schematic:
        cmd += ["-e", schematic]
    if board:
        cmd += ["-b", board]
    return _run(cmd, cwd=project_dir)

if __name__ == "__main__":
    mcp.run()
