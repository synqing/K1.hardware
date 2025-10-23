#!/usr/bin/env python3
"""
MCP server for LCSC OpenAPI (C-number lookup for JLC assembly).
Auth: signature = sha1("key=...&nonce=...&secret=...&timestamp=..."), timestamp (s) expires in 60s.
Endpoints:
- GET /rest/wmsc2agent/search/product?keyword=...
- GET /rest/wmsc2agent/product/info/{product_number}
Base: https://ips.lcsc.com

Docs: https://www.lcsc.com/
"""
import hashlib, os, random, string, time, requests
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("lcsc")
BASE = "https://ips.lcsc.com"
API_KEY = os.environ.get("LCSC_API_KEY", "")
API_SECRET = os.environ.get("LCSC_API_SECRET", "")

def _nonce(n: int = 16) -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

def _sig(key: str, secret: str, nonce: str, ts: str) -> str:
    s = f"key={key}&nonce={nonce}&secret={secret}&timestamp={ts}"
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def _auth_params() -> Dict[str, str]:
    ts = str(int(time.time()))
    n = _nonce(16)
    return {"key": API_KEY, "nonce": n, "timestamp": ts, "signature": _sig(API_KEY, API_SECRET, n, ts)}

@mcp.tool()
def search(keyword: str, is_available: bool = True, page_size: int = 30) -> Dict[str, Any]:
    """Keyword search; best with exact LCSC 'C' numbers."""
    params = {"keyword": keyword, "is_available": str(is_available).lower(), "page_size": page_size, **_auth_params()}
    r = requests.get(f"{BASE}/rest/wmsc2agent/search/product", params=params, timeout=30)
    r.raise_for_status()
    return r.json()

@mcp.tool()
def item(product_number: str) -> Dict[str, Any]:
    """Get details for a single product (LCSC number, pricing, stock)."""
    r = requests.get(f"{BASE}/rest/wmsc2agent/product/info/{product_number}", params=_auth_params(), timeout=30)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    if not (API_KEY and API_SECRET):
        print("WARNING: Set LCSC_API_KEY and LCSC_API_SECRET env vars.", file=__import__('sys').stderr)
    mcp.run()
