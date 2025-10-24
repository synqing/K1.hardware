
K1 Agent Contract Addon — PRO  (2025-10-24)

Files:
- tools/k1_project_v2.json — expanded Design Contract (outline, holes, keepouts, zones, planes, routing, thermals, testpoints).
- plugins/K1_ContractedPlace_PRO.py — KiCad plugin that enforces the contract and adds decouplers, via fences, netclasses, planes, thermal via grids, testpoints.

How to use:
1) Copy tools/k1_project_v2.json into your repo at tools/ and edit as needed (board size, zones, nets).
2) Install plugins/K1_ContractedPlace_PRO.py in your KiCad plugin folder.
3) Open the board in KiCad PCB Editor and run Tools → External Plugins → "K1: Contracted Place PRO".
4) Save, then run your route/DRC/export script.

This adds the "expert" logic you asked for: explicit contract, deterministic placement, decoupler distribution, return-path stitching, power planes, thermal via grids, netclass enforcement, and testpoints — all before routing.
