#!/usr/bin/env python3
"""
MCP server for Nexar (Octopart) GraphQL:
- parts_search(q, limit)
- part_by_mpn(mpn)
- best_datasheet_url(mpn)

Auth: OAuth2 client_credentials → token from https://identity.nexar.com/connect/token
API:  GraphQL at https://api.nexar.com/graphql

Docs: https://docs.nexar.com/
"""
import os, time, requests
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("nexar")

NEXAR_ID = os.environ.get("NEXAR_CLIENT_ID", "")
NEXAR_SECRET = os.environ.get("NEXAR_CLIENT_SECRET", "")
NEXAR_SCOPE = os.environ.get("NEXAR_SCOPE", "supply.domain")
TOKEN_URL = "https://identity.nexar.com/connect/token"
GQL_URL   = "https://api.nexar.com/graphql"

_token_cache: Dict[str, Any] = {"token": None, "exp": 0}

def _get_token() -> str:
    now = time.time()
    if _token_cache["token"] and now < _token_cache["exp"]:
        return _token_cache["token"]
    resp = requests.post(
        TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "k1-lightwave-mcp/1.0"},
        data={"grant_type": "client_credentials", "client_id": NEXAR_ID, "client_secret": NEXAR_SECRET, "scope": NEXAR_SCOPE},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    _token_cache["token"] = data["access_token"]
    _token_cache["exp"] = now + max(60, data.get("expires_in", 3600) - 30)
    return _token_cache["token"]

def _gql(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    tok = _get_token()
    resp = requests.post(GQL_URL, json={"query": query, "variables": variables or {}}, headers={"Authorization": f"Bearer {tok}"}, timeout=45)
    resp.raise_for_status()
    return resp.json()

@mcp.tool()
def parts_search(q: str, limit: int = 3) -> Dict[str, Any]:
    """Search supply data for parts matching free-text (MPN, desc, etc.). Returns MPN, manufacturer, and bestDatasheet URL if available."""
    query = """
    query ($q: String!, $limit: Int!) {
      supSearch(q: $q, limit: $limit) {
        hits {
          results {
            part {
              mpn
              manufacturer { name }
              bestDatasheet { url }
            }
          }
        }
      }
    }
    """
    data = _gql(query, {"q": q, "limit": limit})
    return data

@mcp.tool()
def part_by_mpn(mpn: str) -> Dict[str, Any]:
    """Exact MPN search with basic fields."""
    query = """
    query ($mpn: String!) {
      supSearchMpn(q: $mpn) {
        hits
        results {
          part {
            id
            mpn
            name
            manufacturer { name }
            bestDatasheet { url }
            specs { attribute { name unitsName } value unitsSymbol }
          }
        }
      }
    }
    """
    return _gql(query, {"mpn": mpn})

@mcp.tool()
def best_datasheet_url(mpn: str) -> Dict[str, Any]:
    """Return first bestDatasheet URL for given MPN."""
    r = part_by_mpn(mpn)
    try:
        results = r.get("data", {}).get("supSearchMpn", {}).get("results", [])
        for row in results:
            ds = row.get("part", {}).get("bestDatasheet", {})
            if ds and ds.get("url"):
                return {"mpn": mpn, "url": ds["url"], "ok": True}
    except Exception:
        pass
    return {"mpn": mpn, "url": None, "ok": False}

if __name__ == "__main__":
    if not (NEXAR_ID and NEXAR_SECRET):
        print("WARNING: Set NEXAR_CLIENT_ID and NEXAR_CLIENT_SECRET env vars.", file=sys.stderr)
    mcp.run()
