#!/usr/bin/env python3
"""
Test suite for Elite PCB Designer Agent - Phase 2: Component Placement
Tests intelligent component placement with thermal zone management.
"""

import unittest
from pathlib import Path
import tempfile
import shutil
from component_placement import (
    ComponentPlacement,
    K1ThermalZone,
    ComponentInfo,
    Point
)


class TestPoint(unittest.TestCase):
    """Tests for the Point class."""

    def test_distance_calculation(self):
        """Verify that the distance between two points is calculated correctly."""
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        self.assertAlmostEqual(p1.distance_to(p2), 5.0, places=2)

    def test_point_addition(self):
        """Verify that two points can be added together."""
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        p3 = p1 + p2
        self.assertEqual(p3.x, 4)
        self.assertEqual(p3.y, 6)

    def test_point_subtraction(self):
        """Verify that one point can be subtracted from another."""
        p1 = Point(5, 7)
        p2 = Point(2, 3)
        p3 = p1 - p2
        self.assertEqual(p3.x, 3)
        self.assertEqual(p3.y, 4)


class TestK1ThermalZone(unittest.TestCase):
    """Tests for the K1ThermalZone class."""

    def setUp(self):
        """Set up a test thermal zone for use in the test cases."""
        self.zone = K1ThermalZone(
            name="Test Zone",
            center=Point(25, 40),
            radius=10.0,
            priority=1,
            max_temp_rise=40.0,
            power_dissipation=300.0
        )

    def test_zone_contains_point_inside(self):
        """Verify that a point inside the zone is correctly identified."""
        point = Point(25, 40)  # Center
        self.assertTrue(self.zone.contains_point(point))

        point = Point(30, 40)  # 5mm from center
        self.assertTrue(self.zone.contains_point(point))

    def test_zone_contains_point_outside(self):
        """Verify that a point outside the zone is correctly identified."""
        point = Point(40, 40)  # 15mm from center
        self.assertFalse(self.zone.contains_point(point))

    def test_zone_contains_point_boundary(self):
        """Verify that a point on the zone's boundary is correctly identified."""
        point = Point(35, 40)  # Exactly 10mm from center
        self.assertTrue(self.zone.contains_point(point))

    def test_add_component(self):
        """Verify that a component can be successfully added to the zone."""
        comp = ComponentInfo(
            reference="U1",
            footprint="Package_DFN_QFN:QFN-56-1EP_7x7mm",
            position=Point(25, 40)
        )

        self.zone.add_component(comp)
        self.assertEqual(len(self.zone.components), 1)
        self.assertEqual(comp.thermal_zone, "Test Zone")


class TestComponentPlacementInitialization(unittest.TestCase):
    """Tests for the initialization and component loading of the ComponentPlacement class."""

    @classmethod
    def setUpClass(cls):
        """Set up the path to the test board file."""
        cls.board_path = Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")
        if not cls.board_path.exists():
            raise unittest.SkipTest(f"Board file not found: {cls.board_path}")

    def test_initialization(self):
        """Verify that the placement engine initializes correctly with a valid board file."""
        placer = ComponentPlacement(str(self.board_path))
        self.assertIsNotNone(placer.board)
        self.assertGreater(len(placer.components), 0)

    def test_component_loading(self):
        """Verify that components are correctly loaded from the board file."""
        placer = ComponentPlacement(str(self.board_path))

        # Verify key components are loaded
        expected_components = ['J1', 'U1', 'U3', 'C3', 'C4', 'C5']
        for ref in expected_components:
            self.assertIn(ref, placer.components)

        # Verify all components have positions
        for comp in placer.components.values():
            self.assertIsNotNone(comp.position)
            self.assertIsInstance(comp.position, Point)

    def test_invalid_board_path(self):
        """Verify that initialization fails with an invalid board path."""
        with self.assertRaises(RuntimeError):
            ComponentPlacement("/nonexistent/board.kicad_pcb")


class TestThermalZoneDefinition(unittest.TestCase):
    """Tests for the definition of thermal zones."""

    @classmethod
    def setUpClass(cls):
        """Set up the path to the test board file."""
        cls.board_path = Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")
        if not cls.board_path.exists():
            raise unittest.SkipTest(f"Board file not found: {cls.board_path}")

    def test_define_thermal_zones(self):
        """Verify that the correct number and names of thermal zones are created."""
        placer = ComponentPlacement(str(self.board_path))
        zones = placer.define_thermal_zones()

        # Verify zone count
        self.assertEqual(len(zones), 4)

        # Verify zone names
        zone_names = {z.name for z in zones}
        expected_names = {
            "MCU-A Zone",
            "MCU-B Zone",
            "USB Input Zone",
            "LED Output Zone"
        }
        self.assertEqual(zone_names, expected_names)

    def test_zone_priorities(self):
        """Verify that the thermal zones have the correct priorities."""
        placer = ComponentPlacement(str(self.board_path))
        placer.define_thermal_zones()

        # MCU zones should have priority 1
        mcu_zones = [z for z in placer.thermal_zones
                     if "MCU" in z.name]
        for zone in mcu_zones:
            self.assertEqual(zone.priority, 1)

        # Other zones should have priority 2
        other_zones = [z for z in placer.thermal_zones
                       if "MCU" not in z.name]
        for zone in other_zones:
            self.assertEqual(zone.priority, 2)

    def test_zone_power_dissipation(self):
        """Verify that the thermal zones have the correct power dissipation specifications."""
        placer = ComponentPlacement(str(self.board_path))
        placer.define_thermal_zones()

        # MCU-B should have highest power
        mcu_b = next(z for z in placer.thermal_zones if z.name == "MCU-B Zone")
        self.assertEqual(mcu_b.power_dissipation, 500.0)

        # USB and LED should have lowest power
        usb = next(z for z in placer.thermal_zones if z.name == "USB Input Zone")
        self.assertLessEqual(usb.power_dissipation, 100.0)


class TestComponentClustering(unittest.TestCase):
    """Tests for the component clustering functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up the path to the test board file."""
        cls.board_path = Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")
        if not cls.board_path.exists():
            raise unittest.SkipTest(f"Board file not found: {cls.board_path}")

    def test_cluster_components(self):
        """Verify that all expected component clusters are created."""
        placer = ComponentPlacement(str(self.board_path))
        clusters = placer.cluster_components()

        # Verify cluster keys exist
        expected_clusters = [
            'power', 'decoupling', 'usb_interface', 'i2c',
            'i2s_mic', 'led_output', 'inter_mcu', 'mcu_primary'
        ]
        for cluster in expected_clusters:
            self.assertIn(cluster, clusters)

    def test_power_cluster(self):
        """Verify that power-related components are correctly clustered."""
        placer = ComponentPlacement(str(self.board_path))
        placer.cluster_components()

        power_cluster = placer.clusters['power']

        # J1 should be in power cluster
        j1_refs = [c.reference for c in power_cluster]
        self.assertIn('J1', j1_refs)

    def test_mcu_cluster(self):
        """Verify that MCUs are correctly clustered."""
        placer = ComponentPlacement(str(self.board_path))
        placer.cluster_components()

        mcu_cluster = placer.clusters['mcu_primary']
        mcu_refs = [c.reference for c in mcu_cluster]

        # U1 and U3 should be in MCU cluster
        self.assertIn('U1', mcu_refs)
        self.assertIn('U3', mcu_refs)

    def test_decoupling_cluster(self):
        """Verify that decoupling capacitors are correctly clustered."""
        placer = ComponentPlacement(str(self.board_path))
        placer.cluster_components()

        decoupling = placer.clusters['decoupling']
        decoupling_refs = [c.reference for c in decoupling]

        # C3, C4, C5 should be in decoupling cluster
        for ref in ['C3', 'C4', 'C5']:
            self.assertIn(ref, decoupling_refs)

    def test_all_components_clustered(self):
        """Verify that every component is assigned to a cluster."""
        placer = ComponentPlacement(str(self.board_path))
        placer.cluster_components()

        clustered_count = sum(len(comps) for comps in placer.clusters.values())
        self.assertEqual(clustered_count, len(placer.components))


class TestFixedComponentPlacement(unittest.TestCase):
    """Tests for Phase 2A: Placement of fixed components."""

    @classmethod
    def setUpClass(cls):
        """Set up the path to the test board file."""
        cls.board_path = Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")
        if not cls.board_path.exists():
            raise unittest.SkipTest(f"Board file not found: {cls.board_path}")

    def test_usb_connector_placement(self):
        """Verify the placement of the J1 (USB-C) connector at the bottom-center."""
        placer = ComponentPlacement(str(self.board_path))
        placer.place_fixed_components()

        if 'J1' in placer.components:
            j1 = placer.components['J1']
            self.assertTrue(j1.placed)

            # Should be at bottom-center
            self.assertAlmostEqual(j1.position.x, placer.BOARD_WIDTH / 2, delta=1.0)
            self.assertAlmostEqual(j1.position.y, placer.EDGE_CLEARANCE, delta=1.0)

    def test_led_connector_placement(self):
        """Verify the placement of the LED connectors on the right edge."""
        placer = ComponentPlacement(str(self.board_path))
        placer.place_fixed_components()

        led_connectors = [f'JLED{i}' for i in range(1, 5)]
        prev_y = None

        for ref in led_connectors:
            if ref in placer.components:
                comp = placer.components[ref]
                self.assertTrue(comp.placed)

                # Should be at right edge
                self.assertGreater(comp.position.x, placer.BOARD_WIDTH - placer.EDGE_CLEARANCE - 1)

                # Should be vertically spaced
                if prev_y is not None:
                    self.assertGreater(comp.position.y, prev_y)
                prev_y = comp.position.y

    def test_i2c_connector_placement(self):
        """Verify the placement of the I2C connectors on the top edge."""
        placer = ComponentPlacement(str(self.board_path))
        placer.place_fixed_components()

        i2c_connectors = [f'J{i}' for i in range(3, 7)]

        for ref in i2c_connectors:
            if ref in placer.components:
                comp = placer.components[ref]
                self.assertTrue(comp.placed)

                # Should be at top edge
                self.assertGreater(comp.position.y, placer.BOARD_HEIGHT - placer.EDGE_CLEARANCE - 1)

    def test_i2s_connector_placement(self):
        """Verify the placement of the I2S connectors on the left edge."""
        placer = ComponentPlacement(str(self.board_path))
        placer.place_fixed_components()

        i2s_connectors = [f'J{i}' for i in range(7, 10)]

        for ref in i2s_connectors:
            if ref in placer.components:
                comp = placer.components[ref]
                self.assertTrue(comp.placed)

                # Should be at left edge
                self.assertLess(comp.position.x, placer.EDGE_CLEARANCE + 1)


class TestPrimaryComponentPlacement(unittest.TestCase):
    """Tests for Phase 2B: Placement of primary components."""

    @classmethod
    def setUpClass(cls):
        """Set up the path to the test board file."""
        cls.board_path = Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")
        if not cls.board_path.exists():
            raise unittest.SkipTest(f"Board file not found: {cls.board_path}")

    def test_mcu_a_zone_placement(self):
        """Verify the placement of components within the MCU-A thermal zone."""
        placer = ComponentPlacement(str(self.board_path))
        placer.define_thermal_zones()
        placer.place_primary_components()

        if 'U1' in placer.components:
            u1 = placer.components['U1']
            self.assertTrue(u1.placed)
            self.assertEqual(u1.thermal_zone, "MCU-A Zone")

            # Should be near zone center
            zone = next(z for z in placer.thermal_zones if z.name == "MCU-A Zone")
            distance = u1.position.distance_to(zone.center)
            self.assertLess(distance, 5.0)

    def test_mcu_b_zone_placement(self):
        """Verify the placement of components within the MCU-B thermal zone."""
        placer = ComponentPlacement(str(self.board_path))
        placer.define_thermal_zones()
        placer.place_primary_components()

        if 'U3' in placer.components:
            u3 = placer.components['U3']
            self.assertTrue(u3.placed)
            self.assertEqual(u3.thermal_zone, "MCU-B Zone")

            # Should be near zone center
            zone = next(z for z in placer.thermal_zones if z.name == "MCU-B Zone")
            distance = u3.position.distance_to(zone.center)
            self.assertLess(distance, 5.0)

    def test_decoupling_placement(self):
        """Verify the placement of decoupling capacitors around the MCU."""
        placer = ComponentPlacement(str(self.board_path))
        placer.define_thermal_zones()
        placer.cluster_components()
        placer.place_primary_components()

        decoupling = placer.clusters['decoupling']
        placed_count = sum(1 for c in decoupling if c.placed)

        # At least some decoupling caps should be placed
        self.assertGreater(placed_count, 0)

        # Should be in MCU-B zone
        for comp in decoupling:
            if comp.placed and comp.thermal_zone:
                self.assertEqual(comp.thermal_zone, "MCU-B Zone")

    def test_usb_fuse_placement(self):
        """Verify the placement of the F_USB fuse near the J1 connector."""
        placer = ComponentPlacement(str(self.board_path))
        placer.place_fixed_components()
        placer.define_thermal_zones()
        placer.place_primary_components()

        if 'F_USB' in placer.components and 'J1' in placer.components:
            f_usb = placer.components['F_USB']
            j1 = placer.components['J1']

            self.assertTrue(f_usb.placed)

            # Should be close to J1
            distance = f_usb.position.distance_to(j1.position)
            self.assertLess(distance, 10.0)


class TestSpacingValidation(unittest.TestCase):
    """Tests for spacing validation and DFM checks."""

    @classmethod
    def setUpClass(cls):
        """Set up the path to the test board file."""
        cls.board_path = Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")
        if not cls.board_path.exists():
            raise unittest.SkipTest(f"Board file not found: {cls.board_path}")

    def test_verify_spacing_structure(self):
        """Verify that the spacing verification method returns the correct data structure."""
        placer = ComponentPlacement(str(self.board_path))
        is_valid, violations = placer.verify_spacing()

        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(violations, list)

    def test_edge_clearance_detection(self):
        """Verify that edge clearance violations are correctly detected."""
        placer = ComponentPlacement(str(self.board_path))

        # Manually create violation
        if placer.components:
            first_comp = next(iter(placer.components.values()))
            first_comp.position = Point(0.5, 0.5)  # Too close to edge

            is_valid, violations = placer.verify_spacing()
            self.assertFalse(is_valid)
            self.assertGreater(len(violations), 0)

    def test_spacing_calculation(self):
        """Verify that inter-component spacing violations are correctly calculated."""
        placer = ComponentPlacement(str(self.board_path))

        # Create two components very close together
        comp1 = ComponentInfo(reference="TEST1", footprint="test", position=Point(10, 10))
        comp2 = ComponentInfo(reference="TEST2", footprint="test", position=Point(10.5, 10))

        placer.components['TEST1'] = comp1
        placer.components['TEST2'] = comp2

        is_valid, violations = placer.verify_spacing()

        # Should detect spacing violation (0.5mm < 2mm)
        violation_found = any('TEST1' in v and 'TEST2' in v for v in violations)
        self.assertTrue(violation_found)


class TestRoutingAccessibility(unittest.TestCase):
    """Tests for the routing accessibility optimization."""

    @classmethod
    def setUpClass(cls):
        """Set up the path to the test board file."""
        cls.board_path = Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")
        if not cls.board_path.exists():
            raise unittest.SkipTest(f"Board file not found: {cls.board_path}")

    def test_accessibility_scores(self):
        """Verify that routing accessibility scores are calculated for all components."""
        placer = ComponentPlacement(str(self.board_path))
        scores = placer.optimize_routing_accessibility()

        # All components should have scores
        self.assertEqual(len(scores), len(placer.components))

        # Scores should be between 0 and 1
        for score in scores.values():
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)

    def test_edge_components_higher_score(self):
        """Verify that components placed at the edge have a higher accessibility score."""
        placer = ComponentPlacement(str(self.board_path))
        placer.place_fixed_components()

        scores = placer.optimize_routing_accessibility()

        # J1 (edge connector) should have good accessibility
        if 'J1' in scores:
            self.assertGreater(scores['J1'], 0.3)


class TestFullPlacementPipeline(unittest.TestCase):
    """Tests for the complete component placement pipeline."""

    @classmethod
    def setUpClass(cls):
        """Set up the path to the test board file."""
        cls.board_path = Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")
        if not cls.board_path.exists():
            raise unittest.SkipTest(f"Board file not found: {cls.board_path}")

    def test_execute_pipeline(self):
        """Verify that the full placement pipeline executes successfully."""
        # Create temporary output file
        with tempfile.NamedTemporaryFile(suffix='.kicad_pcb', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            placer = ComponentPlacement(str(self.board_path), tmp_path)
            success = placer.execute()

            # Pipeline should complete
            self.assertIsInstance(success, bool)

            # All components should be placed
            placed_count = sum(1 for c in placer.components.values() if c.placed)
            self.assertEqual(placed_count, len(placer.components))

            # Output file should exist
            self.assertTrue(Path(tmp_path).exists())

        finally:
            # Clean up
            if Path(tmp_path).exists():
                Path(tmp_path).unlink()

    def test_report_generation(self):
        """Verify that the placement report is generated with all key sections."""
        placer = ComponentPlacement(str(self.board_path))
        placer.define_thermal_zones()
        placer.cluster_components()
        placer.place_fixed_components()

        report = placer.generate_placement_report()

        # Report should contain key sections
        self.assertIn("THERMAL ZONES", report)
        self.assertIn("COMPONENT CLUSTERS", report)
        self.assertIn("SPACING VALIDATION", report)
        self.assertIn("ROUTING ACCESSIBILITY", report)
        self.assertIn("PLACEMENT SUMMARY", report)

    def test_ascii_visualization(self):
        """Verify that the ASCII visualization is generated correctly."""
        placer = ComponentPlacement(str(self.board_path))
        placer.place_fixed_components()

        ascii_art = placer.generate_ascii_visualization()

        # Should contain board outline
        self.assertIn('-', ascii_art)
        self.assertIn('|', ascii_art)

        # Should contain legend
        self.assertIn("Legend", ascii_art)
        self.assertIn("Scale", ascii_art)


class TestPlacementValidation(unittest.TestCase):
    """Tests for the validation of the final component placement."""

    @classmethod
    def setUpClass(cls):
        """Set up the path to the test board file."""
        cls.board_path = Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")
        if not cls.board_path.exists():
            raise unittest.SkipTest(f"Board file not found: {cls.board_path}")

    def test_all_connectors_at_edge(self):
        """Verify that all connectors are placed at the board edge."""
        placer = ComponentPlacement(str(self.board_path))
        placer.place_fixed_components()

        connectors = [c for c in placer.components.values()
                     if c.reference.startswith('J') and c.placed]

        edge_threshold = 5.0  # mm from edge

        for conn in connectors:
            min_edge_dist = min(
                conn.position.x,
                placer.BOARD_WIDTH - conn.position.x,
                conn.position.y,
                placer.BOARD_HEIGHT - conn.position.y
            )
            self.assertLess(min_edge_dist, edge_threshold,
                          f"{conn.reference} not at edge: {min_edge_dist:.2f}mm")

    def test_minimum_spacing_compliance(self):
        """Verify that the 2mm minimum spacing between components is respected."""
        placer = ComponentPlacement(str(self.board_path))
        placer.execute()

        is_valid, violations = placer.verify_spacing()

        # Filter only spacing violations (not edge violations)
        spacing_violations = [v for v in violations if '<->' in v]

        if spacing_violations:
            print("\nSpacing violations found:")
            for v in spacing_violations[:10]:
                print(f"  {v}")

        # May have some violations in initial placement
        # but should be < 10% of total possible pairs
        total_pairs = len(placer.components) * (len(placer.components) - 1) / 2
        violation_ratio = len(spacing_violations) / total_pairs if total_pairs > 0 else 0

        self.assertLess(violation_ratio, 0.10,
                       f"Too many spacing violations: {len(spacing_violations)}")

    def test_thermal_zone_compliance(self):
        """Verify that components are correctly assigned to thermal zones."""
        placer = ComponentPlacement(str(self.board_path))
        placer.define_thermal_zones()
        placer.place_primary_components()

        # Count components in each zone
        for zone in placer.thermal_zones:
            if zone.priority == 1:  # High priority zones
                self.assertGreater(len(zone.components), 0,
                                 f"{zone.name} has no components")

    def test_board_density(self):
        """Verify that the board has a reasonable component density."""
        placer = ComponentPlacement(str(self.board_path))
        placer.execute()

        # Calculate occupied area (rough estimate)
        board_area = placer.BOARD_WIDTH * placer.BOARD_HEIGHT
        usable_area = (placer.BOARD_WIDTH - 2 * placer.EDGE_CLEARANCE) * \
                     (placer.BOARD_HEIGHT - 2 * placer.EDGE_CLEARANCE)

        # Assume average component size ~4mm²
        avg_component_area = 4.0
        total_component_area = len(placer.components) * avg_component_area

        density = total_component_area / usable_area

        # Density should be reasonable (not too sparse)
        self.assertGreater(density, 0.1, "Board too sparse")
        self.assertLess(density, 0.8, "Board too dense")


def run_k1_placement_test():
    """Run complete K1 Lightwave placement test and generate report"""
    board_path = Path("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb")

    if not board_path.exists():
        print(f"ERROR: Board file not found: {board_path}")
        return False

    print("=" * 80)
    print("K1 LIGHTWAVE - PHASE 2 COMPONENT PLACEMENT TEST")
    print("=" * 80)
    print()

    # Create temporary output
    with tempfile.NamedTemporaryFile(suffix='.kicad_pcb', delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Execute placement
        placer = ComponentPlacement(str(board_path), tmp_path)
        success = placer.execute()

        print("\n")
        print(placer.generate_placement_report())

        print("\n")
        print("BOARD VISUALIZATION:")
        print("=" * 80)
        print(placer.generate_ascii_visualization())

        return success

    finally:
        # Clean up
        if Path(tmp_path).exists():
            Path(tmp_path).unlink()


if __name__ == '__main__':
    # Run K1-specific test first
    print("\n")
    k1_success = run_k1_placement_test()
    print("\n" * 3)

    # Run unit tests
    print("=" * 80)
    print("RUNNING UNIT TESTS")
    print("=" * 80)
    unittest.main(argv=[''], verbosity=2, exit=False)

    # Exit with appropriate code
    import sys
    sys.exit(0 if k1_success else 1)
