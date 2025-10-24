"""
Elite PCB Designer - Component Placement Optimizer

Intelligently positions components on PCB considering:
- Signal integrity (grouping related signals)
- Thermal zones (heat dissipation)
- Power distribution (minimize traces)
- Manufacturing constraints (testability, assembly)
- EMI/EMC (shield sensitive analog)
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum
import math


class ComponentFamily(Enum):
    """Component functional groups"""
    POWER = "Power Management"
    AUDIO_DSP = "Audio/DSP (MCU-A)"
    LED_CONTROL = "LED Control (MCU-B)"
    USB = "USB Interface"
    ANALOG = "Analog/Sensing"
    PROTECTION = "Protection/ESD"
    DECOUPLING = "Decoupling/Bypass"


class ThermalZone(Enum):
    """Thermal regions on PCB"""
    HEAT_SOURCE = "High heat dissipation zone"
    MODERATE = "Moderate heat zone"
    COOL = "Cool zone (passive components)"
    PROTECTED = "Temperature-sensitive zone"


@dataclass
class ComponentInfo:
    """Component placement requirements"""
    reference: str
    family: ComponentFamily
    footprint: str
    power_mw: float  # Power dissipation in mW
    thermal_zone: ThermalZone
    critical_nets: List[str]  # High-speed signals
    placement_constraints: List[str]  # Mounting, orientation, spacing


@dataclass
class PlacementZone:
    """Defined region on PCB"""
    name: str
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    families: List[ComponentFamily]  # Which families belong here
    priority: int  # Lower = higher priority
    thermal_target: ThermalZone


class K1_BoardDefinition:
    """K1 Lightwave board physical constraints"""

    # K1 Physical dimensions (mm)
    BOARD_WIDTH = 100
    BOARD_HEIGHT = 70
    BOARD_AREA = BOARD_WIDTH * BOARD_HEIGHT

    # Standard component spacing
    MIN_TRACE_WIDTH = 0.25  # 0.25mm
    MIN_CLEARANCE = 0.25
    MIN_VIA_SPACING = 0.5
    BGA_ESCAPE_DISTANCE = 1.5

    # Thermal parameters
    MAX_JUNCTION_TEMP = 85  # Celsius
    AMBIENT_TEMP = 25
    MAX_COPPER_TEMP = 60  # For reliability

    # Define functional zones for K1
    ZONES = [
        # Power input zone - near USB connector
        PlacementZone(
            name="USB Input & Power",
            x_min=0, y_min=0, x_max=25, y_max=35,
            families=[ComponentFamily.USB, ComponentFamily.PROTECTION, ComponentFamily.POWER],
            priority=1,
            thermal_target=ThermalZone.COOL
        ),

        # Audio DSP MCU (COM-A) - needs isolation from LED control
        PlacementZone(
            name="Audio/DSP Zone (COM-A)",
            x_min=60, y_min=0, x_max=100, y_max=35,
            families=[ComponentFamily.AUDIO_DSP, ComponentFamily.ANALOG],
            priority=2,
            thermal_target=ThermalZone.COOL
        ),

        # LED Control MCU (COM-B) - with LED output drivers
        PlacementZone(
            name="LED Control Zone (COM-B)",
            x_min=0, y_min=35, x_max=50, y_max=70,
            families=[ComponentFamily.LED_CONTROL],
            priority=2,
            thermal_target=ThermalZone.MODERATE
        ),

        # LED output drivers & power management
        PlacementZone(
            name="LED Drivers & Output",
            x_min=50, y_min=35, x_max=100, y_max=70,
            families=[ComponentFamily.LED_CONTROL, ComponentFamily.DECOUPLING],
            priority=3,
            thermal_target=ThermalZone.MODERATE
        ),

        # Decoupling capacitors distributed across board
        PlacementZone(
            name="Decoupling Network",
            x_min=0, y_min=0, x_max=100, y_max=70,
            families=[ComponentFamily.DECOUPLING],
            priority=0,  # Highest priority - can be placed anywhere
            thermal_target=ThermalZone.COOL
        ),
    ]

    @staticmethod
    def get_zone_for_component(component: ComponentInfo) -> PlacementZone:
        """Find best zone for component"""
        for zone in K1_BoardDefinition.ZONES:
            if component.family in zone.families:
                return zone
        # Fallback to decoupling zone
        return K1_BoardDefinition.ZONES[-1]


class PlacementOptimizer:
    """Optimize component placement for K1 board"""

    def __init__(self):
        self.board = K1_BoardDefinition()
        self.placements: Dict[str, Tuple[float, float]] = {}  # ref -> (x, y)
        self.components: Dict[str, ComponentInfo] = {}
        self.placement_quality = 0.0

    def add_component(self, component: ComponentInfo):
        """Register component for placement"""
        self.components[component.reference] = component

    def optimize_placement(self) -> Dict[str, Tuple[float, float]]:
        """
        Generate optimal placement for all components

        Returns:
            {reference: (x_mm, y_mm)}
        """
        # Step 1: Group components by functional family
        families = self._group_by_family()

        # Step 2: Assign zones based on functionality
        zone_assignments = self._assign_zones(families)

        # Step 3: Place components within zones
        for zone, components in zone_assignments.items():
            self._place_in_zone(zone, components)

        # Step 4: Distribute decoupling capacitors
        self._distribute_decoupling()

        # Step 5: Validate and score placement
        self._validate_placement()

        return self.placements

    def _group_by_family(self) -> Dict[ComponentFamily, List[ComponentInfo]]:
        """Group components by functional family"""
        families = {}
        for comp in self.components.values():
            if comp.family not in families:
                families[comp.family] = []
            families[comp.family].append(comp)
        return families

    def _assign_zones(self, families: Dict[ComponentFamily, List[ComponentInfo]]
                      ) -> Dict[PlacementZone, List[ComponentInfo]]:
        """Assign component families to zones"""
        zone_assignments = {zone: [] for zone in self.board.ZONES}

        for family, components in families.items():
            # Find best zone for this family
            zone = self._find_best_zone_for_family(family)
            zone_assignments[zone].extend(components)

        return zone_assignments

    def _find_best_zone_for_family(self, family: ComponentFamily) -> PlacementZone:
        """Find zone with highest priority for family"""
        matching_zones = [z for z in self.board.ZONES if family in z.families]
        if not matching_zones:
            return self.board.ZONES[-1]  # Fallback to decoupling zone
        return min(matching_zones, key=lambda z: z.priority)

    def _place_in_zone(self, zone: PlacementZone, components: List[ComponentInfo]):
        """Place components within a zone using grid-based placement"""
        if not components:
            return

        zone_width = zone.x_max - zone.x_min
        zone_height = zone.y_max - zone.y_min

        # Calculate grid based on component count
        cols = max(1, int(math.sqrt(len(components))))
        rows = max(1, (len(components) + cols - 1) // cols)

        x_step = zone_width / (cols + 1)
        y_step = zone_height / (rows + 1)

        # Sort by power dissipation (hottest first)
        sorted_comps = sorted(components, key=lambda c: c.power_mw, reverse=True)

        for idx, comp in enumerate(sorted_comps):
            col = idx % cols
            row = idx // cols

            x = zone.x_min + (col + 1) * x_step
            y = zone.y_min + (row + 1) * y_step

            self.placements[comp.reference] = (x, y)

    def _distribute_decoupling(self):
        """Distribute decoupling capacitors near power consumers"""
        decoupling = [c for c in self.components.values()
                     if c.family == ComponentFamily.DECOUPLING]

        if not decoupling:
            return

        # Get power consumers
        consumers = [c for c in self.components.values()
                    if c.family in [ComponentFamily.AUDIO_DSP, ComponentFamily.LED_CONTROL]
                    and c.reference in self.placements]

        if not consumers:
            return

        # Place decoupling caps near each consumer
        for idx, decap in enumerate(decoupling):
            consumer = consumers[idx % len(consumers)]
            cx, cy = self.placements[consumer.reference]

            # Place offset from consumer
            offset = 5 + (idx // len(consumers)) * 3
            x = cx + offset
            y = cy + offset

            # Constrain to board
            x = max(self.board.ZONES[0].x_min, min(self.board.ZONES[-1].x_max, x))
            y = max(self.board.ZONES[0].y_min, min(self.board.ZONES[-1].y_max, y))

            self.placements[decap.reference] = (x, y)

    def _validate_placement(self):
        """Validate placement and calculate quality score"""
        violations = 0
        total_checks = 0

        # Check for overlaps (simplified)
        for i, (ref1, pos1) in enumerate(list(self.placements.items())):
            for ref2, pos2 in list(self.placements.items())[i+1:]:
                total_checks += 1
                distance = math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
                # Minimum distance is roughly component size
                if distance < 2.0:  # 2mm minimum
                    violations += 1

        # Check all components within board
        for ref, (x, y) in self.placements.items():
            total_checks += 1
            if not (0 <= x <= self.board.BOARD_WIDTH and 0 <= y <= self.board.BOARD_HEIGHT):
                violations += 1

        self.placement_quality = max(0, 100 * (1 - violations / max(1, total_checks)))

    def get_placement_report(self) -> str:
        """Generate human-readable placement report"""
        lines = [
            "=" * 70,
            "COMPONENT PLACEMENT REPORT - K1 Lightwave",
            "=" * 70,
            f"Total components placed: {len(self.placements)}",
            f"Board size: {self.board.BOARD_WIDTH}mm × {self.board.BOARD_HEIGHT}mm",
            f"Placement quality score: {self.placement_quality:.1f}%",
            "",
            "PLACEMENT BY ZONE:",
            "-" * 70,
        ]

        # Group by zone
        zone_comps = {zone.name: [] for zone in self.board.ZONES}
        for comp in self.components.values():
            zone = self.board.get_zone_for_component(comp)
            if comp.reference in self.placements:
                zone_comps[zone.name].append((comp.reference, comp.family.value))

        for zone_name, comps in zone_comps.items():
            if comps:
                lines.append(f"\n{zone_name}:")
                for ref, family in sorted(comps):
                    x, y = self.placements[ref]
                    lines.append(f"  {ref:15s} ({family:20s}) @ ({x:6.2f}, {y:6.2f})")

        return "\n".join(lines)

    def export_kicad_placement(self, output_file: str):
        """Export placement as KiCad python format for automated layout"""
        lines = [
            "# Auto-generated K1 Lightwave component placement",
            "# Generated by Elite PCB Designer",
            "# Use with KiCad python scripting API",
            "",
            "placements = {",
        ]

        for ref, (x, y) in sorted(self.placements.items()):
            # KiCad uses 0.1mm units internally
            x_kicad = int(x * 10)  # Convert mm to 0.1mm
            y_kicad = int(y * 10)
            lines.append(f'    "{ref}": ({x_kicad}, {y_kicad}),  # {x:.2f}mm, {y:.2f}mm')

        lines.append("}")

        with open(output_file, 'w') as f:
            f.write("\n".join(lines))
