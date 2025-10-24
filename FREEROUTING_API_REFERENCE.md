# FreeRouting API Reference (Cloud + CLI + Python Client)

## Table of Contents
1. [REST API (Cloud)](#rest-api-cloud)
2. [CLI Arguments (Local)](#cli-arguments-local)
3. [Python Client Library](#python-client-library)
4. [Implementation Examples](#implementation-examples)

---

## REST API (Cloud)

### Endpoint Root
```
https://api.freerouting.app/v1
```

### Authentication
**Method:** Bearer Token (API Key)

**Headers:**
```
Authorization: Bearer <FREEROUTING_API_KEY>
Content-Type: application/json
```

**Get API Key:** https://www.freerouting.app/ (Free account)

### Endpoints

#### 1. System Status

**Endpoint:** `GET /system/status`

**Purpose:** Check API health

**Request:**
```bash
curl -H "Authorization: Bearer $FREEROUTING_API_KEY" \
  https://api.freerouting.app/v1/system/status
```

**Response:**
```json
{
  "status": "healthy",
  "version": "2.1.0",
  "timestamp": "2025-10-24T12:34:56Z"
}
```

**Status Codes:**
- `200`: API is healthy
- `503`: Service unavailable

#### 2. Create Routing Session

**Endpoint:** `POST /sessions`

**Purpose:** Create a new routing session for a design

**Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer $FREEROUTING_API_KEY" \
  -H "Content-Type: application/json" \
  https://api.freerouting.app/v1/sessions \
  -d '{
    "name": "K1_Lightwave_v1",
    "description": "K1 Lightwave PCB autorouting"
  }'
```

**Request Body:**
```json
{
  "name": "string (required)",
  "description": "string (optional)"
}
```

**Response:**
```json
{
  "session_id": "uuid-12345",
  "name": "K1_Lightwave_v1",
  "created_at": "2025-10-24T12:00:00Z",
  "status": "created"
}
```

**Status Codes:**
- `201`: Session created successfully
- `400`: Invalid request
- `401`: Unauthorized

#### 3. Upload Design (DSN)

**Endpoint:** `POST /sessions/{session_id}/upload`

**Purpose:** Upload DSN file for routing

**Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer $FREEROUTING_API_KEY" \
  https://api.freerouting.app/v1/sessions/{session_id}/upload \
  -F "file=@board.dsn"
```

**Form Data:**
```
file: <DSN file binary>
```

**Response:**
```json
{
  "session_id": "uuid-12345",
  "file_name": "board.dsn",
  "file_size": 125000,
  "upload_time": "2025-10-24T12:01:00Z",
  "status": "uploaded"
}
```

**Status Codes:**
- `200`: File uploaded successfully
- `400`: Invalid file format
- `413`: File too large

#### 4. Start Routing Job

**Endpoint:** `POST /sessions/{session_id}/route`

**Purpose:** Begin autorouting process

**Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer $FREEROUTING_API_KEY" \
  -H "Content-Type: application/json" \
  https://api.freerouting.app/v1/sessions/{session_id}/route \
  -d '{
    "routing_options": {
      "threads": 4,
      "iterations": 100,
      "time_limit": 3600
    }
  }'
```

**Request Body:**
```json
{
  "routing_options": {
    "threads": 4,
    "iterations": 100,
    "time_limit": 3600,
    "routing_mode": "walkaround"
  }
}
```

**Response:**
```json
{
  "job_id": "job-uuid-54321",
  "session_id": "uuid-12345",
  "status": "processing",
  "started_at": "2025-10-24T12:02:00Z"
}
```

**Status Codes:**
- `202`: Job accepted and processing
- `400`: Invalid routing options
- `409`: Session not in uploadable state

#### 5. Get Job Status

**Endpoint:** `GET /sessions/{session_id}/jobs/{job_id}`

**Purpose:** Poll routing progress

**Request:**
```bash
curl -H "Authorization: Bearer $FREEROUTING_API_KEY" \
  https://api.freerouting.app/v1/sessions/{session_id}/jobs/{job_id}
```

**Response (In Progress):**
```json
{
  "job_id": "job-uuid-54321",
  "status": "processing",
  "progress": {
    "nets_routed": 145,
    "total_nets": 200,
    "percentage": 72.5,
    "elapsed_seconds": 450
  }
}
```

**Response (Complete):**
```json
{
  "job_id": "job-uuid-54321",
  "status": "complete",
  "progress": {
    "nets_routed": 200,
    "total_nets": 200,
    "percentage": 100,
    "elapsed_seconds": 1200
  },
  "completed_at": "2025-10-24T12:22:00Z",
  "results": {
    "total_violations": 0,
    "routing_time": "20m 34s"
  }
}
```

**Status Codes:**
- `200`: Job status returned
- `404`: Job not found

#### 6. Download Results (SES)

**Endpoint:** `GET /sessions/{session_id}/results/download`

**Purpose:** Download routed SES file

**Request:**
```bash
curl -H "Authorization: Bearer $FREEROUTING_API_KEY" \
  -o board.ses \
  https://api.freerouting.app/v1/sessions/{session_id}/results/download
```

**Response (Binary):**
```
[SES file binary data]
```

**Status Codes:**
- `200`: File download
- `202`: Job still processing
- `404`: Results not available

---

## CLI Arguments (Local)

### Basic Syntax

```bash
java -jar freerouting-2.1.0.jar [options]
```

### Complete Argument Reference

#### Input/Output

| Argument | Type | Default | Purpose | Example |
|----------|------|---------|---------|---------|
| `-de` | path | None | Design input (DSN file) | `-de board.dsn` |
| `-do` | path | None | Design output (SES file) | `-do board.ses` |

#### Routing Control

| Argument | Type | Default | Purpose | Example |
|----------|------|---------|---------|---------|
| `-mt` | int | 1 | Thread count | `-mt 4` |
| `-oit` | int | 100 | Iterations (0=infinite) | `-oit 1000` |
| `-ps` | int | 100 | Population size | `-ps 200` |
| `-cc` | int | 100 | Cost convergence | `-cc 50` |
| `-sm` | flag | - | Single mode | `-sm` |
| `-dr` | path | - | Design rules file | `-dr rules.rules` |

#### Options

| Argument | Type | Default | Purpose | Example |
|----------|------|---------|---------|---------|
| `-inc` | list | - | Skip nets | `-inc GND,VCC` |
| `-ex` | list | - | Export only nets | `-ex CLK,RESET` |
| `--gui.enabled` | bool | true | Enable GUI | `--gui.enabled=false` |
| `-dl` | flag | - | Disable logging | `-dl` |
| `-oit` | int | 100 | Time limit (seconds) | `-oit 3600` |

#### Logging

| Argument | Type | Default | Purpose | Example |
|----------|------|---------|---------|---------|
| `-dl` | flag | - | Disable logging | `-dl` |
| `-log` | path | - | Log file path | `-log routing.log` |

### Complete CLI Examples

#### Example 1: Basic Headless Routing
```bash
java -Djava.awt.headless=true \
  -jar freerouting-2.1.0.jar \
  -de board.dsn \
  -do board.ses \
  --gui.enabled=false
```

#### Example 2: Multi-threaded with Custom Iterations
```bash
java -Djava.awt.headless=true \
  -Xmx4g \
  -jar freerouting-2.1.0.jar \
  -de board.dsn \
  -do board.ses \
  -mt 8 \
  -oit 500 \
  --gui.enabled=false
```

#### Example 3: Skip Power Nets, Enable Logging
```bash
java -Djava.awt.headless=true \
  -jar freerouting-2.1.0.jar \
  -de board.dsn \
  -do board.ses \
  -inc GND,VCC,5V \
  -log routing.log \
  --gui.enabled=false
```

#### Example 4: Load Custom Design Rules
```bash
java -Djava.awt.headless=true \
  -jar freerouting-2.1.0.jar \
  -de board.dsn \
  -do board.ses \
  -dr design_rules.rules \
  -mt 4 \
  --gui.enabled=false
```

#### Example 5: Time-Limited Routing (30 minutes max)
```bash
java -Djava.awt.headless=true \
  -jar freerouting-2.1.0.jar \
  -de board.dsn \
  -do board.ses \
  -oit 1800 \
  -mt 4 \
  --gui.enabled=false
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Routing successful |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | File not found |
| 4 | Routing incomplete (timeout or iteration limit) |

---

## Python Client Library

### Installation

```bash
pip install freerouting-client
```

### Client Initialization

```python
from freerouting import FreeroutingClient
import os

api_key = os.environ.get("FREEROUTING_API_KEY")
if not api_key:
    raise ValueError("FREEROUTING_API_KEY environment variable not set")

client = FreeroutingClient(api_key=api_key)
```

### Available Methods

#### 1. System Status

```python
status = client.get_system_status()
print(f"FreeRouting API: {status['status']}")
# Output: FreeRouting API: healthy
```

#### 2. Create Session

```python
session = client.create_session(
    name="K1_Lightwave_v1",
    description="K1 PCB autorouting test"
)
session_id = session['session_id']
print(f"Created session: {session_id}")
```

#### 3. Upload Design

```python
result = client.upload_design(
    session_id=session_id,
    dsn_file_path="/path/to/board.dsn"
)
print(f"Uploaded: {result['file_size']} bytes")
```

#### 4. Start Routing

```python
job = client.start_routing_job(
    session_id=session_id,
    threads=4,
    iterations=100,
    time_limit=3600
)
job_id = job['job_id']
print(f"Routing started: {job_id}")
```

#### 5. Poll Job Status

```python
import time

while True:
    status = client.get_job_status(
        session_id=session_id,
        job_id=job_id
    )

    if status['status'] == 'processing':
        progress = status['progress']
        print(f"Progress: {progress['percentage']:.1f}% "
              f"({progress['nets_routed']}/{progress['total_nets']} nets)")
        time.sleep(10)
    elif status['status'] == 'complete':
        print(f"Routing complete in {status['results']['routing_time']}")
        break
    else:
        print(f"Job status: {status['status']}")
        break
```

#### 6. Download Results

```python
import base64

result_data = client.download_results(
    session_id=session_id
)

# Save SES file
with open("board.ses", "wb") as f:
    f.write(base64.b64decode(result_data['data']))

print("Saved: board.ses")
```

#### 7. Complete Workflow (Simplified)

```python
def autoroute_board(dsn_file, output_ses):
    """Complete routing workflow using FreeRouting API."""

    # Initialize client
    client = FreeroutingClient(api_key=os.environ["FREEROUTING_API_KEY"])

    # Check API health
    status = client.get_system_status()
    if status['status'] != 'healthy':
        raise Exception("FreeRouting API not healthy")

    # Create session
    session = client.create_session(name="autoroute_test")
    session_id = session['session_id']

    # Upload design
    print("Uploading DSN...")
    client.upload_design(session_id, dsn_file)

    # Start routing
    print("Starting routing...")
    job = client.start_routing_job(
        session_id=session_id,
        threads=4,
        iterations=100,
        time_limit=3600
    )
    job_id = job['job_id']

    # Poll until complete
    print("Waiting for routing...")
    import time
    while True:
        status = client.get_job_status(session_id, job_id)

        if status['status'] == 'complete':
            break
        elif status['status'] == 'processing':
            progress = status['progress']
            print(f"  {progress['percentage']:.1f}% complete")
            time.sleep(10)
        else:
            raise Exception(f"Job failed: {status['status']}")

    # Download results
    print("Downloading results...")
    result = client.download_results(session_id)

    # Save SES
    with open(output_ses, "wb") as f:
        f.write(base64.b64decode(result['data']))

    print(f"✓ Routed design saved: {output_ses}")

# Usage
autoroute_board("board.dsn", "board.ses")
```

---

## Implementation Examples

### Example 1: Shell Script Wrapper

```bash
#!/bin/bash
# freeroute.sh - Wrapper for FreeRouting

set -e

BOARD="${1:-board}"
THREADS="${2:-4}"
JAR="freerouting-2.1.0.jar"

if [ ! -f "${BOARD}.dsn" ]; then
    echo "Error: ${BOARD}.dsn not found"
    exit 1
fi

echo "Routing ${BOARD}.dsn..."
java -Djava.awt.headless=true \
  -Xmx4g \
  -jar ${JAR} \
  -de ${BOARD}.dsn \
  -do ${BOARD}.ses \
  -mt ${THREADS} \
  --gui.enabled=false

if [ -f "${BOARD}.ses" ]; then
    echo "✓ Routing complete: ${BOARD}.ses"
    exit 0
else
    echo "✗ Routing failed"
    exit 1
fi
```

**Usage:**
```bash
chmod +x freeroute.sh
./freeroute.sh board 4    # Routes board.dsn using 4 threads
```

### Example 2: Python Integration (Complete)

```python
#!/usr/bin/env python3
"""
kicad_autoroute.py - KiCad + FreeRouting integration

This script:
1. Exports KiCad PCB to DSN
2. Routes with FreeRouting
3. Imports SES back to KiCad
4. Runs DRC verification
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import argparse

class KiCadAutorouter:
    def __init__(self, pcb_file, work_dir="/tmp/routing"):
        self.pcb_file = Path(pcb_file)
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(exist_ok=True)

        if not self.pcb_file.exists():
            raise FileNotFoundError(f"PCB file not found: {pcb_file}")

    def export_dsn(self):
        """Export KiCad PCB to Specctra DSN."""
        print("Exporting to Specctra DSN...")

        sys.path.insert(0, "/Applications/KiCad/KiCad.app/Contents/SharedSupport/scripting")
        from pcbnew import DSN

        db = DSN.SPECCTRA_DB()
        db.LoadPCB(str(self.pcb_file))

        dsn_file = self.work_dir / f"{self.pcb_file.stem}.dsn"
        db.ExportPCB(str(dsn_file))

        print(f"✓ DSN exported: {dsn_file}")
        return dsn_file

    def route(self, dsn_file, threads=4, iterations=100):
        """Route with FreeRouting."""
        print(f"Routing with FreeRouting ({threads} threads)...")

        ses_file = dsn_file.with_suffix(".ses")

        cmd = [
            "java",
            "-Djava.awt.headless=true",
            "-Xmx4g",
            "-jar", "freerouting-2.1.0.jar",
            "-de", str(dsn_file),
            "-do", str(ses_file),
            "-mt", str(threads),
            "-oit", str(iterations),
            "--gui.enabled=false"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ Routing failed:\n{result.stderr}")
            return None

        if not ses_file.exists():
            print("✗ SES file not created")
            return None

        print(f"✓ Routing complete: {ses_file}")
        return ses_file

    def import_ses(self, ses_file):
        """Import routed SES back to KiCad."""
        print("Importing routed design...")

        sys.path.insert(0, "/Applications/KiCad/KiCad.app/Contents/SharedSupport/scripting")
        import pcbnew
        from pcbnew import DSN

        board = pcbnew.LoadBoard(str(self.pcb_file))
        db = DSN.SPECCTRA_DB()
        db.LoadSESSION(str(ses_file))
        db.ImportSession(board)

        output_pcb = self.pcb_file.parent / f"{self.pcb_file.stem}_routed.kicad_pcb"
        board.Save(str(output_pcb))

        print(f"✓ Routed design saved: {output_pcb}")
        return output_pcb

    def drc_check(self, pcb_file):
        """Run DRC check."""
        print("Running DRC...")

        drc_report = self.work_dir / "drc.json"

        cmd = [
            "kicad-cli", "pcb", "drc",
            str(pcb_file),
            "--output", "json",
            "--output-file", str(drc_report)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        try:
            with open(drc_report) as f:
                data = json.load(f)
            violations = data.get("violations", [])

            if violations:
                print(f"⚠ {len(violations)} DRC violations found")
                return False
            else:
                print("✓ No DRC violations")
                return True
        except Exception as e:
            print(f"Could not parse DRC results: {e}")
            return None

    def autoroute(self, threads=4, iterations=100, verify=True):
        """Complete autorouting workflow."""
        try:
            dsn_file = self.export_dsn()
            ses_file = self.route(dsn_file, threads, iterations)

            if not ses_file:
                return False

            routed_pcb = self.import_ses(ses_file)

            if verify:
                drc_ok = self.drc_check(routed_pcb)
                if drc_ok is False:
                    print("\n⚠ Routing complete but DRC violations present")
                    return False

            print("\n✓ Autorouting successful")
            return True

        except Exception as e:
            print(f"\n✗ Error: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="KiCad PCB Autorouter")
    parser.add_argument("pcb_file", help="KiCad PCB file")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Thread count")
    parser.add_argument("-i", "--iterations", type=int, default=100, help="Routing iterations")
    parser.add_argument("--no-drc", action="store_true", help="Skip DRC check")

    args = parser.parse_args()

    autorouter = KiCadAutorouter(args.pcb_file)
    success = autorouter.autoroute(
        threads=args.threads,
        iterations=args.iterations,
        verify=not args.no_drc
    )

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
python3 kicad_autoroute.py board.kicad_pcb -t 8 -i 500
```

---

## API Status Codes Reference

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 202 | Accepted | Job accepted (async) |
| 400 | Bad Request | Fix request parameters |
| 401 | Unauthorized | Check API key |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Invalid session state |
| 413 | Payload Too Large | File too large |
| 429 | Rate Limited | Wait before retry |
| 500 | Server Error | API error, contact support |
| 503 | Unavailable | Service down, retry later |

### Job Status Values

| Status | Meaning | Next Action |
|--------|---------|------------|
| `created` | Session created | Upload DSN |
| `uploaded` | DSN uploaded | Start routing job |
| `processing` | Routing in progress | Poll for status |
| `complete` | Routing finished | Download SES |
| `failed` | Routing failed | Check error message |
| `cancelled` | User cancelled | Restart if needed |

---

## Best Practices

### 1. Error Handling

```python
try:
    client = FreeroutingClient(api_key=api_key)
    status = client.get_system_status()
except ConnectionError:
    print("Cannot reach FreeRouting API")
except ValueError as e:
    print(f"API error: {e}")
```

### 2. Timeout Management

```python
import time

max_wait = 3600  # 1 hour max
start_time = time.time()

while True:
    elapsed = time.time() - start_time
    if elapsed > max_wait:
        print("Routing timeout")
        break

    # Poll status
    status = client.get_job_status(...)
    time.sleep(10)
```

### 3. Resource Cleanup

```python
try:
    # Do routing...
    pass
finally:
    # Always cleanup
    if session_id:
        client.delete_session(session_id)
```

### 4. Retry Logic

```python
def retry_upload(dsn_file, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            result = client.upload_design(session_id, dsn_file)
            return result
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

---

## References

- **FreeRouting GitHub:** https://github.com/freerouting/freerouting
- **FreeRouting Python Client:** https://github.com/freerouting/freerouting-python-client
- **FreeRouting API Docs:** https://api.freerouting.app/docs (requires auth)
- **API Status Dashboard:** https://status.freerouting.app/

---

**API Reference Version:** 1.0
**Last Updated:** 2025-10-24
**Status:** Complete Technical Reference
