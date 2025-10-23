# /bench-flash

Build → Flash → Monitor (full cycle)

---

## Command

```
Build and flash the K1 firmware to device, then monitor boot.
Must include /confirm-flash token to proceed.
```

## What Happens

1. Builds firmware
2. **Flashes to device** (gated by `/confirm-flash` token)
3. Monitors serial output
4. Waits for boot banner ("WS ready")
5. Returns status

## When to Use

- ✅ Complete firmware update cycle
- ✅ Testing LED/device behavior
- ✅ Debug device issues
- ✅ Rapid iteration (8-10 seconds total!)

## Requirements

- [ ] Add `/confirm-flash` token to your prompt
- [ ] Device connected via USB
- [ ] Correct port detected

## Typical Sequence

**Your Prompt**:
```
Build and flash the device /confirm-flash
```

**Claude Response**:
1. Detects `/confirm-flash` token ✅
2. Builds firmware
3. Flashes to `/dev/ttyUSB0` (auto-detected)
4. Waits for boot (max 15 seconds)
5. Shows boot output:
   ```
   [Boot sequence]
   ...
   WS ready

   ✅ Device booted successfully!
   Session log: ops/logs/claude/20251022_123456_session.json
   ```

## Duration

- Build: ~5 seconds
- Flash: ~3-5 seconds
- Monitor: ~1-2 seconds
- **Total: 8-10 seconds**

## Troubleshooting

### "Device not found"
```bash
# Check USB connection and drivers:
mcp call esp-idf-local.list_esp_serial_ports
```

### "Flash failed"
- Ensure device is in bootloader mode
- Try manual flash: `idf.py -p /dev/ttyUSB0 flash monitor`

### "Boot timeout (no WS ready)"
- Check device logs: `/bench-backtrace`
- Verify firmware logic

---

*Fastest way to iterate on device code*
