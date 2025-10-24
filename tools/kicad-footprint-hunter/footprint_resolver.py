#!/usr/bin/env python3
"""
KiCad Footprint Resolver - Standalone CLI Agent

Usage:
    python footprint_resolver.py <netlist_file> [--pcb <pcb_file>] [--output <dir>]

Examples:
    python footprint_resolver.py ../hardware/k1-lightwave/k1_motherboard_revA.net
    python footprint_resolver.py netlist.net --pcb board.kicad_pcb --output ./results
    python footprint_resolver.py netlist.net --confidence 0.6 --auto
"""

import sys
import json
from pathlib import Path
from argparse import ArgumentParser
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.footprint_hunter import FootprintHunter


class FootprintResolverAgent:
    """Standalone agent for footprint resolution"""

    def __init__(self, netlist_path: str, pcb_path: Optional[str] = None,
                 output_dir: Optional[str] = None):
        self.netlist_path = netlist_path
        self.pcb_path = pcb_path
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self, confidence_threshold: float = 0.5, auto_assign: bool = False,
            verbose: bool = True) -> bool:
        """
        Execute footprint resolution workflow

        Args:
            confidence_threshold: Minimum confidence for auto-assignment
            auto_assign: Automatically assign top matches
            verbose: Print progress information

        Returns:
            True if successful
        """
        try:
            if verbose:
                print("\n" + "=" * 60)
                print("KiCad Footprint Resolver - Standalone Agent")
                print("=" * 60)

            # Create hunter instance
            hunter = FootprintHunter(
                netlist_path=self.netlist_path,
                pcb_path=self.pcb_path
            )

            if verbose:
                print(f"\nNetlist: {self.netlist_path}")
                print(f"Output: {self.output_dir}")
                print(f"Confidence Threshold: {confidence_threshold:.0%}")
                print(f"Auto-assign: {auto_assign}")
                print("\nRunning resolution workflow...")

            # Execute workflow
            report = hunter.run(
                min_confidence=confidence_threshold,
                auto_assign=auto_assign
            )

            if verbose:
                self._print_report(report, hunter)

            # Save full report
            report_file = self.output_dir / "footprint_resolution_report.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)

            if verbose:
                print(f"\nFull report saved to: {report_file}")

            return report['status'] == 'success'

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return False

    def _print_report(self, report: dict, hunter: FootprintHunter):
        """Print human-readable resolution report"""
        print("\nResolution Steps:")
        print("-" * 60)

        for step in report['steps']:
            status = "✓" if step['status'] == 'success' else "✗"
            print(f"{status} {step['name']}: {step['status'].upper()}")

            # Print key metrics
            if 'missing_count' in step:
                print(f"    - Missing: {step['missing_count']}")
            if 'resolved' in step:
                print(f"    - Resolved: {step['resolved']}")
                if 'resolution_rate' in step:
                    print(f"    - Rate: {step['resolution_rate']}")
            if 'assignments_applied' in step:
                print(f"    - Applied: {step['assignments_applied']}")

        print("\nResolution Summary:")
        print("-" * 60)

        summary = hunter.get_resolution_summary()
        for key, value in summary.items():
            key_display = key.replace('_', ' ').title()
            print(f"{key_display}: {value}")

        unresolved = hunter.get_unresolved_components()
        if unresolved:
            print(f"\nUnresolved Components: {len(unresolved)}")
            print("-" * 60)

            for ref in sorted(unresolved.keys())[:10]:  # Show first 10
                comp = unresolved[ref]
                print(f"{ref} ({comp['value']})")
                print(f"  Library: {comp['library']}")
                if comp['best_match']:
                    print(f"  Best Match: {comp['best_match']}")
                    print(f"  Confidence: {comp['best_confidence']:.0%}")
                else:
                    print(f"  Status: No matches found")

            if len(unresolved) > 10:
                print(f"\n... and {len(unresolved) - 10} more unresolved components")


def main():
    """CLI entry point"""
    parser = ArgumentParser(
        description="KiCad Footprint Resolver - Standalone Agent"
    )

    parser.add_argument(
        'netlist',
        help='Path to KiCad netlist file (.net)'
    )

    parser.add_argument(
        '--pcb',
        help='Path to KiCad PCB file (.kicad_pcb) [optional]'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output directory for results [default: current directory]'
    )

    parser.add_argument(
        '--confidence', '-c',
        type=float,
        default=0.5,
        help='Minimum confidence threshold (0.0-1.0) [default: 0.5]'
    )

    parser.add_argument(
        '--auto', '-a',
        action='store_true',
        help='Automatically assign footprints that meet confidence threshold'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress verbose output'
    )

    args = parser.parse_args()

    # Validate input
    netlist_path = Path(args.netlist)
    if not netlist_path.exists():
        print(f"Error: Netlist file not found: {args.netlist}", file=sys.stderr)
        sys.exit(1)

    if args.pcb:
        pcb_path = Path(args.pcb)
        if not pcb_path.exists():
            print(f"Error: PCB file not found: {args.pcb}", file=sys.stderr)
            sys.exit(1)
    else:
        pcb_path = None

    # Run agent
    agent = FootprintResolverAgent(
        netlist_path=str(netlist_path),
        pcb_path=str(pcb_path) if pcb_path else None,
        output_dir=args.output
    )

    success = agent.run(
        confidence_threshold=args.confidence,
        auto_assign=args.auto,
        verbose=not args.quiet
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
