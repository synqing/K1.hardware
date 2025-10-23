# Build All

Build firmware, web apps, and validate everything locally.

## Commands

```bash
# Build firmware (ESP32S3)
cd firmware/PRISM.k1 && idf.py build

# Build web apps
cd apps/PRISM.node && npm run build
cd ../K1.Landing-Page && npm run build
cd ../M5Stack.tab5 && npm run build

echo "✅ All builds complete"
```

## Notes

- Requires ESP-IDF for firmware builds
- Each app must have `npm run build` defined
- Run from project root

## Troubleshooting

- **Firmware fails**: Check ESP-IDF is installed (`idf.py --version`)
- **Web builds fail**: Run `npm install` in each app directory first
