# /bench-backtrace

Decode device crash logs

---

## Command

```
Capture serial output and symbolicate crash backtrace.
Converts ESP32 addresses to source code locations.
```

## What Happens

1. Monitors device serial for 15 seconds (tail output)
2. Looks for crash/backtrace pattern
3. Uses `esp-idf-local.backtrace_exception` to symbolicate
4. Shows code locations with filenames and line numbers

## When to Use

- ✅ Device crashed, need to debug
- ✅ See where fault occurred in source code
- ✅ Post-crash analysis
- ✅ Memory protection violations

## Example Crash Output

**Raw Device Output**:
```
Guru Meditation Error: Core  0 panic'ed (Double exception (illegal instruction)).

Backtrace:0x40001234:0x3ffe0000 0x40005678:0x3ffe0010 0x40009abc:0x3ffe0020
```

**After Backtrace**:
```
Core 0 crashed at:

0x40001234 (0x40001234) led_driver.c:45 set_led_color()
0x40005678 (0x40005678) main.c:123 app_main()
0x40009abc (0x40009abc) port.c:88 default_exception_handler()
```

## Requirements

- Device must be powered on (or will boot when powered)
- Crash must occur within 15-second window
- Firmware ELF file must be available (auto-detected)

## Duration

~15 seconds to tail + decode

---

*Debug device issues with source-level precision*
