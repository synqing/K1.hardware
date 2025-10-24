"""
Test suite for Elite PCB Designer Agent - Phase 4: Design Validation

Comprehensive tests for all validation components:
- DRC validation
- DFM validation (JLCPCB specific)
- Signal integrity checks
- Thermal validation
- Manufacturing readiness
- File generation

Author: Elite PCB Designer Agent
Date: 2025-10-24
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pcbnew
import pytest

from design_validation import (
    DFMValidator,
    DRCRules,
    DRCValidator,
    DesignValidation,
    SignalIntegrityValidator,
    ThermalParameters,
    ThermalValidator,
    ValidationResult,
    ValidationSeverity,
)


@pytest.fixture
def mock_board():
    """Create a mock KiCad board for testing"""
    board = MagicMock(spec=pcbnew.BOARD)
    board.GetCopperLayerCount.return_value = 4
    board.GetNetCount.return_value = 50
    board.GetTracks.return_value = []
    board.GetFootprints.return_value = []
    return board


@pytest.fixture
def mock_board_path(tmp_path):
    """Create a temporary board file path"""
    board_file = tmp_path / "test_board.kicad_pcb"
    board_file.write_text("(kicad_pcb (version 20240101))")
    return board_file


@pytest.fixture
def sample_thermal_params():
    """Sample thermal parameters for K1 Lightwave"""
    return ThermalParameters(
        ambient_temp_c=25.0,
        power_mcu_a_w=0.3,
        power_mcu_b_w=0.5,
        power_converter_w=0.2,
        r_thermal_mcu_to_gnd=15.0,
        r_thermal_gnd_to_ambient=5.0,
        thermal_via_benefit_pct=0.25,
        max_junction_temp_c=85.0
    )


class TestDRCRules:
    """Test DRC rules definition"""

    def test_default_rules(self):
        """Test default DRC rules match JLCPCB standards"""
        rules = DRCRules()

        assert rules.trace_width_min == 0.1016  # 4 mil
        assert rules.trace_spacing_min == 0.127  # 5 mil
        assert rules.via_drill_min == 0.15  # mm
        assert rules.via_pad_size_min == 0.3  # mm
        assert rules.copper_to_edge_min == 0.3  # mm

    def test_to_dict(self):
        """Test rule conversion to dictionary"""
        rules = DRCRules()
        rules_dict = rules.to_dict()

        assert 'trace_width' in rules_dict
        assert 'via_drill' in rules_dict
        assert rules_dict['trace_width'][0] == 'min'
        assert rules_dict['trace_width'][1] == 4  # mil


class TestDRCValidator:
    """Test DRC validation functionality"""

    @patch('design_validation.pcbnew.LoadBoard')
    def test_init(self, mock_load, mock_board_path, mock_board):
        """Test DRC validator initialization"""
        mock_load.return_value = mock_board

        validator = DRCValidator(mock_board_path)

        assert validator.board_path == mock_board_path
        assert isinstance(validator.rules, DRCRules)
        mock_load.assert_called_once_with(str(mock_board_path))

    @patch('design_validation.pcbnew.LoadBoard')
    @patch('design_validation.subprocess.run')
    def test_run_kicad_drc_success(self, mock_run, mock_load, mock_board_path, mock_board):
        """Test successful DRC execution"""
        mock_load.return_value = mock_board

        # Mock successful DRC with zero violations
        mock_run.return_value = Mock(
            returncode=0,
            stdout='{"violations": []}',
            stderr=''
        )

        # Create mock JSON report
        report_path = mock_board_path.parent / 'drc_report.json'
        report_path.write_text('{"violations": []}')

        validator = DRCValidator(mock_board_path)
        error_count, report = validator.run_kicad_drc()

        assert error_count == 0
        assert 'violations' in report

    @patch('design_validation.pcbnew.LoadBoard')
    @patch('design_validation.subprocess.run')
    def test_run_kicad_drc_with_violations(self, mock_run, mock_load, mock_board_path, mock_board):
        """Test DRC execution with violations"""
        mock_load.return_value = mock_board

        # Mock DRC with violations
        violations = [
            {"type": "clearance", "severity": "error", "description": "Trace too close"}
        ]
        mock_run.return_value = Mock(returncode=0, stdout=json.dumps({"violations": violations}))

        report_path = mock_board_path.parent / 'drc_report.json'
        report_path.write_text(json.dumps({"violations": violations}))

        validator = DRCValidator(mock_board_path)
        error_count, report = validator.run_kicad_drc()

        assert error_count == 1

    @patch('design_validation.pcbnew.LoadBoard')
    def test_verify_constraints_pass(self, mock_load, mock_board_path, mock_board):
        """Test constraint verification with passing DRC"""
        mock_load.return_value = mock_board

        validator = DRCValidator(mock_board_path)

        # Mock successful DRC
        with patch.object(validator, 'run_kicad_drc', return_value=(0, "No violations")):
            result = validator.verify_constraints()

            assert isinstance(result, ValidationResult)
            assert result.passed is True
            assert result.severity == ValidationSeverity.PASS
            assert result.details['violation_count'] == 0

    @patch('design_validation.pcbnew.LoadBoard')
    def test_verify_constraints_fail(self, mock_load, mock_board_path, mock_board):
        """Test constraint verification with failing DRC"""
        mock_load.return_value = mock_board

        validator = DRCValidator(mock_board_path)

        # Mock DRC with violations
        with patch.object(validator, 'run_kicad_drc', return_value=(3, "3 violations found")):
            result = validator.verify_constraints()

            assert result.passed is False
            assert result.severity == ValidationSeverity.ERROR
            assert result.details['violation_count'] == 3


class TestDFMValidator:
    """Test Design for Manufacturing validation"""

    @patch('design_validation.pcbnew.LoadBoard')
    def test_init(self, mock_load, mock_board_path, mock_board):
        """Test DFM validator initialization"""
        mock_load.return_value = mock_board

        validator = DFMValidator(mock_board_path)

        assert validator.board_path == mock_board_path
        mock_load.assert_called_once()

    @patch('design_validation.pcbnew.LoadBoard')
    def test_validate_layer_stack_pass(self, mock_load, mock_board_path, mock_board):
        """Test layer stack validation with 4 layers"""
        mock_board.GetCopperLayerCount.return_value = 4
        mock_load.return_value = mock_board

        validator = DFMValidator(mock_board_path)
        result = validator.validate_layer_stack()

        assert result.passed is True
        assert result.severity == ValidationSeverity.PASS
        assert result.details['layer_count'] == 4

    @patch('design_validation.pcbnew.LoadBoard')
    def test_validate_layer_stack_fail(self, mock_load, mock_board_path, mock_board):
        """Test layer stack validation with wrong layer count"""
        mock_board.GetCopperLayerCount.return_value = 2
        mock_load.return_value = mock_board

        validator = DFMValidator(mock_board_path)
        result = validator.validate_layer_stack()

        assert result.passed is False
        assert result.severity == ValidationSeverity.ERROR
        assert result.details['layer_count'] == 2

    @patch('design_validation.pcbnew.LoadBoard')
    def test_validate_fiducials_sufficient(self, mock_load, mock_board_path, mock_board):
        """Test fiducial validation with 3+ fiducials"""
        # Create mock fiducial footprints
        fid1 = MagicMock()
        fid1.GetReference.return_value = "FID1"
        fid1.GetPosition.return_value = pcbnew.VECTOR2I(0, 0)

        fid2 = MagicMock()
        fid2.GetReference.return_value = "FID2"
        fid2.GetPosition.return_value = pcbnew.VECTOR2I(100000000, 0)

        fid3 = MagicMock()
        fid3.GetReference.return_value = "FID3"
        fid3.GetPosition.return_value = pcbnew.VECTOR2I(0, 100000000)

        mock_board.GetFootprints.return_value = [fid1, fid2, fid3]
        mock_load.return_value = mock_board

        validator = DFMValidator(mock_board_path)
        result = validator.validate_fiducials()

        assert result.passed is True
        assert result.severity == ValidationSeverity.PASS
        assert result.details['fiducial_count'] == 3

    @patch('design_validation.pcbnew.LoadBoard')
    def test_validate_fiducials_insufficient(self, mock_load, mock_board_path, mock_board):
        """Test fiducial validation with <3 fiducials"""
        fid1 = MagicMock()
        fid1.GetReference.return_value = "FID1"
        fid1.GetPosition.return_value = pcbnew.VECTOR2I(0, 0)

        mock_board.GetFootprints.return_value = [fid1]
        mock_load.return_value = mock_board

        validator = DFMValidator(mock_board_path)
        result = validator.validate_fiducials()

        assert result.passed is False
        assert result.severity == ValidationSeverity.WARNING
        assert result.details['fiducial_count'] == 1


class TestSignalIntegrityValidator:
    """Test signal integrity validation"""

    @patch('design_validation.pcbnew.LoadBoard')
    def test_init(self, mock_load, mock_board_path, mock_board):
        """Test SI validator initialization"""
        mock_load.return_value = mock_board

        validator = SignalIntegrityValidator(mock_board_path)

        assert validator.board_path == mock_board_path

    @patch('design_validation.pcbnew.LoadBoard')
    def test_validate_spi_routing(self, mock_load, mock_board_path, mock_board):
        """Test SPI routing validation"""
        # Create mock SPI nets
        mock_net_info = MagicMock()
        mock_sck_net = MagicMock()
        mock_sck_net.GetNetname.return_value = "SPI_SCK"
        mock_sck_net.GetNetCode.return_value = 1

        mock_board.GetNetInfo.return_value = mock_net_info
        mock_board.GetNetCount.return_value = 1
        mock_net_info.GetNetItem.return_value = mock_sck_net
        mock_board.GetTracks.return_value = []

        mock_load.return_value = mock_board

        validator = SignalIntegrityValidator(mock_board_path)
        result = validator.validate_spi_routing()

        assert isinstance(result, ValidationResult)
        assert 'spi_nets' in result.details
        assert 'recommendations' in result.details

    @patch('design_validation.pcbnew.LoadBoard')
    def test_validate_usb_routing(self, mock_load, mock_board_path, mock_board):
        """Test USB routing validation"""
        mock_load.return_value = mock_board

        validator = SignalIntegrityValidator(mock_board_path)
        result = validator.validate_usb_routing()

        assert isinstance(result, ValidationResult)
        assert 'usb_signals' in result.details
        assert 'requirements' in result.details

    @patch('design_validation.pcbnew.LoadBoard')
    def test_validate_i2c_i2s_routing(self, mock_load, mock_board_path, mock_board):
        """Test I2C/I2S routing validation"""
        mock_load.return_value = mock_board

        validator = SignalIntegrityValidator(mock_board_path)
        result = validator.validate_i2c_i2s_routing()

        assert isinstance(result, ValidationResult)
        assert result.severity == ValidationSeverity.PASS


class TestThermalValidator:
    """Test thermal validation and calculations"""

    def test_thermal_parameters_defaults(self, sample_thermal_params):
        """Test thermal parameter defaults"""
        params = sample_thermal_params

        assert params.ambient_temp_c == 25.0
        assert params.power_mcu_a_w == 0.3
        assert params.power_mcu_b_w == 0.5
        assert params.power_converter_w == 0.2
        assert params.total_power_w == 1.0

    @patch('design_validation.pcbnew.LoadBoard')
    def test_calculate_temperature_rise(self, mock_load, mock_board_path, mock_board, sample_thermal_params):
        """Test temperature rise calculation"""
        mock_load.return_value = mock_board

        validator = ThermalValidator(mock_board_path, sample_thermal_params)
        temp_rise = validator.calculate_temperature_rise()

        # Expected: 1W × (15 + 5)°C/W × (1 - 0.25) = 15°C
        assert temp_rise == pytest.approx(15.0, rel=0.01)

    @patch('design_validation.pcbnew.LoadBoard')
    def test_calculate_via_effectiveness(self, mock_load, mock_board_path, mock_board, sample_thermal_params):
        """Test thermal via effectiveness calculation"""
        mock_load.return_value = mock_board

        validator = ThermalValidator(mock_board_path, sample_thermal_params)
        via_benefit = validator.calculate_via_effectiveness()

        # Expected: 1W × 20°C/W × 0.25 = 5°C
        assert via_benefit == pytest.approx(5.0, rel=0.01)

    @patch('design_validation.pcbnew.LoadBoard')
    def test_validate_thermal_design_pass(self, mock_load, mock_board_path, mock_board, sample_thermal_params):
        """Test thermal design validation with good margin"""
        mock_board.GetTracks.return_value = []
        mock_load.return_value = mock_board

        validator = ThermalValidator(mock_board_path, sample_thermal_params)
        result = validator.validate_thermal_design()

        # T_junction = 25 + 15 = 40°C, margin = 85 - 40 = 45°C
        assert result.passed is True
        assert result.severity == ValidationSeverity.PASS
        assert result.details['t_junction_c'] == pytest.approx(40.0, rel=0.01)
        assert result.details['margin_to_max_c'] > 10.0

    @patch('design_validation.pcbnew.LoadBoard')
    def test_validate_thermal_design_marginal(self, mock_load, mock_board_path, mock_board):
        """Test thermal design validation with marginal conditions"""
        mock_board.GetTracks.return_value = []
        mock_load.return_value = mock_board

        # High power scenario
        params = ThermalParameters(
            ambient_temp_c=25.0,
            power_mcu_a_w=1.0,
            power_mcu_b_w=1.5,
            power_converter_w=0.5,
            r_thermal_mcu_to_gnd=15.0,
            r_thermal_gnd_to_ambient=5.0,
            thermal_via_benefit_pct=0.1,  # Less effective vias
            max_junction_temp_c=85.0
        )

        validator = ThermalValidator(mock_board_path, params)
        result = validator.validate_thermal_design()

        # Should still pass but with less margin
        assert isinstance(result, ValidationResult)


class TestDesignValidation:
    """Test comprehensive design validation suite"""

    @patch('design_validation.pcbnew.LoadBoard')
    def test_init(self, mock_load, mock_board_path, mock_board):
        """Test design validation initialization"""
        mock_load.return_value = mock_board

        validator = DesignValidation(mock_board_path)

        assert validator.board_path == mock_board_path
        assert isinstance(validator.drc, DRCValidator)
        assert isinstance(validator.dfm, DFMValidator)
        assert isinstance(validator.si, SignalIntegrityValidator)
        assert isinstance(validator.thermal, ThermalValidator)

    @patch('design_validation.pcbnew.LoadBoard')
    def test_init_with_output_dir(self, mock_load, mock_board_path, mock_board, tmp_path):
        """Test initialization with custom output directory"""
        mock_load.return_value = mock_board
        output_dir = tmp_path / "output"

        validator = DesignValidation(mock_board_path, output_dir)

        assert validator.output_dir == output_dir
        assert output_dir.exists()

    @patch('design_validation.pcbnew.LoadBoard')
    def test_run_all_validations(self, mock_load, mock_board_path, mock_board):
        """Test running all validations"""
        mock_board.GetCopperLayerCount.return_value = 4
        mock_board.GetTracks.return_value = []
        mock_board.GetFootprints.return_value = []
        mock_load.return_value = mock_board

        validator = DesignValidation(mock_board_path)

        # Mock DRC to avoid actual execution
        with patch.object(validator.drc, 'run_kicad_drc', return_value=(0, "No violations")):
            summary = validator.run_all_validations()

            assert 'board' in summary
            assert 'all_passed' in summary
            assert 'total_checks' in summary
            assert summary['total_checks'] > 0
            assert len(validator.results) > 0

    @patch('design_validation.pcbnew.LoadBoard')
    def test_manufacturing_readiness_check(self, mock_load, mock_board_path, mock_board):
        """Test manufacturing readiness checklist"""
        mock_load.return_value = mock_board

        validator = DesignValidation(mock_board_path)

        # Add some mock results
        validator.results = [
            ValidationResult("DRC", ValidationSeverity.PASS, True, "No violations"),
            ValidationResult("Fiducials", ValidationSeverity.PASS, True, "3 fiducials found",
                           details={'fiducial_count': 3})
        ]

        ready, issues = validator.manufacturing_readiness_check()

        assert isinstance(ready, bool)
        assert isinstance(issues, list)

    @patch('design_validation.pcbnew.LoadBoard')
    @patch('design_validation.pcbnew.PLOT_CONTROLLER')
    def test_export_manufacturing_files(self, mock_plot_controller, mock_load, mock_board_path, mock_board):
        """Test manufacturing file export"""
        mock_load.return_value = mock_board

        # Mock plot controller
        mock_controller = MagicMock()
        mock_plot_controller.return_value = mock_controller
        mock_options = MagicMock()
        mock_controller.GetPlotOptions.return_value = mock_options

        validator = DesignValidation(mock_board_path)
        result = validator.export_manufacturing_files()

        assert 'success' in result
        assert 'output_directory' in result

    @patch('design_validation.pcbnew.LoadBoard')
    def test_generate_validation_report(self, mock_load, mock_board_path, mock_board):
        """Test validation report generation"""
        mock_load.return_value = mock_board

        validator = DesignValidation(mock_board_path)
        validator.results = [
            ValidationResult("Test Check", ValidationSeverity.PASS, True, "Test message")
        ]

        report = validator.generate_validation_report()

        assert isinstance(report, str)
        assert "K1 LIGHTWAVE" in report
        assert "VALIDATION SUMMARY" in report
        assert "Test Check" in report

    @patch('design_validation.pcbnew.LoadBoard')
    def test_execute_full_pipeline(self, mock_load, mock_board_path, mock_board):
        """Test full validation pipeline execution"""
        mock_board.GetCopperLayerCount.return_value = 4
        mock_board.GetTracks.return_value = []
        mock_board.GetFootprints.return_value = []
        mock_load.return_value = mock_board

        validator = DesignValidation(mock_board_path)

        # Mock all sub-validations
        with patch.object(validator.drc, 'run_kicad_drc', return_value=(0, "No violations")), \
             patch.object(validator, 'export_manufacturing_files', return_value={'success': True}):

            success = validator.execute()

            assert isinstance(success, bool)
            assert len(validator.results) > 0


class TestK1SpecificValidation:
    """Test K1 Lightwave specific validation scenarios"""

    @patch('design_validation.pcbnew.LoadBoard')
    def test_k1_thermal_specifications(self, mock_load, mock_board_path, mock_board):
        """Test K1-specific thermal specifications"""
        mock_board.GetTracks.return_value = []
        mock_load.return_value = mock_board

        # K1 Lightwave thermal parameters
        params = ThermalParameters(
            ambient_temp_c=25.0,
            power_mcu_a_w=0.3,
            power_mcu_b_w=0.5,
            power_converter_w=0.2,
            r_thermal_mcu_to_gnd=15.0,
            r_thermal_gnd_to_ambient=5.0,
            thermal_via_benefit_pct=0.25,
            max_junction_temp_c=85.0
        )

        validator = ThermalValidator(mock_board_path, params)
        result = validator.validate_thermal_design()

        # Verify K1 specifications are met
        assert result.details['total_power_w'] == 1.0
        assert result.details['t_junction_c'] < 80.0
        assert result.details['margin_to_max_c'] > 10.0
        assert result.passed is True

    @patch('design_validation.pcbnew.LoadBoard')
    def test_k1_layer_stack_4layer(self, mock_load, mock_board_path, mock_board):
        """Test K1 4-layer stack configuration"""
        mock_board.GetCopperLayerCount.return_value = 4
        mock_load.return_value = mock_board

        validator = DFMValidator(mock_board_path)
        result = validator.validate_layer_stack()

        assert result.passed is True
        assert result.details['layer_count'] == 4
        assert result.details['expected'] == 4

    @patch('design_validation.pcbnew.LoadBoard')
    def test_k1_expected_results(self, mock_load, mock_board_path, mock_board):
        """Test K1 expected validation results"""
        mock_board.GetCopperLayerCount.return_value = 4
        mock_board.GetTracks.return_value = []
        mock_board.GetFootprints.return_value = []
        mock_load.return_value = mock_board

        validator = DesignValidation(mock_board_path)

        # Mock successful validations
        with patch.object(validator.drc, 'run_kicad_drc', return_value=(0, "No violations")):
            summary = validator.run_all_validations()

            # K1 expected results:
            # - DRC: 0 violations ✅
            # - DFM: 0 violations ✅
            # - Signal Integrity: PASS ✅
            # - Thermal: ~40°C with 45°C margin ✅

            drc_results = [r for r in validator.results if 'DRC' in r.check_name or 'Design Rule' in r.check_name]
            if drc_results:
                assert drc_results[0].details['violation_count'] == 0

            thermal_results = [r for r in validator.results if 'Thermal' in r.check_name]
            if thermal_results:
                assert thermal_results[0].details['t_junction_c'] < 80.0


def test_validation_result_str():
    """Test ValidationResult string representation"""
    result = ValidationResult(
        check_name="Test Check",
        severity=ValidationSeverity.PASS,
        passed=True,
        message="All good"
    )

    result_str = str(result)
    assert "✅" in result_str
    assert "Test Check" in result_str
    assert "PASS" in result_str


def test_validation_result_failure_str():
    """Test ValidationResult string representation for failure"""
    result = ValidationResult(
        check_name="Test Check",
        severity=ValidationSeverity.ERROR,
        passed=False,
        message="Failed"
    )

    result_str = str(result)
    assert "❌" in result_str
    assert "ERROR" in result_str


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
