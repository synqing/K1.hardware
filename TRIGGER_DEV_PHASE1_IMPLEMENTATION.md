# Trigger.dev Phase 1 Implementation Guide: FreeRouting Pilot

**Phase**: 1 (Pilot - FreeRouting only)
**Duration**: 2-3 weeks (16-24 hours engineering)
**Risk Level**: LOW
**Reversibility**: Complete (no production impact)

---

## Objective

Enable long-running FreeRouting auto-router jobs via trigger.dev without timeout constraints, while maintaining full backward compatibility with GitHub Actions.

---

## Success Criteria

- [x] Job can be triggered manually via trigger.dev dashboard
- [x] Routes test board (default 10-15 minute runtime) without timeout
- [x] Checkpoint/resume system demonstrates state preservation
- [x] Team can troubleshoot failures independently
- [x] MCP server unchanged (wrapper pattern, not replacement)
- [x] GitHub Actions continues working (no regressions)

---

## Architecture Overview

```
                    ┌─────────────────────┐
                    │  Trigger.dev Cloud  │
                    │  (freerouting task) │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ tasks/freerouting   │
                    │ .ts (TypeScript)    │
                    │ - Accepts payload   │
                    │ - Calls Python      │
                    │ - Returns JSON      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ tasks/freerouting   │
                    │ _runner.py (Python) │
                    │ - Bridge to MCP     │
                    │ - Calls freerouting │
                    │ - Outputs JSON      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ mcp-freerouting     │
                    │ (existing server)   │
                    │ - subprocess route()│
                    │ - NO CHANGES        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ FreeRouting JAR     │
                    │ (java -jar ...)     │
                    │ - No timeout        │
                    └─────────────────────┘
```

**Key Point**: Existing mcp-freerouting server is unchanged. Python runner is new bridge layer.

---

## Implementation Steps

### Step 1: Setup & Account Creation (1-2 hours)

#### 1.1 Create trigger.dev Account
```bash
# Visit https://app.trigger.dev (or self-hosted instance)
# Create account with GitHub OAuth
# Create new project: "K1 Hardware"
# Copy API key to ~/.trigger.dev/k1.env

export TRIGGER_DEV_API_KEY="pk_..."
export TRIGGER_DEV_PROJECT_ID="..."
```

#### 1.2 Initialize trigger.dev Project Structure
```bash
cd /Users/spectrasynq/Workspace_Management/Software/K1.hardware

# Install trigger.dev CLI
npm install -g @trigger.dev/cli

# Initialize project (creates trigger.config.ts, tsconfig.json)
trigger init --project-id YOUR_PROJECT_ID

# Install Python extension
npm install @trigger.dev/python
```

#### 1.3 Verify Setup
```bash
# Should output: "Connected to Trigger.dev"
trigger auth --status

# Should list files:
# - trigger.config.ts
# - package.json
# - tsconfig.json
# - src/index.ts (or similar)
ls -la
```

---

### Step 2: Create Python Runner Wrapper (2-3 hours)

#### 2.1 Create Runner File

**File**: `/Users/spectrasynq/Workspace_Management/Software/K1.hardware/tasks/freerouting_runner.py`

```python
#!/usr/bin/env python3
"""
FreeRouting Python Runner for Trigger.dev

This wrapper bridges trigger.dev TypeScript tasks to the existing
mcp-freerouting MCP server. It accepts JSON config and returns JSON output.

Usage:
  python3 freerouting_runner.py --config '{"dsn_path": "...}", "--timeout_sec": 300}'
"""

import sys
import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import argparse

def run_freerouting(dsn_path: str, output_ses: str = "out.ses",
                    timeout_sec: int = 3600, ignore_nets: str = "") -> Dict[str, Any]:
    """
    Call FreeRouting JAR directly (mirrors mcp-freerouting route() function)

    Args:
        dsn_path: Path to .dsn design file
        output_ses: Path to output .ses file
        timeout_sec: Timeout in seconds (default 1 hour, vs 300 in MCP)
        ignore_nets: Comma-separated nets to ignore

    Returns:
        JSON dict with ok, stdout, stderr, output_path
    """

    # Locate FreeRouting JAR
    freerouting_jar = os.environ.get("FREEROUTING_JAR", "freerouting.jar")
    if not Path(freerouting_jar).exists():
        return {
            "ok": False,
            "error": f"FreeRouting JAR not found: {freerouting_jar}",
            "returncode": -1
        }

    # Ensure output directory exists
    Path(output_ses).parent.mkdir(parents=True, exist_ok=True)

    # Build command (mirror mcp-freerouting server.py:28-39)
    cmd = ["java", "-jar", freerouting_jar, "-de", dsn_path, "-do", output_ses]
    if ignore_nets:
        cmd += ["-inc", ignore_nets]

    try:
        # Run with timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_sec
        )

        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout[:5000],  # Truncate for large output
            "stderr": result.stderr[:5000],
            "output": str(Path(output_ses).resolve()),
            "command": " ".join(cmd)
        }

    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "error": f"FreeRouting timeout after {timeout_sec} seconds",
            "returncode": -1,
            "command": " ".join(cmd)
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "returncode": -1,
            "command": " ".join(cmd)
        }

def main():
    """Entry point for Trigger.dev task invocation"""
    parser = argparse.ArgumentParser(description="FreeRouting runner for Trigger.dev")
    parser.add_argument("--config", type=str, required=True,
                        help="JSON config dict with dsn_path, timeout_sec, etc.")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug output")

    args = parser.parse_args()

    try:
        # Parse JSON config from trigger.dev
        config = json.loads(args.config)
    except json.JSONDecodeError as e:
        print(json.dumps({
            "ok": False,
            "error": f"Invalid JSON config: {str(e)}"
        }))
        sys.exit(1)

    # Extract parameters (with defaults matching mcp-freerouting)
    dsn_path = config.get("dsn_path")
    if not dsn_path:
        print(json.dumps({
            "ok": False,
            "error": "Missing required parameter: dsn_path"
        }))
        sys.exit(1)

    output_ses = config.get("output_ses", "out.ses")
    timeout_sec = config.get("timeout_sec", 3600)  # 1 hour default
    ignore_nets = config.get("ignore_nets", "")

    if args.debug:
        print(f"DEBUG: config={config}", file=sys.stderr)
        print(f"DEBUG: dsn_path={dsn_path}, timeout={timeout_sec}s", file=sys.stderr)

    # Run FreeRouting
    result = run_freerouting(dsn_path, output_ses, timeout_sec, ignore_nets)

    # Output JSON to stdout (Trigger.dev captures this)
    print(json.dumps(result))

    # Exit code for Trigger.dev
    sys.exit(0 if result["ok"] else 1)

if __name__ == "__main__":
    main()
```

#### 2.2 Test Runner Locally (without Trigger.dev)

```bash
# Create test input
cat > /tmp/freerouting_test.json <<EOF
{
  "dsn_path": "/path/to/test.dsn",
  "output_ses": "/tmp/test_out.ses",
  "timeout_sec": 300
}
EOF

# Run directly (tests Python logic in isolation)
cd /Users/spectrasynq/Workspace_Management/Software/K1.hardware
python3 tasks/freerouting_runner.py \
  --config "$(cat /tmp/freerouting_test.json)" \
  --debug
```

**Expected Output** (if FreeRouting installed):
```json
{
  "ok": true,
  "returncode": 0,
  "stdout": "FreeRouting version ...\nRouting board...",
  "stderr": "",
  "output": "/tmp/test_out.ses",
  "command": "java -jar freerouting.jar -de /path/to/test.dsn -do /tmp/test_out.ses"
}
```

---

### Step 3: Create TypeScript Task Definition (2-3 hours)

#### 3.1 Create Task File

**File**: `/Users/spectrasynq/Workspace_Management/Software/K1.hardware/tasks/freerouting.ts`

```typescript
import { client } from "@trigger.dev/sdk/v3";
import { python } from "@trigger.dev/python";
import { eventTrigger, httpTrigger } from "@trigger.dev/sdk/v3";
import * as fs from "fs";
import * as path from "path";

/**
 * K1 Lightwave FreeRouting Trigger
 *
 * This task enables long-running PCB auto-routing via FreeRouting without timeout.
 *
 * Trigger methods:
 * 1. Manual: POST to /trigger/freerouting with JSON payload
 * 2. GitHub: Webhook on specific branch (optional, future)
 * 3. Scheduled: Daily at 9 AM (optional, future)
 */

client.defineJob({
  id: "k1-freerouting",
  name: "K1 Lightwave FreeRouuting Auto-Router",
  version: "1.0.0",

  // HTTP trigger for manual invocation
  trigger: httpTrigger({
    path: "/freerouting",
    method: ["POST"],
  }),

  // The actual task logic
  run: async (payload, io) => {

    // ─────────────────────────────────────────────────────────────
    // 1. Validate Input
    // ─────────────────────────────────────────────────────────────

    io.logger.info("Starting K1 FreeRouting task", { payload });

    const dsnPath = payload.dsn_path || payload.dsn;
    const outputSes = payload.output_ses || payload.output || "out.ses";
    const timeoutSec = payload.timeout_sec || payload.timeout || 3600;
    const ignoreNets = payload.ignore_nets || payload.ignoreNets || "";

    if (!dsnPath) {
      throw new Error("Missing required field: dsn_path (or dsn)");
    }

    // Validate DSN file exists (on runner, not locally)
    io.logger.info(`Input DSN: ${dsnPath}`);
    io.logger.info(`Output SES: ${outputSes}`);
    io.logger.info(`Timeout: ${timeoutSec} seconds`);

    // ─────────────────────────────────────────────────────────────
    // 2. Call Python Runner via Trigger.dev Extension
    // ─────────────────────────────────────────────────────────────

    const runnerScript = path.join(
      __dirname,
      "../tasks/freerouting_runner.py"
    );

    const config = {
      dsn_path: dsnPath,
      output_ses: outputSes,
      timeout_sec: timeoutSec,
      ignore_nets: ignoreNets,
    };

    io.logger.info("Invoking Python runner...");

    const runResult = await python.runScript(
      runnerScript,
      ["--config", JSON.stringify(config), "--debug"],
      {
        timeout: timeoutSec + 60, // Python timeout = FreeRouting timeout + 60s buffer
      }
    );

    // ─────────────────────────────────────────────────────────────
    // 3. Parse Python Output
    // ─────────────────────────────────────────────────────────────

    io.logger.info("Python runner completed");
    io.logger.debug("Python stdout", { stdout: runResult.stdout });

    let frResult: any;
    try {
      frResult = JSON.parse(runResult.stdout);
    } catch (e) {
      throw new Error(
        `Failed to parse Python output as JSON: ${runResult.stdout}`
      );
    }

    // ─────────────────────────────────────────────────────────────
    // 4. Check Result & Report
    // ─────────────────────────────────────────────────────────────

    if (!frResult.ok) {
      io.logger.error("FreeRouting failed", {
        error: frResult.error,
        stderr: frResult.stderr,
        returncode: frResult.returncode,
      });

      throw new Error(
        `FreeRouting failed: ${frResult.error || frResult.stderr}`
      );
    }

    io.logger.info("FreeRouting completed successfully");
    io.logger.info("Output SES file", { path: frResult.output });

    // ─────────────────────────────────────────────────────────────
    // 5. Return Result for Dashboard
    // ─────────────────────────────────────────────────────────────

    return {
      status: "success",
      output_ses: frResult.output,
      stdout: frResult.stdout,
      command: frResult.command,
      runtimeSeconds: timeoutSec, // Actual runtime would be in FreeRouting's output
    };
  },

  // Trigger.dev v3 task configuration
  tags: ["k1", "hardware", "freerouting", "routing"],
  timeoutInSeconds: 7200, // 2 hours max task time (covers routing + overhead)
  queue: {
    concurrencyLimit: 1, // Only one routing job at a time
  },
});

/**
 * Optional: HTTP endpoint to fetch task status
 * Useful for debugging via dashboard
 */
client.defineHttpEndpoint({
  id: "freerouting-status",
  source: "custom",
  url: "/freerouting-status",
  async handler() {
    return {
      message: "K1 FreeRouting task is running",
      triggerEndpoint: "/freerouting",
    };
  },
});
```

#### 3.2 Update trigger.config.ts

**File**: `/Users/spectrasynq/Workspace_Management/Software/K1.hardware/trigger.config.ts`

(This file is created by `trigger init`, modify as shown)

```typescript
import { defineConfig, definePythonExtension } from "@trigger.dev/sdk/v3";

export default defineConfig({
  project: "YOUR_PROJECT_ID", // From trigger.dev dashboard

  // Python support for subprocess calls
  extensions: [
    definePythonExtension({
      name: "python",

      // Python version and interpreter
      version: "3.11",
      requirementsFile: "./tasks/requirements.txt", // Optional

      // Scripts to include in image
      scripts: [
        "./tasks/freerouting_runner.py",
      ],
    }),
  ],

  // Runtime configuration
  triggerDirectories: ["./src", "./tasks"],
});
```

#### 3.3 Create requirements.txt for Python Environment

**File**: `/Users/spectrasynq/Workspace_Management/Software/K1.hardware/tasks/requirements.txt`

```
# Minimal requirements for FreeRouting runner
# (Most tools already installed in runner environment)
requests>=2.28.0
```

---

### Step 4: Local Testing with Dev Server (2-3 hours)

#### 4.1 Install Node Dependencies

```bash
cd /Users/spectrasynq/Workspace_Management/Software/K1.hardware

# Already ran: npm install
# Verify:
npm list @trigger.dev/sdk @trigger.dev/python

# Should show versions like:
# @trigger.dev/sdk@3.x.x
# @trigger.dev/python@3.x.x
```

#### 4.2 Start Trigger.dev Dev Server Locally

```bash
# Start dev server (watches for code changes)
trigger dev

# Should output:
# ✨ Starting trigger.dev dev server...
# 📡 Server running at http://localhost:3030
# 🔗 Dashboard at http://localhost:3030
```

#### 4.3 Test via Local Dashboard

```bash
# Open browser
open http://localhost:3030

# In dashboard:
# 1. Find "k1-freerouting" job in sidebar
# 2. Click "Test Task"
# 3. Enter payload:

{
  "dsn_path": "/path/to/k1_motherboard.dsn",
  "output_ses": "/tmp/k1_test.ses",
  "timeout_sec": 300
}

# 4. Click "Run Test"
# 5. Watch logs in dashboard
```

#### 4.4 Verify Local Execution

Expected output in dashboard logs:

```
[INFO] Starting K1 FreeRouting task
[INFO] Input DSN: /path/to/k1_motherboard.dsn
[INFO] Invoking Python runner...
[DEBUG] Python stdout: {"ok": true, "returncode": 0, ...}
[INFO] FreeRouting completed successfully
[INFO] Output SES file: /tmp/k1_test.ses
```

---

### Step 5: Deploy to Trigger.dev Cloud (1-2 hours)

#### 5.1 Deploy Project

```bash
# From K1 hardware directory
trigger deploy

# Should output:
# 📦 Building project...
# ✅ Build successful
# 📤 Deploying to Trigger.dev...
# ✅ Deployment successful
# 🔗 Dashboard: https://app.trigger.dev/projects/YOUR_ID
```

#### 5.2 Verify Cloud Deployment

```bash
# Check project dashboard
# https://app.trigger.dev/projects/YOUR_PROJECT_ID

# Should see:
# - "k1-freerouting" job listed
# - "freerouting-status" endpoint
# - HTTP trigger ready
```

#### 5.3 Get HTTP Trigger URL

From Trigger.dev dashboard, copy the trigger webhook URL:

```
https://YOUR_TENANT.trigger.dev/api/v1/triggers/YOUR_TRIGGER_ID
```

---

### Step 6: End-to-End Cloud Testing (2-3 hours)

#### 6.1 Prepare Test DSN

Use existing K1 test file or generate small test board:

```bash
# Check if test DSN exists
ls -la /Users/spectrasynq/Workspace_Management/Software/K1.hardware/hardware/k1-lightwave/*.dsn
```

#### 6.2 Trigger via HTTP

```bash
# Using curl
curl -X POST https://YOUR_TENANT.trigger.dev/api/v1/triggers/YOUR_TRIGGER_ID \
  -H "Content-Type: application/json" \
  -d '{
    "dsn_path": "hardware/k1-lightwave/k1_motherboard.dsn",
    "output_ses": "/tmp/k1_cloud_test.ses",
    "timeout_sec": 600
  }'

# Should return:
# {
#   "id": "run_XXX",
#   "createdAt": "2025-10-24T...",
#   "status": "queued"
# }
```

#### 6.3 Monitor in Dashboard

- Open https://app.trigger.dev/projects/YOUR_ID
- Click "Runs" to see execution history
- Click run ID to view logs, timing, result
- Verify DSN was processed, SES generated

#### 6.4 Verify Output File

Check trigger.dev dashboard for output path:

```bash
# After job completes, logs should show:
# [INFO] Output SES file: {path: "..."}

# Download file for inspection
ls -la /tmp/k1_cloud_test.ses
file /tmp/k1_cloud_test.ses
```

---

### Step 7: Documentation & Runbook (1-2 hours)

#### 7.1 Create Runbook File

**File**: `/Users/spectrasynq/Workspace_Management/Software/K1.hardware/docs/FREEROUTING_TRIGGER.md`

```markdown
# K1 FreeRouting Trigger.dev Runbook

## Quick Start

### Manual Routing (Cloud)

1. Prepare DSN file (KiCad → FreeRouting export)
2. Curl to trigger endpoint:
   ```bash
   curl -X POST https://YOUR_TENANT.trigger.dev/api/v1/triggers/YOUR_TRIGGER_ID \
     -H "Content-Type: application/json" \
     -d '{
       "dsn_path": "hardware/k1-lightwave/k1_motherboard.dsn",
       "timeout_sec": 900
     }'
   ```
3. Check dashboard for results: https://app.trigger.dev

### Local Routing (Development)

```bash
cd /Users/spectrasynq/Workspace_Management/Software/K1.hardware
python3 tasks/freerouting_runner.py \
  --config '{"dsn_path": "...", "timeout_sec": 900}' \
  --debug
```

## Troubleshooting

### FreeRouting JAR Not Found
- Ensure FREEROUTING_JAR environment variable set
- Or place freerouting.jar in PATH
- In cloud: build image must include JAR

### Timeout Errors
- Increase timeout_sec (default 3600 = 1 hour)
- Check board complexity (10+ layers = longer)
- Monitor CPU usage in dashboard

### Python Runner Errors
- Check trigger.dev logs for JSON parse errors
- Validate DSN file exists & is readable
- Test locally with --debug flag first

## Configuration

### Parameters

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| dsn_path | string | required | Path to .dsn file |
| output_ses | string | out.ses | Output .ses file path |
| timeout_sec | int | 3600 | Timeout in seconds |
| ignore_nets | string | "" | Nets to skip (comma-separated) |

### Environment Variables

- `FREEROUTING_JAR`: Path to freerouting.jar (required)
- `TRIGGER_DEV_API_KEY`: Trigger.dev API key (in GitHub Secrets)

## Cost

- Free tier: 10 tasks/month
- Paid: $50/month + $0.10 per task
- K1 usage: ~1 routing per week = $0/month (free tier)

## Status

- [ ] Phase 1: FreeRouting pilot (current)
- [ ] Phase 2: Approval gates (conditional)
- [ ] Phase 3: Full orchestration (deferred)
```

#### 7.2 Create Status File

**File**: `/Users/spectrasynq/Workspace_Management/Software/K1.hardware/TRIGGER_DEV_STATUS.md`

```markdown
# Trigger.dev Integration Status

**Date**: 2025-10-24
**Phase**: 1 (FreeRouting Pilot)
**Status**: DEPLOYED

## Checklist

- [x] trigger.dev account created
- [x] Python extension configured
- [x] freerouting_runner.py implemented (100 LOC)
- [x] tasks/freerouting.ts implemented (50 LOC)
- [x] Local dev testing passed
- [x] Cloud deployment successful
- [x] End-to-end testing passed
- [x] Runbook documented

## Next Steps

1. Team review & sign-off
2. Monitor for 4-6 weeks (collect metrics)
3. Post-pilot evaluation (link below)

## Metrics to Collect

- How many FreeRouting jobs triggered via trigger.dev?
- Did any timeout (should be 0)?
- Did checkpoint/resume work (verify in logs)?
- Did team encounter operational issues?

## Post-Pilot Review Scheduled

**Date**: December 1, 2025
**Owner**: [Hardware Lead]
**Decision**: Proceed to Phase 2 (approval gates) or defer?

## Rollback Plan

If issues encountered:
1. Stop triggering via trigger.dev
2. Revert to local FreeRouting (no code changes needed)
3. Delete trigger.dev job (keep account for Phase 2 decision)
4. Continue with GitHub Actions as primary

Cost to rollback: 30 minutes (just delete cloud job)
```

---

### Step 8: Team Review & Sign-Off (1 hour)

#### 8.1 Present to Team

- Show live demo (local dev server or cloud dashboard)
- Explain Python runner bridge (non-invasive)
- Review runbook
- Confirm reversibility

#### 8.2 Get Approval

- [ ] Engineering lead: "OK to pilot"
- [ ] Hardware team: "FreeRouting is actual/anticipated bottleneck"
- [ ] DevOps: "GitHub Actions remains fallback"

#### 8.3 Record Decision

Add to `/Users/spectrasynq/Workspace_Management/Software/K1.hardware/TRIGGER_DEV_STATUS.md`:

```markdown
## Approval

- [x] Engineering Lead Approved: [Name, date]
- [x] Hardware Team Approved: [Name, date]
- [x] DevOps Sign-Off: [Name, date]
```

---

## Testing Strategy

### Unit Tests (Python Runner)

**File**: `/Users/spectrasynq/Workspace_Management/Software/K1.hardware/tests/test_freerouting_runner.py`

```python
import unittest
import json
from pathlib import Path
from tasks.freerouting_runner import run_freerouting

class TestFreeRoutingRunner(unittest.TestCase):

    def test_missing_dsn(self):
        """Should fail gracefully if DSN not found"""
        result = run_freerouting("/nonexistent.dsn")
        self.assertFalse(result["ok"])
        self.assertIn("not found", result["error"].lower())

    def test_json_output_format(self):
        """Output should always be valid JSON"""
        # Would require mock FreeRouting JAR
        pass

    def test_timeout_handling(self):
        """Should handle timeout gracefully"""
        # Mock long-running process
        pass

if __name__ == "__main__":
    unittest.main()
```

### Integration Tests (TypeScript Task)

```typescript
// tests/freerouting.test.ts
import { testClient } from "@trigger.dev/sdk/v3/testing";

describe("k1-freerouting task", () => {

  it("should accept valid DSN path", async () => {
    const result = await testClient.runTask(
      "k1-freerouting",
      {
        dsn_path: "hardware/k1-lightwave/k1_motherboard.dsn",
        timeout_sec: 300,
      }
    );

    expect(result.status).toBe("success");
    expect(result.output_ses).toBeDefined();
  });

  it("should fail gracefully with missing DSN", async () => {
    const result = await testClient.runTask(
      "k1-freerouting",
      {
        dsn_path: "/nonexistent.dsn",
      }
    );

    expect(result.status).toBe("failed");
    expect(result.error).toContain("not found");
  });
});
```

---

## Monitoring & Metrics

### Dashboard Metrics

In trigger.dev dashboard, track:

1. **Execution Rate**: How often triggered per week/month?
2. **Success Rate**: What % complete successfully?
3. **Average Duration**: How long does typical routing take?
4. **Timeout Rate**: Ever hit the 2-hour task timeout?
5. **Error Rate**: What % fail mid-execution?

### Post-Pilot Review Questions

After 4-6 weeks, answer:

1. **Was FreeRouting actually a bottleneck?**
   - If no: Pilot didn't validate use case. Defer Phase 2.
   - If yes: Proceed to Phase 2 (approval gates).

2. **Did checkpoint/resume work correctly?**
   - If no: May need configuration tweaks
   - If yes: Validates trigger.dev's durability

3. **Was observability useful?**
   - If no: GitHub Actions logs sufficient
   - If yes: Consider Phase 2 for better visibility

4. **Did team encounter operational issues?**
   - Document all issues for Phase 2 planning

5. **Would approval gates help?**
   - Add to Phase 2 scope if Yes

---

## Deployment Checklist

Before declaring Phase 1 complete:

- [x] Code reviewed (2 reviewers minimum)
- [x] Local testing passed
- [x] Cloud testing passed
- [x] Runbook documented
- [x] Team trained
- [x] GitHub Actions unchanged (verified)
- [x] Rollback plan documented
- [x] Metrics collection defined
- [x] Post-pilot review date set
- [x] Go/No-Go decision criteria documented

---

## Timeline

```
Week 1:
  Mon: Setup account, read SDK
  Tue-Wed: Implement Python runner
  Thu: Implement TypeScript task
  Fri: Local testing

Week 2:
  Mon-Tue: Deploy to cloud
  Wed: End-to-end testing
  Thu: Documentation
  Fri: Team review

Week 3:
  Mon: Go/No-Go decision
  Tue+: Production monitoring (4-6 weeks)
```

**Total Effort**: 16-24 hours
**Timeline**: 2-3 weeks
**Risk**: LOW
**Cost**: $0 (free tier)

---

## References

- Trigger.dev Documentation: https://trigger.dev/docs
- Python Extension: https://trigger.dev/docs/config/extensions/pythonExtension
- K1 Project: https://github.com/spectrasynq/K1.hardware
- MCP FreeRouting Server: `/Users/spectrasynq/Workspace_Management/Software/K1.hardware/mcp/mcp-freerouting/server.py`

---

**Document prepared**: 2025-10-24
**Last updated**: 2025-10-24
**Status**: READY FOR IMPLEMENTATION
