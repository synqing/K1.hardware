"""
Test script for Design Preparation Phase 1
Demonstrates execution on K1 Lightwave motherboard
"""

import sys
from pathlib import Path
import logging

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from design_preparation import DesignPreparation


def test_k1_design_preparation():
    """Tests the full design preparation pipeline on the K1 Lightwave board.

    This function serves as an integration test for the `DesignPreparation`
    class, running all the steps on the actual K1 Lightwave project files. It
    prints a detailed report of the process and its results.

    Returns:
        True if the design preparation pipeline completes successfully, False
        otherwise.
    """

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # K1 file paths
    base_path = Path(__file__).parent
    netlist_path = base_path / "hardware/k1-lightwave/k1_motherboard_revA.net"
    board_path = base_path / "hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb"
    output_path = base_path / "hardware/k1-lightwave/kicad/K1_Lightwave_phase1.kicad_pcb"
    report_path = base_path / "design_preparation_report.json"

    print("\n" + "="*70)
    print("Testing Elite PCB Designer Agent - Phase 1")
    print("K1 Lightwave Motherboard Rev A")
    print("="*70)

    # Verify files exist
    print(f"\nChecking input files...")
    print(f"  Netlist: {netlist_path}")
    print(f"    Exists: {netlist_path.exists()}")
    print(f"  Board:   {board_path}")
    print(f"    Exists: {board_path.exists()}")

    if not netlist_path.exists():
        print("\nERROR: Netlist not found!")
        print(f"Expected: {netlist_path}")
        return False

    if not board_path.exists():
        print("\nERROR: Board file not found!")
        print(f"Expected: {board_path}")
        return False

    # Create design preparation instance
    print("\nInitializing Design Preparation...")
    prep = DesignPreparation(
        netlist_path=netlist_path,
        board_path=board_path,
        output_path=output_path,
        kicad_cli='/opt/homebrew/bin/kicad-cli'
    )

    # Execute Phase 1
    print("\nExecuting Phase 1 pipeline...\n")
    success = prep.execute()

    # Save detailed report
    print(f"\nSaving detailed report...")
    prep.save_report(report_path)
    print(f"Report saved to: {report_path}")

    # Print footprint assignments
    print("\n" + "="*70)
    print("FOOTPRINT ASSIGNMENTS")
    print("="*70)

    assignments = prep.results['footprints_assigned']
    if assignments:
        # Group by footprint type
        by_footprint = {}
        for ref, footprint in sorted(assignments.items()):
            if footprint not in by_footprint:
                by_footprint[footprint] = []
            by_footprint[footprint].append(ref)

        for footprint, refs in sorted(by_footprint.items()):
            print(f"\n{footprint}:")
            print(f"  Components ({len(refs)}): {', '.join(sorted(refs))}")
    else:
        print("No footprint assignments generated")

    # Print IC replacements
    print("\n" + "="*70)
    print("IC PLACEHOLDER REPLACEMENTS NEEDED")
    print("="*70)

    replacements = prep.results['ic_replacements_needed']
    for ref, spec in sorted(replacements.items()):
        print(f"\n{ref}:")
        print(f"  Current:     {spec['current']}")
        print(f"  Target:      {spec['target']}")
        print(f"  Footprint:   {spec['footprint']}")
        print(f"  Description: {spec['description']}")

    # Final status
    print("\n" + "="*70)
    print("FINAL STATUS")
    print("="*70)
    print(f"Overall Success: {success}")
    print(f"Errors:   {len(prep.results['errors'])}")
    print(f"Warnings: {len(prep.results['warnings'])}")

    if output_path.exists():
        print(f"\nOutput board saved to: {output_path}")
    else:
        print(f"\nNote: Output board not created (netlist import may have failed)")
        print(f"This is expected if KiCad CLI import-netlist is not available")

    return success


if __name__ == '__main__':
    success = test_k1_design_preparation()
    sys.exit(0 if success else 1)
