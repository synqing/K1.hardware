#!/usr/bin/env python3
"""
K1 Lightwave Routing Example
=============================

Example usage of the automated routing system for K1 Lightwave board.
Demonstrates all features and provides working reference implementation.

Author: Elite PCB Designer Agent
Date: 2025-10-24
Version: 1.0.0

Usage:
    python3 example_k1_routing.py
"""

import os
import sys
import logging
from pathlib import Path

# Import routing modules
from automated_routing import (
    AutomatedRouting,
    CriticalNetRouter,
    FreeRoutingIntegration,
    K1RoutingConfiguration,
    RoutingStatus,
)
from freerouting_config import (
    K1FreeRoutingProfile,
    print_config_summary,
)


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Setup logging configuration"""
    logger = logging.getLogger("k1_routing")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Console handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def example_full_pipeline():
    """
    Example 1: Complete routing pipeline

    This is the simplest way to route a board - just call execute()
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 1: FULL ROUTING PIPELINE")
    print("=" * 80)

    # Path to K1 board
    board_path = "hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb"

    if not Path(board_path).exists():
        print(f"⚠ Board file not found: {board_path}")
        print("  This is a demonstration - adjust path to your board")
        return

    # Setup logging
    logger = setup_logging(verbose=True)

    # Initialize routing system
    router = AutomatedRouting(
        board_path=board_path,
        freerouting_jar="/usr/local/bin/freerouting.jar",
        logger=logger
    )

    # Execute complete pipeline
    print("\nStarting automated routing...")
    success = router.execute()

    # Print results
    print("\n" + "=" * 80)
    print("ROUTING RESULTS")
    print("=" * 80)
    print(f"Status:          {router.result.status.value}")
    print(f"Success:         {router.result.success}")
    print(f"Nets routed:     {router.result.nets_routed} / {router.result.nets_total}")
    print(f"Completion:      {router.result.completion_percentage:.1f}%")
    print(f"Vias placed:     {router.result.vias_placed}")
    print(f"DRC violations:  {router.result.drc_violations}")
    print(f"Time elapsed:    {router.result.routing_time_sec:.1f}s")

    if router.result.errors:
        print("\nErrors:")
        for error in router.result.errors:
            print(f"  ✗ {error}")

    if router.result.warnings:
        print("\nWarnings:")
        for warning in router.result.warnings:
            print(f"  ⚠ {warning}")

    return success


def example_step_by_step():
    """
    Example 2: Step-by-step routing with control

    Demonstrates manual control over each routing step
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: STEP-BY-STEP ROUTING")
    print("=" * 80)

    board_path = "hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb"

    if not Path(board_path).exists():
        print(f"⚠ Board file not found: {board_path}")
        return

    logger = setup_logging()
    router = AutomatedRouting(board_path=board_path, logger=logger)

    # Step 1: Route critical nets
    print("\n[STEP 1/6] Routing critical nets...")
    critical_results = router.route_critical_nets()
    print(f"✓ Critical nets routed: {critical_results['total_nets']}")

    # Step 2: Export to DSN
    print("\n[STEP 2/6] Exporting to Specctra DSN...")
    if not router.export_for_autorouting():
        print("✗ DSN export failed")
        return False

    # Step 3: Run auto-router
    print("\n[STEP 3/6] Running FreeRouting auto-router...")
    if not router.run_autorouter():
        print("✗ Auto-routing failed")
        return False

    # Step 4: Create copper zones
    print("\n[STEP 4/6] Creating copper zones...")
    zone_results = router.create_copper_zones()
    print(f"✓ Zones created: {len(zone_results['zones_created'])}")

    # Step 5: Place thermal vias
    print("\n[STEP 5/6] Placing thermal vias...")
    via_results = router.place_thermal_vias()
    print(f"✓ Thermal vias placed: {via_results['total_vias']}")

    # Step 6: Validate routing
    print("\n[STEP 6/6] Validating routing...")
    valid, violations = router.validate_routing()

    if valid:
        print("✓ All validation checks passed")
        return True
    else:
        print(f"⚠ {len(violations)} violations found")
        return False


def example_critical_nets_only():
    """
    Example 3: Route critical nets only (no auto-routing)

    Useful for manually routing the remaining nets in KiCad GUI
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: CRITICAL NETS ONLY")
    print("=" * 80)

    board_path = "hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb"

    if not Path(board_path).exists():
        print(f"⚠ Board file not found: {board_path}")
        return

    logger = setup_logging()

    # Initialize critical net router
    router = CriticalNetRouter(board_path, logger)

    # Load board
    if not router.load_board():
        print("✗ Failed to load board")
        return False

    # Route each category
    print("\nRouting power distribution...")
    power_results = router.route_power_nets()
    print(f"✓ Power nets: {len(power_results['nets_routed'])}")

    print("\nRouting SPI signals...")
    spi_results = router.route_spi_signals()
    print(f"✓ SPI nets: {len(spi_results['nets_routed'])}")

    print("\nRouting USB differential pair...")
    usb_results = router.route_usb_signals()
    print(f"✓ USB nets: {len(usb_results['nets_routed'])}")

    print("\nRouting I2C/I2S signals...")
    i2c_results = router.route_i2c_i2s()
    print(f"✓ I2C/I2S nets: {len(i2c_results['nets_routed'])}")

    total_nets = (
        len(power_results['nets_routed']) +
        len(spi_results['nets_routed']) +
        len(usb_results['nets_routed']) +
        len(i2c_results['nets_routed'])
    )

    print(f"\n✓ Total critical nets routed: {total_nets}")
    print("\nNext steps:")
    print("  1. Open board in KiCad PCBnew")
    print("  2. Manually route remaining nets (optional)")
    print("  3. Run DRC check")
    print("  4. Export Gerbers")

    return True


def example_freerouting_configuration():
    """
    Example 4: Custom FreeRouting configuration

    Shows how to use different routing profiles and custom settings
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: FREEROUTING CONFIGURATION")
    print("=" * 80)

    # Show available profiles
    print("\nAvailable routing profiles:")
    print("\n1. Fast Prototype (2-5 minutes)")
    config_fast = K1FreeRoutingProfile.fast_prototype()
    print_config_summary(config_fast)

    print("\n2. Production Quality (10-15 minutes) - DEFAULT")
    config_prod = K1FreeRoutingProfile.production_quality()
    print_config_summary(config_prod)

    print("\n3. Extreme Quality (30-60 minutes)")
    config_extreme = K1FreeRoutingProfile.extreme_quality()
    print_config_summary(config_extreme)

    print("\n4. Minimal Vias (10-15 minutes)")
    config_vias = K1FreeRoutingProfile.minimal_vias()
    print_config_summary(config_vias)

    # Use custom profile with routing
    board_path = "hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb"

    if Path(board_path).exists():
        print("\nUsing custom profile for routing...")

        # You would integrate this with FreeRoutingIntegration
        # by passing the config to configure_freerouting()


def example_k1_specifications():
    """
    Example 5: Display K1 routing specifications

    Shows all K1-specific routing rules and constraints
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 5: K1 LIGHTWAVE SPECIFICATIONS")
    print("=" * 80)

    # Power nets
    print("\nPower Distribution Nets:")
    print("-" * 60)
    for net_name, spec in K1RoutingConfiguration.POWER_NETS.items():
        print(f"{net_name:20s}: {spec.width_mil:3.0f} mil ({spec.width_mm:.2f} mm)")

    # SPI nets
    print("\nSPI Signals (40 MHz):")
    print("-" * 60)
    for net_name, spec in K1RoutingConfiguration.SPI_NETS.items():
        damping = f"+ {spec.series_damping_ohm}Ω" if spec.series_damping_ohm else ""
        print(f"{net_name:20s}: {spec.width_mil:3.0f} mil {damping}")

    # USB nets
    print("\nUSB Differential Pair (12 Mbps):")
    print("-" * 60)
    for net_name, spec in K1RoutingConfiguration.USB_NETS.items():
        print(f"{net_name:20s}: {spec.width_mil:3.0f} mil, spacing {spec.differential_spacing_mil} mil")
        print(f"{'':20s}  length match: ±{spec.length_match_tolerance_mm} mm")

    # Via specifications
    print("\nVia Specifications:")
    print("-" * 60)
    std_via = K1RoutingConfiguration.STANDARD_VIA
    thm_via = K1RoutingConfiguration.THERMAL_VIA
    print(f"Standard via:  {std_via.diameter_mm} mm diameter, {std_via.drill_mm} mm drill")
    print(f"Thermal via:   {thm_via.diameter_mm} mm diameter, {thm_via.drill_mm} mm drill")

    # Copper zones
    print("\nCopper Zones (4-layer board):")
    print("-" * 60)
    for zone in K1RoutingConfiguration.COPPER_ZONES:
        print(f"Layer {zone.layer}: {zone.net_name} ({zone.name})")
        print(f"  Priority: {zone.priority}, Clearance: {zone.clearance_mm} mm")

    # Thermal vias
    print("\nThermal Via Arrays:")
    print("-" * 60)
    for array in K1RoutingConfiguration.THERMAL_VIAS:
        print(f"{array.component_ref}: {array.num_vias} vias in {array.pattern} pattern")
        print(f"  Grid spacing: {array.grid_spacing_mm} mm")

    # Summary
    print("\nTotal Critical Nets:")
    print("-" * 60)
    all_nets = K1RoutingConfiguration.get_all_critical_nets()
    print(f"Power:     {len(K1RoutingConfiguration.POWER_NETS)} nets")
    print(f"SPI:       {len(K1RoutingConfiguration.SPI_NETS)} nets")
    print(f"USB:       {len(K1RoutingConfiguration.USB_NETS)} nets")
    print(f"I2C/I2S:   {len(K1RoutingConfiguration.I2C_I2S_NETS)} nets")
    print(f"Total:     {len(all_nets)} critical nets")


def main():
    """Run all examples"""
    print("=" * 80)
    print("K1 LIGHTWAVE AUTOMATED ROUTING EXAMPLES")
    print("Elite PCB Designer Agent - Phase 3")
    print("=" * 80)

    examples = [
        ("Display K1 Specifications", example_k1_specifications),
        ("FreeRouting Configuration", example_freerouting_configuration),
        ("Critical Nets Only", example_critical_nets_only),
        # Uncomment to run full routing (requires valid board file)
        # ("Step-by-Step Routing", example_step_by_step),
        # ("Full Pipeline", example_full_pipeline),
    ]

    for i, (name, func) in enumerate(examples, 1):
        try:
            func()
        except KeyboardInterrupt:
            print("\n\n✗ Interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n✗ Example {i} failed: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 80)
    print("EXAMPLES COMPLETE")
    print("=" * 80)
    print("\nTo run full routing on K1 board:")
    print("  python3 automated_routing.py hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")


if __name__ == "__main__":
    main()
