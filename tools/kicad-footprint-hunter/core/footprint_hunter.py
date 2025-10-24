"""
KiCad Footprint Hunter - Main orchestrator

Coordinates netlist parsing, footprint resolution, and PCB file updates.
Works as either a Skill (Claude Code integrated) or standalone agent.
"""

from pathlib import Path
from typing import Dict, Optional, List, Tuple
import json
from datetime import datetime

from .netlist_parser import NetlistParser, ComponentMetadata
from .footprint_scraper import FootprintResolver, FootprintMatch
from .pcb_updater import PCBUpdater, NetlistUpdater, SKiDLUpdater


class FootprintHunter:
    """Main orchestrator for footprint resolution"""

    def __init__(self, netlist_path: str, pcb_path: Optional[str] = None,
                 skidl_script_path: Optional[str] = None):
        self.netlist_path = Path(netlist_path)
        self.pcb_path = Path(pcb_path) if pcb_path else None
        self.skidl_script_path = Path(skidl_script_path) if skidl_script_path else None

        self.parser = NetlistParser()
        self.resolver = FootprintResolver(use_kicad_lib=True, use_patterns=True)

        self.components: Dict[str, ComponentMetadata] = {}
        self.footprint_mapping: Dict[str, str] = {}
        self.resolution_details: Dict[str, List[FootprintMatch]] = {}

    def run(self, min_confidence: float = 0.5, auto_assign: bool = True) -> Dict:
        """
        Execute complete footprint hunting workflow

        Args:
            min_confidence: Minimum confidence threshold for auto-assignment
            auto_assign: Automatically assign top match if confidence >= threshold

        Returns:
            Summary report dict
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'netlist': str(self.netlist_path),
            'status': 'starting',
            'steps': []
        }

        try:
            # Step 1: Parse netlist
            report['steps'].append(self._step_parse_netlist())

            # Step 2: Identify missing footprints
            report['steps'].append(self._step_identify_missing())

            # Step 3: Resolve footprints
            report['steps'].append(self._step_resolve_footprints(min_confidence))

            # Step 4: Apply assignments
            report['steps'].append(self._step_apply_assignments(auto_assign))

            # Step 5: Export results
            report['steps'].append(self._step_export_results())

            report['status'] = 'success'

        except Exception as e:
            report['status'] = 'error'
            report['error'] = str(e)

        return report

    def _step_parse_netlist(self) -> Dict:
        """Parse netlist file"""
        self.components = self.parser.parse_file(str(self.netlist_path))
        summary = self.parser.get_component_summary()

        return {
            'name': 'Parse Netlist',
            'status': 'success',
            'summary': summary,
            'total_components': len(self.components)
        }

    def _step_identify_missing(self) -> Dict:
        """Identify components without footprints"""
        missing = self.parser.get_missing_footprints()

        return {
            'name': 'Identify Missing Footprints',
            'status': 'success',
            'missing_count': len(missing),
            'missing_refs': list(missing.keys())
        }

    def _step_resolve_footprints(self, min_confidence: float) -> Dict:
        """Resolve footprints for all missing components"""
        missing = self.parser.get_missing_footprints()
        resolved = 0

        for ref, comp in missing.items():
            matches = self.resolver.resolve(
                ref, comp.value, comp.lib_part, comp.lib_source
            )

            self.resolution_details[ref] = matches

            # Get best match
            if matches and matches[0].confidence >= min_confidence:
                self.footprint_mapping[ref] = matches[0].footprint
                resolved += 1

        return {
            'name': 'Resolve Footprints',
            'status': 'success',
            'missing_components': len(missing),
            'resolved': resolved,
            'resolution_rate': f"{resolved/len(missing)*100:.1f}%" if missing else "0%"
        }

    def _step_apply_assignments(self, auto_assign: bool) -> Dict:
        """Apply footprint assignments"""
        if not auto_assign or not self.footprint_mapping:
            return {
                'name': 'Apply Assignments',
                'status': 'skipped',
                'reason': 'auto_assign=False or no resolved footprints'
            }

        # Update netlist
        updated_path = self.netlist_path.with_stem(
            self.netlist_path.stem + "_resolved"
        )

        success = NetlistUpdater.update_netlist(
            str(self.netlist_path),
            self.footprint_mapping,
            str(updated_path)
        )

        return {
            'name': 'Apply Assignments',
            'status': 'success' if success else 'error',
            'assignments_applied': len(self.footprint_mapping),
            'output_netlist': str(updated_path) if success else None
        }

    def _step_export_results(self) -> Dict:
        """Export resolution results"""
        output_dir = self.netlist_path.parent / "footprint_resolution"
        output_dir.mkdir(exist_ok=True)

        exports = {}

        # Export detailed JSON
        json_file = output_dir / "resolution_details.json"
        self._export_json(json_file)
        exports['json'] = str(json_file)

        # Export CSV
        csv_file = output_dir / "unresolved.csv"
        self._export_unresolved_csv(csv_file)
        exports['csv'] = str(csv_file)

        # Export summary report
        report_file = output_dir / "report.txt"
        self._export_text_report(report_file)
        exports['report'] = str(report_file)

        return {
            'name': 'Export Results',
            'status': 'success',
            'output_directory': str(output_dir),
            'exports': exports
        }

    def _export_json(self, output_file: Path):
        """Export resolution details as JSON"""
        data = {
            'components': {},
            'resolution': {}
        }

        # Component inventory
        for ref, comp in self.components.items():
            data['components'][ref] = {
                'value': comp.value,
                'description': comp.description,
                'library': comp.lib_source,
                'part': comp.lib_part,
                'type': comp.component_type.value,
                'current_footprint': comp.footprint
            }

        # Resolution results
        for ref, matches in self.resolution_details.items():
            data['resolution'][ref] = [
                {
                    'footprint': m.footprint,
                    'source': m.source,
                    'confidence': m.confidence,
                    'notes': m.notes
                }
                for m in matches[:3]  # Top 3 matches
            ]

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _export_unresolved_csv(self, output_file: Path):
        """Export unresolved components as CSV"""
        unresolved = [
            ref for ref in self.parser.get_missing_footprints().keys()
            if ref not in self.footprint_mapping
        ]

        with open(output_file, 'w') as f:
            f.write("Reference,Value,Description,Library,Part,TopMatch,Confidence\n")

            for ref in sorted(unresolved):
                comp = self.components[ref]
                matches = self.resolution_details.get(ref, [])
                top_match = matches[0] if matches else None

                f.write(
                    f"{ref},{comp.value},"
                    f'"{comp.description}",{comp.lib_source},'
                    f"{comp.lib_part},"
                    f"{top_match.footprint if top_match else 'N/A'},"
                    f"{top_match.confidence if top_match else 0}\n"
                )

    def _export_text_report(self, output_file: Path):
        """Export human-readable text report"""
        lines = [
            "KiCad Footprint Hunter - Resolution Report",
            "=" * 50,
            f"Netlist: {self.netlist_path}",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "SUMMARY",
            "-" * 50,
        ]

        summary = self.parser.get_component_summary()
        lines.extend([
            f"Total Components: {summary['total_components']}",
            f"With Footprints: {summary['with_footprints']}",
            f"Missing Footprints: {summary['missing_footprints']}",
            f"Coverage: {summary['coverage_percent']:.1f}%",
            "",
            "RESOLUTION RESULTS",
            "-" * 50,
        ])

        resolved_count = len(self.footprint_mapping)
        missing_count = summary['missing_footprints']

        lines.extend([
            f"Resolved: {resolved_count}/{missing_count}",
            f"Success Rate: {resolved_count/missing_count*100:.1f}%" if missing_count > 0 else "0%",
            "",
            "UNRESOLVED COMPONENTS",
            "-" * 50,
        ])

        unresolved = [
            ref for ref in self.parser.get_missing_footprints().keys()
            if ref not in self.footprint_mapping
        ]

        if unresolved:
            for ref in sorted(unresolved):
                comp = self.components[ref]
                matches = self.resolution_details.get(ref, [])
                top_match = matches[0] if matches else None

                lines.append(f"\n{ref} ({comp.value})")
                lines.append(f"  Description: {comp.description}")
                lines.append(f"  Library: {comp.lib_source}:{comp.lib_part}")

                if top_match:
                    lines.append(f"  Best Match: {top_match.footprint}")
                    lines.append(f"  Confidence: {top_match.confidence:.1%}")
                    lines.append(f"  Source: {top_match.source}")
                else:
                    lines.append("  Status: No matches found")
        else:
            lines.append("All components resolved!")

        with open(output_file, 'w') as f:
            f.write("\n".join(lines))

    def get_resolution_summary(self) -> Dict:
        """Get brief summary of resolution status"""
        missing = self.parser.get_missing_footprints()
        resolved = len(self.footprint_mapping)
        total_missing = len(missing)

        return {
            'total_components': len(self.components),
            'missing_footprints': total_missing,
            'resolved': resolved,
            'unresolved': total_missing - resolved,
            'resolution_rate': f"{resolved/total_missing*100:.1f}%" if total_missing > 0 else "0%"
        }

    def get_unresolved_components(self) -> Dict[str, Dict]:
        """Get details on unresolved components"""
        missing = self.parser.get_missing_footprints()
        unresolved = {}

        for ref in missing:
            if ref not in self.footprint_mapping:
                comp = self.components[ref]
                matches = self.resolution_details.get(ref, [])

                unresolved[ref] = {
                    'value': comp.value,
                    'description': comp.description,
                    'library': f"{comp.lib_source}:{comp.lib_part}",
                    'attempted_matches': len(matches),
                    'best_match': matches[0].footprint if matches else None,
                    'best_confidence': matches[0].confidence if matches else 0
                }

        return unresolved
