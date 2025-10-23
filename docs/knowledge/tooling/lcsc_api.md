# LCSC Electronics API Guide

## Overview

LCSC (JLC Electronics) provides an OpenAPI for programmatic component lookup, pricing, inventory, and availability data. This enables automated vendor synchronization and component resolution.

## API Endpoint

**Base URL**: `https://api.lcsc.com/v1/`

**Authentication**: API Key-based (requires account setup at lcsc.com)

## Getting Credentials

1. Sign up / Log in at [https://www.lcsc.com/](https://www.lcsc.com/)
2. Navigate to **Account Settings** → **API Interface** (or similar)
3. Generate API Key and Secret
4. Store securely (treat like passwords)

## Common Endpoints

### Component Search

**Endpoint**: `GET /products/search`

**Parameters**:
- `keyword`: Search term (C-number, MPN, value, description)
- `limit`: Results per page (1-100, default 50)
- `page`: Page number (for pagination)
- `start`: Result start index

**Example**:
```
GET https://api.lcsc.com/v1/products/search?keyword=ESP32-S3&limit=10
```

**Response**:
```json
{
  "data": {
    "products": [
      {
        "productCode": "C12345",
        "productName": "ESP32-S3-WROOM-1",
        "productModel": "ESP32-S3-WROOM-1",
        "onSale": true,
        "stock": 1500,
        "minOrder": 1,
        "price": [
          {"ladder": 1, "priceusd": 4.25},
          {"ladder": 100, "priceusd": 3.50}
        ],
        "specificationList": [...],
        "datasheet": "https://..."
      }
    ],
    "totalCount": 25
  }
}
```

### Component Details by C-Number

**Endpoint**: `GET /products/{productCode}`

**Parameters**:
- `productCode`: LCSC C-number (e.g., "C2653")

**Example**:
```
GET https://api.lcsc.com/v1/products/C2653
```

**Response**: Full product details including specifications, pricing tiers, datasheet link.

## Request Authentication

LCSC API uses **signed requests** with time-limited tokens.

### Signing Process (Pseudocode)

```python
import hashlib
import hmac
import time
import json

api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"

def sign_request(method, endpoint, params):
    timestamp = int(time.time() * 1000)  # Milliseconds
    auth_string = f"{method} {endpoint} {timestamp}"
    signature = hmac.new(
        api_secret.encode(),
        auth_string.encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Authorization": f"Bearer {api_key}:{signature}:{timestamp}"
    }
    return headers
```

### Time Limit

Signatures are valid for 60 seconds. Ensure server time is synchronized.

## Common Use Cases

### 1. Lookup Component by C-Number

**Task**: Find LCSC product "C2653"

```bash
curl -X GET "https://api.lcsc.com/v1/products/C2653" \
  -H "Authorization: Bearer API_KEY:SIGNATURE:TIMESTAMP"
```

**Response**: Full product details (specs, pricing, stock, datasheet).

### 2. Search by Keyword

**Task**: Find all 10µF capacitors in stock

```bash
curl -X GET "https://api.lcsc.com/v1/products/search?keyword=10µF%20capacitor&limit=20"
```

### 3. Resolve MPN to C-Number

**Task**: Convert MPN "GRM31CR61H106KA19L" (Murata 10µF cap) to LCSC C-number

```bash
curl -X GET "https://api.lcsc.com/v1/products/search?keyword=GRM31CR61H106KA19L"
```

Response includes matching LCSC product code.

## Batch Operations

For **fabops vendor_sync()**, typical batch query:

```python
def resolve_mpns_to_lcsc(mpn_list):
    """Convert list of MPNs to LCSC C-numbers"""
    results = {}
    for mpn in mpn_list:
        response = api_search(keyword=mpn)
        if response['data']['totalCount'] > 0:
            c_num = response['data']['products'][0]['productCode']
            results[mpn] = c_num
    return results
```

## Rate Limiting

- No published rate limit, but avoid excessive parallel requests
- Recommended: 1-2 requests/second
- Implement retry logic with exponential backoff

## Error Handling

**Common HTTP Status Codes**:
- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Invalid/expired credentials
- `404 Not Found` - Product not found
- `429 Too Many Requests` - Rate limited

**Response Error Format**:
```json
{
  "code": "ERROR_CODE",
  "message": "Human-readable error description"
}
```

## Key Response Fields

| Field | Meaning |
|-------|---------|
| `productCode` | LCSC C-number (unique identifier) |
| `productName` | Full product description |
| `stock` | Quantity in stock |
| `minOrder` | Minimum order quantity |
| `price` | Array of price tiers based on quantity |
| `datasheet` | Link to component datasheet PDF |
| `onSale` | Boolean: is product currently available for order |
| `manufacturer` | Component manufacturer (e.g., "Murata", "TI") |

## For K1 Lightwave Vendor Sync

**mcp-fabops** `vendor_sync()` workflow:

1. Extract BOM from schematic (MPN field)
2. For each MPN without LCSC C-number:
   - Call `products/search?keyword={MPN}`
   - Extract `productCode` (C-number)
   - Write C-number back to schematic
3. Update BOM for JLCPCB assembly

**Example**:
```python
# From BOM: ESP32-S3-WROOM-1 (no LCSC assigned)
response = api.search(keyword="ESP32-S3-WROOM-1")
c_number = response["products"][0]["productCode"]
# Write to schematic: LCSC field = "C2653" (example)
```

## Data Persistence

Store resolved C-numbers in:
- Schematic symbol **LCSC** custom field
- BOM spreadsheet
- Component library for future reuse

## Best Practices

1. **Cache results** - Don't query same MPN twice in one session
2. **Handle network errors** - Implement retry with backoff
3. **Store credentials** - Use environment variables (not hardcoded)
4. **Validate C-numbers** - Double-check pricing/availability before ordering
5. **Check stock levels** - Verify "stock > minOrder" before committing to BOM

**Note**: This is a summary. For latest API details, consult [LCSC Developer Documentation](https://dev.lcsc.com/).

Source: LCSC API Documentation (cached)
