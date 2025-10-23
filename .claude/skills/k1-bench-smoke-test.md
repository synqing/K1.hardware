# K1 Bench Smoke Test

Complete build → flash → boot → health check in one command.

## Purpose

Quick validation that K1 firmware builds, device boots, and is ready for live testing. Run daily before pushing to CI or after major changes.

## What It Does

```
Step 1: BUILD .......................... Compile firmware (esp-idf)
Step 2: PORTS .......................... Detect K1 on USB
Step 3: FLASH .......................... Upload binary to device
Step 4: WAIT FOR BOOT .................. Monitor output; assert "WS ready" banner
Step 5: HEALTH CHECK ................... Verify no exceptions in boot logs
[RESULT] ✅ PASS or ❌ FAIL
```

## Tools Used

Internally calls (in sequence):
1. `mcp call esp-idf-local.build_esp_related_project`
2. `mcp call esp-idf-local.list_esp_serial_ports`
3. `mcp call esp-idf-local.flash_and_wait_boot`
4. `mcp call esp-idf-local.monitor_serial_output`

## Pass Criteria

All of the following must be true:
- ✅ Build succeeds with 0 errors (warnings OK)
- ✅ K1 device detected on FTDI port
- ✅ Flash operation completes without errors
- ✅ Boot banner "WS ready" captured in monitor output
- ✅ No exceptions (Guru Meditation, panic, etc) in first 30s of boot

If any criterion fails, skill returns `[FAIL]` with error details.

## Usage

### Basic
```
/k1-bench-smoke-test
```

### With Custom Project Path
```
/k1-bench-smoke-test projectPath=/Users/you/path/to/firmware/PRISM.k1/firmware
```

### With Custom Timeout
```
/k1-bench-smoke-test timeout_sec=20
```

### Expected Output (Success)
```
[BUILD] ✅ Compiled in 12.3s
  Artifacts: build/firmware.elf (245 KB)

[PORTS] ✅ K1 detected: /dev/ttyUSB0 (FTDI)
  Confidence: high

[FLASH] ✅ Upload to /dev/ttyUSB0 completed (3.2s)
  Binary size: 245 KB
  Flash rate: 78 KB/s

[WAIT FOR BOOT] ✅ "WS ready" captured (2.1s)
  Boot time: 2.1 seconds (target <5s)
  Boot banner: WS ready on 192.168.1.100:8080

[HEALTH] ✅ No exceptions in boot logs
  First 30s of monitor output: clean
  LED matrix: initialized
  Network: ready

═══════════════════════════════════════════════════════════════════════════
[PASS] ✅ Bench smoke test complete. Device ready for live testing.
═══════════════════════════════════════════════════════════════════════════
```

### Expected Output (Failure)
```
[BUILD] ✅ Compiled in 12.3s

[PORTS] ❌ K1 device NOT DETECTED
  Available ports: [/dev/cu.usbserial-ABC123]
  Expected: FTDI device

ACTION: Plug in K1 USB cable; verify power

═══════════════════════════════════════════════════════════════════════════
[FAIL] ❌ K1 device not found. Connect device and retry.
═══════════════════════════════════════════════════════════════════════════
```

## Troubleshooting

### "Build fails with errors"
```
Check:
1. firmware/PRISM.k1/firmware/CMakeLists.txt syntax
2. All components compile independently
3. Recent commits didn't break anything

Fix:
1. Run: idf.py clean
2. Run: idf.py build
3. Check error output for missing includes or typos
```

### "K1 not detected"
```
Check:
1. Is K1 plugged into USB port?
2. Is power LED lit on K1?
3. Does /dev/ttyUSB* or /dev/cu.* appear when plugged in?

Fix (macOS):
1. Install FTDI driver if needed
2. Unplug K1; wait 2s; plug back in
3. Try: ls -la /dev/tty.usbserial*
```

### "Flash succeeds but boot times out"
```
Check:
1. Device may be in bootloader mode
2. Firmware may have exception on startup

Fix:
1. Manually reset K1 (power cycle or reset button)
2. Check firmware/components/network/ws_server.c for startup issues
3. Run: mcp call esp-idf-local.monitor_serial_output for full logs
```

### "Boot banner found but exceptions present"
```
Check:
1. Guru Meditation error: likely memory/stack issue
2. Assertion failure: check which component panicked
3. WDT timeout: device stuck in loop

Fix:
1. Read full monitor output for stack trace
2. Use backtrace tool: mcp call esp-idf-local.backtrace_exception
3. Check firmware/CMakeLists.txt for WDT settings
```

## Related Tools

| Tool | Use When | Time |
|------|----------|------|
| `/k1-bench-smoke-test` | Daily smoke test (this tool) | <2 min |
| `mcp call esp-idf-local.build_esp_related_project` | Just want to compile | ~10s |
| `mcp call esp-idf-local.flash_and_wait_boot` | Flash only (skip build) | ~5s |
| `mcp call esp-idf-local.monitor_serial_output` | Tail logs manually | varies |
| `mcp call esp-idf-local.backtrace_exception` | Debug exception | depends |

## Context & History

- **Phase**: MVP development iteration
- **Purpose**: Fast feedback loop; catch regressions early
- **Owner**: embedded-firmware-coder
- **Dependencies**: ESP-IDF 6.0.0, esp-idf-local MCP (Phase 1a)
- **Created**: 2025-10-22 (Phase 1b)

## Notes

- Skill is idempotent: safe to run multiple times
- Does NOT reset device between runs (preserves state)
- Does NOT erase flash (use `idf.py erase-flash` if needed)
- All output logged to `.claude/mcp-*.log` files

## Future Enhancements (Phase 1c+)

- [ ] Parse boot logs for performance metrics (boot time trend)
- [ ] LED matrix self-test (verify all 320 pixels addressable)
- [ ] WebSocket connection test (verify node connection)
- [ ] Scene playback validation (check DMA/I2S timing)
- [ ] Dashboard integration (post results to metrics)
