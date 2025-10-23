# Nexar (Octopart) GraphQL API Reference

**Complete Nexar GraphQL API Documentation**

For integration with K1 Lightwave PCB design pipeline (parts search, datasheets, pricing).

---

## Overview

Nexar provides **GraphQL API** for querying Octopart supply data. Unlike REST APIs, GraphQL allows requesting only the fields you need, reducing bandwidth and improving performance.

### Key Capabilities

1. **Supply Search** — Find components by keyword/MPN
2. **Part Details** — Full specifications, datasheets, pricing
3. **Manufacturer Info** — Company details, product lines
4. **Distributor Pricing** — Real-time availability and cost across distributors
5. **Datasheets** — Direct links to PDF documentation

---

## Getting Started

### Prerequisites

1. Create Nexar account at https://nexar.com/
2. Sign up for free API tier (includes supply domain access)
3. Create API application:
   - Dashboard → API Credentials → Create App
   - Copy **Client ID** and **Client Secret**
4. Setup credentials in K1 project:
   ```bash
   export NEXAR_CLIENT_ID="your_id"
   export NEXAR_CLIENT_SECRET="your_secret"
   ```

### Endpoint

```
GraphQL API: https://api.nexar.com/graphql
Auth:        OAuth2 client_credentials
Scope:       supply.domain
```

---

## Authentication

### OAuth2 Client Credentials Flow

**Step 1: Get Access Token**

```bash
curl -X POST "https://identity.nexar.com/connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "scope=supply.domain"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ik...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

**Step 2: Query GraphQL API**

```bash
curl -X POST "https://api.nexar.com/graphql" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ supSearch(q:\"ESP32-S3\") { hits } }"}'
```

### Python Implementation

```python
import requests
import time

class NexarClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_exp = 0
        self.gql_url = "https://api.nexar.com/graphql"
        self.token_url = "https://identity.nexar.com/connect/token"

    def get_token(self) -> str:
        """Get or refresh access token"""
        now = time.time()
        if self.token and now < self.token_exp:
            return self.token

        resp = requests.post(self.token_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": "supply.domain"
            },
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        self.token = data["access_token"]
        self.token_exp = now + data.get("expires_in", 3600) - 30
        return self.token

    def query(self, query: str, variables: dict = None) -> dict:
        """Execute GraphQL query"""
        token = self.get_token()
        resp = requests.post(self.gql_url,
            json={"query": query, "variables": variables or {}},
            headers={"Authorization": f"Bearer {token}"},
            timeout=45
        )
        resp.raise_for_status()
        return resp.json()

    def search_parts(self, q: str, limit: int = 10) -> list:
        """Search for parts by keyword/MPN"""
        query = """
        query ($q: String!, $limit: Int!) {
            supSearch(q: $q, limit: $limit) {
                hits
                results {
                    part {
                        id
                        mpn
                        name
                        manufacturer { id name }
                        bestDatasheet { url }
                        shortDescription
                    }
                }
            }
        }
        """
        result = self.query(query, {"q": q, "limit": limit})
        return result.get("data", {}).get("supSearch", {}).get("results", [])

    def get_part_details(self, mpn: str) -> dict:
        """Get detailed info for part by MPN"""
        query = """
        query ($mpn: String!) {
            supSearchMpn(q: $mpn) {
                results {
                    part {
                        id
                        mpn
                        name
                        manufacturer { id name }
                        status
                        category { id name }
                        bestDatasheet { url }
                        specs {
                            attribute { name unitsName }
                            value
                            unitsSymbol
                        }
                        distributors(limit: 5) {
                            name
                            sku
                            pricing {
                                pricingTiers { quantity unitPrice currency }
                                updatedAt
                            }
                            leadTime { value unit }
                        }
                    }
                }
            }
        }
        """
        result = self.query(query, {"mpn": mpn})
        return result.get("data", {}).get("supSearchMpn", {}).get("results", [{}])[0].get("part", {})

    def get_datasheet(self, mpn: str) -> str:
        """Get datasheet URL for part"""
        query = """
        query ($mpn: String!) {
            supSearchMpn(q: $mpn) {
                results {
                    part {
                        bestDatasheet { url }
                        datasheets(limit: 1) { url }
                    }
                }
            }
        }
        """
        result = self.query(query, {"mpn": mpn})
        data = result.get("data", {}).get("supSearchMpn", {}).get("results", [{}])[0].get("part", {})
        url = data.get("bestDatasheet", {}).get("url")
        if not url and data.get("datasheets"):
            url = data["datasheets"][0].get("url")
        return url
```

---

## GraphQL Queries

### Query: supSearch

Full-text search across MPNs, descriptions, and manufacturer names.

**Input:**
```graphql
query ($q: String!, $limit: Int!) {
    supSearch(q: $q, limit: $limit) {
        hits
        results {
            part {
                # ... fields
            }
        }
    }
}
```

**Variables:**
- `q` (String!) — Search term (MPN, description, etc.)
- `limit` (Int) — Max results (default: 10, max: 100)

**Response:**
```json
{
  "data": {
    "supSearch": {
      "hits": 42,
      "results": [
        {
          "part": {
            "mpn": "ESP32-S3-WROOM-1",
            "manufacturer": { "name": "Espressif Systems" },
            "bestDatasheet": { "url": "https://..." }
          }
        }
      ]
    }
  }
}
```

---

### Query: supSearchMpn

Exact MPN search with full part specifications.

**Input:**
```graphql
query ($mpn: String!) {
    supSearchMpn(q: $mpn) {
        hits
        results {
            part {
                id
                mpn
                name
                manufacturer { id name }
                status
                category { id name }
                shortDescription
                bestDatasheet { url }
                specs { attribute { name unitsName } value unitsSymbol }
                distributors(limit: 5) {
                    name
                    sku
                    leadTime { value unit }
                    pricing { pricingTiers { quantity unitPrice currency } }
                }
            }
        }
    }
}
```

**Variables:**
- `mpn` (String!) — Exact manufacturer part number

**Response:**
```json
{
  "data": {
    "supSearchMpn": {
      "hits": 1,
      "results": [
        {
          "part": {
            "id": "part_esp32_s3_wroom_1",
            "mpn": "ESP32-S3-WROOM-1",
            "name": "ESP32-S3-WROOM-1 WiFi + BLE MCU Module",
            "manufacturer": {
              "id": "mfg_espressif",
              "name": "Espressif Systems"
            },
            "status": "ACTIVE",
            "category": {
              "id": "cat_microcontrollers",
              "name": "Microcontrollers"
            },
            "shortDescription": "Dual-core 32-bit MCU, WiFi 6, BLE 5.0",
            "bestDatasheet": {
              "url": "https://octopart.com/datasheets/esp32-s3-wroom-1.pdf"
            },
            "specs": [
              {
                "attribute": { "name": "Processor Type", "unitsName": null },
                "value": "Xtensa Dual-Core 32-bit",
                "unitsSymbol": null
              },
              {
                "attribute": { "name": "Frequency", "unitsName": "MHz" },
                "value": "240",
                "unitsSymbol": "MHz"
              },
              {
                "attribute": { "name": "RAM", "unitsName": "KB" },
                "value": "512",
                "unitsSymbol": "KB"
              }
            ],
            "distributors": [
              {
                "name": "Digi-Key Electronics",
                "sku": "1214-2057-ND",
                "leadTime": { "value": 0, "unit": "weeks" },
                "pricing": {
                  "pricingTiers": [
                    { "quantity": 1, "unitPrice": 6.50, "currency": "USD" },
                    { "quantity": 10, "unitPrice": 5.85, "currency": "USD" }
                  ]
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

---

### Query: supCategory

List available component categories.

**Input:**
```graphql
{
    supCategory {
        id
        name
        parentId
    }
}
```

**Response:**
```json
{
  "data": {
    "supCategory": [
      { "id": "cat_ic_semiconductor", "name": "Integrated Circuits", "parentId": null },
      { "id": "cat_passives", "name": "Passive Components", "parentId": null },
      { "id": "cat_resistors", "name": "Resistors", "parentId": "cat_passives" }
    ]
  }
}
```

---

### Query: supCompanySearch

Search for manufacturers and distributors.

**Input:**
```graphql
query ($q: String!, $limit: Int!) {
    supCompanySearch(q: $q, limit: $limit) {
        results {
            company {
                id
                name
                countryCode
                type
            }
        }
    }
}
```

**Variables:**
- `q` (String!) — Company name
- `limit` (Int) — Max results

---

## Part Object Fields

**Available fields when querying part objects:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | ID | Unique part identifier |
| `mpn` | String | Manufacturer Part Number |
| `name` | String | Part name/description |
| `manufacturer` | Company | Manufacturer info (id, name, countryCode) |
| `category` | Category | Component category (id, name) |
| `status` | String | ACTIVE, OBSOLETE, NRFND, etc. |
| `shortDescription` | String | Brief description |
| `bestDatasheet` | Datasheet | Primary datasheet link |
| `datasheets` | [Datasheet] | All available datasheets |
| `specs` | [Spec] | Technical specifications (attribute, value, unitsSymbol) |
| `distributors` | [Distributor] | Pricing/availability across distributors |
| `rohs` | Boolean | RoHS compliant |
| `images` | [Image] | Product images |
| `comments` | String | Community comments/notes |

---

## Distributor Fields

When querying distributor information:

| Field | Type | Description |
|-------|------|-------------|
| `id` | ID | Distributor ID |
| `name` | String | Distributor name (Digi-Key, Mouser, LCSC, etc.) |
| `sku` | String | Distributor SKU |
| `leadTime` | LeadTime | Estimated delivery time |
| `pricing` | Pricing | Price breaks and currency |
| `availability` | Int | Units in stock |
| `packaging` | String | Tape, tray, bulk, etc. |

---

## Error Handling

Common GraphQL errors:

```json
{
  "errors": [
    {
      "message": "Authentication failed",
      "extensions": { "code": "UNAUTHENTICATED" }
    }
  ]
}
```

**Common Error Codes:**
- `UNAUTHENTICATED` — Invalid/expired token
- `FORBIDDEN` — Insufficient permissions
- `BAD_USER_INPUT` — Invalid query variables
- `INTERNAL_ERROR` — Server error (retry with exponential backoff)

---

## Rate Limiting

- **Free tier:** 100 requests/hour
- **Commercial tier:** Higher limits

**Rate limit headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1634567890
```

If rate-limited (HTTP 429), wait before retrying:
```python
import time
if response.status_code == 429:
    reset_time = int(response.headers['X-RateLimit-Reset'])
    wait_seconds = reset_time - time.time()
    time.sleep(wait_seconds + 1)
```

---

## K1 Integration Patterns

### Pattern 1: Search for Resistors/Capacitors

```python
client = NexarClient(client_id, client_secret)

# Search 10k resistors
results = client.search_parts("10k 1% resistor 0805", limit=5)
for part in results:
    print(f"{part['mpn']} - {part['manufacturer']['name']}")
```

### Pattern 2: Get Pricing for BOM

```python
# BOM from design spec
bom = [
    "ESP32-S3-WROOM-1",
    "TPS54302",
    "WS2812B",
    "100µF 10V ceramic capacitor"
]

pricing = {}
for part_desc in bom:
    details = client.get_part_details(part_desc)
    if details:
        mpn = details.get('mpn')
        pricing[mpn] = {
            'distributors': details.get('distributors', []),
            'datasheet': client.get_datasheet(mpn)
        }
```

### Pattern 3: Validate Part Availability

```python
def check_availability(mpn: str, required_qty: int = 100) -> bool:
    details = client.get_part_details(mpn)
    if not details or details.get('status') != 'ACTIVE':
        return False

    for dist in details.get('distributors', []):
        if dist.get('availability', 0) >= required_qty:
            return True
    return False
```

---

## Comparison: Nexar vs LCSC vs Manual Search

| Aspect | Nexar | LCSC | Manual |
|--------|-------|------|--------|
| **Availability** | Worldwide distributors | JLC only | N/A |
| **Pricing** | Real-time cross-distributor | Real-time JLC | Outdated |
| **Datasheets** | Comprehensive | Limited | Browser search |
| **API Support** | GraphQL | REST | None |
| **Compliance** | RoHS, lead-free tracking | JLC standards | N/A |
| **Use Case** | Design validation, sourcing | JLC assembly, quick pricing | Reference only |

**K1 Strategy:**
1. Use Nexar for part validation and datasheet retrieval
2. Use LCSC for JLC-specific pricing and assembly surcharges
3. Fall back to manual search if both unavailable

---

## Resources

- **Official Docs:** https://docs.nexar.com/
- **GraphQL Explorer:** https://api.nexar.com/graphiql
- **Status Dashboard:** https://nexar-status.io/
- **Support:** https://nexar.com/support

---

## Integration with mcp-nexar Server

The K1 project includes an MCP server wrapper at `mcp/mcp-nexar/server.py` that provides:

```python
# Available tools in Claude Code:
parts_search(q: str, limit: int)    # Full-text search
part_by_mpn(mpn: str)                # Exact MPN lookup
best_datasheet_url(mpn: str)         # Get datasheet link
```

These tools automatically handle OAuth2 authentication and token caching.

---

**Last Updated:** October 23, 2025
**API Version:** 2024.10
**K1 Pipeline Integration:** Complete
