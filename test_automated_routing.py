"""
Test Suite for Automated Routing System
========================================

Comprehensive tests for Phase 3 routing including:
- Critical net routing
- FreeRouting integration
- Copper zone creation
- Thermal via placement
- Validation checks

Author: Elite PCB Designer Agent
Date: 2025-10-24
Version: 1.0.0
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Import module under test
from automated_routing import (
    NetType,
    RoutingStatus,
    TraceSpecification,
    ViaSpecification,
    CopperZone,
    ThermalViaArray,
    RoutingResult,
    K1RoutingConfiguration,
    CriticalNetRouter,
    FreeRoutingIntegration,
    AutomatedRouting,
)


class TestTraceSpecification(unittest.TestCase):
    """Test TraceSpecification dataclass"""

    def test_trace_spec_creation(self):
        """Test creating a trace specification"""
        spec = TraceSpecification(
            net_name="VCC",
            net_type=NetType.POWER,
            width_mil=50,
            width_mm=1.27,
            clearance_mil=8,
            clearance_mm=0.2,
        )

        self.assertEqual(spec.net_name, "VCC")
        self.assertEqual(spec.net_type, NetType.POWER)
        self.assertEqual(spec.width_mil, 50)
        self.assertEqual(spec.width_mm, 1.27)
        self.assertEqual(spec.width_um, 1270)
        self.assertEqual(spec.clearance_um, 200)

    def test_differential_pair_spec(self):
        """Test differential pair specification"""
        spec = TraceSpecification(
            net_name="USB_D+",
            net_type=NetType.DIFFERENTIAL,
            width_mil=10,
            width_mm=0.25,
            clearance_mil=8,
            clearance_mm=0.2,
            differential_pair=True,
            differential_spacing_mil=8,
            length_match_tolerance_mm=0.5,
        )

        self.assertTrue(spec.differential_pair)
        self.assertEqual(spec.differential_spacing_mil, 8)
        self.assertEqual(spec.length_match_tolerance_mm, 0.5)


class TestViaSpecification(unittest.TestCase):
    """Test ViaSpecification dataclass"""

    def test_standard_via(self):
        """Test standard via specification"""
        via = ViaSpecification(
            diameter_mm=0.6,
            drill_mm=0.3,
            via_type="through"
        )

        self.assertEqual(via.diameter_mm, 0.6)
        self.assertEqual(via.diameter_um, 600)
        self.assertEqual(via.drill_mm, 0.3)
        self.assertEqual(via.drill_um, 300)
        self.assertEqual(via.via_type, "through")
        self.assertFalse(via.thermal_relief)

    def test_thermal_via(self):
        """Test thermal via specification"""
        via = ViaSpecification(
            diameter_mm=0.3,
            drill_mm=0.15,
            via_type="thermal",
            thermal_relief=False
        )

        self.assertEqual(via.diameter_mm, 0.3)
        self.assertEqual(via.via_type, "thermal")


class TestCopperZone(unittest.TestCase):
    """Test CopperZone dataclass"""

    def test_copper_zone_creation(self):
        """Test creating a copper zone"""
        zone = CopperZone(
            name="GND_L2",
            net_name="GND",
            layer="In1.Cu",
            priority=1,
            clearance_mm=0.2,
            min_width_mm=0.25,
            thermal_relief=True,
            fill_mode="solid"
        )

        self.assertEqual(zone.name, "GND_L2")
        self.assertEqual(zone.net_name, "GND")
        self.assertEqual(zone.layer, "In1.Cu")
        self.assertEqual(zone.priority, 1)
        self.assertTrue(zone.thermal_relief)
        self.assertEqual(zone.fill_mode, "solid")


class TestRoutingResult(unittest.TestCase):
    """Test RoutingResult dataclass"""

    def test_routing_result_success(self):
        """Test successful routing result"""
        result = RoutingResult(
            status=RoutingStatus.COMPLETED,
            nets_routed=50,
            nets_total=50,
            vias_placed=25,
            routing_time_sec=120.5,
            drc_violations=0
        )

        self.assertTrue(result.success)
        self.assertEqual(result.completion_percentage, 100.0)

    def test_routing_result_partial(self):
        """Test partial routing result"""
        result = RoutingResult(
            status=RoutingStatus.COMPLETED,
            nets_routed=45,
            nets_total=50,
            vias_placed=20,
            routing_time_sec=150.0,
            drc_violations=2
        )

        self.assertFalse(result.success)  # Has DRC violations
        self.assertEqual(result.completion_percentage, 90.0)

    def test_routing_result_failed(self):
        """Test failed routing result"""
        result = RoutingResult(
            status=RoutingStatus.FAILED,
            nets_routed=0,
            nets_total=50,
            vias_placed=0,
            routing_time_sec=5.0,
            drc_violations=10
        )

        self.assertFalse(result.success)
        self.assertEqual(result.completion_percentage, 0.0)


class TestK1RoutingConfiguration(unittest.TestCase):
    """Test K1 Lightwave routing configuration"""

    def test_power_nets(self):
        """Test power net specifications"""
        power_nets = K1RoutingConfiguration.POWER_NETS

        self.assertIn("VBUS_USB_5V", power_nets)
        self.assertIn("+3V3", power_nets)
        self.assertIn("LED_5V", power_nets)
        self.assertIn("GND", power_nets)

        # Check LED_5V is fattest trace (8A)
        led_5v = power_nets["LED_5V"]
        self.assertEqual(led_5v.width_mil, 160)
        self.assertEqual(led_5v.width_mm, 4.06)

    def test_spi_nets(self):
        """Test SPI net specifications"""
        spi_nets = K1RoutingConfiguration.SPI_NETS

        self.assertIn("SPI_SCK_A2B", spi_nets)
        self.assertIn("SPI_MOSI_A2B", spi_nets)
        self.assertIn("SPI_MISO_B2A", spi_nets)

        # Check series damping resistors
        for net in ["SPI_SCK_A2B", "SPI_MOSI_A2B", "SPI_MISO_B2A"]:
            self.assertEqual(spi_nets[net].series_damping_ohm, 33)

    def test_usb_nets(self):
        """Test USB differential pair specifications"""
        usb_nets = K1RoutingConfiguration.USB_NETS

        self.assertIn("USB_D+", usb_nets)
        self.assertIn("USB_D-", usb_nets)

        # Check differential pair properties
        for net in ["USB_D+", "USB_D-"]:
            spec = usb_nets[net]
            self.assertTrue(spec.differential_pair)
            self.assertEqual(spec.differential_spacing_mil, 8)
            self.assertEqual(spec.length_match_tolerance_mm, 0.5)

    def test_copper_zones(self):
        """Test copper zone specifications"""
        zones = K1RoutingConfiguration.COPPER_ZONES

        self.assertEqual(len(zones), 3)

        # Check GND plane
        gnd_zone = zones[0]
        self.assertEqual(gnd_zone.name, "GND_L2")
        self.assertEqual(gnd_zone.layer, "In1.Cu")
        self.assertEqual(gnd_zone.priority, 1)

    def test_thermal_vias(self):
        """Test thermal via array specifications"""
        thermal_vias = K1RoutingConfiguration.THERMAL_VIAS

        self.assertEqual(len(thermal_vias), 3)

        # Check MCU-A thermal vias
        mcu_a = thermal_vias[0]
        self.assertEqual(mcu_a.component_ref, "U1")
        self.assertEqual(mcu_a.num_vias, 16)
        self.assertEqual(mcu_a.grid_spacing_mm, 1.27)

    def test_get_all_critical_nets(self):
        """Test getting all critical nets"""
        all_nets = K1RoutingConfiguration.get_all_critical_nets()

        self.assertGreater(len(all_nets), 0)
        self.assertIn("VBUS_USB_5V", all_nets)
        self.assertIn("SPI_SCK_A2B", all_nets)
        self.assertIn("USB_D+", all_nets)
        self.assertIn("I2C_SDA", all_nets)


class TestCriticalNetRouter(unittest.TestCase):
    """Test CriticalNetRouter class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.board_path = Path(self.temp_dir) / "test_board.kicad_pcb"
        self.board_path.touch()

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)

    @patch('automated_routing.pcbnew')
    def test_load_board(self, mock_pcbnew):
        """Test loading KiCad board"""
        mock_board = Mock()
        mock_pcbnew.LoadBoard.return_value = mock_board

        router = CriticalNetRouter(str(self.board_path))
        success = router.load_board()

        self.assertTrue(success)
        self.assertEqual(router.board, mock_board)

    def test_route_power_nets(self):
        """Test routing power nets"""
        router = CriticalNetRouter(str(self.board_path))
        router.board = Mock()

        results = router.route_power_nets()

        self.assertEqual(results["status"], "completed")
        self.assertGreater(len(results["nets_routed"]), 0)
        self.assertIn("VBUS_USB_5V", results["nets_routed"])
        self.assertIn("LED_5V", results["nets_routed"])

    def test_route_spi_signals(self):
        """Test routing SPI signals"""
        router = CriticalNetRouter(str(self.board_path))
        router.board = Mock()

        results = router.route_spi_signals()

        self.assertEqual(results["status"], "completed")
        self.assertIn("SPI_SCK_A2B", results["nets_routed"])
        self.assertIn("SPI_MOSI_A2B", results["nets_routed"])

    def test_route_usb_signals(self):
        """Test routing USB differential pair"""
        router = CriticalNetRouter(str(self.board_path))
        router.board = Mock()

        results = router.route_usb_signals()

        self.assertEqual(results["status"], "completed")
        self.assertIn("USB_D+", results["nets_routed"])
        self.assertIn("USB_D-", results["nets_routed"])

    def test_route_i2c_i2s(self):
        """Test routing I2C and I2S signals"""
        router = CriticalNetRouter(str(self.board_path))
        router.board = Mock()

        results = router.route_i2c_i2s()

        self.assertEqual(results["status"], "completed")
        self.assertIn("I2C_SDA", results["nets_routed"])
        self.assertIn("I2S_BCLK", results["nets_routed"])


class TestFreeRoutingIntegration(unittest.TestCase):
    """Test FreeRoutingIntegration class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.board_path = Path(self.temp_dir) / "test_board.kicad_pcb"
        self.board_path.touch()

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test FreeRouting integration initialization"""
        integration = FreeRoutingIntegration(str(self.board_path))

        self.assertEqual(integration.board_path, self.board_path)
        self.assertTrue(integration.work_dir.exists())

    def test_find_freerouting_jar_custom(self):
        """Test finding custom FreeRouting JAR"""
        jar_path = Path(self.temp_dir) / "freerouting.jar"
        jar_path.touch()

        integration = FreeRoutingIntegration(
            str(self.board_path),
            freerouting_jar=str(jar_path)
        )

        self.assertTrue(integration.find_freerouting_jar())
        self.assertEqual(integration.freerouting_jar, jar_path)

    @patch('automated_routing.DSN')
    def test_export_to_dsn(self, mock_dsn_module):
        """Test DSN export"""
        mock_db = Mock()
        mock_dsn_module.SPECCTRA_DB.return_value = mock_db

        integration = FreeRoutingIntegration(str(self.board_path))

        # Create mock DSN file
        dsn_file = integration.work_dir / f"{self.board_path.stem}.dsn"
        dsn_file.touch()

        with patch.object(integration, 'dsn_file', dsn_file):
            success = integration.export_to_dsn()

        self.assertTrue(success)

    def test_configure_freerouting(self):
        """Test FreeRouting configuration"""
        integration = FreeRoutingIntegration(str(self.board_path))
        config = integration.configure_freerouting()

        self.assertIn("threads", config)
        self.assertIn("effort_level", config)
        self.assertEqual(config["effort_level"], "high")
        self.assertEqual(config["timeout_seconds"], 900)

    @patch('automated_routing.subprocess.run')
    def test_run_freerouting_success(self, mock_run):
        """Test successful FreeRouting execution"""
        # Mock successful subprocess
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Routing completed"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Create mock files
        jar_path = Path(self.temp_dir) / "freerouting.jar"
        jar_path.touch()

        integration = FreeRoutingIntegration(
            str(self.board_path),
            freerouting_jar=str(jar_path)
        )

        # Create DSN file
        integration.dsn_file = integration.work_dir / "test.dsn"
        integration.dsn_file.touch()

        # Create SES file (simulating FreeRouting output)
        integration.ses_file = integration.work_dir / "test.ses"
        integration.ses_file.touch()

        success = integration.run_freerouting(timeout=60)

        self.assertTrue(success)
        mock_run.assert_called_once()

    def test_verify_routing(self):
        """Test routing verification"""
        integration = FreeRoutingIntegration(str(self.board_path))

        success, message = integration.verify_routing()

        self.assertTrue(success)
        self.assertIsInstance(message, str)


class TestAutomatedRouting(unittest.TestCase):
    """Test AutomatedRouting orchestrator"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.board_path = Path(self.temp_dir) / "test_board.kicad_pcb"
        self.board_path.touch()

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test AutomatedRouting initialization"""
        router = AutomatedRouting(str(self.board_path))

        self.assertEqual(router.board_path, self.board_path)
        self.assertIsNotNone(router.critical_router)
        self.assertIsNotNone(router.freerouting)
        self.assertEqual(router.result.status, RoutingStatus.PENDING)

    @patch.object(CriticalNetRouter, 'load_board')
    @patch.object(CriticalNetRouter, 'route_power_nets')
    @patch.object(CriticalNetRouter, 'route_spi_signals')
    @patch.object(CriticalNetRouter, 'route_usb_signals')
    @patch.object(CriticalNetRouter, 'route_i2c_i2s')
    def test_route_critical_nets(self, mock_i2c, mock_usb, mock_spi, mock_power, mock_load):
        """Test critical net routing orchestration"""
        mock_load.return_value = True
        mock_power.return_value = {"nets_routed": ["VCC"], "status": "completed"}
        mock_spi.return_value = {"nets_routed": ["SPI_SCK"], "status": "completed"}
        mock_usb.return_value = {"nets_routed": ["USB_D+"], "status": "completed"}
        mock_i2c.return_value = {"nets_routed": ["I2C_SDA"], "status": "completed"}

        router = AutomatedRouting(str(self.board_path))
        results = router.route_critical_nets()

        self.assertGreater(results["total_nets"], 0)
        self.assertIn("power", results)
        self.assertIn("spi", results)
        self.assertIn("usb", results)
        self.assertIn("i2c_i2s", results)

    def test_create_copper_zones(self):
        """Test copper zone creation"""
        router = AutomatedRouting(str(self.board_path))
        results = router.create_copper_zones()

        self.assertEqual(results["status"], "completed")
        self.assertGreater(len(results["zones_created"]), 0)

    def test_place_thermal_vias(self):
        """Test thermal via placement"""
        router = AutomatedRouting(str(self.board_path))
        results = router.place_thermal_vias()

        self.assertEqual(results["status"], "completed")
        self.assertGreater(results["total_vias"], 0)
        self.assertEqual(router.result.vias_placed, results["total_vias"])


class TestIntegration(unittest.TestCase):
    """Integration tests for full routing pipeline"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.board_path = Path(self.temp_dir) / "k1_test.kicad_pcb"
        self.board_path.touch()

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)

    @patch.object(CriticalNetRouter, 'load_board')
    @patch.object(FreeRoutingIntegration, 'export_to_dsn')
    @patch.object(FreeRoutingIntegration, 'run_freerouting')
    @patch.object(FreeRoutingIntegration, 'import_routing_results')
    @patch.object(FreeRoutingIntegration, 'verify_routing')
    def test_full_pipeline_mock(self, mock_verify, mock_import, mock_run, mock_export, mock_load):
        """Test full routing pipeline with mocked external dependencies"""
        mock_load.return_value = True
        mock_export.return_value = True
        mock_run.return_value = True
        mock_import.return_value = True
        mock_verify.return_value = (True, "Success")

        router = AutomatedRouting(str(self.board_path))

        # Mock critical router methods
        router.critical_router.route_power_nets = Mock(
            return_value={"nets_routed": ["VCC"], "status": "completed"}
        )
        router.critical_router.route_spi_signals = Mock(
            return_value={"nets_routed": ["SPI_SCK"], "status": "completed"}
        )
        router.critical_router.route_usb_signals = Mock(
            return_value={"nets_routed": ["USB_D+"], "status": "completed"}
        )
        router.critical_router.route_i2c_i2s = Mock(
            return_value={"nets_routed": ["I2C_SDA"], "status": "completed"}
        )

        success = router.execute()

        # Verify all steps were called
        self.assertTrue(success)
        self.assertEqual(router.result.status, RoutingStatus.COMPLETED)


def suite():
    """Create test suite"""
    test_suite = unittest.TestSuite()

    # Add all test classes
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTraceSpecification))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestViaSpecification))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCopperZone))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRoutingResult))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestK1RoutingConfiguration))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCriticalNetRouter))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestFreeRoutingIntegration))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAutomatedRouting))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIntegration))

    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    sys.exit(0 if result.wasSuccessful() else 1)
