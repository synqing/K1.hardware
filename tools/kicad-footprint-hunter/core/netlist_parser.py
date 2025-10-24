"""
KiCad Netlist Parser - Extract component metadata from .net files

Parses KiCad netlist format and extracts:
- Component references (U1, C3, R5, etc.)
- Component values (1u, 10k, ESP32-S3-WROOM-1, etc.)
- Component descriptions
- Library source (Device, Connector, MCU, etc.)
- Current footprints (often empty for SKiDL-generated netlists)
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class ComponentType(Enum):
    """Common component type classifications"""
    RESISTOR = "Resistor"
    CAPACITOR = "Capacitor"
    INDUCTOR = "Inductor"
    DIODE = "Diode"
    IC = "IC"
    CONNECTOR = "Connector"
    UNKNOWN = "Unknown"


@dataclass
class ComponentMetadata:
    """Stores metadata for a single component"""
    reference: str  # e.g., "C3", "U1", "R_SPI_SCK"
    value: str  # e.g., "1u", "10k", "ESP32-S3-WROOM-1"
    description: str  # e.g., "Unpolarized capacitor"
    lib_source: str  # e.g., "Device", "Connector_USB"
    lib_part: str  # e.g., "C", "R", "USB_C_Receptacle"
    footprint: str  # e.g., "Capacitor_SMD:C_0603_1608Metric" or ""
    component_type: ComponentType = ComponentType.UNKNOWN

    def is_footprint_assigned(self) -> bool:
        """Check if footprint is already assigned"""
        return bool(self.footprint.strip())

    def get_part_type_prefix(self) -> str:
        """Extract type prefix from reference (C, R, U, etc.)"""
        return self.reference[0] if self.reference else ""

    def classify_component(self) -> ComponentType:
        """Classify component based on reference, value, and description"""
        prefix = self.reference[0].upper() if self.reference else ""
        desc_lower = self.description.lower()
        value_lower = self.value.lower()
        lib_part_lower = self.lib_part.lower()

        # Classification priority: reference prefix > description > lib source
        if prefix == 'R' or 'resistor' in desc_lower:
            return ComponentType.RESISTOR
        elif prefix == 'C' or 'capacitor' in desc_lower:
            return ComponentType.CAPACITOR
        elif prefix == 'L' or 'inductor' in desc_lower:
            return ComponentType.INDUCTOR
        elif prefix == 'D' or 'diode' in desc_lower:
            return ComponentType.DIODE
        elif prefix == 'U' or 'ic' in desc_lower or 'integrated circuit' in desc_lower:
            return ComponentType.IC
        elif prefix == 'J' or 'connector' in desc_lower or 'connector' in lib_part_lower:
            return ComponentType.CONNECTOR

        return ComponentType.UNKNOWN


class NetlistParser:
    """Parse KiCad .net netlist files and extract component metadata"""

    def __init__(self):
        self.components: Dict[str, ComponentMetadata] = {}
        self.raw_content: str = ""

    def parse_file(self, filepath: str) -> Dict[str, ComponentMetadata]:
        """
        Parse a KiCad netlist file and return component metadata

        Args:
            filepath: Path to .net file

        Returns:
            Dictionary of {reference: ComponentMetadata}
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            self.raw_content = f.read()

        self.components = self._parse_components()
        return self.components

    def _parse_components(self) -> Dict[str, ComponentMetadata]:
        """Extract component definitions from netlist content"""
        components = {}

        # Use regex to find all comp blocks with their complete nested structures
        # This pattern captures from (comp to matching closing paren
        # We'll use a character-by-character approach with proper nesting

        i = 0
        while i < len(self.raw_content):
            # Find next '(comp ' (with space after to ensure it's component, not compound word)
            idx = self.raw_content.find('(comp', i)
            if idx == -1:
                break

            # Check if it's really a component (not company, component_classes, etc.)
            # Should be followed by whitespace or newline
            if idx + 5 < len(self.raw_content):
                next_char = self.raw_content[idx+5]
                if next_char not in ' \n\t':
                    i = idx + 1
                    continue

            # Found a potential component start
            # Now find its matching closing parenthesis
            paren_depth = 0
            j = idx

            while j < len(self.raw_content):
                char = self.raw_content[j]

                # Handle string literals (don't count parens inside quotes)
                if char == '"':
                    # Skip to end of string
                    j += 1
                    while j < len(self.raw_content) and self.raw_content[j] != '"':
                        if self.raw_content[j] == '\\':
                            j += 2
                        else:
                            j += 1
                    j += 1
                    continue

                if char == '(':
                    paren_depth += 1
                elif char == ')':
                    paren_depth -= 1
                    if paren_depth == 0:
                        # Found the end
                        comp_block = self.raw_content[idx+5:j]  # Skip '(comp'
                        comp = self._parse_single_component(comp_block)
                        if comp:
                            components[comp.reference] = comp
                        i = j + 1
                        break

                j += 1

            if j >= len(self.raw_content):
                # Reached end without finding closing paren
                break

        return components

    def _parse_single_component(self, comp_block: str) -> Optional[ComponentMetadata]:
        """Parse a single component block from netlist"""
        try:
            # Extract reference
            ref_match = re.search(r'\(ref\s+"([^"]+)"', comp_block)
            ref = ref_match.group(1) if ref_match else None
            if not ref:
                return None

            # Extract value
            value_match = re.search(r'\(value\s+"([^"]+)"', comp_block)
            value = value_match.group(1) if value_match else ""

            # Extract description
            desc_match = re.search(r'\(description\s+"([^"]+)"', comp_block)
            description = desc_match.group(1) if desc_match else ""

            # Extract footprint
            footprint_match = re.search(r'\(footprint\s+"([^"]*)"', comp_block)
            footprint = footprint_match.group(1) if footprint_match else ""

            # Extract libsource (library and part)
            libsource_match = re.search(
                r'\(libsource\s+\(lib\s+"([^"]+)"\)\s+\(part\s+"([^"]+)"\)',
                comp_block
            )
            lib_source = libsource_match.group(1) if libsource_match else ""
            lib_part = libsource_match.group(2) if libsource_match else ""

            metadata = ComponentMetadata(
                reference=ref,
                value=value,
                description=description,
                lib_source=lib_source,
                lib_part=lib_part,
                footprint=footprint
            )

            # Classify component type
            metadata.component_type = metadata.classify_component()

            return metadata

        except Exception as e:
            print(f"Error parsing component block: {e}")
            return None

    def get_components_by_type(self, comp_type: ComponentType) -> Dict[str, ComponentMetadata]:
        """Get all components of a specific type"""
        return {
            ref: comp for ref, comp in self.components.items()
            if comp.component_type == comp_type
        }

    def get_missing_footprints(self) -> Dict[str, ComponentMetadata]:
        """Get all components without footprints assigned"""
        return {
            ref: comp for ref, comp in self.components.items()
            if not comp.is_footprint_assigned()
        }

    def get_component_summary(self) -> Dict:
        """Generate summary statistics about components"""
        total = len(self.components)
        with_footprints = sum(1 for c in self.components.values() if c.is_footprint_assigned())
        missing_footprints = total - with_footprints

        # Count by type
        by_type = {}
        for comp in self.components.values():
            comp_type = comp.component_type.value
            by_type[comp_type] = by_type.get(comp_type, 0) + 1

        return {
            'total_components': total,
            'with_footprints': with_footprints,
            'missing_footprints': missing_footprints,
            'coverage_percent': (with_footprints / total * 100) if total > 0 else 0,
            'by_type': by_type,
        }

    def export_missing(self, output_file: str):
        """Export list of components missing footprints to CSV"""
        missing = self.get_missing_footprints()

        with open(output_file, 'w') as f:
            f.write("Reference,Value,Description,Library,Part,ComponentType\n")
            for ref in sorted(missing.keys()):
                comp = missing[ref]
                f.write(
                    f"{comp.reference},{comp.value},"
                    f'"{comp.description}",{comp.lib_source},'
                    f"{comp.lib_part},{comp.component_type.value}\n"
                )
