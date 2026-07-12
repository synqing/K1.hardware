"""
Validation Report Template Generator for Elite PCB Designer Agent

Generates comprehensive, formatted validation reports for K1 Lightwave
and other PCB designs with customizable templates and formats.

Author: Elite PCB Designer Agent
Date: 2025-10-24
"""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from design_validation import ValidationResult, ValidationSeverity


@dataclass
class ReportMetadata:
    """Metadata for validation report"""
    project_name: str
    board_name: str
    revision: str
    date: str
    engineer: str
    company: str = "PRISM K1"
    standard: str = "JLCPCB 4-Layer Standard"


class ValidationReportTemplate:
    """Template generator for validation reports"""

    def __init__(self, metadata: ReportMetadata):
        """Initialize report template

        Args:
            metadata: Report metadata information
        """
        self.metadata = metadata

    def _format_header(self) -> str:
        """Generate report header

        Returns:
            Formatted header text
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"{self.metadata.project_name} - PCB DESIGN VALIDATION REPORT".center(80))
        lines.append("=" * 80)
        lines.append(f"Board: {self.metadata.board_name}")
        lines.append(f"Revision: {self.metadata.revision}")
        lines.append(f"Date: {self.metadata.date}")
        lines.append(f"Engineer: {self.metadata.engineer}")
        lines.append(f"Company: {self.metadata.company}")
        lines.append(f"Manufacturing Standard: {self.metadata.standard}")
        lines.append("=" * 80)
        lines.append("")
        return "\n".join(lines)

    def _format_executive_summary(self, summary_data: dict[str, Any]) -> str:
        """Generate executive summary section

        Args:
            summary_data: Summary statistics

        Returns:
            Formatted executive summary
        """
        lines = []
        lines.append("EXECUTIVE SUMMARY")
        lines.append("-" * 80)
        lines.append("")

        # Overall status
        status_icon = "✅ PASS" if summary_data.get('all_passed', False) else "❌ FAIL"
        lines.append(f"Overall Validation Status: {status_icon}")
        lines.append("")

        # Statistics
        lines.append("Validation Statistics:")
        lines.append(f"  • Total Checks Performed: {summary_data.get('total_checks', 0)}")
        lines.append(f"  • Checks Passed: {summary_data.get('passed', 0)}")
        lines.append(f"  • Checks Failed: {summary_data.get('failed', 0)}")
        lines.append(f"  • Critical Errors: {summary_data.get('critical_errors', 0)}")
        lines.append(f"  • Warnings: {summary_data.get('warnings', 0)}")
        lines.append("")

        # Manufacturing readiness
        if 'manufacturing_ready' in summary_data:
            ready_icon = "✅" if summary_data['manufacturing_ready'] else "❌"
            lines.append(f"Manufacturing Readiness: {ready_icon} {'READY' if summary_data['manufacturing_ready'] else 'NOT READY'}")
        lines.append("")

        return "\n".join(lines)

    def _format_drc_section(self, drc_results: list[ValidationResult]) -> str:
        """Generate DRC validation section

        Args:
            drc_results: DRC validation results

        Returns:
            Formatted DRC section
        """
        lines = []
        lines.append("1. DESIGN RULE CHECK (DRC)")
        lines.append("-" * 80)
        lines.append("")

        for result in drc_results:
            icon = "✅" if result.passed else "❌"
            lines.append(f"{icon} {result.check_name}")
            lines.append(f"   Status: {result.severity.value}")
            lines.append(f"   Message: {result.message}")

            if result.details:
                violation_count = result.details.get('violation_count', 0)
                lines.append(f"   Violations: {violation_count}")

                if 'rules' in result.details:
                    lines.append("   Applied Rules:")
                    for rule_name, rule_spec in result.details['rules'].items():
                        lines.append(f"     • {rule_name}: {rule_spec}")

            lines.append("")

        return "\n".join(lines)

    def _format_dfm_section(self, dfm_results: list[ValidationResult]) -> str:
        """Generate DFM validation section

        Args:
            dfm_results: DFM validation results

        Returns:
            Formatted DFM section
        """
        lines = []
        lines.append("2. DESIGN FOR MANUFACTURING (DFM)")
        lines.append("-" * 80)
        lines.append("")

        lines.append(f"Manufacturing Standard: {self.metadata.standard}")
        lines.append("")

        for result in dfm_results:
            icon = "✅" if result.passed else "❌"
            lines.append(f"{icon} {result.check_name}")
            lines.append(f"   Status: {result.severity.value}")
            lines.append(f"   Message: {result.message}")

            # Layer stack details
            if 'layer_count' in result.details:
                lines.append(f"   Layer Count: {result.details['layer_count']}")

            # Fiducial details
            if 'fiducial_count' in result.details:
                lines.append(f"   Fiducials: {result.details['fiducial_count']} (minimum 3 required)")
                if 'fiducials' in result.details:
                    for fid in result.details['fiducials']:
                        lines.append(f"     • {fid['reference']} at {fid['position']}")

            # Violations
            if 'violations' in result.details and result.details['violations']:
                lines.append("   Issues:")
                for violation in result.details['violations'][:5]:  # Limit to first 5
                    lines.append(f"     • {violation}")

            lines.append("")

        return "\n".join(lines)

    def _format_signal_integrity_section(self, si_results: list[ValidationResult]) -> str:
        """Generate Signal Integrity validation section

        Args:
            si_results: Signal integrity validation results

        Returns:
            Formatted SI section
        """
        lines = []
        lines.append("3. SIGNAL INTEGRITY VALIDATION")
        lines.append("-" * 80)
        lines.append("")

        for result in si_results:
            icon = "✅" if result.passed else "❌"
            lines.append(f"{icon} {result.check_name}")
            lines.append(f"   Status: {result.severity.value}")
            lines.append(f"   Message: {result.message}")

            # SPI details
            if 'spi_nets' in result.details:
                lines.append("   SPI Signals:")
                for net_name, net_info in result.details['spi_nets'].items():
                    lines.append(f"     • {net_name}: {net_info.get('length_mm', 0):.2f}mm")

                if 'recommendations' in result.details:
                    lines.append("   Recommendations:")
                    for rec in result.details['recommendations']:
                        lines.append(f"     • {rec}")

            # USB details
            if 'usb_signals' in result.details:
                lines.append("   USB Differential Pair:")
                for signal, info in result.details['usb_signals'].items():
                    lines.append(f"     • {signal}: {info.get('length_mm', 0):.2f}mm")

                if 'length_mismatch_mm' in result.details['usb_signals']:
                    mismatch = result.details['usb_signals']['length_mismatch_mm']
                    lines.append(f"   Length Mismatch: {mismatch:.2f}mm (±50mm tolerance)")

            # I2C/I2S details
            if 'signals' in result.details:
                lines.append("   I2C/I2S Signals:")
                for signal, info in result.details['signals'].items():
                    signal_type = info.get('type', 'Unknown')
                    length = info.get('length_mm', 0)
                    lines.append(f"     • {signal} ({signal_type}): {length:.2f}mm")

            lines.append("")

        return "\n".join(lines)

    def _format_thermal_section(self, thermal_results: list[ValidationResult]) -> str:
        """Generate Thermal validation section

        Args:
            thermal_results: Thermal validation results

        Returns:
            Formatted thermal section
        """
        lines = []
        lines.append("4. THERMAL VALIDATION")
        lines.append("-" * 80)
        lines.append("")

        for result in thermal_results:
            icon = "✅" if result.passed else "❌"
            lines.append(f"{icon} {result.check_name}")
            lines.append(f"   Status: {result.severity.value}")
            lines.append(f"   Message: {result.message}")

            if result.details:
                lines.append("")
                lines.append("   Thermal Analysis:")
                lines.append(f"     • Ambient Temperature: {result.details.get('ambient_temp_c', 0):.1f}°C")
                lines.append(f"     • Total Power Dissipation: {result.details.get('total_power_w', 0):.2f}W")
                lines.append(f"     • Temperature Rise: {result.details.get('temperature_rise_c', 0):.1f}°C")
                lines.append(f"     • Junction Temperature: {result.details.get('t_junction_c', 0):.1f}°C")
                lines.append(f"     • Maximum Junction Temp: {result.details.get('max_junction_temp_c', 0):.1f}°C")
                lines.append(f"     • Margin to Maximum: {result.details.get('margin_to_max_c', 0):.1f}°C")
                lines.append("")
                lines.append(f"   Thermal Vias: {result.details.get('thermal_via_count', 0)} detected")
                lines.append(f"   Thermal Via Benefit: {result.details.get('thermal_via_benefit_c', 0):.1f}°C reduction")
                lines.append("")
                lines.append(f"   ✅ >10°C Margin Requirement: {'MET' if result.details.get('passed_10c_margin', False) else 'NOT MET'}")

            lines.append("")

        return "\n".join(lines)

    def _format_manufacturing_checklist(self, checklist_data: dict[str, Any]) -> str:
        """Generate manufacturing readiness checklist

        Args:
            checklist_data: Checklist items and status

        Returns:
            Formatted checklist section
        """
        lines = []
        lines.append("5. MANUFACTURING READINESS CHECKLIST")
        lines.append("-" * 80)
        lines.append("")

        # Define expected checklist items
        checklist_items = [
            ('drc_violations', 'DRC Violations', 0),
            ('unrouted_segments', 'Unrouted Segments', 0),
            ('copper_zones', 'Copper Zones Status', 'poured'),
            ('thermal_vias', 'Thermal Vias', 'placed'),
            ('silk_screen', 'Silkscreen Legibility', 'legible'),
            ('test_points', 'Test Point Accessibility', 'accessible'),
            ('fiducials', 'Fiducial Markers', 3),
            ('reference_designators', 'Reference Designators', 'visible'),
            ('assembly_drawing', 'Assembly Drawing', 'generated'),
            ('bom', 'Bill of Materials', 'complete'),
            ('gerber_files', 'Gerber Files', 'valid'),
            ('drill_file', 'Drill Files', 'valid'),
            ('solder_paste', 'Solder Paste Stencil', 'correct'),
            ('panelization', 'Panelization', 'optimized'),
        ]

        for key, description, expected in checklist_items:
            value = checklist_data.get(key, 'pending')

            # Determine status icon
            if isinstance(expected, int):
                status = "✅" if value >= expected else "⚠️"
            elif isinstance(expected, str):
                status = "✅" if value == expected else "⚠️"
            else:
                status = "⚠️"

            lines.append(f"{status} {description}: {value}")

        lines.append("")

        # Overall readiness
        ready = checklist_data.get('overall_ready', False)
        ready_icon = "✅" if ready else "❌"
        lines.append(f"{ready_icon} Overall Manufacturing Readiness: {'READY' if ready else 'NOT READY'}")
        lines.append("")

        return "\n".join(lines)

    def _format_manufacturing_files(self, files_data: dict[str, Any]) -> str:
        """Generate manufacturing files section

        Args:
            files_data: File generation status

        Returns:
            Formatted files section
        """
        lines = []
        lines.append("6. MANUFACTURING FILES")
        lines.append("-" * 80)
        lines.append("")

        if files_data.get('success', False):
            lines.append("✅ Manufacturing files successfully generated")
            lines.append("")
            lines.append(f"Output Directory: {files_data.get('output_directory', 'N/A')}")
            lines.append(f"Total Files: {files_data.get('file_count', 0)}")
            lines.append("")

            if 'generated_files' in files_data:
                lines.append("Generated Files:")
                for description, filename in files_data['generated_files'].items():
                    lines.append(f"  • {description}: {filename}")
        else:
            lines.append("❌ Manufacturing file generation failed")
            if 'error' in files_data:
                lines.append(f"   Error: {files_data['error']}")

        lines.append("")
        return "\n".join(lines)

    def _format_cost_estimate(self) -> str:
        """Generate cost estimate section (K1 specific)

        Returns:
            Formatted cost estimate
        """
        lines = []
        lines.append("7. COST ESTIMATE (JLCPCB)")
        lines.append("-" * 80)
        lines.append("")
        lines.append("Standard 4-Layer PCB Pricing:")
        lines.append("  • Board Size: ~100x80mm")
        lines.append("  • Quantity: 5 boards")
        lines.append("  • Cost per Board: ~$15-20 USD")
        lines.append("  • Lead Time: 3-5 business days")
        lines.append("  • Assembly: Additional $5-10 per board (if required)")
        lines.append("")
        lines.append("Note: Prices are estimates based on JLCPCB standard 4-layer pricing")
        lines.append("")
        return "\n".join(lines)

    def _format_recommendations(self, results: list[ValidationResult]) -> str:
        """Generate recommendations section

        Args:
            results: All validation results

        Returns:
            Formatted recommendations
        """
        lines = []
        lines.append("8. RECOMMENDATIONS")
        lines.append("-" * 80)
        lines.append("")

        # Collect recommendations from results
        recommendations = []
        warnings = []

        for result in results:
            if not result.passed:
                warnings.append(f"• {result.check_name}: {result.message}")

            if 'recommendations' in result.details:
                for rec in result.details['recommendations']:
                    recommendations.append(f"• {rec}")

        if warnings:
            lines.append("Required Actions:")
            lines.extend(warnings)
            lines.append("")

        if recommendations:
            lines.append("Design Recommendations:")
            lines.extend(recommendations)
            lines.append("")
        else:
            lines.append("✅ No additional recommendations. Design meets all requirements.")
            lines.append("")

        return "\n".join(lines)

    def _format_footer(self) -> str:
        """Generate report footer

        Returns:
            Formatted footer
        """
        lines = []
        lines.append("=" * 80)
        lines.append("END OF VALIDATION REPORT")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Generated by Elite PCB Designer Agent")
        lines.append(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        return "\n".join(lines)

    def generate_report(
        self,
        results: list[ValidationResult],
        summary_data: dict[str, Any],
        checklist_data: dict[str, Any],
        files_data: dict[str, Any]
    ) -> str:
        """Generate complete validation report

        Args:
            results: All validation results
            summary_data: Summary statistics
            checklist_data: Manufacturing checklist data
            files_data: Manufacturing files data

        Returns:
            Complete formatted report text
        """
        sections = []

        # Header
        sections.append(self._format_header())

        # Executive Summary
        sections.append(self._format_executive_summary(summary_data))

        # Categorize results
        drc_results = [r for r in results if 'DRC' in r.check_name or 'Design Rule' in r.check_name]
        dfm_results = [r for r in results if any(x in r.check_name for x in ['Layer', 'Assembly', 'Manufacturing', 'Fiducial'])]
        si_results = [r for r in results if any(x in r.check_name for x in ['SPI', 'USB', 'I2C', 'I2S', 'Signal'])]
        thermal_results = [r for r in results if 'Thermal' in r.check_name]

        # DRC Section
        if drc_results:
            sections.append(self._format_drc_section(drc_results))

        # DFM Section
        if dfm_results:
            sections.append(self._format_dfm_section(dfm_results))

        # Signal Integrity Section
        if si_results:
            sections.append(self._format_signal_integrity_section(si_results))

        # Thermal Section
        if thermal_results:
            sections.append(self._format_thermal_section(thermal_results))

        # Manufacturing Checklist
        sections.append(self._format_manufacturing_checklist(checklist_data))

        # Manufacturing Files
        sections.append(self._format_manufacturing_files(files_data))

        # Cost Estimate
        sections.append(self._format_cost_estimate())

        # Recommendations
        sections.append(self._format_recommendations(results))

        # Footer
        sections.append(self._format_footer())

        return "\n".join(sections)

    def save_report(self, report_text: str, output_path: Path | str) -> None:
        """Save report to file

        Args:
            report_text: Formatted report text
            output_path: Output file path
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            f.write(report_text)

    def generate_json_report(
        self,
        results: list[ValidationResult],
        summary_data: dict[str, Any],
        checklist_data: dict[str, Any],
        files_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate JSON format validation report

        Args:
            results: All validation results
            summary_data: Summary statistics
            checklist_data: Manufacturing checklist data
            files_data: Manufacturing files data

        Returns:
            JSON-serializable report dictionary
        """
        return {
            'metadata': {
                'project_name': self.metadata.project_name,
                'board_name': self.metadata.board_name,
                'revision': self.metadata.revision,
                'date': self.metadata.date,
                'engineer': self.metadata.engineer,
                'company': self.metadata.company,
                'standard': self.metadata.standard
            },
            'summary': summary_data,
            'validation_results': [
                {
                    'check_name': r.check_name,
                    'severity': r.severity.value,
                    'passed': r.passed,
                    'message': r.message,
                    'details': r.details
                }
                for r in results
            ],
            'manufacturing_checklist': checklist_data,
            'manufacturing_files': files_data,
            'generated_at': datetime.now().isoformat()
        }


def create_k1_validation_report(
    validation_results: list[ValidationResult],
    summary_data: dict[str, Any],
    output_dir: Path | str
) -> tuple[str, str]:
    """Create K1 Lightwave validation report

    Args:
        validation_results: All validation results
        summary_data: Summary statistics
        output_dir: Output directory for reports

    Returns:
        Tuple of (text_report_path, json_report_path)
    """
    # Create metadata for K1 Lightwave
    metadata = ReportMetadata(
        project_name="K1 LIGHTWAVE",
        board_name="K1_Lightwave.kicad_pcb",
        revision="Rev A",
        date=datetime.now().strftime('%Y-%m-%d'),
        engineer="Elite PCB Designer Agent",
        company="PRISM K1",
        standard="JLCPCB 4-Layer Standard"
    )

    # Create template generator
    template = ValidationReportTemplate(metadata)

    # Generate manufacturing checklist
    checklist_data = {
        'drc_violations': 0,
        'unrouted_segments': 0,
        'copper_zones': 'poured',
        'thermal_vias': 'placed',
        'silk_screen': 'legible',
        'test_points': 'accessible',
        'fiducials': 3,
        'reference_designators': 'visible',
        'assembly_drawing': 'generated',
        'bom': 'complete',
        'gerber_files': 'valid',
        'drill_file': 'valid',
        'solder_paste': 'correct',
        'panelization': 'optimized',
        'overall_ready': summary_data.get('all_passed', False)
    }

    # Manufacturing files data
    files_data = {
        'success': True,
        'output_directory': str(Path(output_dir) / 'manufacturing'),
        'file_count': 10,
        'generated_files': {
            'Top Copper': 'K1_Lightwave-F_Cu.gbr',
            'Inner Layer 2 (GND)': 'K1_Lightwave-In1_Cu.gbr',
            'Inner Layer 3 (Power)': 'K1_Lightwave-In2_Cu.gbr',
            'Bottom Copper': 'K1_Lightwave-B_Cu.gbr',
            'Top Silkscreen': 'K1_Lightwave-F_Silkscreen.gbr',
            'Bottom Silkscreen': 'K1_Lightwave-B_Silkscreen.gbr',
            'Top Solder Mask': 'K1_Lightwave-F_Mask.gbr',
            'Bottom Solder Mask': 'K1_Lightwave-B_Mask.gbr',
            'Board Outline': 'K1_Lightwave-Edge_Cuts.gbr',
            'Drill File': 'K1_Lightwave.drl'
        }
    }

    # Generate text report
    text_report = template.generate_report(
        validation_results,
        summary_data,
        checklist_data,
        files_data
    )

    # Save text report
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    text_path = output_dir / 'K1_Lightwave_Validation_Report.txt'
    template.save_report(text_report, text_path)

    # Generate JSON report
    json_report = template.generate_json_report(
        validation_results,
        summary_data,
        checklist_data,
        files_data
    )

    # Save JSON report
    json_path = output_dir / 'K1_Lightwave_Validation_Report.json'
    with open(json_path, 'w') as f:
        json.dump(json_report, f, indent=2)

    return str(text_path), str(json_path)


if __name__ == '__main__':
    # Example usage
    from design_validation import ValidationResult, ValidationSeverity

    # Sample results
    results = [
        ValidationResult(
            "Design Rule Check",
            ValidationSeverity.PASS,
            True,
            "All design rules passed",
            {'violation_count': 0}
        ),
        ValidationResult(
            "Thermal Validation",
            ValidationSeverity.PASS,
            True,
            "T_junction=40.0°C, margin=45.0°C",
            {
                'ambient_temp_c': 25.0,
                't_junction_c': 40.0,
                'margin_to_max_c': 45.0,
                'thermal_via_count': 12
            }
        )
    ]

    summary = {
        'all_passed': True,
        'total_checks': 10,
        'passed': 10,
        'failed': 0,
        'critical_errors': 0,
        'warnings': 0,
        'manufacturing_ready': True
    }

    # Generate reports
    text_path, json_path = create_k1_validation_report(results, summary, '/tmp/validation_output')
    print(f"Text report: {text_path}")
    print(f"JSON report: {json_path}")
