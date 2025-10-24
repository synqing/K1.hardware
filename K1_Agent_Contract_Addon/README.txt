
K1 Agent Contract Addon — 2025-10-24

Files:
- tools/k1_project.json — the Design Contract (board outline, holes, keepouts, edge placements, zones, rules).
- plugins/K1_ContractedPlace.py — KiCad plugin that enforces the contract: outline/holes/edge placements/zones/keepouts.

How to use:
1) Copy tools/k1_project.json to your repo at tools/.
2) Open the board in KiCad PCB Editor.
3) Tools → External Plugins → K1: Contracted Place (Design Contract).
4) The plugin will draw the outline if missing, add mounting holes, place USB and LED connectors on the requested edges, place COM-A / COM-B in their zones, apply antenna keepout, and save.

This is the missing "ask the right questions" layer. Change values in k1_project.json once; the board becomes reproducible and non-ambiguous.
