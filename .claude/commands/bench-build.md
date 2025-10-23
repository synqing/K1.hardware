# /bench-build

Build firmware only (no flash)

---

## Command

```
Build the K1 firmware and show output. No flash, no device needed.
```

## What Happens

1. Builds `firmware/PRISM.k1/firmware/` using `idf.py build`
2. Shows build output (errors, warnings, sizes)
3. Reports success/failure and artifact locations
4. Does NOT flash to device

## When to Use

- ✅ Quick syntax check
- ✅ Before hardware testing
- ✅ Verify compilation without device
- ✅ Check build sizes

## Typical Output

```
Building PRISM.k1 firmware...

[Build output]
...
app binary size: 256 KB
total size: 512 KB (of 4096 KB available)

Build complete! ✅
```

## Duration

~5 seconds on ESP32-S3

---

*Convenience command for PRISM K1 development*
