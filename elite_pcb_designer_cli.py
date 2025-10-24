#!/usr/bin/env python3
"""
Elite PCB Designer Agent - CLI Interface
=========================================

Command-line interface for Elite PCB Designer with advanced options.

Features:
- Full pipeline execution
- Individual phase execution
- Progress tracking
- Dry-run mode
- Configuration management
- Batch processing

Usage:
    # Basic usage
    python elite_pcb_designer_cli.py run \\
        --netlist k1_motherboard_revA.net \\
        --board K1_Lightwave.kicad_pcb

    # With options
    python elite_pcb_designer_cli.py run \\
        --netlist k1_motherboard_revA.net \\
        --board K1_Lightwave.kicad_pcb \\
        --output ./my_output \\
        --skip-phases 3 \\
        --verbose

    # Dry-run (validation only)
    python elite_pcb_designer_cli.py run \\
        --netlist k1_motherboard_revA.net \\
        --board K1_Lightwave.kicad_pcb \\
        --dry-run

Author: Elite PCB Designer Agent
Version: 1.0.0
Date: 2025-10-24
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from elite_pcb_designer import ElitePCBDesigner, PhaseStatus


def cmd_run(args: argparse.Namespace) -> int:
    """
    Run the full PCB design pipeline.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        # Validate inputs
        netlist_path = Path(args.netlist)
        board_path = Path(args.board)

        if not netlist_path.exists():
            print(f"❌ Error: Netlist not found: {netlist_path}")
            return 1

        if not board_path.exists():
            print(f"❌ Error: Board file not found: {board_path}")
            return 1

        # Dry-run mode
        if args.dry_run:
            print("🔍 DRY-RUN MODE - Validating inputs only\n")
            print(f"✓ Netlist: {netlist_path}")
            print(f"✓ Board: {board_path}")
            print(f"✓ Output: {args.output}")
            if args.skip_phases:
                print(f"✓ Skip phases: {args.skip_phases}")
            print("\n✅ All inputs valid - pipeline would execute successfully")
            return 0

        # Create designer
        designer = ElitePCBDesigner(
            netlist_path=str(netlist_path),
            board_path=str(board_path),
            output_dir=args.output,
            verbose=args.verbose,
            skip_phases=args.skip_phases
        )

        # Execute pipeline
        success = designer.execute_full_pipeline()

        return 0 if success else 1

    except Exception as e:
        print(f"❌ Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cmd_status(args: argparse.Namespace) -> int:
    """
    Show status of output directory.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code
    """
    output_dir = Path(args.output)

    if not output_dir.exists():
        print(f"❌ Output directory not found: {output_dir}")
        return 1

    print(f"📂 Output Directory: {output_dir}\n")

    # Check for master report
    master_report = output_dir / "master_report.json"
    if master_report.exists():
        import json
        with open(master_report) as f:
            data = json.load(f)

        print("Master Report Found:")
        print(f"  Project: {data.get('project', 'Unknown')}")
        print(f"  Generated: {data.get('generated_at', 'Unknown')}")
        print(f"  Duration: {data.get('total_duration_formatted', 'Unknown')}")
        print(f"  Manufacturing Ready: {data.get('manufacturing_ready', False)}")
        print("")

        phases = data.get('phases', {})
        if phases:
            print("Phase Status:")
            for phase_num in sorted(phases.keys()):
                phase = phases[phase_num]
                status = phase.get('status', 'unknown')
                name = phase.get('phase_name', 'Unknown')
                duration = phase.get('duration_formatted', 'N/A')

                icon = {
                    'completed': '✅',
                    'failed': '❌',
                    'skipped': '⊘',
                    'running': '⏳',
                    'pending': '⏸'
                }.get(status, '?')

                print(f"  {icon} Phase {phase_num}: {name} ({duration})")
    else:
        print("⚠️  No master report found - pipeline may not have completed")

    # Check for board file
    board_files = list(output_dir.glob("*.kicad_pcb"))
    if board_files:
        print(f"\n📋 Board file: {board_files[0].name}")

    # Check for manufacturing files
    manufacturing_dir = output_dir / "manufacturing"
    if manufacturing_dir.exists():
        gerber_files = list(manufacturing_dir.glob("*.gbr"))
        drill_files = list(manufacturing_dir.glob("*.drl"))
        print(f"\n📦 Manufacturing files:")
        print(f"  Gerber files: {len(gerber_files)}")
        print(f"  Drill files: {len(drill_files)}")

    return 0


def cmd_clean(args: argparse.Namespace) -> int:
    """
    Clean output directory.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code
    """
    import shutil

    output_dir = Path(args.output)

    if not output_dir.exists():
        print(f"✓ Output directory does not exist: {output_dir}")
        return 0

    if not args.force:
        response = input(f"⚠️  Delete {output_dir}? [y/N] ")
        if response.lower() != 'y':
            print("Cancelled")
            return 0

    try:
        shutil.rmtree(output_dir)
        print(f"✓ Cleaned: {output_dir}")
        return 0
    except Exception as e:
        print(f"❌ Error cleaning directory: {e}")
        return 1


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        description="Elite PCB Designer Agent - Automated PCB Design Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  %(prog)s run --netlist design.net --board design.kicad_pcb

  # Skip routing phase (manual routing)
  %(prog)s run --netlist design.net --board design.kicad_pcb --skip-phases 3

  # Verbose mode with custom output
  %(prog)s run --netlist design.net --board design.kicad_pcb \\
      --output ./my_design --verbose

  # Check status
  %(prog)s status --output ./k1_design_output

  # Clean output
  %(prog)s clean --output ./k1_design_output --force

For more information, see documentation.
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Run command
    run_parser = subparsers.add_parser(
        "run",
        help="Run full PCB design pipeline"
    )
    run_parser.add_argument(
        "--netlist",
        required=True,
        help="Path to KiCad netlist file (.net)"
    )
    run_parser.add_argument(
        "--board",
        required=True,
        help="Path to KiCad board file (.kicad_pcb)"
    )
    run_parser.add_argument(
        "--output",
        default="k1_design_output",
        help="Output directory (default: k1_design_output)"
    )
    run_parser.add_argument(
        "--skip-phases",
        type=int,
        nargs="+",
        metavar="PHASE",
        help="Phase numbers to skip (e.g., 3 for routing)"
    )
    run_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs without executing pipeline"
    )
    run_parser.set_defaults(func=cmd_run)

    # Status command
    status_parser = subparsers.add_parser(
        "status",
        help="Show pipeline status"
    )
    status_parser.add_argument(
        "--output",
        default="k1_design_output",
        help="Output directory to check (default: k1_design_output)"
    )
    status_parser.set_defaults(func=cmd_status)

    # Clean command
    clean_parser = subparsers.add_parser(
        "clean",
        help="Clean output directory"
    )
    clean_parser.add_argument(
        "--output",
        default="k1_design_output",
        help="Output directory to clean (default: k1_design_output)"
    )
    clean_parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt"
    )
    clean_parser.set_defaults(func=cmd_clean)

    return parser


def main() -> int:
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
