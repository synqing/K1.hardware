#!/usr/bin/env python3
"""
Demo: K1 Lightwave Component Placement
Demonstrates intelligent component placement with netlist import.
"""

import sys
import tempfile
import shutil
from pathlib import Path

try:
    import pcbnew
except ImportError:
    print("ERROR: pcbnew module not found.")
    print("Please run this script with KiCad's Python:")
    print("  ./run_placement_demo.sh")
    sys.exit(1)

from component_placement import ComponentPlacement


def import_netlist_to_board(board_path: str, netlist_path: str) -> bool:
    """
    Import netlist into KiCad board.

    Args:
        board_path: Path to .kicad_pcb file
        netlist_path: Path to .net netlist file

    Returns:
        True if successful
    """
    try:
        # Load board
        board = pcbnew.LoadBoard(board_path)

        # Create netlist reader
        netlist = pcbnew.NETLIST()

        # Try to read netlist
        try:
            # KiCad 9.x API
            reader = netlist.ReadNetlistFile(netlist_path)
        except AttributeError:
            # Alternative API for different KiCad versions
            print("Note: Using alternative netlist import method")
            # For this demo, we'll create mock components instead
            return False

        # Get list of components from netlist
        components = netlist.GetComponentList()

        print(f"Found {len(components)} components in netlist")

        # Add footprints to board
        for comp_idx in range(len(components)):
            component = components[comp_idx]
            ref = component.GetReference()
            footprint_name = component.GetFootprint()

            # Create footprint
            footprint = pcbnew.FootprintLoad(
                component.GetFootprintLibrary(),
                footprint_name
            )

            if footprint:
                footprint.SetReference(ref)
                # Place at origin initially (placement engine will move it)
                footprint.SetPosition(pcbnew.VECTOR2I(0, 0))
                board.Add(footprint)

        # Save board with imported components
        board.Save(board_path)
        print(f"Imported {len(components)} components to board")

        return True

    except Exception as e:
        print(f"Netlist import failed: {e}")
        return False


def create_mock_board(board_path: str) -> bool:
    """
    Create a mock K1 board with representative components for demo.

    Args:
        board_path: Path to save board

    Returns:
        True if successful
    """
    try:
        # Create new board
        board = pcbnew.BOARD()

        # Set board outline (50mm x 80mm)
        outline_shape = pcbnew.PCB_SHAPE()
        outline_shape.SetShape(pcbnew.SHAPE_T_RECT)
        outline_shape.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(0), pcbnew.FromMM(0)))
        outline_shape.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(50), pcbnew.FromMM(80)))
        outline_shape.SetLayer(pcbnew.Edge_Cuts)
        outline_shape.SetWidth(pcbnew.FromMM(0.1))
        board.Add(outline_shape)

        # Define representative components with their footprints
        mock_components = [
            # MCUs
            ("U1", "Package_DFN_QFN:QFN-56-1EP_7x7mm_P0.4mm_EP5.6x5.6mm"),
            ("U3", "Package_DFN_QFN:QFN-56-1EP_7x7mm_P0.4mm_EP5.6x5.6mm"),
            ("U6", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"),
            ("U7", "Package_TO_SOT_SMD:SOT-23-5"),
            ("U8", "Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm"),

            # Connectors
            ("J1", "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12"),
            ("J3", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"),
            ("J4", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"),
            ("J5", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"),
            ("J6", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"),
            ("J7", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"),
            ("J8", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"),
            ("J9", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"),
            ("JLED1", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical"),
            ("JLED2", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical"),
            ("JLED3", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical"),
            ("JLED4", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical"),

            # Capacitors
            ("C3", "Capacitor_SMD:C_0603_1608Metric"),
            ("C4", "Capacitor_SMD:C_0603_1608Metric"),
            ("C5", "Capacitor_SMD:C_0603_1608Metric"),
            ("C_BIN1", "Capacitor_SMD:C_1206_3216Metric"),
            ("C_BOUT1", "Capacitor_SMD:C_1206_3216Metric"),

            # Resistors
            ("R1", "Resistor_SMD:R_0603_1608Metric"),
            ("R2", "Resistor_SMD:R_0603_1608Metric"),
            ("R3", "Resistor_SMD:R_0603_1608Metric"),
            ("R4", "Resistor_SMD:R_0603_1608Metric"),
            ("R5", "Resistor_SMD:R_0603_1608Metric"),
            ("R_USB_DP", "Resistor_SMD:R_0603_1608Metric"),
            ("R_USB_DM", "Resistor_SMD:R_0603_1608Metric"),
            ("R_CC1", "Resistor_SMD:R_0603_1608Metric"),
            ("R_CC2", "Resistor_SMD:R_0603_1608Metric"),
            ("RLED1", "Resistor_SMD:R_0603_1608Metric"),
            ("RLED2", "Resistor_SMD:R_0603_1608Metric"),
            ("RLED3", "Resistor_SMD:R_0603_1608Metric"),
            ("RLED4", "Resistor_SMD:R_0603_1608Metric"),

            # Diodes
            ("D1", "Diode_SMD:D_SOD-323"),
            ("D2", "Diode_SMD:D_SOD-323"),
            ("D3", "Diode_SMD:D_SOD-323"),
            ("D4", "Diode_SMD:D_SOD-323"),
            ("D_ESD_DP", "Package_TO_SOT_SMD:SOT-23"),
            ("D_ESD_DM", "Package_TO_SOT_SMD:SOT-23"),

            # Fuses
            ("F1", "Fuse:Fuse_1206_3216Metric"),
            ("F2", "Fuse:Fuse_1206_3216Metric"),
            ("F3", "Fuse:Fuse_1206_3216Metric"),
            ("F4", "Fuse:Fuse_1206_3216Metric"),
            ("F_USB", "Fuse:Fuse_1206_3216Metric"),
        ]

        print(f"Creating mock board with {len(mock_components)} components...")

        # Add each component as a footprint
        for ref, footprint_name in mock_components:
            # Create a simple footprint with pads
            footprint = pcbnew.FOOTPRINT(board)
            footprint.SetReference(ref)
            footprint.SetValue(footprint_name.split(':')[-1])

            # Set initial position at origin (placement engine will move it)
            footprint.SetPosition(pcbnew.VECTOR2I(
                pcbnew.FromMM(25),  # Center of board
                pcbnew.FromMM(40)
            ))

            # Add simple pad for visualization
            pad = pcbnew.PAD(footprint)
            pad.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(1), pcbnew.FromMM(1)))
            pad.SetShape(pcbnew.PAD_SHAPE_RECT)
            pad.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
            pad.SetLayerSet(pad.SMDMask())
            footprint.Add(pad)

            board.Add(footprint)

        # Save board
        board.Save(board_path)
        print(f"Mock board saved to {board_path}")

        return True

    except Exception as e:
        print(f"Failed to create mock board: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main demo function"""
    print("=" * 80)
    print("K1 LIGHTWAVE COMPONENT PLACEMENT DEMO")
    print("=" * 80)
    print()

    # Paths
    project_root = Path(__file__).parent
    netlist_path = project_root / "hardware/k1-lightwave/k1_motherboard_revA_resolved.net"
    board_path = project_root / "hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb"

    # Create temporary working board
    with tempfile.TemporaryDirectory() as tmpdir:
        demo_board_path = Path(tmpdir) / "K1_Lightwave_demo.kicad_pcb"

        # Try to import netlist first
        print("[Step 1/4] Preparing board...")
        if netlist_path.exists():
            print(f"Found netlist: {netlist_path}")
            # Copy original board to temp location
            shutil.copy(board_path, demo_board_path)

            # Try netlist import
            if not import_netlist_to_board(str(demo_board_path), str(netlist_path)):
                print("Netlist import not available, creating mock board instead...")
                create_mock_board(str(demo_board_path))
        else:
            print("Netlist not found, creating mock board...")
            create_mock_board(str(demo_board_path))

        # Verify board has components
        board = pcbnew.LoadBoard(str(demo_board_path))
        footprints = list(board.GetFootprints())
        print(f"Board loaded with {len(footprints)} components")

        if len(footprints) == 0:
            print("\nWARNING: Board has no components!")
            print("The placement engine requires a populated board.")
            print("Please import the netlist in KiCad first:")
            print("  Tools -> Update PCB from Schematic")
            print()
            return 1

        print()

        # Initialize placement engine
        print("[Step 2/4] Initializing placement engine...")
        output_path = Path(tmpdir) / "K1_Lightwave_placed.kicad_pcb"
        placer = ComponentPlacement(str(demo_board_path), str(output_path))
        print(f"Loaded {len(placer.components)} components")
        print()

        # Execute placement
        print("[Step 3/4] Executing intelligent placement...")
        success = placer.execute()
        print()

        # Generate reports
        print("[Step 4/4] Generating reports...")
        print()
        print(placer.generate_placement_report())
        print()
        print()
        print("BOARD VISUALIZATION:")
        print("=" * 80)
        print(placer.generate_ascii_visualization())
        print()

        # Save results
        if success:
            # Copy placed board to project directory
            final_output = project_root / "K1_Lightwave_placed_demo.kicad_pcb"
            shutil.copy(output_path, final_output)
            print(f"✓ Placed board saved to: {final_output}")

            # Save reports
            report_path = project_root / "placement_report_demo.txt"
            with open(report_path, 'w') as f:
                f.write(placer.generate_placement_report())
                f.write("\n\n")
                f.write("BOARD VISUALIZATION:\n")
                f.write("=" * 80 + "\n")
                f.write(placer.generate_ascii_visualization())
            print(f"✓ Report saved to: {report_path}")

            print()
            print("=" * 80)
            print("DEMO COMPLETE - PLACEMENT SUCCESSFUL!")
            print("=" * 80)
            return 0
        else:
            print()
            print("=" * 80)
            print("DEMO COMPLETE - PLACEMENT HAD VIOLATIONS")
            print("Review the report above for details.")
            print("=" * 80)
            return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nERROR: Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
