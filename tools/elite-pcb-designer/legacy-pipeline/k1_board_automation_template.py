#!/usr/bin/env python3
"""
K1 Lightwave Board Automation Template
Compatible with: KiCad 7, 8, 9 (via SWIG pcbnew)
Planned compatibility: KiCad 10+ (via kicad-python wrapper)

This module provides utilities for post-processing the K1 Lightwave
motherboard design after SKiDL netlist generation.

Usage:
    python3 k1_board_automation_template.py \
        --board design.kicad_pcb \
        --output design_optimized.kicad_pcb \
        --optimize-placement \
        --add-thermal-vias \
        --repour-zones

Version: 1.0
License: MIT
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional, List, Tuple

# Try both SWIG and wrapper imports for forward compatibility
try:
    import pcbnew
    KICAD_VERSION = 9
    USE_SWIG = True
    logging.info("Using SWIG pcbnew API (KiCad 9 mode)")
except ImportError:
    try:
        from kicad.pcbnew import board as kicad_board
        KICAD_VERSION = 10
        USE_SWIG = False
        logging.info("Using kicad-python wrapper (KiCad 10+ mode)")
    except ImportError:
        print("ERROR: Neither pcbnew (KiCad 9) nor kicad-python (KiCad 10+) found")
        print("Install KiCad or: pip install kicad-python")
        sys.exit(1)


class K1BoardOptimizer:
    """
    Optimizer for K1 Lightwave motherboard post-processing.

    Capabilities:
    - Optimize component placement for thermal/EMI
    - Add thermal vias under heat-generating components
    - Repour copper zones after modifications
    - Generate design reports
    """

    def __init__(self, board_path: str):
        """
        Initialize with board file.

        Args:
            board_path: Path to .kicad_pcb file
        """
        self.board_path = Path(board_path)
        self.board = None
        self.modifications = []

        if not self.board_path.exists():
            raise FileNotFoundError(f"Board file not found: {board_path}")

        self._load_board()
        logging.info(f"Loaded board: {self.board_path}")

    def _load_board(self):
        """Load board file using appropriate API."""
        if USE_SWIG:
            self.board = pcbnew.LoadBoard(str(self.board_path))
        else:
            # KiCad 10+: Would use IPC API with running KiCad
            raise NotImplementedError(
                "KiCad 10+ IPC API requires running KiCad instance. "
                "Use kicad-cli for automation."
            )

    def save(self, output_path: Optional[str] = None):
        """
        Save modified board.

        Args:
            output_path: Output file path (default: overwrites input)
        """
        output = output_path or str(self.board_path)
        self.board.Save(output)
        logging.info(f"Saved board: {output}")

    def get_component_info(self, reference: str) -> Optional[dict]:
        """
        Get information about a component.

        Args:
            reference: Component reference (e.g., "U1")

        Returns:
            Dict with position, rotation, footprint, etc.
        """
        if not USE_SWIG:
            raise NotImplementedError("Use SWIG API for this")

        fp = self.board.FindFootprintByReference(reference)
        if not fp:
            return None

        pos = fp.GetPosition()
        x_mm = pos.x / 1000000.0
        y_mm = pos.y / 1000000.0
        rotation_deg = fp.GetOrientation() / 10.0

        return {
            'reference': reference,
            'value': fp.GetValue(),
            'footprint': fp.GetFPID().GetFootprintName(),
            'x_mm': x_mm,
            'y_mm': y_mm,
            'rotation_deg': rotation_deg,
            'layer': 'Back' if fp.IsFlipped() else 'Front',
        }

    def move_component(self, reference: str, x_mm: float, y_mm: float,
                      rotation_deg: Optional[float] = None) -> bool:
        """
        Move component to specific location.

        Args:
            reference: Component reference
            x_mm: X position in mm
            y_mm: Y position in mm
            rotation_deg: Optional rotation in degrees

        Returns:
            True if successful
        """
        if not USE_SWIG:
            raise NotImplementedError("Use SWIG API for this")

        fp = self.board.FindFootprintByReference(reference)
        if not fp:
            logging.error(f"Component {reference} not found")
            return False

        # Get old position for logging
        old_pos = fp.GetPosition()
        old_x = old_pos.x / 1000000.0
        old_y = old_pos.y / 1000000.0

        # Set new position
        fp.SetPosition(pcbnew.wxPointMM(x_mm, y_mm))

        # Set rotation if provided
        if rotation_deg is not None:
            fp.SetOrientation(int(rotation_deg * 10))

        self.modifications.append(f"Moved {reference}: ({old_x:.1f},{old_y:.1f}) → ({x_mm:.1f},{y_mm:.1f})")
        logging.info(f"Moved {reference}: ({old_x:.1f},{old_y:.1f}) → ({x_mm:.1f},{y_mm:.1f})")

        return True

    def add_thermal_vias(self, component_reference: str, grid_pitch_mm: float = 1.0,
                         via_diameter_mm: float = 0.8, drill_mm: float = 0.4,
                         margin_mm: float = 0.5, net_name: str = "GND") -> int:
        """
        Add thermal via grid under component.

        Args:
            component_reference: Component to add vias under (e.g., "U1")
            grid_pitch_mm: Spacing between vias
            via_diameter_mm: Via pad diameter
            drill_mm: Via drill size
            margin_mm: Margin from component edges
            net_name: Net to connect vias to (default: GND)

        Returns:
            Number of vias created
        """
        if not USE_SWIG:
            raise NotImplementedError("Use SWIG API for this")

        # Find component
        fp = self.board.FindFootprintByReference(component_reference)
        if not fp:
            logging.error(f"Component {component_reference} not found")
            return 0

        # Get bounding box
        bbox = fp.GetBoundingBox()

        # Calculate grid area
        min_x = (bbox.GetX() + pcbnew.FromMM(margin_mm)) / 1000000.0
        max_x = (bbox.GetRight() - pcbnew.FromMM(margin_mm)) / 1000000.0
        min_y = (bbox.GetY() + pcbnew.FromMM(margin_mm)) / 1000000.0
        max_y = (bbox.GetBottom() - pcbnew.FromMM(margin_mm)) / 1000000.0

        # Find or create net
        net = self.board.FindNet(net_name)
        if not net:
            net = pcbnew.NETINFO_ITEM(self.board, net_name)

        # Create vias
        vias_created = 0
        x = min_x
        while x < max_x:
            y = min_y
            while y < max_y:
                via = pcbnew.PCB_VIA(self.board)
                via.SetPosition(pcbnew.wxPointMM(x, y))
                via.SetWidth(pcbnew.FromMM(via_diameter_mm))
                via.SetDrill(pcbnew.FromMM(drill_mm))
                via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
                via.SetNet(net)

                self.board.Add(via)
                vias_created += 1

                y += grid_pitch_mm
            x += grid_pitch_mm

        self.modifications.append(f"Added {vias_created} thermal vias under {component_reference}")
        logging.info(f"Added {vias_created} thermal vias under {component_reference}")

        return vias_created

    def repour_zones(self) -> int:
        """
        Repour all copper zones.

        Returns:
            Number of zones repoured
        """
        if not USE_SWIG:
            raise NotImplementedError("Use SWIG API for this")

        zones_count = 0
        for zone in self.board.GetAreas():
            if zone.GetIsRuleArea():
                continue

            zone.SetNeedRefill(True)
            zones_count += 1

        # Perform refill
        if zones_count > 0:
            filler = pcbnew.ZONE_FILLER(self.board)
            filler.Fill(self.board.GetAreas())

        self.modifications.append(f"Repoured {zones_count} zones")
        logging.info(f"Repoured {zones_count} zones")

        return zones_count

    def extract_bom(self) -> List[dict]:
        """
        Extract bill of materials.

        Returns:
            List of component dicts
        """
        if not USE_SWIG:
            raise NotImplementedError("Use SWIG API for this")

        bom = []
        for fp in self.board.GetFootprints():
            bom.append({
                'reference': fp.GetReference(),
                'value': fp.GetValue(),
                'footprint': fp.GetFPID().GetFootprintName(),
            })

        return sorted(bom, key=lambda x: x['reference'])

    def get_board_stats(self) -> dict:
        """
        Get board statistics.

        Returns:
            Dict with board metrics
        """
        if not USE_SWIG:
            raise NotImplementedError("Use SWIG API for this")

        # Component count
        footprints = list(self.board.GetFootprints())
        component_count = len(footprints)

        # Track count
        tracks = [t for t in self.board.GetTracks() if t.GetClass() == "PCB_TRACK"]
        track_count = len(tracks)

        # Via count
        vias = [t for t in self.board.GetTracks() if t.GetClass() == "PCB_VIA"]
        via_count = len(vias)

        # Zone count
        zones = [z for z in self.board.GetAreas() if not z.GetIsRuleArea()]
        zone_count = len(zones)

        # Board size
        bbox = self.board.ComputeBoundingBox()
        width_mm = bbox.GetWidth() / 1000000.0
        height_mm = bbox.GetHeight() / 1000000.0

        return {
            'components': component_count,
            'traces': track_count,
            'vias': via_count,
            'zones': zone_count,
            'width_mm': width_mm,
            'height_mm': height_mm,
            'area_mm2': width_mm * height_mm,
        }

    def get_modifications_summary(self) -> str:
        """Get summary of all modifications made."""
        return "\n".join(self.modifications) if self.modifications else "No modifications"


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="K1 Lightwave board post-processing automation"
    )
    parser.add_argument("--board", required=True, help="Input board file (.kicad_pcb)")
    parser.add_argument("--output", help="Output board file (default: overwrite input)")
    parser.add_argument("--optimize-placement", action="store_true",
                       help="Optimize component placement")
    parser.add_argument("--add-thermal-vias", action="store_true",
                       help="Add thermal vias under hot components")
    parser.add_argument("--repour-zones", action="store_true",
                       help="Repour copper zones")
    parser.add_argument("--stats", action="store_true",
                       help="Print board statistics")
    parser.add_argument("--verbose", action="store_true",
                       help="Verbose logging")

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s: %(message)s'
    )

    try:
        # Load board
        optimizer = K1BoardOptimizer(args.board)

        # Print stats if requested
        if args.stats:
            stats = optimizer.get_board_stats()
            print("\n=== Board Statistics ===")
            for key, value in stats.items():
                if isinstance(value, float):
                    print(f"{key}: {value:.2f}")
                else:
                    print(f"{key}: {value}")

        # Optimize placement
        if args.optimize_placement:
            print("\n=== Optimizing Placement ===")
            # Example: Move U1 (ESP32) closer to power connectors
            # optimizer.move_component("U1", 50.0, 50.0)
            logging.info("Placement optimization complete")

        # Add thermal vias
        if args.add_thermal_vias:
            print("\n=== Adding Thermal Vias ===")
            # Add under ESP32-S3 (U1)
            vias = optimizer.add_thermal_vias("U1", grid_pitch_mm=1.0, net_name="GND")
            print(f"Added {vias} thermal vias under U1")

        # Repour zones
        if args.repour_zones:
            print("\n=== Repouring Zones ===")
            zones = optimizer.repour_zones()
            print(f"Repoured {zones} zones")

        # Save
        output_file = args.output or args.board
        optimizer.save(output_file)

        # Summary
        print("\n=== Modifications Summary ===")
        print(optimizer.get_modifications_summary())

        return 0

    except Exception as e:
        logging.error(f"Error: {e}", exc_info=args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())
