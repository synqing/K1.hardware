#!/usr/bin/env python3
"""
Elite PCB Designer Agent - K1 Lightwave Complete Design Example
================================================================

Complete example showing how to automate the K1 Lightwave PCB design
from netlist to manufacturing-ready board.

This script demonstrates:
- Full pipeline execution
- Custom configuration
- Error handling
- Result inspection
- Manufacturing file generation

Usage:
    python example_k1_full_design.py

Requirements:
- KiCad 8.0+ with Python API
- FreeRouting (optional, for Phase 3)
- K1 Lightwave netlist and board files

Author: Elite PCB Designer Agent
Version: 1.0.0
Date: 2025-10-24
"""

import sys
from pathlib import Path
from elite_pcb_designer import ElitePCBDesigner, PhaseStatus


def verify_requirements() -> bool:
    """Verify all required files exist"""
    print("Verifying requirements...")

    # Check for netlist
    netlist_paths = [
        Path("hardware/k1-lightwave/k1_motherboard_revA.net"),
        Path("k1_motherboard_revA.net"),
    ]

    netlist_path = None
    for path in netlist_paths:
        if path.exists():
            netlist_path = path
            break

    if not netlist_path:
        print("❌ Error: K1 netlist not found")
        print("   Expected: hardware/k1-lightwave/k1_motherboard_revA.net")
        return False

    print(f"✅ Netlist found: {netlist_path}")

    # Check for board
    board_paths = [
        Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb"),
        Path("K1_Lightwave.kicad_pcb"),
    ]

    board_path = None
    for path in board_paths:
        if path.exists():
            board_path = path
            break

    if not board_path:
        print("❌ Error: K1 board file not found")
        print("   Expected: hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")
        return False

    print(f"✅ Board found: {board_path}")

    # Try to import pcbnew
    try:
        import pcbnew
        print("✅ KiCad Python API available")
    except ImportError:
        print("⚠️  Warning: KiCad Python API not found")
        print("   Install KiCad 8.0+ with Python support")
        return False

    return True


def run_full_design(skip_routing: bool = False) -> bool:
    """
    Run complete K1 Lightwave design automation.

    Args:
        skip_routing: If True, skip Phase 3 (routing) for manual completion

    Returns:
        True if design completed successfully
    """
    # Define file paths
    netlist_path = "hardware/k1-lightwave/k1_motherboard_revA.net"
    board_path = "hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb"
    output_dir = "k1_design_output"

    print("\n" + "=" * 80)
    print("K1 LIGHTWAVE - AUTOMATED PCB DESIGN")
    print("=" * 80)
    print(f"Netlist: {netlist_path}")
    print(f"Board: {board_path}")
    print(f"Output: {output_dir}")
    if skip_routing:
        print("Mode: Skip routing (manual finish)")
    print("=" * 80 + "\n")

    # Create designer
    try:
        designer = ElitePCBDesigner(
            netlist_path=netlist_path,
            board_path=board_path,
            output_dir=output_dir,
            verbose=True,
            skip_phases=[3] if skip_routing else None
        )
    except Exception as e:
        print(f"❌ Failed to initialize designer: {e}")
        return False

    # Execute pipeline
    print("Starting automated PCB design pipeline...")
    print("This will take approximately 20-30 minutes.")
    print("Press Ctrl+C to interrupt at any time.\n")

    try:
        success = designer.execute_full_pipeline()

        if success:
            print("\n" + "=" * 80)
            print("✅ PCB DESIGN COMPLETE!")
            print("=" * 80)

            # Print detailed results
            print_detailed_results(designer)

            # Print next steps
            print_next_steps(output_dir, skip_routing)

            return True
        else:
            print("\n" + "=" * 80)
            print("❌ PCB DESIGN FAILED")
            print("=" * 80)

            # Print failure analysis
            print_failure_analysis(designer)

            return False

    except KeyboardInterrupt:
        print("\n\n⚠️  Design interrupted by user")
        print("Progress saved to:", output_dir)
        return False


def print_detailed_results(designer: ElitePCBDesigner) -> None:
    """Print detailed results from all phases"""
    print("\n📊 DETAILED RESULTS")
    print("-" * 80)

    for phase_num in sorted(designer.results.keys()):
        result = designer.results[phase_num]

        status_icon = {
            PhaseStatus.COMPLETED: "✅",
            PhaseStatus.FAILED: "❌",
            PhaseStatus.SKIPPED: "⊘",
        }.get(result.status, "?")

        print(f"\n{status_icon} Phase {phase_num}: {result.phase_name}")
        print(f"   Status: {result.status.value.upper()}")
        print(f"   Duration: {result.duration_str}")

        if result.details:
            print("   Details:")
            for key, value in result.details.items():
                print(f"      {key}: {value}")


def print_failure_analysis(designer: ElitePCBDesigner) -> None:
    """Print failure analysis and recovery suggestions"""
    print("\n🔍 FAILURE ANALYSIS")
    print("-" * 80)

    failed_phases = [
        (num, result)
        for num, result in designer.results.items()
        if result.status == PhaseStatus.FAILED
    ]

    if not failed_phases:
        print("No failures detected (unexpected)")
        return

    for phase_num, result in failed_phases:
        print(f"\n❌ Phase {phase_num}: {result.phase_name}")
        if result.error_message:
            print(f"   Error: {result.error_message}")

        # Provide phase-specific recovery suggestions
        if phase_num == 1:
            print("\n   Recovery suggestions:")
            print("   1. Verify netlist format (KiCad 8.0+)")
            print("   2. Check board file exists and is valid")
            print("   3. Ensure all components have footprints")

        elif phase_num == 2:
            print("\n   Recovery suggestions:")
            print("   1. Check board dimensions (50×80mm)")
            print("   2. Verify footprint sizes are reasonable")
            print("   3. Manually place large components first")

        elif phase_num == 3:
            print("\n   Recovery suggestions:")
            print("   1. Install FreeRouting (freerouting.app)")
            print("   2. Or use --skip-phases 3 for manual routing")
            print("   3. Check critical nets are routable")

        elif phase_num == 4:
            print("\n   Recovery suggestions:")
            print("   1. Review DRC violations in KiCad")
            print("   2. Fix spacing and clearance issues")
            print("   3. Re-run validation after fixes")


def print_next_steps(output_dir: str, skip_routing: bool) -> None:
    """Print next steps for user"""
    print("\n📝 NEXT STEPS")
    print("-" * 80)

    if skip_routing:
        print("1. Open board in KiCad")
        print("2. Complete routing manually")
        print("3. Run Phase 4 (validation) separately")
    else:
        print("1. Review master report:")
        print(f"   open {output_dir}/master_report.txt")
        print("")
        print("2. Inspect board in KiCad:")
        print(f"   open {output_dir}/K1_Lightwave.kicad_pcb")
        print("")
        print("3. Check manufacturing files:")
        print(f"   ls {output_dir}/manufacturing/")
        print("")
        print("4. Upload to JLCPCB:")
        print("   - Go to jlcpcb.com")
        print("   - Upload Gerber zip file")
        print("   - Select 4-layer PCB")
        print("   - Review and order (~$15-20 per board)")

    print("\n💰 ESTIMATED COSTS")
    print("-" * 80)
    print("PCB Manufacturing (JLCPCB):")
    print("  • 5 boards: $15-20 USD")
    print("  • 10 boards: $20-25 USD")
    print("  • Lead time: 3-5 business days")
    print("  • Shipping: 5-7 days (standard)")


def main() -> int:
    """Main entry point"""
    print("\n" + "=" * 80)
    print("ELITE PCB DESIGNER AGENT - K1 LIGHTWAVE EXAMPLE")
    print("=" * 80)

    # Verify requirements
    if not verify_requirements():
        print("\n❌ Requirements check failed")
        print("Please install required dependencies and try again.")
        return 1

    # Ask user for configuration
    print("\nConfiguration:")
    print("1. Full automation (all 4 phases)")
    print("2. Skip routing (manual routing in KiCad)")

    choice = input("\nSelect option [1-2]: ").strip()

    skip_routing = (choice == "2")

    # Confirm before starting
    print("\nThis will execute the automated PCB design pipeline.")
    confirm = input("Continue? [y/N]: ").strip().lower()

    if confirm != 'y':
        print("Cancelled")
        return 0

    # Run design
    success = run_full_design(skip_routing=skip_routing)

    return 0 if success else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
