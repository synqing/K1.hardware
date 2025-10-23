#!/usr/bin/env python3
"""
MCP server exposing a SKiDL → KiCad netlist tool.
It executes a SKiDL script and emits a KiCad 8/9 S-expression netlist.

Docs: https://devbisme.github.io/skidl/
"""
import os, sys
from pathlib import Path
from runpy import run_path
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("skidl")

@mcp.tool()
def skidl_gen_netlist(script_path: str, out_net: str = "skidl_out.net") -> Dict[str, Any]:
    """Run a SKiDL Python script and write a KiCad 8/9 S-expression netlist."""
    try:
        from skidl import default_circuit, reset
        from skidl.tools.kicad9.gen_netlist import gen_netlist
    except ImportError:
        return {"error": "SKiDL not installed. Run: pip install skidl"}

    # Start fresh.
    reset()

    # Execute user SKiDL file in isolated globals.
    try:
        run_path(script_path, run_name="__skidl_run__")
    except Exception as e:
        return {"error": f"SKiDL script failed: {str(e)}"}

    # Generate and write netlist.
    outp = Path(out_net)
    outp.parent.mkdir(parents=True, exist_ok=True)
    try:
        net_sexpr = gen_netlist(default_circuit)
        outp.write_text(net_sexpr, encoding="utf-8")
    except Exception as e:
        return {"error": f"Netlist generation failed: {str(e)}"}

    return {
        "output": str(outp.resolve()),
        "parts": len(default_circuit.parts),
        "nets": len(default_circuit.nets),
        "ok": True
    }

if __name__ == "__main__":
    mcp.run()
