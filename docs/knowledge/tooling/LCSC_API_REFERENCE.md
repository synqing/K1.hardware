# LCSC API Reference

**Complete LCSC (JLC PCB) API Documentation**

For integration with K1 Lightwave PCB design pipeline (parts search, pricing, ordering).

---

## Overview

LCSC provides **8 RESTful API services** for automating component selection, ordering, and shipment tracking.

### Available APIs

1. **Category API** — List available component categories
2. **Manufacturer API** — Search manufacturers
3. **Categorical Item List API** — Find components by category
4. **Item Details API** — Get detailed component info + pricing + stock
5. **Keyword Search API** — Search components by part number/name
6. **Order Create API** — Submit orders
7. **Check Order API** — Track order status
8. **Get Shipment API** — Retrieve shipment information

---

## Getting Started

### Prerequisites

1. Create account at https://www.lcsc.com/
2. Submit application materials:
   - Company website
   - Business license/certificate
   - Contact info
   - Estimated order quantity
   - Cooperation mode
3. Request API key via support@lcsc.com

### Authentication

All LCSC API requests require **request validation** using:

```
Parameters required:
  - key        (API key/user ID from LCSC)
  - nonce      (random 16-bit string)
  - timestamp  (Unix timestamp of request)
  - signature  (SHA1 hash)
```

**IMPORTANT:** API secret is NOT included in request; only used for signature calculation.

### Signature Generation

```
signature = SHA1(key=XXX&nonce=XXX&secret=XXX&timestamp=XXX)
```

**Example:**

```
key=7dc6035da7874b5b9bc245bd28017290
secret=eiru73y343r36fdi
timestamp=1524662065
nonce=63yeike7dy6c2kjd

→ String for hashing:
  key=7dc6035da7874b5b9bc245bd28017290&nonce=63yeike7dy6c2kjd&secret=eiru73y343r36fdi&timestamp=1524662065

→ SHA1 result:
  5960caf5c9675e9b4cad58ef46bf722b5413e9fa
```

**Timestamp expiration:** Requests older than 60 seconds are rejected.

---

## Response Format

All API responses follow this structure:

```json
{
  "success": true,
  "code": 200,
  "message": "",
  "result": {}
}
```

| Field | Description |
|-------|-------------|
| success | Boolean: true (success) or false (error) |
| code | HTTP status code |
| message | Error message (if applicable) |
| result | Response data (varies by API) |

---

## API Endpoints

### 1. Category API

**Purpose:** Get list of component categories

**Endpoint:** `GET /api/products/getCategories`

**Parameters:**
```
key=XXX
nonce=XXX
timestamp=XXX
signature=XXX
```

**Response:**
```json
{
  "success": true,
  "code": 200,
  "result": [
    {
      "catId": 1,
      "catName": "Resistor",
      "parentId": 0
    },
    {
      "catId": 2,
      "catName": "Capacitor",
      "parentId": 0
    }
  ]
}
```

**Use case:** Get available component categories for filtering/selection

---

### 2. Manufacturer API

**Purpose:** Search manufacturers

**Endpoint:** `GET /api/products/getBrand`

**Parameters:**
```
key=XXX
nonce=XXX
timestamp=XXX
signature=XXX
brandKeyword=<search_term>  // e.g., "Texas Instruments"
```

**Response:**
```json
{
  "success": true,
  "code": 200,
  "result": [
    {
      "brandId": 1,
      "brandName": "Texas Instruments"
    },
    {
      "brandId": 2,
      "brandName": "Murata"
    }
  ]
}
```

**Use case:** Find components from specific manufacturers

---

### 3. Categorical Item List API

**Purpose:** Find components by category

**Endpoint:** `GET /api/products/getCategoryProduct`

**Parameters:**
```
key=XXX
nonce=XXX
timestamp=XXX
signature=XXX
categoryId=<category_id>     // From Category API
startPage=1                  // Pagination
pageSize=100                 // Results per page (max 100)
```

**Response:**
```json
{
  "success": true,
  "code": 200,
  "result": {
    "totalCount": 5000,
    "pageNo": 1,
    "pageSize": 100,
    "products": [
      {
        "productId": "C12345",
        "productCode": "TPS54302",
        "productName": "TPS54302 Voltage Regulator",
        "productModel": "TPS54302",
        "productBrand": "Texas Instruments",
        "productCatalog": "Power Management",
        "productPrice": "1.20",
        "productStock": "500"
      }
    ]
  }
}
```

**Use case:** Browse components by category with pagination

---

### 4. Item Details API

**Purpose:** Get full component information (spec, pricing, stock, datasheet)

**Endpoint:** `GET /api/products/getProduct`

**Parameters:**
```
key=XXX
nonce=XXX
timestamp=XXX
signature=XXX
productId=<component_id>     // From search results, e.g., "C12345"
```

**Response:**
```json
{
  "success": true,
  "code": 200,
  "result": {
    "productId": "C12345",
    "productCode": "TPS54302",
    "productName": "TPS54302 Voltage Regulator",
    "productBrand": "Texas Instruments",
    "productUnit": "1",
    "productImage": "https://image.lcsc.com/...",
    "productDatasheet": "https://datasheet.lcsc.com/...",
    "productPrice": [
      {
        "quantity": "1",
        "price": "2.50"
      },
      {
        "quantity": "10",
        "price": "2.20"
      },
      {
        "quantity": "100",
        "price": "1.80"
      }
    ],
    "productStock": "500",
    "productAttribute": [
      {
        "attributeName": "Package Type",
        "attributeValue": "LQFP-48"
      },
      {
        "attributeName": "Input Voltage",
        "attributeValue": "5V-28V"
      }
    ]
  }
}
```

**Use case:** Get complete component info for BOM including pricing at different quantities

---

### 5. Keyword Search API

**Purpose:** Search components by part number or name

**Endpoint:** `GET /api/products/getProductByKeyword`

**Parameters:**
```
key=XXX
nonce=XXX
timestamp=XXX
signature=XXX
keyword=<search_term>        // e.g., "ESP32-S3" or "C12345"
startPage=1                  // Pagination
pageSize=100                 // Results per page
```

**Response:**
```json
{
  "success": true,
  "code": 200,
  "result": {
    "totalCount": 25,
    "pageNo": 1,
    "pageSize": 100,
    "products": [
      {
        "productId": "C67890",
        "productCode": "ESP32-S3-WROOM-1",
        "productName": "ESP32-S3-WROOM-1 MCU Module",
        "productBrand": "Espressif",
        "productPrice": "3.50",
        "productStock": "1000"
      }
    ]
  }
}
```

**Use case:** Search for specific parts during BOM creation

---

### 6. Order Create API

**Purpose:** Submit orders

**Endpoint:** `POST /api/orders/submitOrder`

**Parameters (JSON body):**
```json
{
  "key": "XXX",
  "nonce": "XXX",
  "timestamp": "XXX",
  "signature": "XXX",
  "emailAddress": "user@company.com",
  "userAddress": {
    "addressType": 1,
    "addressCountry": "CN",
    "addressState": "Beijing",
    "addressCity": "Beijing",
    "addressDetail": "123 Main St",
    "postCode": "100000",
    "addressName": "Company Headquarters",
    "phoneNumber": "+86-10-1234-5678"
  },
  "currencyType": "RMB",
  "expressType": "SF",
  "paymentType": "auto",
  "poCode": "PO-2024-001",
  "productInfo": [
    {
      "productId": "C12345",
      "productAmount": "10"
    },
    {
      "productId": "C67890",
      "productAmount": "5"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "code": 200,
  "result": {
    "orderId": "LC2024001",
    "orderNo": "2024001",
    "orderTime": "2024-10-23 10:30:00",
    "totalPrice": "150.00"
  }
}
```

**Parameters:**
| Field | Description |
|-------|-------------|
| emailAddress | LCSC account email |
| userAddress | Delivery address details |
| currencyType | RMB or USD |
| expressType | Shipping method (SF, DHL, etc.) |
| paymentType | auto (credit card) or other |
| poCode | Purchase order number (optional) |
| productInfo | Array of products + quantities |

**Use case:** Automated ordering of components for PCB production

---

### 7. Check Order API

**Purpose:** Get order status and details

**Endpoint:** `GET /api/orders/getOrder`

**Parameters:**
```
key=XXX
nonce=XXX
timestamp=XXX
signature=XXX
orderNo=<order_number>       // From order creation, e.g., "2024001"
```

**Response:**
```json
{
  "success": true,
  "code": 200,
  "result": {
    "orderId": "LC2024001",
    "orderNo": "2024001",
    "orderTime": "2024-10-23 10:30:00",
    "orderStatus": "Shipped",
    "trackingNumber": "SF123456789CN",
    "totalPrice": "150.00",
    "products": [
      {
        "productId": "C12345",
        "productCode": "TPS54302",
        "productAmount": "10",
        "productPrice": "1.20"
      }
    ]
  }
}
```

**Order statuses:** pending, processing, shipped, delivered, cancelled

**Use case:** Track order progress and shipping status

---

### 8. Get Shipment API

**Purpose:** Get shipment tracking information

**Endpoint:** `POST /api/shipments/getShipment`

**Parameters (JSON body):**
```json
{
  "key": "XXX",
  "nonce": "XXX",
  "timestamp": "XXX",
  "signature": "XXX",
  "orderNo": ["2024001", "2024002"]
}
```

**Response:**
```json
{
  "success": true,
  "code": 200,
  "result": [
    {
      "orderNo": "2024001",
      "shipmentNo": "SF123456789CN",
      "shipmentProvider": "SF Express",
      "shipmentStatus": "Delivered",
      "estimateDeliveryTime": "2024-10-30",
      "trackingUrl": "https://track.sf-express.com/..."
    }
  ]
}
```

**Use case:** Track shipments of multiple orders in one call

---

## Error Codes

| Code | Description | Meaning |
|------|-------------|---------|
| 200 | Success | Request completed successfully |
| 412 | Date Is Required | Missing timestamp parameter |
| 413 | Not Found This Category | Category ID doesn't exist |
| 414 | Email not found | Account not found |
| 415 | User address error | Invalid shipping address |
| 416 | Order failed: JSON malformed | Product parameters are invalid |
| 417 | Order failed: Pro or Qty is empty | Missing product ID or quantity |
| 418 | Order failed: Express type empty | Shipping method required |
| 419 | Order failed: Invalid express type | Unsupported shipping method |
| 420 | Order failed: Qty out of range | Quantity must be 1-1 billion |
| 421 | No support pay method | Payment method not available |
| 422 | Auto pay error | Payment processing failed |
| 423 | Dealer does not exist | Account not authorized |
| 424 | Key Is Required | Missing API key |
| 425 | Nonce Is Required | Missing random nonce |
| 426 | Timestamp Is Required | Missing timestamp |
| 427 | Signature Is Required | Missing signature |
| 428 | Timestamp expired | Request older than 60 seconds |
| 429 | Not Found This Product | Product ID doesn't exist |
| 430 | Appsecret failed verification | Signature is incorrect |
| 431 | No access to information | Insufficient permissions |
| 432 | No permission | Account not authorized for operation |
| 433 | Incorrect currency | Currency type not supported |
| 434 | Check orders exceed limit | Max 10 orders per request |
| 435 | Please check your participation | Account status issue |
| 436 | RMB not supported outside Mainland | Currency/region mismatch |
| 437 | Rate limit exceeded: Retry in 1 min | Too many requests |
| 438 | Rate limit exceeded: Retry in 1 day | Daily limit exceeded |
| 439 | PO code exceeds 256 chars | PO code too long |
| 440 | Review items on LCSC website | Product verification needed |

---

## Rate Limiting

- **Per-minute limit:** Specified in error 437 (retry after 1 min)
- **Per-day limit:** Specified in error 438 (retry after 1 day)
- **Recommended:** Implement exponential backoff + caching

---

## Security & Terms of Use

**Restrictions:**

- ❌ No bulk data capture
- ❌ Don't share datasheets/images with 3rd parties
- ❌ Don't resell data
- ❌ Don't share API keys
- ❌ Don't expose API secrets
- ❌ Don't reverse-engineer APIs
- ❌ Don't stress-test or DDoS

**Compliance:**

- ✅ Identify LCSC as data source
- ✅ Follow return policies
- ✅ Comply with laws & regulations
- ✅ Don't aggregate into competing APIs

---

## Implementation Example (Python)

```python
import hashlib
import time
import random
import requests
from datetime import datetime

class LCSCClient:
    BASE_URL = "https://api.lcsc.com"

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def _generate_signature(self, nonce: str, timestamp: int) -> str:
        """Generate SHA1 signature for LCSC authentication"""
        sig_string = f"key={self.api_key}&nonce={nonce}&secret={self.api_secret}&timestamp={timestamp}"
        return hashlib.sha1(sig_string.encode()).hexdigest()

    def _get_auth_params(self) -> dict:
        """Generate authentication parameters"""
        nonce = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
        timestamp = int(time.time())
        signature = self._generate_signature(nonce, timestamp)

        return {
            'key': self.api_key,
            'nonce': nonce,
            'timestamp': timestamp,
            'signature': signature
        }

    def search_product(self, keyword: str, page: int = 1, page_size: int = 50) -> dict:
        """Search for products by keyword"""
        params = self._get_auth_params()
        params.update({
            'keyword': keyword,
            'startPage': page,
            'pageSize': page_size
        })

        response = requests.get(f"{self.BASE_URL}/api/products/getProductByKeyword", params=params)
        return response.json()

    def get_product_details(self, product_id: str) -> dict:
        """Get full product information including pricing"""
        params = self._get_auth_params()
        params['productId'] = product_id

        response = requests.get(f"{self.BASE_URL}/api/products/getProduct", params=params)
        return response.json()

    def get_categories(self) -> dict:
        """Get list of component categories"""
        params = self._get_auth_params()
        response = requests.get(f"{self.BASE_URL}/api/products/getCategories", params=params)
        return response.json()

# Usage example
client = LCSCClient("your_api_key", "your_api_secret")

# Search for resistors
results = client.search_product("10k resistor", page=1, page_size=20)
print(f"Found {results['result']['totalCount']} resistors")

# Get details on first result
if results['result']['products']:
    product = results['result']['products'][0]
    details = client.get_product_details(product['productId'])
    print(f"Price: {details['result']['productPrice']}")
    print(f"Stock: {details['result']['productStock']}")
```

---

## Integration with K1 Lightwave PCB Pipeline

The **mcp-lcsc** MCP server wraps these APIs and exposes them to Claude Code agents:

```python
# In kicad-part-picker skill
from mcp_lcsc import lcsc_search, lcsc_get_pricing, lcsc_check_stock

def pick_parts(bom: List[Part]) -> List[MPN]:
    """Select orderable MPNs for each BOM line item"""
    results = []

    for part in bom:
        # Search LCSC
        search_result = lcsc_search(part.value, part.voltage)

        # Get pricing for quantities [1, 10, 100, 1000]
        pricing = lcsc_get_pricing(search_result[0]['product_id'])

        # Check stock
        stock = lcsc_check_stock(search_result[0]['product_id'])

        results.append({
            'lcsc_id': search_result[0]['product_id'],
            'mfg_part_number': search_result[0]['mfg_code'],
            'price': pricing,
            'stock': stock
        })

    return results
```

---

## Resources

- **LCSC Main:** https://www.lcsc.com/
- **LCSC Support:** support@lcsc.com
- **OpenAPI Docs:** https://www.lcsc.com/docs/openapi/
- **Terms of Use:** https://support.lcsc.com/article/20-terms

---

## Latest Updates

- **API Version:** 2.0 (as of 2024)
- **Last Updated:** 2024-10-23
- **Documentation Status:** Complete

For real-time updates and OpenAPI schema, visit: https://www.lcsc.com/docs/index.html
