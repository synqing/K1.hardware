# Flash Firmware

Build and flash ESP32S3 firmware to device.

## Prerequisites

- ESP32S3 development board connected via USB
- ESP-IDF installed and configured
- `idf.py` available in PATH

## Commands

```bash
cd firmware/PRISM.k1

# Build firmware
idf.py build

# Flash to device (with auto-detection)
idf.py flash

# Monitor serial output
idf.py monitor

# Or do all three in one:
idf.py build flash monitor
```

## Troubleshooting

- **Port not found**: Check USB connection, try `idf.py monitor -p /dev/ttyUSB0` (Linux) or `/dev/tty.usbserial-*` (macOS)
- **Permission denied**: On Linux, add user to `dialout` group: `sudo usermod -aG dialout $USER`
- **Build fails**: Run `idf.py clean` and rebuild

## Monitoring

Once flashed, view logs with:
```bash
idf.py monitor
```

Press `Ctrl+]` to exit monitor mode.
