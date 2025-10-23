#!/usr/bin/env python3
"""
MCP server exposing FreeRouting headless routing:
- Input:  DSN design file
- Output: SES routed session file

Docs: https://github.com/freerouting/freerouting
"""
import os, subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("freerouting")
FREEROUTING_JAR = os.environ.get("FREEROUTING_JAR", "freerouting.jar")

def _run(cmd: List[str], timeout: Optional[int] = None) -> Dict[str, Any]:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return {
        "cmd": " ".join(cmd),
        "returncode": p.returncode,
        "stdout": p.stdout,
        "stderr": p.stderr,
        "ok": p.returncode == 0
    }

@mcp.tool()
def route(dsn: str, ses_out: str = "out.ses", ignore_nets: str = "", timeout_sec: Optional[int] = 300) -> Dict[str, Any]:
    """
    Run the autorouter on DSN and write SES.
    - ignore_nets: comma-separated list (e.g., "GND,VCC") passed via -inc argument when supported.
    """
    Path(ses_out).parent.mkdir(parents=True, exist_ok=True)
    cmd = ["java", "-jar", FREEROUTING_JAR, "-de", dsn, "-do", ses_out]
    if ignore_nets:
        cmd += ["-inc", ignore_nets]
    res = _run(cmd, timeout=timeout_sec)
    res.update({"output": str(Path(ses_out).resolve())})
    return res

if __name__ == "__main__":
    mcp.run()
