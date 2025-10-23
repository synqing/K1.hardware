# Start Development Stack

Start all development servers concurrently.

## Prerequisites

- Node.js 20+ installed
- All dependencies installed (`npm install` in each app)
- Ports 3000, 3001, 5173 available (adjust as needed)

## Commands

### Option 1: Using npm scripts (if root package.json configured)
```bash
npm run dev:web
```

### Option 2: Manual (in separate terminals)

**Terminal 1 - PRISM.node:**
```bash
cd apps/PRISM.node
npm run dev
```

**Terminal 2 - K1.Landing-Page:**
```bash
cd apps/K1.Landing-Page
npm run dev
```

**Terminal 3 - M5Stack.tab5 (optional):**
```bash
cd apps/M5Stack.tab5
npm run dev
```

### Option 3: Using tmux (Linux/macOS)
```bash
tmux new-session -d -s prism-dev

tmux send-keys -t prism-dev "cd apps/PRISM.node && npm run dev" Enter
tmux split-window -h -t prism-dev "cd apps/K1.Landing-Page && npm run dev"

# View sessions:
tmux list-sessions
```

## Access Points

- PRISM.node: http://localhost:3000
- K1.Landing-Page: http://localhost:3001
- M5Stack.tab5: http://localhost:5173 (typical Vite)

## Stopping

- **Manual**: `Ctrl+C` in each terminal
- **tmux**: `tmux kill-session -t prism-dev`

## Notes

- Hot reload enabled in dev mode
- Check `.env` files for correct API endpoints
- Some apps may require a running backend (PRISM.node API)
