"""
Elite PCB Designer Agent - Phase 1: Design Preparation
K1 Lightwave Motherboard Automation

This module handles:
1. Load netlist into KiCad board
2. Assign missing footprints (Device library components)
3. Replace IC placeholders with proper symbols
4. Validate nets (check for floating pins)
5. Run ERC (Electrical Rule Check)

Author: Elite PCB Designer Agent
Version: 1.0
Date: 2025-10-24
"""

import subprocess
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

# Try to import KiCad Python API
try:
    import pcbnew
    PCBNEW_AVAILABLE = True
except ImportError:
    PCBNEW_AVAILABLE = False


@dataclass
class FootprintAssignment:
    """Footprint assignment rule"""
    pattern: str
    footprint: str
    description: str
    value_filter: Optional[str] = None


class DesignPreparation:
    """
    Phase 1: Design Preparation
    Load netlist, assign footprints, validate design
    """

    # Footprint mapping rules for K1 Lightwave
    FOOTPRINT_RULES = [
        # Resistors - all 0603 except special cases
        FootprintAssignment(
            pattern=r'^R\d+$',
            footprint='Resistor_SMD:R_0603_1608Metric',
            description='Standard resistors (0603)'
        ),
        FootprintAssignment(
            pattern=r'^R_(USB|SPI|LED|FET|READY|PDM|LVT|BYPASS).*',
            footprint='Resistor_SMD:R_0603_1608Metric',
            description='Signal resistors (0603)'
        ),

        # Capacitors - size by value
        FootprintAssignment(
            pattern=r'^C\d+$',
            footprint='Capacitor_SMD:C_0603_1608Metric',
            description='Small capacitors <1uF (0603)',
            value_filter=r'(p|n|[0-9]+[pn])'  # pF or nF
        ),
        FootprintAssignment(
            pattern=r'^C_(BIN|BOUT|INA).*',
            footprint='Capacitor_SMD:C_1206_3216Metric',
            description='Bulk capacitors >=10uF (1206)',
            value_filter=r'10u'
        ),
        FootprintAssignment(
            pattern=r'^C\d+$',
            footprint='Capacitor_SMD:C_0603_1608Metric',
            description='Decoupling capacitors (0603)',
            value_filter=r'(100n|1u)'
        ),

        # Diodes - TVS and signal
        FootprintAssignment(
            pattern=r'^D_ESD_.*',
            footprint='Diode_SMD:D_SOD-323',
            description='ESD protection diodes (SOD-323)'
        ),
        FootprintAssignment(
            pattern=r'^D\d+$',
            footprint='Diode_SMD:D_SOD-323',
            description='TVS diodes (SOD-323)'
        ),
        FootprintAssignment(
            pattern=r'^D_IDEAL$',
            footprint='Diode_SMD:D_SOD-123',
            description='Schottky diode (SOD-123)'
        ),

        # Fuses - polyfuse 1206
        FootprintAssignment(
            pattern=r'^F\d+$',
            footprint='Fuse:Fuse_1206_3216Metric',
            description='Polyfuses (1206)'
        ),
        FootprintAssignment(
            pattern=r'^F_USB$',
            footprint='Fuse:Fuse_1206_3216Metric',
            description='USB input fuse (1206)'
        ),

        # Switches
        FootprintAssignment(
            pattern=r'^SW\d+$',
            footprint='Button_Switch_SMD:SW_SPST_TL3342',
            description='Push button switch'
        ),
    ]

    # IC placeholder mapping (for documentation)
    IC_REPLACEMENTS = {
        'U2': {
            'current': 'Device:C (placeholder)',
            'target': 'Regulator_Switching:TPS62160',
            'footprint': 'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',
            'description': 'Buck converter 5V->3.3V, 1.5A'
        },
        'U5': {
            'current': 'Device:C (placeholder)',
            'target': 'Power_Management:LTC4412',
            'footprint': 'Package_TO_SOT_SMD:SOT-23-5',
            'description': 'Ideal diode controller'
        },
        'U6': {
            'current': 'Device:C (placeholder)',
            'target': 'Memory_Flash:W25Q128JV',
            'footprint': 'Package_SO:SOIC-16_3.9x9.9mm_P1.27mm',
            'description': 'SPI flash memory 128Mbit'
        },
        'U7': {
            'current': 'Device:C (placeholder)',
            'target': 'Sensor_Current:INA226',
            'footprint': 'Package_SO:MSOP-10_3x3mm_P0.5mm',
            'description': 'I2C current/voltage monitor'
        },
        'U8': {
            'current': 'Device:R (placeholder)',
            'target': 'Logic_LevelTranslator:SN74AXC2T245',
            'footprint': 'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',
            'description': '2-bit voltage translator'
        },
    }

    def __init__(
        self,
        netlist_path: Path,
        board_path: Path,
        output_path: Optional[Path] = None,
        kicad_cli: str = '/opt/homebrew/bin/kicad-cli'
    ):
        """
        Initialize Design Preparation

        Args:
            netlist_path: Path to KiCad netlist (.net)
            board_path: Path to KiCad PCB file (.kicad_pcb)
            output_path: Optional output path (defaults to board_path)
            kicad_cli: Path to kicad-cli executable
        """
        self.netlist_path = Path(netlist_path)
        self.board_path = Path(board_path)
        self.output_path = Path(output_path) if output_path else self.board_path
        self.kicad_cli = kicad_cli

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Results storage
        self.results = {
            'netlist_loaded': False,
            'footprints_assigned': {},
            'ic_replacements_needed': {},
            'nets_valid': False,
            'erc_passed': False,
            'errors': [],
            'warnings': []
        }

    def load_netlist(self) -> bool:
        """
        Import netlist into KiCad board

        Parses netlist, applies footprint rules, and populates board with footprints
        using KiCad Python API (pcbnew)

        Returns:
            True if successful
        """
        self.logger.info(f"Loading netlist: {self.netlist_path}")

        if not self.netlist_path.exists():
            error = f"Netlist not found: {self.netlist_path}"
            self.logger.error(error)
            self.results['errors'].append(error)
            return False

        if not self.board_path.exists():
            error = f"Board file not found: {self.board_path}"
            self.logger.error(error)
            self.results['errors'].append(error)
            return False

        if not PCBNEW_AVAILABLE:
            error = "KiCad Python API (pcbnew) not available. Run with KiCad's Python interpreter."
            self.logger.error(error)
            self.results['errors'].append(error)
            return False

        try:
            self.logger.info("Parsing netlist and populating board with footprints...")

            # Parse netlist file to extract components
            with open(self.netlist_path, 'r') as f:
                netlist_content = f.read()

            # Extract component definitions from netlist
            # Format: (comp (ref "XXX") (value "YYY") ...)
            comp_pattern = r'\(comp\s+\(ref "([^"]+)"\)\s+\(value "([^"]+)"\)'
            components = re.findall(comp_pattern, netlist_content)

            self.logger.info(f"Found {len(components)} components in netlist")

            if len(components) == 0:
                warning = "Netlist contains no components"
                self.logger.warning(warning)
                self.results['warnings'].append(warning)
                return False

            # Load the board
            self.logger.info(f"Loading board: {self.board_path}")
            board = pcbnew.LoadBoard(str(self.board_path))

            # Add footprints to board
            added_count = 0
            skipped_count = 0
            failed_refs = []

            for ref, value in components:
                try:
                    self.logger.debug(f"Processing {ref} ({value})")

                    # Determine footprint using assignment rules
                    footprint_name = None
                    for rule in self.FOOTPRINT_RULES:
                        if re.match(rule.pattern, ref):
                            # Check value filter if present
                            if rule.value_filter:
                                if not re.search(rule.value_filter, value, re.IGNORECASE):
                                    continue
                            footprint_name = rule.footprint
                            self.logger.debug(f"  Matched rule: {rule.description}")
                            break

                    if not footprint_name:
                        self.logger.warning(f"  ❌ {ref} ({value}) - no matching footprint rule")
                        failed_refs.append(f"{ref} (no rule match)")
                        skipped_count += 1
                        continue

                    # Parse footprint library and name
                    # Format: "Library:Footprint"
                    if ':' not in footprint_name:
                        self.logger.warning(f"  ❌ {ref} - invalid footprint format: {footprint_name}")
                        failed_refs.append(f"{ref} (invalid format)")
                        skipped_count += 1
                        continue

                    lib_name, fp_name = footprint_name.split(':', 1)
                    self.logger.debug(f"  Loading {fp_name} from {lib_name}")

                    # Load footprint from KiCad library
                    footprint = pcbnew.FootprintLoad(lib_name, fp_name)

                    if footprint:
                        footprint.SetReference(ref)
                        # Place at origin (0,0), will be moved by placement engine
                        footprint.SetPosition(pcbnew.VECTOR2I(0, 0))
                        board.Add(footprint)
                        self.logger.info(f"  ✅ Added {ref} with {footprint_name}")
                        added_count += 1
                    else:
                        self.logger.warning(f"  ❌ Failed to load {footprint_name} for {ref}")
                        failed_refs.append(f"{ref} ({footprint_name})")
                        skipped_count += 1

                except Exception as e:
                    self.logger.error(f"  ❌ Error processing {ref}: {str(e)}")
                    failed_refs.append(f"{ref} (error: {str(e)})")
                    skipped_count += 1
                    continue

            self.logger.info(f"\nNetlist import results:")
            self.logger.info(f"  ✅ Added: {added_count} footprints")
            self.logger.info(f"  ❌ Skipped/Failed: {skipped_count} components")

            if failed_refs:
                self.logger.warning(f"\nFailed to add (first 10):")
                for ref in failed_refs[:10]:
                    self.logger.warning(f"  - {ref}")
                if len(failed_refs) > 10:
                    self.logger.warning(f"  ... and {len(failed_refs) - 10} more")

            # Save board with populated footprints
            self.logger.info(f"\nSaving board with {added_count} footprints to: {self.output_path}")
            board.Save(str(self.output_path))

            self.logger.info(f"✅ Netlist import SUCCESSFUL: {added_count} footprints added")
            self.results['netlist_loaded'] = True
            self.results['components_added'] = added_count
            self.results['components_skipped'] = skipped_count

            return added_count > 0

        except Exception as e:
            error = f"Netlist import exception: {str(e)}"
            self.logger.error(error)
            self.results['errors'].append(error)
            return False

    def assign_footprints(self) -> Dict[str, str]:
        """
        Assign missing footprints to Device library components

        Reads netlist, matches components by reference pattern,
        generates footprint assignments.

        Returns:
            Dictionary of {component_ref: footprint}
        """
        self.logger.info("Analyzing footprint assignments...")

        assignments = {}

        try:
            # Parse netlist to find components without footprints
            with open(self.netlist_path, 'r') as f:
                netlist_content = f.read()

            # Extract component definitions
            comp_pattern = r'\(comp\s+\(ref "([^"]+)"\)\s+\(value "([^"]+)"\).*?\(footprint "([^"]*)"\)'
            components = re.findall(comp_pattern, netlist_content, re.DOTALL)

            missing_count = 0
            assigned_count = 0

            for ref, value, footprint in components:
                if footprint == "":  # Missing footprint
                    missing_count += 1

                    # Match against footprint rules
                    for rule in self.FOOTPRINT_RULES:
                        if re.match(rule.pattern, ref):
                            # Check value filter if present
                            if rule.value_filter:
                                if not re.search(rule.value_filter, value, re.IGNORECASE):
                                    continue

                            assignments[ref] = rule.footprint
                            assigned_count += 1
                            self.logger.info(
                                f"  {ref} ({value}) -> {rule.footprint}"
                            )
                            break

            self.logger.info(
                f"Found {missing_count} components without footprints, "
                f"assigned {assigned_count}"
            )

            self.results['footprints_assigned'] = assignments

            # Note: Actual footprint assignment requires KiCad Python API
            # or manual editing. This generates the mapping.
            if missing_count > assigned_count:
                warning = (
                    f"{missing_count - assigned_count} components still need "
                    "footprints (manual assignment required)"
                )
                self.logger.warning(warning)
                self.results['warnings'].append(warning)

            return assignments

        except Exception as e:
            error = f"Footprint assignment error: {str(e)}"
            self.logger.error(error)
            self.results['errors'].append(error)
            return {}

    def replace_ic_placeholders(self) -> Dict[str, Dict]:
        """
        Document IC replacements needed

        Returns:
            Dictionary of IC replacement specifications
        """
        self.logger.info("Analyzing IC placeholder replacements...")

        self.results['ic_replacements_needed'] = self.IC_REPLACEMENTS

        self.logger.info("IC replacements needed:")
        for ref, spec in self.IC_REPLACEMENTS.items():
            self.logger.info(f"  {ref}:")
            self.logger.info(f"    Current: {spec['current']}")
            self.logger.info(f"    Target:  {spec['target']}")
            self.logger.info(f"    Footprint: {spec['footprint']}")
            self.logger.info(f"    Description: {spec['description']}")

        warning = (
            f"{len(self.IC_REPLACEMENTS)} IC placeholders need manual "
            "replacement in KiCad schematic"
        )
        self.logger.warning(warning)
        self.results['warnings'].append(warning)

        return self.IC_REPLACEMENTS

    def validate_nets(self) -> Tuple[bool, str]:
        """
        Validate all nets are properly connected

        Checks for:
        - Floating pins
        - Unconnected nets
        - Net integrity

        Returns:
            (success, message)
        """
        self.logger.info("Validating net connectivity...")

        try:
            # Parse netlist for net analysis
            with open(self.netlist_path, 'r') as f:
                netlist_content = f.read()

            # Count nets and nodes
            net_pattern = r'\(net\s+\(code \d+\)\s+\(name "([^"]+)"\)'
            nets = re.findall(net_pattern, netlist_content)

            node_pattern = r'\(node\s+\(ref "([^"]+)"\)\s+\(pin "([^"]+)"\)'
            nodes = re.findall(node_pattern, netlist_content)

            self.logger.info(f"Found {len(nets)} nets with {len(nodes)} connections")

            # Check for single-node nets (potential floating)
            net_node_count = {}
            current_net = None

            for line in netlist_content.split('\n'):
                net_match = re.search(r'\(name "([^"]+)"\)', line)
                if net_match and '(net' in line:
                    current_net = net_match.group(1)
                    net_node_count[current_net] = 0
                elif current_net and '(node' in line:
                    net_node_count[current_net] += 1

            floating_nets = [
                net for net, count in net_node_count.items()
                if count < 2
            ]

            if floating_nets:
                warning = f"Found {len(floating_nets)} potentially floating nets"
                self.logger.warning(warning)
                for net in floating_nets[:5]:  # Show first 5
                    self.logger.warning(f"  - {net}")
                self.results['warnings'].append(warning)

            self.results['nets_valid'] = len(floating_nets) == 0

            message = (
                f"Net validation: {len(nets)} nets, {len(nodes)} nodes, "
                f"{len(floating_nets)} floating"
            )

            return True, message

        except Exception as e:
            error = f"Net validation error: {str(e)}"
            self.logger.error(error)
            self.results['errors'].append(error)
            return False, error

    def run_erc(self) -> Tuple[bool, str]:
        """
        Run Electrical Rule Check

        Uses: kicad-cli erc

        Acceptance criteria:
        - Errors: 0 (must pass)
        - Warnings: <= 100 (acceptable for placeholders)

        Returns:
            (success, message)
        """
        self.logger.info("Running Electrical Rule Check (ERC)...")

        # ERC requires schematic file, not netlist
        # For K1, we need to find the schematic
        schematic_path = self.netlist_path.parent / "K1_Lightwave.kicad_sch"

        if not schematic_path.exists():
            # Try alternate locations
            alt_paths = [
                self.netlist_path.parent / "k1_lightwave.kicad_sch",
                self.board_path.parent / "K1_Lightwave.kicad_sch",
                self.board_path.parent / "k1_lightwave.kicad_sch"
            ]

            for alt in alt_paths:
                if alt.exists():
                    schematic_path = alt
                    break
            else:
                warning = (
                    "Schematic file not found for ERC. "
                    "Expected: K1_Lightwave.kicad_sch"
                )
                self.logger.warning(warning)
                self.results['warnings'].append(warning)
                self.results['erc_passed'] = None  # Unknown
                return False, warning

        try:
            # Run KiCad ERC
            cmd = [
                self.kicad_cli,
                'sch', 'erc',
                '--input', str(schematic_path),
                '--exit-code-violations'
            ]

            self.logger.info(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            # Parse ERC output
            output = result.stdout + result.stderr

            # Extract error/warning counts
            error_match = re.search(r'(\d+)\s+errors?', output, re.IGNORECASE)
            warning_match = re.search(r'(\d+)\s+warnings?', output, re.IGNORECASE)

            error_count = int(error_match.group(1)) if error_match else 0
            warning_count = int(warning_match.group(1)) if warning_match else 0

            self.logger.info(f"ERC Results: {error_count} errors, {warning_count} warnings")

            # Check acceptance criteria
            passed = error_count == 0 and warning_count <= 100

            if passed:
                self.logger.info("ERC PASSED")
                self.results['erc_passed'] = True
                message = f"ERC passed: {error_count} errors, {warning_count} warnings"
                return True, message
            else:
                if error_count > 0:
                    error = f"ERC FAILED: {error_count} errors (must be 0)"
                    self.logger.error(error)
                    self.results['errors'].append(error)

                if warning_count > 100:
                    error = f"ERC FAILED: {warning_count} warnings (max 100)"
                    self.logger.error(error)
                    self.results['errors'].append(error)

                self.results['erc_passed'] = False
                message = f"ERC failed: {error_count} errors, {warning_count} warnings"
                return False, message

        except subprocess.TimeoutExpired:
            error = "ERC timed out (>60s)"
            self.logger.error(error)
            self.results['errors'].append(error)
            return False, error
        except Exception as e:
            error = f"ERC exception: {str(e)}"
            self.logger.error(error)
            self.results['errors'].append(error)
            return False, error

    def execute(self) -> bool:
        """
        Run full Phase 1 pipeline

        Returns:
            True if all steps successful
        """
        self.logger.info("="*60)
        self.logger.info("PHASE 1: DESIGN PREPARATION")
        self.logger.info("K1 Lightwave Motherboard")
        self.logger.info("="*60)

        success = True

        # Step 1: Load netlist
        self.logger.info("\n[1/5] Loading netlist into board...")
        if not self.load_netlist():
            success = False
            self.logger.error("Failed to load netlist")

        # Step 2: Assign footprints
        self.logger.info("\n[2/5] Assigning missing footprints...")
        assignments = self.assign_footprints()
        self.logger.info(f"Assigned {len(assignments)} footprints")

        # Step 3: Document IC replacements
        self.logger.info("\n[3/5] Analyzing IC placeholders...")
        replacements = self.replace_ic_placeholders()
        self.logger.info(f"Documented {len(replacements)} IC replacements")

        # Step 4: Validate nets
        self.logger.info("\n[4/5] Validating net connectivity...")
        nets_ok, net_msg = self.validate_nets()
        self.logger.info(net_msg)

        # Step 5: Run ERC
        self.logger.info("\n[5/5] Running Electrical Rule Check...")
        erc_ok, erc_msg = self.run_erc()
        self.logger.info(erc_msg)

        # Summary
        self.logger.info("\n" + "="*60)
        self.logger.info("PHASE 1 SUMMARY")
        self.logger.info("="*60)
        self.logger.info(f"Netlist Loaded: {self.results['netlist_loaded']}")
        self.logger.info(f"Footprints Assigned: {len(assignments)}")
        self.logger.info(f"IC Replacements Needed: {len(replacements)}")
        self.logger.info(f"Nets Valid: {self.results['nets_valid']}")
        self.logger.info(f"ERC Passed: {self.results['erc_passed']}")
        self.logger.info(f"Errors: {len(self.results['errors'])}")
        self.logger.info(f"Warnings: {len(self.results['warnings'])}")

        if self.results['errors']:
            self.logger.error("\nERRORS:")
            for error in self.results['errors']:
                self.logger.error(f"  - {error}")

        if self.results['warnings']:
            self.logger.warning("\nWARNINGS:")
            for warning in self.results['warnings'][:10]:  # First 10
                self.logger.warning(f"  - {warning}")

        overall_success = (
            self.results['netlist_loaded'] and
            len(self.results['errors']) == 0
        )

        self.logger.info("\n" + "="*60)
        if overall_success:
            self.logger.info("PHASE 1: SUCCESS")
        else:
            self.logger.error("PHASE 1: FAILED")
        self.logger.info("="*60)

        return overall_success

    def save_report(self, report_path: Path) -> None:
        """
        Save detailed report to JSON

        Args:
            report_path: Path to save report
        """
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        self.logger.info(f"Report saved to: {report_path}")


def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Elite PCB Designer Agent - Phase 1: Design Preparation'
    )
    parser.add_argument(
        'netlist',
        type=Path,
        help='Path to KiCad netlist (.net)'
    )
    parser.add_argument(
        'board',
        type=Path,
        help='Path to KiCad PCB file (.kicad_pcb)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output PCB file (default: overwrite input)'
    )
    parser.add_argument(
        '--report',
        type=Path,
        help='Save detailed report to JSON file'
    )
    parser.add_argument(
        '--kicad-cli',
        default='/opt/homebrew/bin/kicad-cli',
        help='Path to kicad-cli executable'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose logging'
    )

    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Create design preparation instance
    prep = DesignPreparation(
        netlist_path=args.netlist,
        board_path=args.board,
        output_path=args.output,
        kicad_cli=args.kicad_cli
    )

    # Execute Phase 1
    success = prep.execute()

    # Save report if requested
    if args.report:
        prep.save_report(args.report)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
