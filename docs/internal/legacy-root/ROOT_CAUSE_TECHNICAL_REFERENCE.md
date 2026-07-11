# ROOT CAUSE TECHNICAL REFERENCE
**Comprehensive Code Location Index**

---

## PRIMARY BUG LOCATION

### Bug Location #1: Parameter Passing Error
**File:** `elite_pcb_designer.py`
**Lines:** 193-195
**Severity:** CRITICAL

```python
193 │ phase2 = ComponentPlacement(
194 │     board_path=self.config.board_path,
195 │     output_path=self.config.output_dir  # ← DIRECTORY, NOT FILE
196 │ )
```

**The Problem:**
- `self.config.output_dir` evaluates to `"k1_design_output"` (a directory)
- ComponentPlacement expects `output_path` to be a file path like `"k1_design_output/K1_Lightwave.kicad_pcb"`
- When directory path is passed to `board.Save()`, KiCad silently ignores it

**Fix:**
```python
import os
board_output_file = os.path.join(
    self.config.output_dir,
    os.path.basename(self.config.board_path)
)
phase2 = ComponentPlacement(
    board_path=self.config.board_path,
    output_path=board_output_file
)
```

---

## SECONDARY FAILURE LOCATION

### Bug Location #2: Path Handling in Constructor
**File:** `component_placement.py`
**Line:** 108
**Severity:** MEDIUM (enables Bug #1 to persist silently)

```python
107 │ self.board_path = Path(board_path)
108 │ self.output_path = Path(output_path) if output_path else self.board_path
```

**The Problem:**
- No validation that `output_path` is a file path vs directory path
- Silently accepts directory paths
- When directory path reaches `board.Save()` at line 861, KiCad fails silently

**Optional Fix (defensive programming):**
```python
self.board_path = Path(board_path)
if output_path:
    output_path = Path(output_path)
    # If directory path provided, use board filename in that directory
    if output_path.is_dir():
        self.output_path = output_path / self.board_path.name
    else:
        self.output_path = output_path
else:
    self.output_path = self.board_path
```

---

## PERSISTENCE FAILURE LOCATION

### Bug Location #3: Silent Save Failure
**File:** `component_placement.py`
**Lines:** 857-864
**Severity:** HIGH

```python
857 │ # Apply to board
858 │ print("\n[8/8] Applying placement to KiCad board...")
859 │ self.apply_placement_to_board()
860 │ if self.pcbnew_available and self.board is not None:
861 │     self.board.Save(str(self.output_path))
862 │     print(f"      Board saved to {self.output_path}")
863 │ else:
864 │     print(f"      Board update skipped (pcbnew not available)")
```

**The Problem:**
1. Line 861: `board.Save()` is called with directory path `"k1_design_output"`
2. KiCad's Save() API does not raise an exception for invalid paths
3. No file is created on disk
4. Line 862: Success message is printed regardless of actual save result
5. User has no indication that the save failed

**User sees:** "Board saved to k1_design_output"
**Reality:** No .kicad_pcb file was created

**Fix:**
```python
if self.pcbnew_available and self.board is not None:
    try:
        self.board.Save(str(self.output_path))

        # VERIFY FILE ACTUALLY WROTE TO DISK
        if not Path(self.output_path).exists():
            raise RuntimeError(
                f"Save failed: no file created at {self.output_path}"
            )

        file_size = Path(self.output_path).stat().st_size
        if file_size < 2000:
            raise RuntimeError(
                f"Save produced invalid file ({file_size} bytes, expected >2KB)"
            )

        print(f"      ✅ Board saved to {self.output_path} ({file_size} bytes)")

    except Exception as e:
        print(f"      ❌ ERROR: Board save failed: {e}")
        raise
else:
    print(f"      Board update skipped (pcbnew not available)")
```

---

## CALL STACK ANALYSIS

### How Bug Propagates Through System

```
elite_pcb_designer.py:193
    │
    ├─ output_path="k1_design_output" (DIRECTORY)
    │
    └─→ ComponentPlacement.__init__(board_path, output_path)
            │
            ├─ component_placement.py:108
            │     self.output_path = Path("k1_design_output")  # Still directory
            │
            └─→ component_placement.py:115
                    board = pcbnew.LoadBoard(board_path)  # ✅ Succeeds

                    ... [820-850] placement algorithm ...

                    └─→ component_placement.py:861
                            board.Save("k1_design_output")  # ❌ FAILS

                            └─→ KiCad API: Silent failure
                                    No exception
                                    No file created

                                    └─→ Line 862: Print success anyway
                                            False positive!
```

---

## DATA VERIFICATION

### Board File State Analysis

**Initial State (Before Phase 2):**
- File: `hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb`
- Size: 1,981 bytes
- Contents: Board skeleton only
  - Layer definitions ✓
  - Setup parameters ✓
  - 1 footprint (empty placeholder) ✓
  - 0 traces ✗

**After Phase 2 (Current):**
- File: `hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb`
- Size: **UNCHANGED - 1,981 bytes** (should be 5+ KB)
- Contents: **UNCHANGED** - still skeleton
- Conclusion: **NO CHANGES PERSISTED**

**Expected After Phase 2 (With Fix):**
- File: `k1_design_output/K1_Lightwave.kicad_pcb`
- Size: 5,000-8,000 bytes (contains placements)
- Contents: 52 footprints with positions
- Conclusion: **CHANGES PERSISTED**

---

## API USAGE VERIFICATION

### Correct API Calls (Working)

**Line 794-796: VECTOR2I Creation**
```python
new_pos = pcbnew.VECTOR2I(
    pcbnew.FromMM(pos.x),
    pcbnew.FromMM(pos.y)
)
```
✅ **Correct:** FromMM() converts mm to internal units, VECTOR2I constructor valid

**Line 798: SetPosition()**
```python
footprint.SetPosition(new_pos)
```
✅ **Correct:** VECTOR2I parameter type accepted

**Line 802-804: SetOrientation()**
```python
footprint.SetOrientation(
    pcbnew.EDA_ANGLE(self.components[ref].rotation, pcbnew.DEGREES_T)
)
```
✅ **Correct:** EDA_ANGLE with DEGREES_T enum valid

### Incorrect API Call (Broken)

**Line 861: board.Save()**
```python
self.board.Save(str(self.output_path))
```
❌ **Problem:** self.output_path = Path("k1_design_output") [DIRECTORY]
❌ **Result:** KiCad silently rejects directory path, no exception raised

**Should be:**
```python
self.board.Save(str(Path(self.output_path).with_suffix('.kicad_pcb')))
```
or
```python
self.board.Save(str(self.output_path / 'K1_Lightwave.kicad_pcb'))
```

---

## SECONDARY ISSUES (Separate Bugs)

### Issue #2: DSN Module Availability
**File:** `automated_routing.py`
**Line:** 770-771
**Severity:** HIGH

```python
770 │ try:
771 │     import pcbnew
772 │     from pcbnew import DSN  # ← May not exist in all KiCad builds!
773 │
774 │     # Load original board
775 │     board = pcbnew.LoadBoard(str(self.board_path))
```

**Problem:**
- DSN module only available if KiCad built with Specctra support
- No fallback if DSN unavailable
- ImportError crashes Phase 3

**Fix:**
```python
try:
    from pcbnew import DSN
    HAS_DSN = True
except ImportError:
    HAS_DSN = False
    self.logger.warning("DSN module not available in this KiCad build")
    return False  # Fallback or error

if HAS_DSN:
    db = DSN.SPECCTRA_DB()
    db.LoadSESSION(str(self.ses_file))
    db.ImportSession(board)
```

---

### Issue #3: No Footprint Validation
**File:** `component_placement.py`
**Line:** 790
**Severity:** MEDIUM

```python
790 │ for footprint in self.board.GetFootprints():
```

**Problem:**
- If board has no footprints, GetFootprints() returns empty
- Loop silently does nothing
- User gets success message for placement of 0 components
- No warning that board is empty

**Fix:**
```python
footprints = self.board.GetFootprints()
if not footprints:
    logging.error("No footprints found on board - cannot place components")
    return False

for footprint in footprints:
    # ... placement logic ...
```

---

### Issue #4: No File I/O Error Handling
**Files:** Multiple (component_placement.py:861, automated_routing.py:783)
**Severity:** MEDIUM

**Problem:**
- board.Save() has no try-except protection
- Disk space, permission, or path errors crash silently
- No user feedback on I/O failures

**Fix:**
```python
try:
    self.board.Save(str(self.output_path))
    if not Path(self.output_path).exists():
        raise FileNotFoundError(f"Save failed: no file at {self.output_path}")
except Exception as e:
    logging.error(f"Failed to save board: {e}")
    raise
```

---

## REPRODUCTION STEPS

**To Reproduce the Bug:**

1. Create output directory: `mkdir -p k1_design_output`
2. Run Phase 2:
   ```bash
   python component_placement.py hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb k1_design_output
   ```
3. Check results:
   ```bash
   ls -lah k1_design_output/
   ```

**Current Behavior:**
```
(no .kicad_pcb file in k1_design_output)
```

**Expected Behavior:**
```
-rw-r--r--  6.5K K1_Lightwave.kicad_pcb
```

---

## FIX VERIFICATION CHECKLIST

After applying fixes:

```
Phase 2 Fixes:
  [ ] elite_pcb_designer.py line 193: Pass file path instead of directory
  [ ] component_placement.py line 108: Add directory auto-detection
  [ ] component_placement.py line 861: Add save error detection

Phase 3 Fixes:
  [ ] automated_routing.py line 770: Add DSN availability check
  [ ] automated_routing.py line 774: Handle missing footprints

Verification:
  [ ] Phase 2 creates output .kicad_pcb file
  [ ] Output file size > 5 KB
  [ ] Output file contains 52 footprints
  [ ] Phase 3 loads output from Phase 2
  [ ] Gerber export contains trace data
  [ ] No silent failures in any phase
```

---

## SUMMARY TABLE

| Issue | File | Line | Type | Fix Time |
|-------|------|------|------|----------|
| Directory path passed | elite_pcb_designer.py | 195 | CRITICAL | 2 min |
| No path validation | component_placement.py | 108 | MEDIUM | 3 min |
| Silent save failure | component_placement.py | 861 | HIGH | 5 min |
| DSN not available | automated_routing.py | 770 | HIGH | 5 min |
| No footprint check | component_placement.py | 790 | MEDIUM | 2 min |
| No I/O error handling | Multiple | - | MEDIUM | 5 min |
| **TOTAL** | | | | **22 min** |

---

**This reference provides exact line numbers and code snippets for all issues and fixes.**
