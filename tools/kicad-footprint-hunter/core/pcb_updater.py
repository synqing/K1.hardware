"""
KiCad PCB File Updater - Update .kicad_pcb files with footprint assignments

Reads netlist, coordinates with footprint resolver, and updates PCB file
with discovered footprints. Works in conjunction with KiCad's netlist import.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class FootprintUpdate:
    """Represents a footprint assignment for a component"""
    reference: str
    old_footprint: str
    new_footprint: str
    confidence: float
    notes: str = ""


class PCBUpdater:
    """Update KiCad PCB files with footprint information"""

    def __init__(self, pcb_file_path: str, netlist_file_path: str):
        self.pcb_file = Path(pcb_file_path)
        self.netlist_file = Path(netlist_file_path)
        self.updates: List[FootprintUpdate] = []

    def apply_footprints(self, footprint_mapping: Dict[str, str]) -> Tuple[int, int]:
        """
        Apply footprints to netlist and generate updated netlist for import

        Args:
            footprint_mapping: {component_ref: footprint_path}

        Returns:
            (total_updated, successful_updates)
        """
        updated = 0
        successful = 0

        with open(self.netlist_file, 'r') as f:
            content = f.read()

        for component_ref, footprint in footprint_mapping.items():
            # Find component block in netlist
            pattern = rf'(\(comp\s+\(ref\s+"{re.escape(component_ref)}".*?\(footprint\s+")([^"]*)'
            match = re.search(pattern, content, re.DOTALL)

            if match:
                old_footprint = match.group(2)

                # Replace footprint
                new_content = content[:match.start(2)] + footprint + content[match.end(2):]
                content = new_content

                updated += 1
                successful += 1

                self.updates.append(FootprintUpdate(
                    reference=component_ref,
                    old_footprint=old_footprint,
                    new_footprint=footprint,
                    confidence=1.0
                ))

        # Write updated netlist
        output_file = self.netlist_file.with_stem(
            self.netlist_file.stem + "_with_footprints"
        )
        with open(output_file, 'w') as f:
            f.write(content)

        return updated, successful

    def generate_skidl_updates(self, footprint_mapping: Dict[str, str]) -> str:
        """
        Generate Python code to update SKiDL script with footprints

        This is useful for making changes persistent in the source script.
        """
        code_lines = [
            "# Auto-generated footprint assignments from Footprint Hunter",
            "# Add these to your Part() definitions in SKiDL script:\n",
        ]

        for ref, footprint in sorted(footprint_mapping.items()):
            code_lines.append(f'# {ref}: footprint="{footprint}"')

        return "\n".join(code_lines)

    def export_report(self, output_file: str):
        """Export update report as JSON"""
        report = {
            'total_updates': len(self.updates),
            'successful_updates': sum(1 for u in self.updates if u.confidence == 1.0),
            'updates': [
                {
                    'reference': u.reference,
                    'old_footprint': u.old_footprint,
                    'new_footprint': u.new_footprint,
                    'confidence': u.confidence,
                    'notes': u.notes
                }
                for u in self.updates
            ]
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

    def export_csv(self, output_file: str):
        """Export updates as CSV"""
        with open(output_file, 'w') as f:
            f.write("Reference,OldFootprint,NewFootprint,Confidence,Notes\n")
            for u in self.updates:
                f.write(
                    f'{u.reference},{u.old_footprint},"{u.new_footprint}",'
                    f'{u.confidence},"{u.notes}"\n'
                )


class NetlistUpdater:
    """Update KiCad netlist files with footprint information"""

    @staticmethod
    def update_netlist(netlist_path: str, footprint_mapping: Dict[str, str],
                       output_path: Optional[str] = None) -> bool:
        """
        Update netlist file with footprint assignments

        Args:
            netlist_path: Path to .net file
            footprint_mapping: {component_ref: footprint}
            output_path: Optional output path (if None, overwrites input)

        Returns:
            True if successful
        """
        try:
            with open(netlist_path, 'r') as f:
                content = f.read()

            # Update each component's footprint
            for component_ref, footprint in footprint_mapping.items():
                # Match component block with reference and its footprint field
                pattern = (
                    rf'(\(comp\s+\(ref\s+"{re.escape(component_ref)}".*?)'
                    r'(\(footprint\s+")([^"]*?)(")'
                )

                def replacer(match):
                    prefix = match.group(1)
                    fp_before = match.group(2)
                    fp_after = match.group(4)
                    return prefix + fp_before + footprint + fp_after

                content = re.sub(pattern, replacer, content, flags=re.DOTALL)

            # Write output
            target_path = output_path or netlist_path
            with open(target_path, 'w') as f:
                f.write(content)

            return True

        except Exception as e:
            print(f"Error updating netlist: {e}")
            return False

    @staticmethod
    def validate_netlist(netlist_path: str) -> Tuple[bool, List[str]]:
        """
        Validate netlist format

        Returns:
            (is_valid, error_messages)
        """
        errors = []

        try:
            with open(netlist_path, 'r') as f:
                content = f.read()

            # Check for valid netlist structure
            if not re.search(r'\(export\s+\(version', content):
                errors.append("Missing export/version declaration")

            if not re.search(r'\(components', content):
                errors.append("Missing components section")

            # Check for unmatched parentheses
            open_count = content.count('(')
            close_count = content.count(')')
            if open_count != close_count:
                errors.append(f"Unmatched parentheses ({open_count} open, {close_count} close)")

            return len(errors) == 0, errors

        except Exception as e:
            return False, [f"Error reading netlist: {e}"]


class SKiDLUpdater:
    """Generate updated SKiDL script with footprint assignments"""

    @staticmethod
    def generate_updated_script(original_script_path: str,
                                footprint_mapping: Dict[str, str],
                                output_path: str) -> bool:
        """
        Generate updated SKiDL script with footprint assignments

        Args:
            original_script_path: Path to original .py script
            footprint_mapping: {component_ref: footprint}
            output_path: Path to write updated script

        Returns:
            True if successful
        """
        try:
            with open(original_script_path, 'r') as f:
                lines = f.readlines()

            updated_lines = []
            ref_to_var = {}  # Map reference to variable name

            # First pass: identify component variable names
            for line in lines:
                # Look for patterns like: u_esp32a = Part(...)
                match = re.search(r'(\w+)\s*=\s*Part\([^)]*ref\s*=\s*["\']([^"\']+)["\']',
                                  line)
                if match:
                    var_name = match.group(1)
                    ref = match.group(2)
                    ref_to_var[ref] = var_name

            # Second pass: update Part() definitions
            for line in lines:
                updated_line = line

                # Find all Part() definitions and add footprints
                for ref, var_name in ref_to_var.items():
                    if var_name in line:
                        if ref in footprint_mapping:
                            footprint = footprint_mapping[ref]

                            # Add footprint parameter if not present
                            if 'footprint=' not in line:
                                # Insert footprint before closing parenthesis
                                updated_line = re.sub(
                                    r'(\)\s*)$',
                                    f', footprint="{footprint}")\n',
                                    line.rstrip() + '\n'
                                )
                            else:
                                # Update existing footprint
                                updated_line = re.sub(
                                    r'footprint="[^"]*"',
                                    f'footprint="{footprint}"',
                                    line
                                )

                updated_lines.append(updated_line)

            # Write updated script
            with open(output_path, 'w') as f:
                f.writelines(updated_lines)

            return True

        except Exception as e:
            print(f"Error updating SKiDL script: {e}")
            return False
