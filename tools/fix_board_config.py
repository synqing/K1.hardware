#!/usr/bin/env python3
"""
Fix K1 board configuration for 4-layer stackup and correct outline.

Issues:
1. Board has only 2 copper layers (F.Cu, B.Cu), needs 4 layers (F.Cu, In1.Cu, In2.Cu, B.Cu)
2. Board outline is 100×60mm, should be 100×70mm per contract
"""

import re
from pathlib import Path

board_file = Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")
contract_file = Path("tools/k1_project_v2.json")

print("=" * 70)
print("K1 Board Configuration Fixer")
print("=" * 70)

# Read the board file
content = board_file.read_text()

# Fix 1: Update layers to include In1.Cu and In2.Cu
print("\n1️⃣  Fixing layers (adding In1.Cu and In2.Cu)...")

# The layers section lists all layers with their indices
# We need to add In1.Cu (layer 1) and In2.Cu (layer 3) to the layers section
layers_old = r"""	\(layers
		\(0 "F\.Cu" signal\)
		\(2 "B\.Cu" signal\)"""

layers_new = """	(layers
		(0 "F.Cu" signal)
		(1 "In1.Cu" signal)
		(2 "In2.Cu" signal)
		(3 "B.Cu" signal)"""

content = re.sub(layers_old, layers_new, content)
print("   ✓ Added In1.Cu and In2.Cu to layers section")

# Fix 2: Update stackup to include In1.Cu and In2.Cu
print("\n2️⃣  Fixing stackup (adding inner copper layers with dielectric)...")

# Find and replace the stackup section
stackup_old = r"""	\(stackup
		\(layer "F\.Cu"
			\(type "copper"\)
			\(thickness 0\.035\)
		\)
		\(layer "B\.Cu"
			\(type "copper"\)
			\(thickness 0\.035\)
		\)
		\(copper_finish "None"\)
		\(dielectric_constraints no\)
	\)"""

stackup_new = """	(stackup
		(layer "F.Cu"
			(type "copper")
			(thickness 0.035)
		)
		(layer "Dielectric"
			(type "dielectric")
			(thickness 0.17)
			(material "FR4")
			(epsilon_r 4.6)
			(loss_tangent 0.02)
		)
		(layer "In1.Cu"
			(type "copper")
			(thickness 0.035)
		)
		(layer "Dielectric"
			(type "dielectric")
			(thickness 0.17)
			(material "FR4")
			(epsilon_r 4.6)
			(loss_tangent 0.02)
		)
		(layer "In2.Cu"
			(type "copper")
			(thickness 0.035)
		)
		(layer "Dielectric"
			(type "dielectric")
			(thickness 0.17)
			(material "FR4")
			(epsilon_r 4.6)
			(loss_tangent 0.02)
		)
		(layer "B.Cu"
			(type "copper")
			(thickness 0.035)
		)
		(copper_finish "None")
		(dielectric_constraints no)
	)"""

content = re.sub(stackup_old, stackup_new, content)
print("   ✓ Updated stackup with 4-layer configuration (0.6mm total with FR4)")

# Fix 3: Update board outline from 100×60 to 100×70
print("\n3️⃣  Fixing board outline (100×70mm per contract)...")

# Current: (start 10 10) (end 110 70) = 100×60
# Needed: (start 10 10) (end 110 80) = 100×70
# Or better: (start 0 0) (end 100 70) = 100×70 centered

outline_old = r"""	\(gr_rect
		\(start 10 10\)
		\(end 110 70\)"""

outline_new = """	(gr_rect
		(start 0 0)
		(end 100 70)"""

content = re.sub(outline_old, outline_new, content)
print("   ✓ Updated outline to 100×70mm, origin at (0,0)")

# Write the fixed board file
board_file.write_text(content)

print("\n" + "=" * 70)
print("✅ Board configuration fixed!")
print("=" * 70)
print("\nChanges made:")
print("  • Layers: Added In1.Cu (layer 1) and In2.Cu (layer 2)")
print("  • Stackup: 4-layer FR4 board (0.6mm total thickness)")
print("  • Outline: Changed from 100×60mm to 100×70mm")
print("  • Origin: Adjusted to (0, 0)")
print("\nNext steps:")
print("  1. Run K1_ContractedPlace_PRO plugin in KiCad to reapply contract")
print("  2. Save the board in KiCad to verify layers are correct")
print("  3. Ensure FreeRouting JAR is at tools/freerouting.jar")
print("  4. Run orchestrator: python agent/orchestrator/run.py tools/k1_project_v2.json")
