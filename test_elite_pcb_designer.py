#!/usr/bin/env python3
"""
Elite PCB Designer Agent - Integration Tests
=============================================

Comprehensive test suite for the master orchestrator.

Tests:
- Initialization and input validation
- Phase execution and sequencing
- Error handling and recovery
- Report generation
- Output organization
- K1 Lightwave end-to-end execution

Author: Elite PCB Designer Agent
Version: 1.0.0
Date: 2025-10-24
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from elite_pcb_designer import (
    ElitePCBDesigner,
    PhaseResult,
    PhaseStatus
)


class TestElitePCBDesignerInitialization(unittest.TestCase):
    """Test initialization and validation"""

    def setUp(self):
        """Create temporary test files"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.netlist_path = self.temp_dir / "test.net"
        self.board_path = self.temp_dir / "test.kicad_pcb"
        self.output_dir = self.temp_dir / "output"

        # Create dummy files
        self.netlist_path.write_text("(export (version D)")
        self.board_path.write_text("(kicad_pcb (version 20221018)")

    def tearDown(self):
        """Clean up temporary files"""
        shutil.rmtree(self.temp_dir)

    def test_initialization_valid_inputs(self):
        """Test successful initialization with valid inputs"""
        designer = ElitePCBDesigner(
            netlist_path=str(self.netlist_path),
            board_path=str(self.board_path),
            output_dir=str(self.output_dir)
        )

        self.assertEqual(designer.netlist_path, self.netlist_path)
        self.assertEqual(designer.board_path, self.board_path)
        self.assertEqual(designer.output_dir, self.output_dir)
        self.assertFalse(designer.verbose)
        self.assertEqual(len(designer.skip_phases), 0)

    def test_initialization_missing_netlist(self):
        """Test initialization fails with missing netlist"""
        with self.assertRaises(FileNotFoundError):
            ElitePCBDesigner(
                netlist_path="nonexistent.net",
                board_path=str(self.board_path)
            )

    def test_initialization_missing_board(self):
        """Test initialization fails with missing board"""
        with self.assertRaises(FileNotFoundError):
            ElitePCBDesigner(
                netlist_path=str(self.netlist_path),
                board_path="nonexistent.kicad_pcb"
            )

    def test_initialization_with_skip_phases(self):
        """Test initialization with skip phases"""
        designer = ElitePCBDesigner(
            netlist_path=str(self.netlist_path),
            board_path=str(self.board_path),
            skip_phases=[2, 3]
        )

        self.assertEqual(designer.skip_phases, {2, 3})

    def test_initialization_verbose_mode(self):
        """Test initialization with verbose mode"""
        designer = ElitePCBDesigner(
            netlist_path=str(self.netlist_path),
            board_path=str(self.board_path),
            verbose=True
        )

        self.assertTrue(designer.verbose)


class TestPhaseExecution(unittest.TestCase):
    """Test individual phase execution"""

    def setUp(self):
        """Create temporary test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.netlist_path = self.temp_dir / "test.net"
        self.board_path = self.temp_dir / "test.kicad_pcb"

        # Create dummy files
        self.netlist_path.write_text("(export (version D)")
        self.board_path.write_text("(kicad_pcb (version 20221018)")

        self.designer = ElitePCBDesigner(
            netlist_path=str(self.netlist_path),
            board_path=str(self.board_path)
        )

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir)

    @patch('elite_pcb_designer.DesignPreparation')
    def test_phase_1_success(self, mock_phase1):
        """Test Phase 1 successful execution"""
        # Mock Phase 1 to return success
        mock_instance = MagicMock()
        mock_instance.execute.return_value = True
        mock_instance.component_count = 52
        mock_instance.footprints_assigned = 42
        mock_phase1.return_value = mock_instance

        success = self.designer._execute_phase_1()

        self.assertTrue(success)
        self.assertIn(1, self.designer.results)
        result = self.designer.results[1]
        self.assertEqual(result.status, PhaseStatus.COMPLETED)
        self.assertGreater(result.duration_seconds, 0)

    @patch('elite_pcb_designer.DesignPreparation')
    def test_phase_1_failure(self, mock_phase1):
        """Test Phase 1 failure handling"""
        mock_instance = MagicMock()
        mock_instance.execute.return_value = False
        mock_phase1.return_value = mock_instance

        success = self.designer._execute_phase_1()

        self.assertFalse(success)
        self.assertIn(1, self.designer.results)
        result = self.designer.results[1]
        self.assertEqual(result.status, PhaseStatus.FAILED)

    @patch('elite_pcb_designer.DesignPreparation')
    def test_phase_1_exception(self, mock_phase1):
        """Test Phase 1 exception handling"""
        mock_instance = MagicMock()
        mock_instance.execute.side_effect = Exception("Test error")
        mock_phase1.return_value = mock_instance

        success = self.designer._execute_phase_1()

        self.assertFalse(success)
        result = self.designer.results[1]
        self.assertEqual(result.status, PhaseStatus.FAILED)
        self.assertIsNotNone(result.error_message)

    def test_phase_skip(self):
        """Test phase skipping"""
        self.designer.skip_phases = {1}
        self.designer._skip_phase(1, "Design Preparation")

        self.assertIn(1, self.designer.results)
        result = self.designer.results[1]
        self.assertEqual(result.status, PhaseStatus.SKIPPED)


class TestReportGeneration(unittest.TestCase):
    """Test report generation"""

    def setUp(self):
        """Create test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.netlist_path = self.temp_dir / "test.net"
        self.board_path = self.temp_dir / "test.kicad_pcb"
        self.output_dir = self.temp_dir / "output"

        self.netlist_path.write_text("(export (version D)")
        self.board_path.write_text("(kicad_pcb (version 20221018)")

        self.designer = ElitePCBDesigner(
            netlist_path=str(self.netlist_path),
            board_path=str(self.board_path),
            output_dir=str(self.output_dir)
        )

        # Add mock results
        from datetime import datetime, timedelta
        start_time = datetime.now()
        self.designer.results = {
            1: PhaseResult(
                phase_num=1,
                phase_name="Design Preparation",
                status=PhaseStatus.COMPLETED,
                start_time=start_time,
                end_time=start_time + timedelta(seconds=30),
                duration_seconds=30.0,
                details={'components_loaded': 52}
            ),
            2: PhaseResult(
                phase_num=2,
                phase_name="Component Placement",
                status=PhaseStatus.COMPLETED,
                start_time=start_time + timedelta(seconds=30),
                end_time=start_time + timedelta(seconds=180),
                duration_seconds=150.0,
                details={'components_placed': 52}
            )
        }
        self.designer.start_time = start_time
        self.designer.end_time = start_time + timedelta(seconds=180)

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir)

    def test_text_report_generation(self):
        """Test text report generation"""
        report = self.designer._generate_text_report()

        self.assertIn("ELITE PCB DESIGNER AGENT", report)
        self.assertIn("K1 Lightwave Motherboard", report)
        self.assertIn("Phase 1: Design Preparation", report)
        self.assertIn("Phase 2: Component Placement", report)
        self.assertIn("COMPLETED", report)

    def test_json_report_generation(self):
        """Test JSON report generation"""
        report = self.designer._generate_json_report()

        self.assertIn('project', report)
        self.assertIn('phases', report)
        self.assertIn('manufacturing_ready', report)
        self.assertEqual(report['project'], 'K1 Lightwave Motherboard')
        self.assertIn('1', report['phases'])
        self.assertIn('2', report['phases'])

    def test_combined_report_saving(self):
        """Test combined report saving"""
        report_path = self.designer.generate_combined_report()

        # Check text report
        text_report = Path(report_path)
        self.assertTrue(text_report.exists())
        content = text_report.read_text()
        self.assertIn("ELITE PCB DESIGNER AGENT", content)

        # Check JSON report
        json_report = self.output_dir / "master_report.json"
        self.assertTrue(json_report.exists())
        with open(json_report) as f:
            data = json.load(f)
        self.assertIn('phases', data)


class TestOutputOrganization(unittest.TestCase):
    """Test output directory organization"""

    def setUp(self):
        """Create test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.netlist_path = self.temp_dir / "test.net"
        self.board_path = self.temp_dir / "test.kicad_pcb"
        self.output_dir = self.temp_dir / "output"

        self.netlist_path.write_text("(export (version D)")
        self.board_path.write_text("(kicad_pcb (version 20221018)")

        self.designer = ElitePCBDesigner(
            netlist_path=str(self.netlist_path),
            board_path=str(self.board_path),
            output_dir=str(self.output_dir)
        )

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir)

    def test_output_directory_creation(self):
        """Test output directory structure creation"""
        outputs = self.designer.save_all_outputs()

        # Check main output directory
        self.assertTrue(self.output_dir.exists())

        # Check phase directories
        self.assertTrue((self.output_dir / "phase1_design_prep").exists())
        self.assertTrue((self.output_dir / "phase2_placement").exists())
        self.assertTrue((self.output_dir / "phase3_routing").exists())
        self.assertTrue((self.output_dir / "phase4_validation").exists())

        # Check manufacturing directory
        self.assertTrue((self.output_dir / "manufacturing").exists())

        # Check board file copied
        self.assertIn('board', outputs)
        self.assertTrue(Path(outputs['board']).exists())


class TestPhaseResult(unittest.TestCase):
    """Test PhaseResult dataclass"""

    def test_phase_result_creation(self):
        """Test PhaseResult creation"""
        from datetime import datetime

        start = datetime.now()
        result = PhaseResult(
            phase_num=1,
            phase_name="Test Phase",
            status=PhaseStatus.COMPLETED,
            start_time=start,
            end_time=start,
            duration_seconds=120.5
        )

        self.assertEqual(result.phase_num, 1)
        self.assertEqual(result.phase_name, "Test Phase")
        self.assertEqual(result.status, PhaseStatus.COMPLETED)
        self.assertEqual(result.duration_seconds, 120.5)

    def test_duration_string_formatting(self):
        """Test duration string formatting"""
        result = PhaseResult(
            phase_num=1,
            phase_name="Test",
            status=PhaseStatus.COMPLETED,
            duration_seconds=125.7
        )

        self.assertEqual(result.duration_str, "2:05")

    def test_phase_result_to_dict(self):
        """Test PhaseResult to dict conversion"""
        from datetime import datetime

        start = datetime.now()
        result = PhaseResult(
            phase_num=1,
            phase_name="Test Phase",
            status=PhaseStatus.COMPLETED,
            start_time=start,
            duration_seconds=60.0,
            details={'test_key': 'test_value'}
        )

        data = result.to_dict()

        self.assertIn('phase_num', data)
        self.assertIn('phase_name', data)
        self.assertIn('status', data)
        self.assertIn('duration_formatted', data)
        self.assertIn('details', data)
        self.assertEqual(data['phase_num'], 1)
        self.assertEqual(data['details']['test_key'], 'test_value')


class TestErrorRecovery(unittest.TestCase):
    """Test error handling and recovery"""

    def setUp(self):
        """Create test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.netlist_path = self.temp_dir / "test.net"
        self.board_path = self.temp_dir / "test.kicad_pcb"

        self.netlist_path.write_text("(export (version D)")
        self.board_path.write_text("(kicad_pcb (version 20221018)")

        self.designer = ElitePCBDesigner(
            netlist_path=str(self.netlist_path),
            board_path=str(self.board_path)
        )

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir)

    @patch('elite_pcb_designer.DesignPreparation')
    def test_phase_failure_stops_pipeline(self, mock_phase1):
        """Test that phase failure stops pipeline"""
        mock_instance = MagicMock()
        mock_instance.execute.return_value = False
        mock_phase1.return_value = mock_instance

        success = self.designer.execute_full_pipeline()

        self.assertFalse(success)
        # Only Phase 1 should be attempted
        self.assertIn(1, self.designer.results)
        self.assertNotIn(2, self.designer.results)

    @patch('elite_pcb_designer.DesignPreparation')
    def test_keyboard_interrupt_handling(self, mock_phase1):
        """Test keyboard interrupt handling"""
        mock_instance = MagicMock()
        mock_instance.execute.side_effect = KeyboardInterrupt()
        mock_phase1.return_value = mock_instance

        success = self.designer.execute_full_pipeline()

        self.assertFalse(success)
        self.assertIsNotNone(self.designer.end_time)


class TestUtilityMethods(unittest.TestCase):
    """Test utility and helper methods"""

    def test_format_duration(self):
        """Test duration formatting"""
        from elite_pcb_designer import ElitePCBDesigner

        # 0 seconds
        self.assertEqual(ElitePCBDesigner._format_duration(0), "0:00")

        # 30 seconds
        self.assertEqual(ElitePCBDesigner._format_duration(30), "0:30")

        # 90 seconds
        self.assertEqual(ElitePCBDesigner._format_duration(90), "1:30")

        # 3665 seconds (1 hour 1 minute 5 seconds)
        self.assertEqual(ElitePCBDesigner._format_duration(3665), "61:05")


def run_integration_test_suite():
    """Run complete integration test suite"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestElitePCBDesignerInitialization))
    suite.addTests(loader.loadTestsFromTestCase(TestPhaseExecution))
    suite.addTests(loader.loadTestsFromTestCase(TestReportGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestOutputOrganization))
    suite.addTests(loader.loadTestsFromTestCase(TestPhaseResult))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorRecovery))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityMethods))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_test_suite()
    exit(0 if success else 1)
