# JLCPCB PCB Panelization Guidelines

## Overview

JLCPCB allows customers to merge multiple PCB designs into a single panel, though this may incur additional charges due to increased fabrication complexity.

## Cost-Saving Method for Prototypes

For prototype phases, designs can be "placed all inside one overall board outline" with silk layer markings to separate them. Users must manually cut boards apart after receiving them (recommended before assembly). This method is free for up to 5 designs, but "more than 5 designs...still needs to be charged as different designs," with a maximum of 10 designs per board.

## V-Cut/V-Groove Method

This technique accelerates SMT soldering by creating separation lines between sub-boards.

**Key Specifications:**
- V-cut lines must match sub-PCB outlines with zero spacing
- Only vertical or horizontal straight lines allowed
- Minimum panel size: 70×70mm
- Maximum edge length: 400mm; minimum width: 70mm
- Lines must cross the entire panel (cannot stop midway)

**Maximum Panel Sizes by Thickness:**
- 0.6mm: 100×100mm
- 0.8–1.2mm: 200×200mm
- 1.6mm: 300×300mm
- Panels with 5+ designs: 200×200mm maximum

## Additional Notes

When selecting "Panel by JLCPCB," edge rails, marks, and positioning holes are added automatically, though fiducial marks aren't applied to individual pieces.

Source: JLCPCB Support Documentation
