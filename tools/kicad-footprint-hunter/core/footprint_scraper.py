"""
KiCad Footprint Scraper - Hunt for footprints from multiple sources

Searches:
1. KiCad standard libraries (installed locally)
2. GitHub repositories (kicad-footprints, pretty-libraries)
3. LCSC database (via C-number or specs)
4. Component type fallback patterns
"""

import os
import re
import json
from pathlib import Path
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass
import platform


@dataclass
class FootprintMatch:
    """Represents a potential footprint match"""
    footprint: str  # e.g., "Resistor_SMD:R_0603_1608Metric"
    source: str  # "kicad_lib", "github", "lcsc", "pattern"
    confidence: float  # 0.0 to 1.0
    notes: str = ""


class FootprintScraperBase:
    """Base class for footprint scrapers"""

    def search(self, component_ref: str, value: str, lib_part: str,
               lib_source: str) -> List[FootprintMatch]:
        """Search for footprints matching component specs"""
        raise NotImplementedError


class KiCadLibraryScraper(FootprintScraperBase):
    """Search local KiCad library for footprints"""

    def __init__(self):
        self.footprint_paths = self._find_kicad_footprint_libs()

    def _find_kicad_footprint_libs(self) -> List[Path]:
        """Locate KiCad footprint library paths on the system"""
        paths = []

        # Platform-specific paths
        if platform.system() == 'Darwin':
            mac_paths = [
                Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints'),
                Path.home() / 'Library/Application Support/kicad/8.0/footprints',
                Path.home() / 'Library/Application Support/kicad/footprints',
            ]
            paths.extend([p for p in mac_paths if p.exists()])

        elif platform.system() == 'Linux':
            linux_paths = [
                Path('/usr/share/kicad/footprints'),
                Path.home() / '.local/share/kicad/footprints',
                Path.home() / '.kicad_plugins/footprints',
            ]
            paths.extend([p for p in linux_paths if p.exists()])

        elif platform.system() == 'Windows':
            win_paths = [
                Path('C:/Program Files/KiCad/share/kicad/footprints'),
                Path.home() / 'AppData/Roaming/kicad/footprints',
            ]
            paths.extend([p for p in win_paths if p.exists()])

        return paths

    def search(self, component_ref: str, value: str, lib_part: str,
               lib_source: str) -> List[FootprintMatch]:
        """Search KiCad libraries for matching footprints"""
        matches = []

        # Search all footprint libraries
        for lib_path in self.footprint_paths:
            fp_files = list(lib_path.glob('**/*.kicad_mod'))

            for fp_file in fp_files:
                # Extract footprint name from file
                footprint_name = fp_file.stem

                # Score based on matching with part/value
                score = self._score_match(footprint_name, lib_part, value, component_ref)
                if score > 0.3:  # Threshold
                    lib_dir = fp_file.parent.name
                    full_footprint = f"{lib_dir}:{footprint_name}"

                    matches.append(FootprintMatch(
                        footprint=full_footprint,
                        source="kicad_lib",
                        confidence=score,
                        notes=f"Local KiCad library: {fp_file.parent}"
                    ))

        # Sort by confidence
        matches.sort(key=lambda m: m.confidence, reverse=True)
        return matches[:5]  # Top 5 matches

    @staticmethod
    def _score_match(footprint_name: str, lib_part: str, value: str,
                     component_ref: str) -> float:
        """Score how well a footprint matches the component"""
        score = 0.0
        fp_lower = footprint_name.lower()
        part_lower = lib_part.lower()

        # Direct match on part name
        if part_lower in fp_lower:
            score += 0.7

        # Package size matching (e.g., 0603, 0805, SOT23)
        if any(pkg in fp_lower for pkg in ['0603', '1608']):
            if 'r_' in fp_lower or component_ref[0].lower() == 'r':
                score += 0.2

        if any(pkg in fp_lower for pkg in ['soic', 'tssop', 'qfn']):
            if component_ref[0].lower() == 'u':
                score += 0.2

        return min(score, 1.0)


class PatternBasedScraper(FootprintScraperBase):
    """Use component type patterns to suggest footprints"""

    # Common footprint patterns by component type
    FOOTPRINT_PATTERNS = {
        'Resistor': [
            'Resistor_SMD:R_0603_1608Metric',
            'Resistor_SMD:R_0402_1005Metric',
            'Resistor_SMD:R_0805_2012Metric',
            'Resistor_THT:R_Axial_DL_7.0mm_W2.55mm_P10.16mm',
        ],
        'Capacitor': [
            'Capacitor_SMD:C_0603_1608Metric',
            'Capacitor_SMD:C_0402_1005Metric',
            'Capacitor_SMD:C_0805_2012Metric',
            'Capacitor_SMD:C_1206_3216Metric',
            'Capacitor_SMD:CP_Elec_6.3x5.8',
        ],
        'Inductor': [
            'Inductor_SMD:L_0603_1608Metric',
            'Inductor_SMD:L_0805_2012Metric',
        ],
        'Diode': [
            'Diode_SMD:D_0603_1608Metric',
            'Diode_SMD:D_SOD-323_HandSoldering',
            'Diode_SMD:D_SOD-323F',
        ],
        'Connector': [
            'Connector_USB:USB_C_Receptacle_Horizontal_GCT_USB4125-GF',
            'Connector_USB:USB_Micro-B_Wuerth_65100516121',
            'Connector_JST:JST_PH_B2B-PH-K_02x2.00mm_Straight',
        ],
        'MCU': [
            'Package_SON:LQFP-32_7x7mm_P0.8mm',
            'Package_BGA:ESP32-S3_QFN56',
            'Package_DFN_QFN:QFN-48_7x7mm_P0.5mm',
        ],
    }

    def search(self, component_ref: str, value: str, lib_part: str,
               lib_source: str) -> List[FootprintMatch]:
        """Generate footprint suggestions based on component type"""
        matches = []

        # Classify component type from reference
        comp_type = self._get_component_type(component_ref, lib_part, value)

        # Get pattern-based suggestions
        if comp_type in self.FOOTPRINT_PATTERNS:
            patterns = self.FOOTPRINT_PATTERNS[comp_type]
            for i, pattern in enumerate(patterns):
                confidence = 1.0 - (i * 0.15)  # Decreasing confidence
                matches.append(FootprintMatch(
                    footprint=pattern,
                    source="pattern",
                    confidence=max(confidence, 0.3),
                    notes=f"Pattern-based suggestion for {comp_type}"
                ))

        return matches

    @staticmethod
    def _get_component_type(component_ref: str, lib_part: str, value: str) -> str:
        """Classify component type"""
        prefix = component_ref[0].upper() if component_ref else ""

        if prefix == 'R':
            return 'Resistor'
        elif prefix == 'C':
            return 'Capacitor'
        elif prefix == 'L':
            return 'Inductor'
        elif prefix == 'D':
            return 'Diode'
        elif prefix == 'J':
            return 'Connector'
        elif prefix == 'U' or 'ESP' in value or 'STM' in value:
            return 'MCU'

        return 'Unknown'


class LCSCDatabaseScraper(FootprintScraperBase):
    """Search LCSC database for component footprints

    Note: This would require API integration or web scraping.
    For now, provides structure for future implementation.
    """

    def __init__(self, c_number: Optional[str] = None):
        self.c_number = c_number

    def search(self, component_ref: str, value: str, lib_part: str,
               lib_source: str) -> List[FootprintMatch]:
        """Search LCSC database (placeholder)"""
        matches = []

        # In production, this would:
        # 1. Query LCSC API with component specs
        # 2. Extract footprint information from returned JSON
        # 3. Return high-confidence matches

        # For now, return empty (can be extended later)
        return matches


class FootprintResolver:
    """Coordinate all footprint scrapers and find best matches"""

    def __init__(self, use_kicad_lib: bool = True, use_patterns: bool = True,
                 use_lcsc: bool = False):
        self.scrapers = []

        if use_kicad_lib:
            self.scrapers.append(KiCadLibraryScraper())
        if use_patterns:
            self.scrapers.append(PatternBasedScraper())
        if use_lcsc:
            self.scrapers.append(LCSCDatabaseScraper())

    def resolve(self, component_ref: str, value: str, lib_part: str,
                lib_source: str, prefer_source: Optional[str] = None
                ) -> List[FootprintMatch]:
        """
        Resolve footprint for a component by querying all scrapers

        Args:
            component_ref: Reference designator (e.g., "C3")
            value: Component value (e.g., "1u")
            lib_part: Library part name (e.g., "C")
            lib_source: Library source (e.g., "Device")
            prefer_source: Preferred source if available

        Returns:
            List of FootprintMatch sorted by confidence
        """
        all_matches = []

        # Query all scrapers
        for scraper in self.scrapers:
            try:
                matches = scraper.search(component_ref, value, lib_part, lib_source)
                all_matches.extend(matches)
            except Exception as e:
                print(f"Warning: Scraper {scraper.__class__.__name__} failed: {e}")

        # Sort by confidence and source preference
        all_matches.sort(
            key=lambda m: (
                m.source == prefer_source if prefer_source else False,
                m.confidence
            ),
            reverse=True
        )

        return all_matches

    def resolve_best(self, component_ref: str, value: str, lib_part: str,
                     lib_source: str, min_confidence: float = 0.3
                     ) -> Optional[FootprintMatch]:
        """Get single best footprint match"""
        matches = self.resolve(component_ref, value, lib_part, lib_source)

        if matches and matches[0].confidence >= min_confidence:
            return matches[0]

        return None
