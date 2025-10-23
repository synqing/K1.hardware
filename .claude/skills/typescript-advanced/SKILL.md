# TypeScript Advanced Patterns for PRISM.node

**Purpose:** Advanced TypeScript patterns used in PRISM.node Light Lab editor

**Auto-activation keywords:** `TypeScript`, `generics`, `utility types`, `type inference`, `Zustand`, `advanced types`, `conditional types`

---

## Quick Start

Use this skill when you need to:
- Write type-safe generic components
- Use utility types (`Partial`, `Pick`, `Omit`, `Readonly`, etc.)
- Understand conditional types and type predicates
- Implement Zustand store patterns with full type safety
- Extract types from external libraries

---

## Generics: Building Reusable Type-Safe Components

### Basic Generic Pattern

```typescript
// Generic component that wraps a data value with loading state
interface AsyncData<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

// Generic function to create AsyncData
function createAsyncData<T>(data: T): AsyncData<T> {
  return {
    data,
    loading: false,
    error: null,
  };
}

// Usage
const numberData = createAsyncData(42);  // Type: AsyncData<number>
const stringData = createAsyncData("hello");  // Type: AsyncData<string>
```

### Generic Constraints

```typescript
// Only allow objects with specific properties
interface HasId {
  id: string;
}

function getId<T extends HasId>(obj: T): string {
  return obj.id;
}

// ✓ Works: object has id property
getId({ id: "123", name: "John" });

// ✗ Error: missing id property
getId({ name: "John" });
```

### Generic Constraints in PRISM.node

```typescript
// Node type constraint: all nodes must have id, type, position
interface BaseNode {
  id: string;
  type: string;
  position: { x: number; y: number };
}

// Generic node handler function
function processNode<T extends BaseNode>(node: T): void {
  console.log(`Processing node ${node.id} at ${node.position.x},${node.position.y}`);
}

// Specific node types
interface ColorNode extends BaseNode {
  type: 'color';
  color: string;
}

interface AnimationNode extends BaseNode {
  type: 'animation';
  duration: number;
  easing: 'linear' | 'ease-in' | 'ease-out';
}

// Process any node type
processNode<ColorNode>(colorNode);
processNode<AnimationNode>(animationNode);
```

---

## Utility Types: Type Transformations

### `Partial<T>` - All Properties Optional

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

// Update function accepts partial user data
function updateUser(id: string, updates: Partial<User>) {
  // Only provided fields are updated
}

// ✓ Works: partial data
updateUser("123", { name: "John" });

// ✗ Error: extra fields not allowed
updateUser("123", { name: "John", extraField: "nope" });
```

### `Pick<T, K>` - Select Specific Properties

```typescript
interface Node {
  id: string;
  type: string;
  position: { x: number; y: number };
  properties: Record<string, unknown>;
  connections: string[];
}

// Extract just position data
type NodePosition = Pick<Node, 'id' | 'position'>;
// Equivalent to: { id: string; position: { x: number; y: number } }

function renderNode(nodePos: NodePosition) {
  // Only has access to id and position
  drawPoint(nodePos.position.x, nodePos.position.y);
}
```

### `Omit<T, K>` - Exclude Specific Properties

```typescript
// Get all Node properties except 'connections'
type NodeWithoutConnections = Omit<Node, 'connections'>;

// Use in upload payload (don't send connection data to firmware)
function uploadNodeToDevice(node: NodeWithoutConnections) {
  const payload = JSON.stringify(node);
  // payload doesn't include connections
  websocket.send(payload);
}
```

### `Record<K, V>` - Key-Value Maps

```typescript
// Color mapping: node type → RGB color
type ColorMap = Record<'color' | 'animation' | 'trigger', string>;

const nodeColors: ColorMap = {
  color: '#FF0000',
  animation: '#00FF00',
  trigger: '#0000FF',
};

// Type-safe access
const colorNodeColor = nodeColors['color'];  // ✓ OK
// const invalid = nodeColors['invalid'];  // ✗ Error
```

---

## Conditional Types: Type-Level Logic

### Basic Conditional Type

```typescript
// If T is an array, extract element type; otherwise return T
type ElementType<T> = T extends (infer E)[] ? E : T;

type NumberArray = ElementType<number[]>;     // number
type PlainString = ElementType<string>;       // string
```

### Conditional Types in PRISM

```typescript
// Extract property type from node
type GetProperty<T, K extends keyof T> = T[K];

interface ColorNode {
  type: 'color';
  color: string;
  opacity: number;
}

type ColorNodeColor = GetProperty<ColorNode, 'color'>;  // string
type ColorNodeOpacity = GetProperty<ColorNode, 'opacity'>;  // number
```

### Mapped Conditional Types

```typescript
// For each property in T, create a getter function
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface Node {
  id: string;
  type: string;
  enabled: boolean;
}

type NodeGetters = Getters<Node>;
// Results in:
// {
//   getId: () => string;
//   getType: () => string;
//   getEnabled: () => boolean;
// }
```

---

## Type Predicates: Runtime Type Guards

### Type Predicate Function

```typescript
// Narrow type at runtime
function isColorNode(node: BaseNode): node is ColorNode {
  return node.type === 'color' && 'color' in node;
}

function processNode(node: BaseNode) {
  if (isColorNode(node)) {
    // TypeScript now knows node is ColorNode
    console.log(node.color);  // ✓ OK, color exists
  } else {
    // console.log(node.color);  // ✗ Error, color doesn't exist
  }
}
```

### Custom Type Guard for PRISM

```typescript
// Verify node has required properties for LED rendering
function isRenderableNode(node: unknown): node is BaseNode {
  return (
    typeof node === 'object' &&
    node !== null &&
    'id' in node &&
    'type' in node &&
    'position' in node &&
    typeof (node as any).id === 'string' &&
    typeof (node as any).type === 'string'
  );
}

function uploadNode(data: unknown) {
  if (isRenderableNode(data)) {
    // Safe to use as BaseNode
    sendToDevice(data);
  } else {
    throw new Error('Invalid node structure');
  }
}
```

---

## Zustand Store: Type-Safe State Management

### Basic Zustand Store

```typescript
import { create } from 'zustand';

interface AppState {
  // State properties
  nodes: Node[];
  selectedNodeId: string | null;
  zoom: number;

  // State actions
  addNode: (node: Node) => void;
  removeNode: (id: string) => void;
  selectNode: (id: string | null) => void;
  setZoom: (zoom: number) => void;
}

const useAppStore = create<AppState>((set) => ({
  // Initial state
  nodes: [],
  selectedNodeId: null,
  zoom: 1.0,

  // Action implementations
  addNode: (node) => set((state) => ({
    nodes: [...state.nodes, node],
  })),

  removeNode: (id) => set((state) => ({
    nodes: state.nodes.filter((n) => n.id !== id),
  })),

  selectNode: (id) => set({ selectedNodeId: id }),

  setZoom: (zoom) => set({ zoom }),
}));

// Usage
const nodes = useAppStore((state) => state.nodes);
const addNode = useAppStore((state) => state.addNode);
```

### Advanced Store Selectors

```typescript
// Selector: only re-render when nodes change
const nodes = useAppStore((state) => state.nodes);

// Memoized selector: only re-render if selected node ID changes
const selectedNode = useAppStore((state) => {
  const node = state.nodes.find((n) => n.id === state.selectedNodeId);
  return node;
});

// Shallow equality selector: safe for objects
import { shallow } from 'zustand/react/shallow';
const { nodes, zoom } = useAppStore(
  (state) => ({ nodes: state.nodes, zoom: state.zoom }),
  shallow
);
```

### Middleware for DevTools

```typescript
import { devtools } from 'zustand/middleware';

const useAppStore = create<AppState>(
  devtools((set) => ({
    // ... store implementation
  }), { name: 'AppStore' })
);

// In browser:
// - Open Redux DevTools extension
// - See state timeline
// - Time-travel to any previous state
```

### Persist Store to localStorage

```typescript
import { persist } from 'zustand/middleware';

const useAppStore = create<AppState>(
  persist(
    (set) => ({
      // ... store implementation
    }),
    {
      name: 'prism-app-store',
      storage: localStorage,
      version: 1,
    }
  )
);

// State automatically saved to localStorage
// Automatically restored on page reload
```

---

## Type Inference: Let TypeScript Figure It Out

### Inferred Return Types

```typescript
// TypeScript infers return type from function body
function createNode(id: string, type: string) {
  return {
    id,
    type,
    created: new Date(),
    enabled: true,
  };
  // Inferred type: { id: string; type: string; created: Date; enabled: boolean }
}

const node = createNode('1', 'color');
// node has full type information without explicit annotation
```

### Inferred Generic Types

```typescript
// TypeScript infers T from argument
function wrapInArray<T>(item: T): T[] {
  return [item];
}

const strings = wrapInArray('hello');  // T inferred as string
const numbers = wrapInArray(42);       // T inferred as number
```

### `as const` for Literal Types

```typescript
// Without as const: string type (too general)
const nodeTypes = ['color', 'animation', 'trigger'];

// With as const: literal types (exact values)
const nodeTypes = ['color', 'animation', 'trigger'] as const;

type NodeType = typeof nodeTypes[number];  // 'color' | 'animation' | 'trigger'
```

---

## PRISM.node Specific Patterns

### Color Space Type Safety

```typescript
// Color in different spaces
interface ColorSpaces {
  sRGB: { r: number; g: number; b: number };
  OKLCH: { l: number; c: number; h: number };
  hex: string;
}

// Track which color space is currently used
type ColorSpace = keyof ColorSpaces;

interface ColorNode extends BaseNode {
  type: 'color';
  value: ColorSpaces['sRGB'] | ColorSpaces['OKLCH'];
  space: ColorSpace;
}

function convertColor<From extends ColorSpace, To extends ColorSpace>(
  color: ColorSpaces[From],
  from: From,
  to: To
): ColorSpaces[To] {
  // Implementation converts between color spaces
  // Type system ensures valid conversions
}
```

### Node Graph Traversal

```typescript
// Generic graph traversal with type preservation
function traverseNodes<T extends BaseNode>(
  nodes: T[],
  callback: (node: T, depth: number) => void,
  visited = new Set<string>()
) {
  nodes.forEach((node) => {
    if (!visited.has(node.id)) {
      visited.add(node.id);
      callback(node, visited.size);

      // Recursively process connections
      const connected = nodes.filter((n) =>
        'connections' in n &&
        Array.isArray((n as any).connections) &&
        (n as any).connections.includes(node.id)
      );

      traverseNodes<T>(connected, callback, visited);
    }
  });
}
```

### Type-Safe WebSocket Messages

```typescript
// Define all possible WebSocket message types
type WebSocketMessage =
  | { type: 'pattern:upload'; payload: Pattern }
  | { type: 'pattern:play'; patternId: string }
  | { type: 'pattern:stop' }
  | { type: 'device:status'; status: DeviceStatus }
  | { type: 'error'; message: string };

function handleMessage(msg: WebSocketMessage) {
  switch (msg.type) {
    case 'pattern:upload':
      uploadPattern(msg.payload);  // payload is Pattern
      break;
    case 'pattern:play':
      playPattern(msg.patternId);  // patternId is string
      break;
    case 'device:status':
      updateDeviceStatus(msg.status);  // status is DeviceStatus
      break;
    // TypeScript ensures all cases are handled
  }
}
```

---

## Common Mistakes to Avoid

### ❌ DON'T: Use `any` Type

```typescript
// ❌ Loses all type safety
function processNode(node: any) {
  node.nonExistentProperty;  // No error, but will crash at runtime
}

// ✓ Use unknown with type guard
function processNode(node: unknown) {
  if (isRenderableNode(node)) {
    // TypeScript now knows node is safe
  }
}
```

### ❌ DON'T: Overly Complex Generics

```typescript
// ❌ Hard to understand and maintain
type ComplexType<T extends Record<string, any>> = T extends (infer U)[]
  ? U extends { [K in keyof T]: infer V }
    ? V
    : never
  : T;

// ✓ Keep it simple and readable
type ElementType<T> = T extends (infer E)[] ? E : T;
```

### ❌ DON'T: Mix Runtime and Type-Level

```typescript
// ❌ Type doesn't match runtime
type NodeType = 'color' | 'animation' | 'trigger';
const nodeTypes = ['color', 'animation'];  // Missing 'trigger' — bug!

// ✓ Single source of truth
const nodeTypes = ['color', 'animation', 'trigger'] as const;
type NodeType = typeof nodeTypes[number];
```

---

## Testing TypeScript Types

### Using `expectType` Helper

```typescript
import { expectType } from 'tsd';

// Verify that nodeColor has correct type
const nodeColor = createNode('1', 'color');
expectType<ColorNode>(nodeColor);  // ✓ Passes if type matches

// Test utility type
expectType<string>({} as Pick<Node, 'id'>['id']);
```

### Type Tests File

```typescript
// types.test.ts
import type { ElementType, GetProperty } from './types';

// Verify ElementType works correctly
type Test1 = ElementType<number[]>;
type Test1Assertion = Test1 extends number ? true : false;

const _: Test1Assertion = true;  // ✓ Passes
```

---

## Performance Considerations

### Avoid Deep Generic Nesting

```typescript
// ❌ Slow TypeScript compilation
type DeepNest<T> = T extends any
  ? DeepNest<DeepNest<T>>
  : never;

// ✓ Flatten structure
type Result = Flatten<NestedType>;
```

### Use `satisfies` Operator (TypeScript 4.9+)

```typescript
// ✓ Verify type without widening
const nodeConfig = {
  color: '#FF0000',
  animation: 'fade',
} satisfies Record<string, string>;

// Still has literal type, not string
type ConfigType = typeof nodeConfig;  // { color: "#FF0000"; animation: "fade" }
```

---

## Related Skills

- **React** — Component type patterns, hooks types
- **PRISM.node-API** — WebSocket message types, node system types
- **Zustand** — Store patterns (covered in this skill)

---

**Last Updated:** 2025-10-22
**Author:** Claude (TypeScript Patterns)
**Status:** Production Ready
