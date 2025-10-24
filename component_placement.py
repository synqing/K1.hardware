#!/usr/bin/env python3
"""
Elite PCB Designer Agent - Phase 2: Component Placement
Intelligent component placement with thermal zone management for K1 Lightwave board.

This module implements:
- Thermal zone definition and management
- Component clustering by function
- Multi-phase placement algorithm
- Spacing validation and DFM checks
- Routing accessibility optimization
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import math
import logging

# Try to import pcbnew (KiCad Python API), but fall back if unavailable
try:
    import pcbnew
    PCBNEW_AVAILABLE = True
except ImportError as e:
    PCBNEW_AVAILABLE = False
    logging.warning(f"KiCad Python API (pcbnew) not available: {e}")


@dataclass
class Point:
    """2D point in mm"""
    x: float
    y: float

    def distance_to(self, other: 'Point') -> float:
        """Calculate Euclidean distance to another point"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)


@dataclass
class ComponentInfo:
    """Component placement information"""
    reference: str
    footprint: str
    position: Optional[Point] = None
    rotation: float = 0.0  # degrees
    placed: bool = False
    thermal_zone: Optional[str] = None
    cluster: Optional[str] = None


@dataclass
class K1ThermalZone:
    """Represents a thermal zone on the K1 board"""
    name: str
    center: Point
    radius: float  # mm
    priority: int  # 1 = highest
    max_temp_rise: float  # °C
    power_dissipation: float  # mW
    components: List[ComponentInfo] = field(default_factory=list)

    def contains_point(self, point: Point) -> bool:
        """Check if point is within thermal zone"""
        return self.center.distance_to(point) <= self.radius

    def add_component(self, comp: ComponentInfo) -> None:
        """Add component to this thermal zone"""
        self.components.append(comp)
        comp.thermal_zone = self.name


class ComponentPlacement:
    """
    Intelligent component placement engine for K1 Lightwave board.

    Implements multi-phase placement algorithm:
    - Phase 2A: Fixed components (board edge connectors)
    - Phase 2B: Primary components (MCUs, power)
    - Phase 2C: Supporting components (passives)
    - Phase 2D: Remaining components
    """

    # K1 Board dimensions (mm)
    BOARD_WIDTH = 50.0
    BOARD_HEIGHT = 80.0
    EDGE_CLEARANCE = 5.0  # Safe border

    # Manufacturing constraints (JLCPCB)
    MIN_SPACING = 2.0  # mm between component edges
    MIN_EDGE_DISTANCE = 2.0  # mm from board edge

    def __init__(self, board_path: str, output_path: Optional[str] = None):
        """
        Initialize component placement engine.

        Args:
            board_path: Path to KiCad .kicad_pcb file
            output_path: Optional output path for modified board
        """
        self.board_path = Path(board_path)
        if output_path:
            output_path = Path(output_path)
            # If directory path provided, auto-correct to use board filename in directory
            if output_path.is_dir():
                self.output_path = output_path / self.board_path.name
                logging.info(f"Output is directory, using: {self.output_path}")
            else:
                self.output_path = output_path
        else:
            self.output_path = self.board_path
        self.pcbnew_available = PCBNEW_AVAILABLE

        # Load KiCad board
        self.board = None
        if PCBNEW_AVAILABLE:
            try:
                self.board = pcbnew.LoadBoard(str(self.board_path))
            except Exception as e:
                logging.warning(f"Failed to load board with pcbnew: {e}")
                self.pcbnew_available = False

        if not self.pcbnew_available:
            logging.info("Using fallback mode (simulation) for component placement")

        # Component tracking
        self.components: Dict[str, ComponentInfo] = {}
        self.thermal_zones: List[K1ThermalZone] = []
        self.clusters: Dict[str, List[ComponentInfo]] = {}

        # Placement results
        self.placement_results: Dict[str, Point] = {}
        self.violations: List[str] = []

        self._load_components()

    def _load_components(self) -> None:
        """Load all components from board"""
        if not self.pcbnew_available or self.board is None:
            # Fallback: Create dummy components for simulation
            logging.info("Generating simulated component inventory (52 components)")
            dummy_refs = [
                "C3", "C4", "C5", "C_BIN1", "C_BOUT1", "C_INA",
                "D1", "D2", "D3", "D4", "D_ESD_CC1", "D_ESD_CC2",
                "D_ESD_DM", "D_ESD_DP", "D_IDEAL",
                "F1", "F2", "F3", "F4", "F_USB",
                "J11", "J12",
                "R1", "R2", "R3", "R4", "R5", "R6", "R7",
                "RLED1", "RLED2", "RLED3", "RLED4",
                "R_BYPASS_CLK", "R_BYPASS_DATA", "R_FET_GATE",
                "R_LVT_CLK_IN", "R_LVT_CLK_OUT", "R_LVT_DATA_IN", "R_LVT_DATA_OUT",
                "R_PDM_CLK_SER", "R_READY_PD", "R_SPI_CS_PU",
                "R_SPI_MISO_SER", "R_SPI_MOSI_SER", "R_SPI_SCK_SER",
                "R_USB_DM_SER", "R_USB_DP_SER",
                "SW1", "U3", "U4", "U8"
            ]
            for ref in dummy_refs:
                self.components[ref] = ComponentInfo(
                    reference=ref,
                    footprint="Unknown",
                    position=Point(0.0, 0.0),
                    rotation=0.0,
                    placed=False
                )
            return

        # Real mode: Load from KiCad board
        for footprint in self.board.GetFootprints():
            ref = footprint.GetReference()
            fp_name = str(footprint.GetFPID().GetLibItemName())

            # Get current position
            pos = footprint.GetPosition()
            current_pos = Point(
                pcbnew.ToMM(pos.x),
                pcbnew.ToMM(pos.y)
            )

            comp = ComponentInfo(
                reference=ref,
                footprint=fp_name,
                position=current_pos,
                rotation=footprint.GetOrientation().AsDegrees(),
                placed=False
            )
            self.components[ref] = comp

    def define_thermal_zones(self) -> List[K1ThermalZone]:
        """
        Define K1 Lightwave thermal zones.

        Returns:
            List of thermal zones with priorities
        """
        self.thermal_zones = [
            K1ThermalZone(
                name="MCU-A Zone",
                center=Point(25.0, 60.0),  # Top-center
                radius=15.0,
                priority=1,
                max_temp_rise=40.0,
                power_dissipation=300.0
            ),
            K1ThermalZone(
                name="MCU-B Zone",
                center=Point(25.0, 20.0),  # Bottom-center
                radius=15.0,
                priority=1,
                max_temp_rise=50.0,
                power_dissipation=500.0
            ),
            K1ThermalZone(
                name="USB Input Zone",
                center=Point(15.0, 10.0),  # Bottom-left
                radius=10.0,
                priority=2,
                max_temp_rise=30.0,
                power_dissipation=100.0
            ),
            K1ThermalZone(
                name="LED Output Zone",
                center=Point(45.0, 40.0),  # Right-center
                radius=12.0,
                priority=2,
                max_temp_rise=35.0,
                power_dissipation=100.0
            )
        ]

        return self.thermal_zones

    def cluster_components(self) -> Dict[str, List[ComponentInfo]]:
        """
        Group components by functional clusters.

        Returns:
            Dictionary of cluster names to component lists
        """
        self.clusters = {
            'power': [],
            'decoupling': [],
            'usb_interface': [],
            'i2c': [],
            'i2s_mic': [],
            'led_output': [],
            'inter_mcu': [],
            'mcu_primary': [],
            'remaining': []
        }

        for ref, comp in self.components.items():
            # Power components
            if ref in ['J1', 'F_USB'] or ref.startswith('C_BIN') or ref.startswith('C_BOUT'):
                self.clusters['power'].append(comp)
                comp.cluster = 'power'

            # Decoupling capacitors
            elif ref in ['C3', 'C4', 'C5']:
                self.clusters['decoupling'].append(comp)
                comp.cluster = 'decoupling'

            # USB interface
            elif any(x in ref for x in ['D_ESD', 'R_USB', 'R_CC']):
                self.clusters['usb_interface'].append(comp)
                comp.cluster = 'usb_interface'

            # I2C connectors and pull-ups
            elif ref.startswith('J') and ref[1:2].isdigit() and int(ref[1:2]) in [3, 4, 5, 6]:
                self.clusters['i2c'].append(comp)
                comp.cluster = 'i2c'

            # I2S/Mic interface
            elif ref.startswith('J') and ref[1:2].isdigit() and int(ref[1:2]) in [7, 8, 9]:
                self.clusters['i2s_mic'].append(comp)
                comp.cluster = 'i2s_mic'
            elif ref.startswith('R_LVT') or ref == 'U8':
                self.clusters['i2s_mic'].append(comp)
                comp.cluster = 'i2s_mic'

            # LED output
            elif any(ref.startswith(x) for x in ['JLED', 'F', 'D', 'RLED']):
                if ref[1:].replace('LED', '').isdigit():
                    self.clusters['led_output'].append(comp)
                    comp.cluster = 'led_output'

            # Inter-MCU communication
            elif any(x in ref for x in ['R_SPI', 'R_READY']):
                self.clusters['inter_mcu'].append(comp)
                comp.cluster = 'inter_mcu'

            # Primary MCUs and associated ICs
            elif ref in ['U1', 'U3', 'U6', 'U7']:
                self.clusters['mcu_primary'].append(comp)
                comp.cluster = 'mcu_primary'

            # Everything else
            else:
                self.clusters['remaining'].append(comp)
                comp.cluster = 'remaining'

        return self.clusters

    def place_fixed_components(self) -> Dict[str, Point]:
        """
        Phase 2A: Place fixed components at board edges.

        Returns:
            Dictionary of reference to position
        """
        placements = {}

        # J1 (USB-C): Bottom-center
        if 'J1' in self.components:
            pos = Point(self.BOARD_WIDTH / 2, self.EDGE_CLEARANCE)
            self.components['J1'].position = pos
            self.components['J1'].placed = True
            placements['J1'] = pos

        # LED connectors (JLED1-4): Right edge, vertical spacing
        led_connectors = [f'JLED{i}' for i in range(1, 5)]
        start_y = 20.0
        spacing_y = 15.0

        for i, ref in enumerate(led_connectors):
            if ref in self.components:
                pos = Point(
                    self.BOARD_WIDTH - self.EDGE_CLEARANCE,
                    start_y + i * spacing_y
                )
                self.components[ref].position = pos
                self.components[ref].placed = True
                placements[ref] = pos

        # I2C connectors (J3-J6): Top edge
        i2c_connectors = [f'J{i}' for i in range(3, 7)]
        start_x = 10.0
        spacing_x = 10.0

        for i, ref in enumerate(i2c_connectors):
            if ref in self.components:
                pos = Point(
                    start_x + i * spacing_x,
                    self.BOARD_HEIGHT - self.EDGE_CLEARANCE
                )
                self.components[ref].position = pos
                self.components[ref].placed = True
                placements[ref] = pos

        # I2S connectors (J7-J9): Left edge
        i2s_connectors = [f'J{i}' for i in range(7, 10)]
        start_y = 40.0
        spacing_y = 12.0

        for i, ref in enumerate(i2s_connectors):
            if ref in self.components:
                pos = Point(
                    self.EDGE_CLEARANCE,
                    start_y + i * spacing_y
                )
                self.components[ref].position = pos
                self.components[ref].placed = True
                placements[ref] = pos

        return placements

    def place_primary_components(self) -> Dict[str, Point]:
        """
        Phase 2B: Place primary components in thermal zones.

        Returns:
            Dictionary of reference to position
        """
        placements = {}

        # MCU-A Zone: U1 + power components
        mcu_a_zone = next((z for z in self.thermal_zones if z.name == "MCU-A Zone"), None)
        if mcu_a_zone and 'U1' in self.components:
            # Place U1 at zone center
            self.components['U1'].position = Point(mcu_a_zone.center.x, mcu_a_zone.center.y)
            self.components['U1'].placed = True
            mcu_a_zone.add_component(self.components['U1'])
            placements['U1'] = self.components['U1'].position

            # Place C_BIN1, C_BOUT1 nearby
            offset = 8.0
            for i, ref in enumerate(['C_BIN1', 'C_BOUT1']):
                if ref in self.components:
                    angle = math.radians(i * 90)
                    pos = Point(
                        mcu_a_zone.center.x + offset * math.cos(angle),
                        mcu_a_zone.center.y + offset * math.sin(angle)
                    )
                    self.components[ref].position = pos
                    self.components[ref].placed = True
                    mcu_a_zone.add_component(self.components[ref])
                    placements[ref] = pos

        # MCU-B Zone: U3 + U6 + U7 + decoupling
        mcu_b_zone = next((z for z in self.thermal_zones if z.name == "MCU-B Zone"), None)
        if mcu_b_zone:
            # Place U3 (bare ESP32-S3) at zone center
            if 'U3' in self.components:
                self.components['U3'].position = Point(mcu_b_zone.center.x, mcu_b_zone.center.y)
                self.components['U3'].placed = True
                mcu_b_zone.add_component(self.components['U3'])
                placements['U3'] = self.components['U3'].position

            # Place U6, U7 adjacent
            offset = 10.0
            for i, ref in enumerate(['U6', 'U7']):
                if ref in self.components:
                    pos = Point(
                        mcu_b_zone.center.x + (i - 0.5) * offset,
                        mcu_b_zone.center.y - offset
                    )
                    self.components[ref].position = pos
                    self.components[ref].placed = True
                    mcu_b_zone.add_component(self.components[ref])
                    placements[ref] = pos

            # Distribute decoupling capacitors around zone
            decoupling = self.clusters.get('decoupling', [])
            for i, comp in enumerate(decoupling):
                if not comp.placed:
                    angle = math.radians(i * (360 / len(decoupling)))
                    radius = 8.0
                    pos = Point(
                        mcu_b_zone.center.x + radius * math.cos(angle),
                        mcu_b_zone.center.y + radius * math.sin(angle)
                    )
                    comp.position = pos
                    comp.placed = True
                    mcu_b_zone.add_component(comp)
                    placements[comp.reference] = pos

        # USB Zone: F_USB near J1
        usb_zone = next((z for z in self.thermal_zones if z.name == "USB Input Zone"), None)
        if usb_zone and 'F_USB' in self.components and 'J1' in self.components:
            j1_pos = self.components['J1'].position
            pos = Point(j1_pos.x + 5.0, j1_pos.y + 3.0)
            self.components['F_USB'].position = pos
            self.components['F_USB'].placed = True
            usb_zone.add_component(self.components['F_USB'])
            placements['F_USB'] = pos

        return placements

    def place_supporting_components(self) -> Dict[str, Point]:
        """
        Phase 2C: Place supporting components along signal paths.

        Returns:
            Dictionary of reference to position
        """
        placements = {}

        # ESD diodes: 5mm from J1
        if 'J1' in self.components:
            j1_pos = self.components['J1'].position
            esd_refs = ['D_ESD_DP', 'D_ESD_DM']

            for i, ref in enumerate(esd_refs):
                if ref in self.components:
                    pos = Point(
                        j1_pos.x + (i - 0.5) * 6.0,
                        j1_pos.y + 7.0
                    )
                    self.components[ref].position = pos
                    self.components[ref].placed = True
                    placements[ref] = pos

        # USB resistors near J1
        usb_resistors = [r for r in self.components.values()
                        if 'R_USB' in r.reference or 'R_CC' in r.reference]

        if 'J1' in self.components:
            j1_pos = self.components['J1'].position
            for i, comp in enumerate(usb_resistors):
                if not comp.placed:
                    pos = Point(
                        j1_pos.x + (i - 1) * 3.0,
                        j1_pos.y + 10.0
                    )
                    comp.position = pos
                    comp.placed = True
                    placements[comp.reference] = pos

        # LED output components: near LED connectors
        led_zone = next((z for z in self.thermal_zones if z.name == "LED Output Zone"), None)
        if led_zone:
            led_comps = [c for c in self.clusters.get('led_output', []) if not c.placed]

            for i, comp in enumerate(led_comps):
                row = i // 4
                col = i % 4
                pos = Point(
                    led_zone.center.x - 8.0 - col * 3.0,
                    led_zone.center.y - 15.0 + row * 6.0
                )
                comp.position = pos
                comp.placed = True
                led_zone.add_component(comp)
                placements[comp.reference] = pos

        return placements

    def place_remaining_components(self) -> Dict[str, Point]:
        """
        Phase 2D: Place remaining components in available space.

        Returns:
            Dictionary of reference to position
        """
        placements = {}

        # Find all unplaced components
        unplaced = [c for c in self.components.values() if not c.placed]

        # Grid placement in safe area
        grid_x_start = self.EDGE_CLEARANCE + 2.0
        grid_y_start = self.EDGE_CLEARANCE + 2.0
        grid_spacing = 4.0

        cols = int((self.BOARD_WIDTH - 2 * grid_x_start) / grid_spacing)

        for i, comp in enumerate(unplaced):
            row = i // cols
            col = i % cols

            pos = Point(
                grid_x_start + col * grid_spacing,
                grid_y_start + row * grid_spacing
            )

            # Verify position is in safe area
            if (pos.x < self.BOARD_WIDTH - self.EDGE_CLEARANCE and
                pos.y < self.BOARD_HEIGHT - self.EDGE_CLEARANCE):
                comp.position = pos
                comp.placed = True
                placements[comp.reference] = pos

        return placements

    def verify_spacing(self) -> Tuple[bool, List[str]]:
        """
        Validate all spacing constraints.

        Returns:
            Tuple of (is_valid, list of violations)
        """
        violations = []

        components_list = list(self.components.values())

        # Check inter-component spacing
        for i, comp1 in enumerate(components_list):
            if not comp1.position:
                continue

            # Check edge clearance
            if (comp1.position.x < self.MIN_EDGE_DISTANCE or
                comp1.position.x > self.BOARD_WIDTH - self.MIN_EDGE_DISTANCE or
                comp1.position.y < self.MIN_EDGE_DISTANCE or
                comp1.position.y > self.BOARD_HEIGHT - self.MIN_EDGE_DISTANCE):
                violations.append(
                    f"{comp1.reference}: Too close to board edge "
                    f"(pos: {comp1.position.x:.2f}, {comp1.position.y:.2f})"
                )

            # Check spacing to other components
            for comp2 in components_list[i+1:]:
                if not comp2.position:
                    continue

                distance = comp1.position.distance_to(comp2.position)
                if distance < self.MIN_SPACING:
                    violations.append(
                        f"{comp1.reference} <-> {comp2.reference}: "
                        f"Spacing violation ({distance:.2f}mm < {self.MIN_SPACING}mm)"
                    )

        self.violations = violations
        return len(violations) == 0, violations

    def optimize_routing_accessibility(self) -> Dict[str, float]:
        """
        Calculate routing accessibility score for each component.

        Returns:
            Dictionary of reference to accessibility score (0-1)
        """
        scores = {}

        for ref, comp in self.components.items():
            if not comp.position:
                scores[ref] = 0.0
                continue

            # Calculate based on:
            # 1. Distance to nearest edge (closer = better access)
            # 2. Number of nearby components (fewer = better)
            # 3. Thermal zone priority (higher priority = more critical)

            edge_distances = [
                comp.position.x,
                self.BOARD_WIDTH - comp.position.x,
                comp.position.y,
                self.BOARD_HEIGHT - comp.position.y
            ]
            min_edge_dist = min(edge_distances)
            edge_score = min(min_edge_dist / 10.0, 1.0)

            # Count nearby components (within 10mm)
            nearby = sum(1 for c in self.components.values()
                        if c.position and c.reference != ref and
                        comp.position.distance_to(c.position) < 10.0)
            density_score = max(0.0, 1.0 - nearby / 10.0)

            # Combined score
            scores[ref] = (edge_score * 0.4 + density_score * 0.6)

        return scores

    def generate_placement_report(self) -> str:
        """
        Generate comprehensive placement report.

        Returns:
            Multi-line report string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("K1 LIGHTWAVE - COMPONENT PLACEMENT REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Board info
        lines.append(f"Board Dimensions: {self.BOARD_WIDTH}mm × {self.BOARD_HEIGHT}mm")
        lines.append(f"Total Components: {len(self.components)}")
        lines.append(f"Placed Components: {sum(1 for c in self.components.values() if c.placed)}")
        lines.append("")

        # Thermal zones
        lines.append("THERMAL ZONES:")
        lines.append("-" * 80)
        for zone in self.thermal_zones:
            lines.append(f"  {zone.name}:")
            lines.append(f"    Center: ({zone.center.x:.1f}, {zone.center.y:.1f})mm")
            lines.append(f"    Radius: {zone.radius:.1f}mm")
            lines.append(f"    Power: {zone.power_dissipation:.0f}mW")
            lines.append(f"    Max Temp Rise: {zone.max_temp_rise:.0f}°C")
            lines.append(f"    Components: {len(zone.components)}")
            for comp in zone.components:
                lines.append(f"      - {comp.reference}")
            lines.append("")

        # Component clusters
        lines.append("COMPONENT CLUSTERS:")
        lines.append("-" * 80)
        for cluster_name, comps in self.clusters.items():
            if comps:
                lines.append(f"  {cluster_name}: {len(comps)} components")
                refs = ', '.join(c.reference for c in comps[:10])
                if len(comps) > 10:
                    refs += f", ... (+{len(comps) - 10} more)"
                lines.append(f"    {refs}")
        lines.append("")

        # Spacing validation
        is_valid, violations = self.verify_spacing()
        lines.append("SPACING VALIDATION:")
        lines.append("-" * 80)
        if is_valid:
            lines.append("  ✓ All spacing constraints satisfied")
        else:
            lines.append(f"  ✗ {len(violations)} violations found:")
            for violation in violations[:20]:  # Limit output
                lines.append(f"    - {violation}")
            if len(violations) > 20:
                lines.append(f"    ... (+{len(violations) - 20} more violations)")
        lines.append("")

        # Routing accessibility
        scores = self.optimize_routing_accessibility()
        avg_score = sum(scores.values()) / len(scores) if scores else 0.0
        lines.append("ROUTING ACCESSIBILITY:")
        lines.append("-" * 80)
        lines.append(f"  Average Score: {avg_score:.2f}/1.00")

        # Highlight low accessibility components
        low_access = [(ref, score) for ref, score in scores.items() if score < 0.3]
        if low_access:
            lines.append(f"  Components with low accessibility ({len(low_access)}):")
            for ref, score in sorted(low_access, key=lambda x: x[1])[:10]:
                lines.append(f"    - {ref}: {score:.2f}")
        lines.append("")

        # Summary
        lines.append("PLACEMENT SUMMARY:")
        lines.append("-" * 80)
        lines.append(f"  ✓ Fixed components placed: {len([c for c in self.clusters.get('power', []) if c.placed])}")
        lines.append(f"  ✓ Primary components placed: {len([c for c in self.clusters.get('mcu_primary', []) if c.placed])}")
        lines.append(f"  ✓ Supporting components placed: {sum(1 for c in self.components.values() if c.placed and c.cluster in ['usb_interface', 'led_output'])}")
        lines.append(f"  ✓ Remaining components placed: {len([c for c in self.clusters.get('remaining', []) if c.placed])}")
        lines.append("")
        lines.append(f"  Status: {'PASS' if is_valid else 'FAIL - Spacing violations detected'}")
        lines.append("=" * 80)

        return '\n'.join(lines)

    def generate_ascii_visualization(self) -> str:
        """
        Generate ASCII art visualization of component placement.

        Returns:
            ASCII diagram string
        """
        # Create grid (2mm per character)
        scale = 2.0  # mm per character
        width = int(self.BOARD_WIDTH / scale)
        height = int(self.BOARD_HEIGHT / scale)

        grid = [[' ' for _ in range(width)] for _ in range(height)]

        # Draw board outline
        for x in range(width):
            grid[0][x] = '-'
            grid[height-1][x] = '-'
        for y in range(height):
            grid[y][0] = '|'
            grid[y][width-1] = '|'

        # Draw thermal zones
        for zone in self.thermal_zones:
            cx = int(zone.center.x / scale)
            cy = int(zone.center.y / scale)
            r = int(zone.radius / scale)

            # Draw zone circle (approximate)
            for dy in range(-r, r+1):
                for dx in range(-r, r+1):
                    if dx*dx + dy*dy <= r*r:
                        x, y = cx + dx, cy + dy
                        if 0 <= x < width and 0 <= y < height:
                            if grid[y][x] == ' ':
                                grid[y][x] = '·'

        # Draw components
        for comp in self.components.values():
            if comp.position:
                x = int(comp.position.x / scale)
                y = int(comp.position.y / scale)

                if 0 <= x < width and 0 <= y < height:
                    # Use different symbols for different component types
                    if comp.reference.startswith('U'):
                        grid[y][x] = 'U'
                    elif comp.reference.startswith('J'):
                        grid[y][x] = 'J'
                    elif comp.reference.startswith('C'):
                        grid[y][x] = 'C'
                    elif comp.reference.startswith('R'):
                        grid[y][x] = 'R'
                    elif comp.reference.startswith('D'):
                        grid[y][x] = 'D'
                    elif comp.reference.startswith('F'):
                        grid[y][x] = 'F'
                    else:
                        grid[y][x] = '*'

        # Convert to string
        lines = [''.join(row) for row in grid]

        # Add legend
        legend = [
            "",
            "Legend:",
            "  U = IC/Module    J = Connector",
            "  C = Capacitor    R = Resistor",
            "  D = Diode        F = Fuse",
            "  · = Thermal Zone * = Other",
            f"  Scale: {scale}mm per character"
        ]

        return '\n'.join(lines + legend)

    def apply_placement_to_board(self) -> None:
        """Apply calculated placements to KiCad board"""
        if not self.pcbnew_available or self.board is None:
            logging.info("Skipping board update (pcbnew not available)")
            return

        for footprint in self.board.GetFootprints():
            ref = footprint.GetReference()
            if ref in self.components and self.components[ref].position:
                pos = self.components[ref].position
                new_pos = pcbnew.VECTOR2I(
                    pcbnew.FromMM(pos.x),
                    pcbnew.FromMM(pos.y)
                )
                footprint.SetPosition(new_pos)

                # Set rotation if needed
                if self.components[ref].rotation != 0:
                    footprint.SetOrientation(
                        pcbnew.EDA_ANGLE(self.components[ref].rotation, pcbnew.DEGREES_T)
                    )

    def execute(self) -> bool:
        """
        Execute full Phase 2 placement pipeline.

        Returns:
            True if successful, False otherwise
        """
        try:
            print("Starting Phase 2: Component Placement")
            print("-" * 80)

            # Step 1: Define thermal zones
            print("\n[1/7] Defining thermal zones...")
            self.define_thermal_zones()
            print(f"      Created {len(self.thermal_zones)} thermal zones")

            # Step 2: Cluster components
            print("\n[2/7] Clustering components by function...")
            self.cluster_components()
            total_clustered = sum(len(comps) for comps in self.clusters.values())
            print(f"      Clustered {total_clustered} components into {len(self.clusters)} groups")

            # Step 3: Place fixed components
            print("\n[3/7] Placing fixed components (board edge)...")
            fixed = self.place_fixed_components()
            print(f"      Placed {len(fixed)} fixed components")

            # Step 4: Place primary components
            print("\n[4/7] Placing primary components (thermal zones)...")
            primary = self.place_primary_components()
            print(f"      Placed {len(primary)} primary components")

            # Step 5: Place supporting components
            print("\n[5/7] Placing supporting components...")
            supporting = self.place_supporting_components()
            print(f"      Placed {len(supporting)} supporting components")

            # Step 6: Place remaining components
            print("\n[6/7] Placing remaining components...")
            remaining = self.place_remaining_components()
            print(f"      Placed {len(remaining)} remaining components")

            # Step 7: Validate and optimize
            print("\n[7/7] Validating spacing and optimizing routing...")
            is_valid, violations = self.verify_spacing()
            scores = self.optimize_routing_accessibility()
            avg_score = sum(scores.values()) / len(scores) if scores else 0.0

            print(f"      Spacing validation: {'PASS' if is_valid else 'FAIL'}")
            print(f"      Routing accessibility: {avg_score:.2f}/1.00")

            # Apply to board
            print("\n[8/8] Applying placement to KiCad board...")
            self.apply_placement_to_board()
            if self.pcbnew_available and self.board is not None:
                try:
                    self.board.Save(str(self.output_path))

                    # VERIFY FILE ACTUALLY CREATED
                    if not Path(self.output_path).exists():
                        raise RuntimeError(
                            f"board.Save() failed: no file created at {self.output_path}. "
                            f"Ensure path is a file (not directory) and disk has space."
                        )

                    file_size = Path(self.output_path).stat().st_size
                    if file_size < 2000:
                        raise RuntimeError(
                            f"board.Save() produced empty file ({file_size} bytes). "
                            f"Board modifications may not have been saved."
                        )

                    print(f"      ✅ Board saved: {self.output_path} ({file_size} bytes)")

                except Exception as e:
                    print(f"      ❌ FAILED to save board: {e}")
                    raise
            else:
                print(f"      Board update skipped (pcbnew not available)")

            print("\n" + "=" * 80)
            print("Phase 2 Complete!")
            print("=" * 80)

            return is_valid

        except Exception as e:
            print(f"\nERROR: Placement failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point for command-line usage"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python component_placement.py <board.kicad_pcb> [output.kicad_pcb]")
        sys.exit(1)

    board_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    # Create placement engine
    placer = ComponentPlacement(board_path, output_path)

    # Execute placement
    success = placer.execute()

    # Generate reports
    print("\n\n")
    print(placer.generate_placement_report())
    print("\n\n")
    print("BOARD VISUALIZATION:")
    print(placer.generate_ascii_visualization())

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
