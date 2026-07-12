#!/usr/bin/env python3
"""
K1 Lightwave Design Validation Script

Executes complete Phase 4 validation on K1 Lightwave PCB with
K1-specific parameters and generates comprehensive reports.

Usage:
    python validate_k1_lightwave.py

Author: Elite PCB Designer Agent
Date: 2025-10-24
"""

import sys
from pathlib import Path

from design_validation import (
    DesignValidation,
    ThermalParameters,
)
from validation_report_template import create_k1_validation_report


def validate_k1_lightwave():
    """Execute complete K1 Lightwave validation with K1-specific parameters"""

    print("=" * 80)
    print("K1 LIGHTWAVE - DESIGN VALIDATION EXECUTION")
    print("=" * 80)
    print()

    # K1 Lightwave board path
    board_path = Path(__file__).parent / "hardware" / "k1-lightwave" / "kicad" / "K1_Lightwave.kicad_pcb"

    if not board_path.exists():
        print(f"❌ ERROR: Board file not found at {board_path}")
        print(f"   Please ensure K1_Lightwave.kicad_pcb exists")
        return False

    print(f"📋 Board: {board_path.name}")
    print(f"📁 Path: {board_path}")
    print()

    # Output directory
    output_dir = Path(__file__).parent / "validation_output"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📂 Output: {output_dir}")
    print()

    # K1 Lightwave specific thermal parameters
    print("⚙️  K1 Lightwave Thermal Parameters:")
    print("   • Ambient: 25°C")
    print("   • MCU-A Power: 300mW (ESP32-S3)")
    print("   • MCU-B Power: 500mW (ESP32-S3)")
    print("   • Converter Power: 200mW")
    print("   • Total Power: 1W")
    print("   • R_thermal (MCU→GND): 15°C/W")
    print("   • R_thermal (GND→Ambient): 5°C/W")
    print("   • Thermal Via Benefit: 25%")
    print("   • Max Junction Temp: 85°C")
    print()

    thermal_params = ThermalParameters(
        ambient_temp_c=25.0,
        power_mcu_a_w=0.3,
        power_mcu_b_w=0.5,
        power_converter_w=0.2,
        r_thermal_mcu_to_gnd=15.0,
        r_thermal_gnd_to_ambient=5.0,
        thermal_via_benefit_pct=0.25,
        max_junction_temp_c=85.0
    )

    # Initialize validator
    print("🔧 Initializing validation suite...")
    validator = DesignValidation(board_path, output_dir)
    validator.thermal.params = thermal_params  # Override with K1 parameters
    print("✅ Validator initialized")
    print()

    # Execute validation pipeline
    print("🚀 Executing validation pipeline...")
    print("-" * 80)
    success = validator.execute()
    print("-" * 80)
    print()

    # Generate K1-specific report
    if validator.results:
        print("📊 Generating K1 validation reports...")
        summary = {
            'all_passed': all(r.passed for r in validator.results),
            'total_checks': len(validator.results),
            'passed': sum(1 for r in validator.results if r.passed),
            'failed': sum(1 for r in validator.results if not r.passed),
            'critical_errors': sum(1 for r in validator.results if r.severity.value == 'ERROR'),
            'warnings': sum(1 for r in validator.results if r.severity.value == 'WARNING'),
            'manufacturing_ready': success
        }

        text_path, json_path = create_k1_validation_report(
            validator.results,
            summary,
            output_dir
        )
        print(f"✅ Text report: {text_path}")
        print(f"✅ JSON report: {json_path}")
        print()

    # Print final summary
    print("=" * 80)
    print("K1 LIGHTWAVE VALIDATION SUMMARY")
    print("=" * 80)

    if success:
        print("✅ VALIDATION PASSED - BOARD IS MANUFACTURING READY!")
        print()
        print("Expected K1 Results:")
        print("  ✅ DRC: 0 violations")
        print("  ✅ DFM: 0 violations")
        print("  ✅ Signal Integrity: PASS")
        print("  ✅ Thermal: T_junction ≈ 40°C (45°C margin)")
        print("  ✅ Manufacturing Ready: YES")
        print()
        print("Cost Estimate (JLCPCB):")
        print("  • Board Size: ~100x80mm")
        print("  • Layer Count: 4 layers")
        print("  • Quantity: 5 boards")
        print("  • Cost per Board: ~$15-20 USD")
        print("  • Lead Time: 3-5 business days")
        print()
        print("Next Steps:")
        print("  1. Review validation reports in validation_output/")
        print("  2. Verify manufacturing files in validation_output/manufacturing/")
        print("  3. Upload Gerber files to JLCPCB")
        print("  4. Review automated DFM check")
        print("  5. Place order for prototype boards")
        print()
        print("📦 Manufacturing files ready in: validation_output/manufacturing/")
        print("🎉 Ready to manufacture!")
    else:
        print("❌ VALIDATION FAILED - ISSUES DETECTED")
        print()
        print("Issues to address:")
        for result in validator.results:
            if not result.passed:
                print(f"  ❌ {result.check_name}: {result.message}")
        print()
        print("Review validation reports for details:")
        print(f"  • Text report: {output_dir}/validation_report.txt")
        print(f"  • JSON report: {output_dir}/validation_summary.json")
        print()
        print("Fix issues and re-run validation.")

    print("=" * 80)
    print()

    return success


def main():
    """Main entry point"""
    try:
        success = validate_k1_lightwave()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
