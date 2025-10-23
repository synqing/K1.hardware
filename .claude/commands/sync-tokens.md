# Sync Design Tokens

Synchronize design tokens from K1.Landing-Page to the shared directory.

## Purpose

Maintain a single source of truth for design tokens (colors, typography, spacing) used across:
- PRISM.node (web dashboard)
- K1.Landing-Page (marketing site)
- M5Stack.tab5 (touchscreen UI)

## Commands

```bash
# Check if K1.Landing-Page has tokens-web directory
ls -la apps/K1.Landing-Page/

# Copy tokens to shared location (if not already there)
if [ -d "apps/K1.Landing-Page/tokens-web" ]; then
  cp -r apps/K1.Landing-Page/tokens-web/* shared/design-tokens/
  echo "✅ Tokens synced to shared/design-tokens/"
else
  echo "⚠️  No tokens-web found in K1.Landing-Page"
fi

# Update PRISM.node to use shared tokens
cd apps/PRISM.node
# Add to tailwind.config.js or import shared tokens

# Update K1.Landing-Page to use shared tokens (optional)
cd ../K1.Landing-Page
# Update imports to reference ../../shared/design-tokens/
```

## Token Structure

```
shared/design-tokens/
├── css/
│   ├── k1-tokens.css
│   └── shadcn-theme.css
├── tailwind/
│   ├── k1-tokens-tailwind.js
│   └── tailwind-preset.cjs
└── README.md
```

## Next Steps

1. Identify token format in K1.Landing-Page
2. Standardize exports (CSS, JS, JSON)
3. Update both web apps to import from shared
