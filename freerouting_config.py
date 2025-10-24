"""
FreeRouting Configuration for K1 Lightwave
===========================================

Configuration management and parameter tuning for FreeRouting auto-router.
Optimized for K1 Lightwave board with 40 MHz SPI, USB 2.0, and high-current
LED power distribution.

Author: Elite PCB Designer Agent
Date: 2025-10-24
Version: 1.0.0
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class EffortLevel(Enum):
    """FreeRouting effort levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class OptimizationMode(Enum):
    """FreeRouting optimization priorities"""
    LENGTH = "length"           # Minimize total trace length
    VIA_COUNT = "via_count"     # Minimize number of vias
    BALANCED = "balanced"       # Balance between length and vias


@dataclass
class FreeRoutingConfig:
    """FreeRouting configuration parameters"""

    # Threading
    threads: int = 4

    # Effort and optimization
    effort_level: EffortLevel = EffortLevel.HIGH
    optimization_mode: OptimizationMode = OptimizationMode.LENGTH

    # Routing parameters
    max_passes: int = 100
    via_optimization: bool = True
    fanout_optimization: bool = True
    post_route_optimization: bool = True

    # Cost function weights (0-100)
    trace_length_cost: int = 50
    via_cost: int = 20
    trace_layer_change_cost: int = 30

    # Layer preferences
    preferred_signal_layers: List[str] = None
    avoid_inner_layer_routing: bool = False

    # Via settings
    minimize_vias: bool = True
    via_keepout_margin_mm: float = 0.5
    max_via_count: Optional[int] = 50

    # Trace settings
    trace_pull_tight: bool = True
    trace_corner_optimization: bool = True

    # Timing
    timeout_seconds: int = 900  # 15 minutes

    # Output
    save_intermediate_results: bool = False
    verbose_logging: bool = True

    def __post_init__(self):
        """Initialize default values"""
        if self.preferred_signal_layers is None:
            self.preferred_signal_layers = ["F.Cu", "B.Cu"]

    def to_cli_args(self) -> List[str]:
        """
        Convert configuration to FreeRouting CLI arguments

        Returns:
            List of command-line arguments
        """
        args = []

        # Threading
        args.extend(["-mt", str(self.threads)])

        # Optimization
        if self.via_optimization:
            args.append("--via-optimization")

        # Max passes
        args.extend(["-oit", str(self.max_passes)])

        # Disable GUI (headless mode)
        args.append("--gui.enabled=false")

        return args

    def to_rules_file(self) -> Dict[str, any]:
        """
        Generate FreeRouting design rules configuration

        Returns:
            Dictionary of design rules
        """
        rules = {
            "effort_level": self.effort_level.value,
            "optimization": {
                "mode": self.optimization_mode.value,
                "trace_length_cost": self.trace_length_cost,
                "via_cost": self.via_cost,
                "layer_change_cost": self.trace_layer_change_cost,
            },
            "via_settings": {
                "minimize": self.minimize_vias,
                "keepout_margin_mm": self.via_keepout_margin_mm,
                "max_count": self.max_via_count,
            },
            "trace_settings": {
                "pull_tight": self.trace_pull_tight,
                "corner_optimization": self.trace_corner_optimization,
            },
            "layer_preferences": {
                "signal_layers": self.preferred_signal_layers,
                "avoid_inner": self.avoid_inner_layer_routing,
            }
        }

        return rules


class K1FreeRoutingProfile:
    """Predefined FreeRouting profiles for K1 Lightwave"""

    @staticmethod
    def fast_prototype() -> FreeRoutingConfig:
        """
        Fast routing for quick prototypes

        - Lower effort
        - Fewer passes
        - Faster completion (2-5 minutes)
        - May have more vias and longer traces
        """
        return FreeRoutingConfig(
            threads=4,
            effort_level=EffortLevel.MEDIUM,
            optimization_mode=OptimizationMode.VIA_COUNT,
            max_passes=50,
            timeout_seconds=300,  # 5 minutes
            via_optimization=True,
            post_route_optimization=False,
        )

    @staticmethod
    def production_quality() -> FreeRoutingConfig:
        """
        High-quality routing for production boards (DEFAULT)

        - High effort
        - More passes
        - Optimized trace lengths
        - Minimal vias
        - Longer routing time (10-30 minutes)
        """
        return FreeRoutingConfig(
            threads=4,
            effort_level=EffortLevel.HIGH,
            optimization_mode=OptimizationMode.LENGTH,
            max_passes=100,
            timeout_seconds=900,  # 15 minutes
            via_optimization=True,
            fanout_optimization=True,
            post_route_optimization=True,
            minimize_vias=True,
            trace_pull_tight=True,
            trace_corner_optimization=True,
        )

    @staticmethod
    def extreme_quality() -> FreeRoutingConfig:
        """
        Maximum quality routing (use for critical boards)

        - Extreme effort
        - Maximum passes
        - Absolute minimum trace length
        - Very long routing time (30-120 minutes)
        """
        return FreeRoutingConfig(
            threads=8,
            effort_level=EffortLevel.EXTREME,
            optimization_mode=OptimizationMode.LENGTH,
            max_passes=200,
            timeout_seconds=3600,  # 60 minutes
            via_optimization=True,
            fanout_optimization=True,
            post_route_optimization=True,
            minimize_vias=True,
            trace_pull_tight=True,
            trace_corner_optimization=True,
            trace_length_cost=70,
            via_cost=30,
        )

    @staticmethod
    def minimal_vias() -> FreeRoutingConfig:
        """
        Minimize via count (for cost reduction)

        - Optimizes for fewer vias
        - May have longer traces
        - Good for simple boards
        """
        return FreeRoutingConfig(
            threads=4,
            effort_level=EffortLevel.HIGH,
            optimization_mode=OptimizationMode.VIA_COUNT,
            max_passes=100,
            timeout_seconds=600,  # 10 minutes
            via_optimization=True,
            minimize_vias=True,
            trace_length_cost=30,
            via_cost=70,
            max_via_count=30,
        )

    @staticmethod
    def two_layer_board() -> FreeRoutingConfig:
        """
        Configuration for 2-layer boards

        - Routes only on top and bottom
        - No inner layers
        - More vias expected
        """
        return FreeRoutingConfig(
            threads=4,
            effort_level=EffortLevel.HIGH,
            optimization_mode=OptimizationMode.BALANCED,
            max_passes=100,
            timeout_seconds=600,
            preferred_signal_layers=["F.Cu", "B.Cu"],
            avoid_inner_layer_routing=True,
        )

    @staticmethod
    def four_layer_board() -> FreeRoutingConfig:
        """
        Configuration for 4-layer boards (K1 Lightwave default)

        - Uses all 4 layers
        - Inner layers for GND/power planes
        - Outer layers for signal routing
        """
        return FreeRoutingConfig(
            threads=4,
            effort_level=EffortLevel.HIGH,
            optimization_mode=OptimizationMode.LENGTH,
            max_passes=100,
            timeout_seconds=900,
            preferred_signal_layers=["F.Cu", "B.Cu"],
            avoid_inner_layer_routing=False,  # Allow routing on In1.Cu, In2.Cu if needed
        )


def generate_freerouting_command(
    dsn_file: str,
    ses_file: str,
    config: Optional[FreeRoutingConfig] = None,
    jar_path: str = "freerouting.jar"
) -> List[str]:
    """
    Generate complete FreeRouting command-line invocation

    Args:
        dsn_file: Input DSN file path
        ses_file: Output SES file path
        config: FreeRouting configuration (default: production_quality)
        jar_path: Path to FreeRouting JAR file

    Returns:
        List of command arguments
    """
    if config is None:
        config = K1FreeRoutingProfile.production_quality()

    cmd = [
        "java",
        "-Djava.awt.headless=true",
        "-Xmx4g",  # 4GB heap memory
        "-jar", jar_path,
        "-de", dsn_file,
        "-do", ses_file,
    ]

    cmd.extend(config.to_cli_args())

    return cmd


def print_config_summary(config: FreeRoutingConfig):
    """
    Print human-readable configuration summary

    Args:
        config: FreeRouting configuration to display
    """
    print("FreeRouting Configuration")
    print("=" * 60)
    print(f"Effort level:        {config.effort_level.value}")
    print(f"Optimization mode:   {config.optimization_mode.value}")
    print(f"Threads:             {config.threads}")
    print(f"Max passes:          {config.max_passes}")
    print(f"Timeout:             {config.timeout_seconds}s ({config.timeout_seconds/60:.1f} min)")
    print()
    print("Cost Function:")
    print(f"  Trace length:      {config.trace_length_cost}")
    print(f"  Via count:         {config.via_cost}")
    print(f"  Layer changes:     {config.trace_layer_change_cost}")
    print()
    print("Via Settings:")
    print(f"  Minimize vias:     {config.minimize_vias}")
    print(f"  Max via count:     {config.max_via_count or 'unlimited'}")
    print(f"  Keepout margin:    {config.via_keepout_margin_mm} mm")
    print()
    print("Optimizations:")
    print(f"  Via optimization:  {config.via_optimization}")
    print(f"  Fanout:            {config.fanout_optimization}")
    print(f"  Post-route:        {config.post_route_optimization}")
    print(f"  Pull tight:        {config.trace_pull_tight}")
    print(f"  Corner opt:        {config.trace_corner_optimization}")
    print("=" * 60)


def main():
    """CLI for testing FreeRouting configurations"""
    import argparse

    parser = argparse.ArgumentParser(
        description="FreeRouting Configuration Generator"
    )
    parser.add_argument(
        "--profile",
        choices=[
            "fast",
            "production",
            "extreme",
            "minimal-vias",
            "2-layer",
            "4-layer"
        ],
        default="production",
        help="Configuration profile"
    )
    parser.add_argument(
        "--dsn",
        required=True,
        help="Input DSN file"
    )
    parser.add_argument(
        "--ses",
        required=True,
        help="Output SES file"
    )
    parser.add_argument(
        "--jar",
        default="freerouting.jar",
        help="Path to FreeRouting JAR"
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Print command without executing"
    )

    args = parser.parse_args()

    # Select profile
    profiles = {
        "fast": K1FreeRoutingProfile.fast_prototype,
        "production": K1FreeRoutingProfile.production_quality,
        "extreme": K1FreeRoutingProfile.extreme_quality,
        "minimal-vias": K1FreeRoutingProfile.minimal_vias,
        "2-layer": K1FreeRoutingProfile.two_layer_board,
        "4-layer": K1FreeRoutingProfile.four_layer_board,
    }

    config = profiles[args.profile]()

    # Generate command
    cmd = generate_freerouting_command(
        dsn_file=args.dsn,
        ses_file=args.ses,
        config=config,
        jar_path=args.jar
    )

    # Print configuration
    print_config_summary(config)
    print()
    print("Generated Command:")
    print(" ".join(cmd))
    print()

    if not args.print_only:
        print("Executing FreeRouting...")
        import subprocess
        result = subprocess.run(cmd)
        return result.returncode

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
