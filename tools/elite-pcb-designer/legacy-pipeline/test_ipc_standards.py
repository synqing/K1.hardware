"""
Test Suite for IPC Standards Library
=====================================

Comprehensive test cases for IPC-2221A, IPC-6012, IPC-A-610,
and K1-specific implementations.

Run with: python -m pytest test_ipc_standards.py -v
"""

import unittest
import math
from ipc_standards_library import (
    IPC2221A,
    IPC6012,
    IPCA610,
    K1Configuration,
    IPCReporter,
    validate_design,
    TemperatureRise,
    VoltageClass,
    EnvironmentalCondition,
    PCBClass,
    SolderJointQuality,
)


# =============================================================================
# IPC-2221A TRACE WIDTH TESTS
# =============================================================================

class TestIPC2221ATraceWidth(unittest.TestCase):
    """Tests for IPC-2221A trace width calculations."""

    def test_trace_width_calculation_external_500ma(self):
        """Verify the trace width calculation for an external layer with 500mA current."""
        trace_width, area = IPC2221A.calculate_trace_width(
            current_ma=500,
            temp_rise=TemperatureRise.DIGITAL_EXTERNAL,
            is_external=True,
            copper_oz=1.0,
        )
        # Expected: roughly 2-3 mils for external layer, 500mA, 25°C rise
        self.assertGreater(trace_width, 1.0)
        self.assertLess(trace_width, 10.0)
        self.assertGreater(area, 0)

    def test_trace_width_calculation_internal_500ma(self):
        """Verify the trace width calculation for an internal layer with 500mA current."""
        trace_width, area = IPC2221A.calculate_trace_width(
            current_ma=500,
            temp_rise=TemperatureRise.DIGITAL_INTERNAL,
            is_external=False,
            copper_oz=1.0,
        )
        # Internal traces require larger area due to reduced constant
        self.assertGreater(trace_width, 1.0)
        self.assertLess(trace_width, 20.0)

    def test_high_current_power_trace(self):
        """Verify the trace width calculation for a high-current power trace (8A)."""
        trace_width, area = IPC2221A.calculate_trace_width(
            current_ma=8000,  # 8 amperes
            temp_rise=TemperatureRise.POWER_EXTERNAL,
            is_external=True,
            copper_oz=1.0,
        )
        # High current should result in wide trace
        self.assertGreater(trace_width, 20.0)
        print(f"8A @ 30°C rise: {trace_width:.2f} mils (area: {area:.2f} mils²)")

    def test_copper_thickness_effect(self):
        """Verify that copper thickness correctly affects the calculated trace width."""
        # 2oz copper should allow narrower traces
        width_1oz, _ = IPC2221A.calculate_trace_width(
            current_ma=1000,
            temp_rise=TemperatureRise.POWER_EXTERNAL,
            is_external=True,
            copper_oz=1.0,
        )
        width_2oz, _ = IPC2221A.calculate_trace_width(
            current_ma=1000,
            temp_rise=TemperatureRise.POWER_EXTERNAL,
            is_external=True,
            copper_oz=2.0,
        )
        # 2oz copper should result in narrower traces
        self.assertLess(width_2oz, width_1oz)
        print(f"1oz: {width_1oz:.2f} mils, 2oz: {width_2oz:.2f} mils")

    def test_trace_width_rounding(self):
        """Verify that trace widths are correctly rounded to standard values."""
        # 2.7 mils should round to 3 mils
        rounded = IPC2221A.round_trace_width(2.7)
        self.assertEqual(rounded, 3.0)

        # 15.5 mils should round to 20 mils
        rounded = IPC2221A.round_trace_width(15.5)
        self.assertEqual(rounded, 20.0)

        # 0.5 mils should round to 1 mil
        rounded = IPC2221A.round_trace_width(0.5)
        self.assertEqual(rounded, 1.0)

    def test_k1_usb_domain_trace_width(self):
        """Verify the trace width calculation for the K1's VBUS_USB_5V power domain."""
        domain = K1Configuration.POWER_DOMAINS['VBUS_USB_5V']
        trace_width, _ = IPC2221A.calculate_trace_width(
            current_ma=domain.current_peak_ma,
            temp_rise=domain.temp_rise,
            is_external=True,
        )
        trace_width_rounded = IPC2221A.round_trace_width(trace_width * 1.5)
        self.assertGreaterEqual(trace_width_rounded, K1Configuration.DESIGN_RULES['min_trace_width'])
        print(f"K1 VBUS 5V domain peak current trace: {trace_width_rounded} mils")

    def test_k1_led_domain_trace_width(self):
        """Verify the trace width calculation for the K1's high-current LED_5V power domain."""
        domain = K1Configuration.POWER_DOMAINS['LED_5V']
        trace_width, _ = IPC2221A.calculate_trace_width(
            current_ma=domain.current_peak_ma,
            temp_rise=domain.temp_rise,
            is_external=True,
        )
        trace_width_rounded = IPC2221A.round_trace_width(trace_width * 1.5)
        # LED domain with 8A peak should require very wide traces
        self.assertGreater(trace_width_rounded, 20.0)
        print(f"K1 LED 5V domain peak current trace: {trace_width_rounded} mils")


# =============================================================================
# IPC-2221A CLEARANCE TESTS
# =============================================================================

class TestIPC2221AClearance(unittest.TestCase):
    """Tests for IPC-2221A clearance calculations."""

    def test_clearance_trace_to_trace_low_voltage_class1(self):
        """Verify trace-to-trace clearance for low voltage in a Class 1 environment."""
        clearance = IPC2221A.get_clearance(
            'trace_to_trace',
            VoltageClass.LOW,
            EnvironmentalCondition.CLASS_1,
        )
        self.assertEqual(clearance, 3)

    def test_clearance_increases_with_voltage(self):
        """Verify that clearance requirements increase with higher voltage classes."""
        clearance_low = IPC2221A.get_clearance(
            'trace_to_trace',
            VoltageClass.ULTRA_LOW,
            EnvironmentalCondition.CLASS_2A,
        )
        clearance_high = IPC2221A.get_clearance(
            'trace_to_trace',
            VoltageClass.HIGH,
            EnvironmentalCondition.CLASS_2A,
        )
        self.assertLess(clearance_low, clearance_high)

    def test_clearance_increases_with_environment_severity(self):
        """Verify that clearance requirements increase in more severe environments."""
        clearance_dry = IPC2221A.get_clearance(
            'trace_to_trace',
            VoltageClass.MEDIUM,
            EnvironmentalCondition.CLASS_1,
        )
        clearance_humid = IPC2221A.get_clearance(
            'trace_to_trace',
            VoltageClass.MEDIUM,
            EnvironmentalCondition.CLASS_3B,
        )
        self.assertLess(clearance_dry, clearance_humid)

    def test_clearance_trace_to_edge_high_voltage(self):
        """Verify trace-to-board-edge clearance for high voltage applications."""
        clearance = IPC2221A.get_clearance(
            'trace_to_edge',
            VoltageClass.HIGH,
            EnvironmentalCondition.CLASS_3B,
        )
        # Should be 125 mils for highest severity
        self.assertEqual(clearance, 125)

    def test_clearance_trace_to_leads(self):
        """Verify trace-to-component-lead clearance."""
        clearance = IPC2221A.get_clearance(
            'trace_to_leads',
            VoltageClass.MEDIUM_LOW,
            EnvironmentalCondition.CLASS_2A,
        )
        self.assertEqual(clearance, 15)

    def test_k1_clearance_requirements_usb_domain(self):
        """Verify the clearance requirements for the K1's VBUS_USB_5V power domain."""
        clearances = K1Configuration.get_clearance_for_domain('VBUS_USB_5V')
        self.assertIn('trace_to_trace', clearances)
        self.assertIn('trace_to_edge', clearances)
        self.assertIn('trace_to_leads', clearances)
        # Low voltage, Class 2A environment should be relaxed
        self.assertGreaterEqual(clearances['trace_to_trace'], 3)

    def test_k1_clearance_led_domain(self):
        """Verify the clearance requirements for the K1's LED_5V power domain."""
        clearances = K1Configuration.get_clearance_for_domain('LED_5V')
        # Same voltage class as VBUS but isolated
        trace_clearance = clearances['trace_to_trace']
        self.assertGreater(trace_clearance, 0)


# =============================================================================
# IPC-6012 PCB CLASS TESTS
# =============================================================================

class TestIPC6012PCBClass(unittest.TestCase):
    """Tests for IPC-6012 PCB classification and requirements."""

    def test_class_1_characteristics(self):
        """Verify the characteristics of a Class 1 (General Electronic Products) PCB."""
        class_1_def = IPC6012.CLASS_DEFINITIONS[PCBClass.CLASS_1]
        self.assertIn('Consumer', class_1_def['typical_applications'][0])

    def test_class_2_characteristics(self):
        """Verify the characteristics of a Class 2 (Dedicated Service Electronic Products) PCB."""
        class_2_def = IPC6012.CLASS_DEFINITIONS[PCBClass.CLASS_2]
        self.assertIn('Automotive', class_2_def['typical_applications'][0])

    def test_class_3_characteristics(self):
        """Verify the characteristics of a Class 3 (High Reliability Electronic Products) PCB."""
        class_3_def = IPC6012.CLASS_DEFINITIONS[PCBClass.CLASS_3]
        self.assertIn('Military', class_3_def['typical_applications'][0])

    def test_minimum_trace_width_progression(self):
        """Verify that trace width requirements become stricter for higher PCB classes."""
        class_1_width = IPC6012.get_requirement('Trace Width/Spacing', PCBClass.CLASS_1)
        class_2_width = IPC6012.get_requirement('Trace Width/Spacing', PCBClass.CLASS_2)
        class_3_width = IPC6012.get_requirement('Trace Width/Spacing', PCBClass.CLASS_3)

        # Class 1: 5/5 mil, Class 2: 4/4 mil, Class 3: 3/3 mil
        self.assertEqual(class_1_width, '5 mil / 5 mil')
        self.assertEqual(class_2_width, '4 mil / 4 mil')
        self.assertEqual(class_3_width, '3 mil / 3 mil')

    def test_via_plating_thickness(self):
        """Verify the via plating thickness requirements for different PCB classes."""
        class_1_plating = IPC6012.get_requirement('Plating Thickness (Copper)', PCBClass.CLASS_1)
        class_3_plating = IPC6012.get_requirement('Plating Thickness (Copper)', PCBClass.CLASS_3)
        # Class 3 requires thicker plating than Class 1
        self.assertIn('0.0007', class_1_plating)
        self.assertIn('0.0015', class_3_plating)

    def test_electrical_test_voltage_progression(self):
        """Verify that hi-pot test voltage increases for higher PCB classes."""
        class_1_voltage = IPC6012.ELECTRICAL_TEST_REQUIREMENTS[PCBClass.CLASS_1]['test_voltage']
        class_2_voltage = IPC6012.ELECTRICAL_TEST_REQUIREMENTS[PCBClass.CLASS_2]['test_voltage']
        class_3_voltage = IPC6012.ELECTRICAL_TEST_REQUIREMENTS[PCBClass.CLASS_3]['test_voltage']

        self.assertEqual(class_1_voltage, '100V min')
        self.assertEqual(class_2_voltage, '250V min')
        self.assertEqual(class_3_voltage, '500V min')

    def test_select_class_automotive(self):
        """Verify that an automotive application correctly maps to PCB Class 2."""
        selected_class = IPC6012.select_class_for_application("automotive audio processor")
        self.assertEqual(selected_class, PCBClass.CLASS_2)

    def test_select_class_consumer(self):
        """Verify that a consumer application correctly maps to PCB Class 1."""
        selected_class = IPC6012.select_class_for_application("consumer gadget")
        self.assertEqual(selected_class, PCBClass.CLASS_1)

    def test_select_class_medical(self):
        """Verify that a medical application correctly maps to PCB Class 3."""
        selected_class = IPC6012.select_class_for_application("medical device control board")
        self.assertEqual(selected_class, PCBClass.CLASS_3)

    def test_k1_selected_class(self):
        """Verify that the K1 project is correctly designated as PCB Class 2."""
        selected_class = K1Configuration.DESIGN_RULES['pcb_class']
        self.assertEqual(selected_class, PCBClass.CLASS_2)


# =============================================================================
# IPC-A-610 ASSEMBLY STANDARDS TESTS
# =============================================================================

class TestIPCA610Assembly(unittest.TestCase):
    """Tests for IPC-A-610 assembly standards."""

    def test_solder_joint_criteria_defined(self):
        """Verify that all required solder joint criteria are defined."""
        required_criteria = [
            'fillet_shape',
            'wetting',
            'solder_volume',
            'voiding',
            'pad_coverage',
            'coplanarity',
            'lead_bend',
            'bridging',
        ]
        for criterion in required_criteria:
            self.assertIn(criterion, IPCA610.SOLDER_JOINT_CRITERIA)

    def test_placement_tolerance_class_1(self):
        """Verify the component placement tolerances for Class 1 assembly."""
        tolerance = IPCA610.PLACEMENT_TOLERANCES['chip_component_x_y']['class_1']
        self.assertEqual(tolerance, 100)  # ±0.100 inch

    def test_placement_tolerance_class_3(self):
        """Verify the stricter component placement tolerances for Class 3 assembly."""
        tolerance = IPCA610.PLACEMENT_TOLERANCES['chip_component_x_y']['class_3']
        self.assertEqual(tolerance, 50)  # ±0.050 inch

    def test_pad_size_0402(self):
        """Verify the minimum pad size requirements for 0402 components."""
        pad_req = IPCA610.PAD_SIZE_REQUIREMENTS['chip_0402']
        self.assertEqual(pad_req['min_pad_length'], 30)
        self.assertEqual(pad_req['min_pad_width'], 30)
        self.assertEqual(pad_req['min_paste_coverage'], 50)

    def test_pad_size_bga(self):
        """Verify the pad size requirements for BGA packages."""
        pad_req = IPCA610.PAD_SIZE_REQUIREMENTS['bga']
        self.assertEqual(pad_req['min_pad_diameter'], 8)
        self.assertEqual(pad_req['min_paste_coverage'], 75)  # Higher for BGA

    def test_test_point_requirements(self):
        """Verify the spacing and clearance requirements for test points."""
        test_point_req = IPCA610.TEST_POINT_REQUIREMENTS
        self.assertEqual(test_point_req['diameter_min'], 25)
        self.assertEqual(test_point_req['diameter_max'], 50)
        self.assertEqual(test_point_req['spacing'], 100)

    def test_solder_joint_evaluation_perfect(self):
        """Verify that a perfect solder joint is evaluated as acceptable."""
        measurements = {
            'fillet_shape': True,
            'wetting': True,
            'solder_volume': True,
            'voiding': True,
            'pad_coverage': True,
            'coplanarity': True,
            'lead_bend': True,
            'bridging': True,
        }
        result = IPCA610.evaluate_solder_joint(measurements, 'class_2')
        self.assertEqual(result, SolderJointQuality.ACCEPTABLE)

    def test_solder_joint_evaluation_rework(self):
        """Verify that a solder joint with minor defects is evaluated as requiring rework."""
        measurements = {
            'fillet_shape': True,
            'wetting': True,
            'solder_volume': False,
            'voiding': True,
            'pad_coverage': True,
            'coplanarity': True,
            'lead_bend': True,
            'bridging': True,
        }  # 7/8 pass = 87.5%
        result = IPCA610.evaluate_solder_joint(measurements, 'class_2')
        self.assertEqual(result, SolderJointQuality.ACCEPTABLE)  # Just above 85% for Class 2

    def test_solder_joint_evaluation_reject(self):
        """Verify that a solder joint with major defects is evaluated as a reject."""
        measurements = {
            'fillet_shape': False,
            'wetting': False,
            'solder_volume': True,
            'voiding': False,
            'pad_coverage': False,
            'coplanarity': True,
            'lead_bend': True,
            'bridging': True,
        }  # 4/8 pass = 50%
        result = IPCA610.evaluate_solder_joint(measurements, 'class_2')
        self.assertEqual(result, SolderJointQuality.REJECT)


# =============================================================================
# K1 CONFIGURATION TESTS
# =============================================================================

class TestK1Configuration(unittest.TestCase):
    """Tests for the K1 Lightwave project-specific configuration."""

    def test_k1_power_domains_defined(self):
        """Verify that all required power domains for the K1 project are defined."""
        required_domains = ['VBUS_USB_5V', 'LED_5V', '3V3_LOGIC']
        for domain in required_domains:
            self.assertIn(domain, K1Configuration.POWER_DOMAINS)

    def test_k1_usb_domain_properties(self):
        """Verify the properties of the VBUS_USB_5V power domain."""
        domain = K1Configuration.POWER_DOMAINS['VBUS_USB_5V']
        self.assertEqual(domain.voltage, 5.0)
        self.assertEqual(domain.current_typical_ma, 500)
        self.assertFalse(domain.isolation_required)

    def test_k1_led_domain_properties(self):
        """Verify the properties of the high-current LED_5V power domain."""
        domain = K1Configuration.POWER_DOMAINS['LED_5V']
        self.assertEqual(domain.voltage, 5.0)
        self.assertEqual(domain.current_peak_ma, 8000)
        self.assertTrue(domain.isolation_required)

    def test_k1_logic_domain_properties(self):
        """Verify the properties of the 3V3_LOGIC power domain."""
        domain = K1Configuration.POWER_DOMAINS['3V3_LOGIC']
        self.assertEqual(domain.voltage, 3.3)
        self.assertLess(domain.current_peak_ma, 1000)
        self.assertFalse(domain.isolation_required)

    def test_k1_design_rules(self):
        """Verify that the K1 project's design rules are reasonable."""
        rules = K1Configuration.DESIGN_RULES
        self.assertGreaterEqual(rules['min_trace_width'], 3)
        self.assertLessEqual(rules['min_trace_width'], 10)
        self.assertEqual(rules['pcb_class'], PCBClass.CLASS_2)

    def test_k1_trace_width_recommendation_usb(self):
        """Verify the trace width recommendation for the USB power domain."""
        width = K1Configuration.get_recommended_trace_width('VBUS_USB_5V')
        self.assertGreater(width, 0)
        self.assertLess(width, 50)

    def test_k1_trace_width_recommendation_led(self):
        """Verify the trace width recommendation for the high-current LED power domain."""
        width = K1Configuration.get_recommended_trace_width('LED_5V')
        # Should be much wider due to high peak current (8A)
        self.assertGreater(width, 20)
        print(f"K1 LED_5V recommended trace width: {width} mils")

    def test_k1_operating_conditions(self):
        """Verify that the K1's operating conditions are within reasonable limits."""
        conditions = K1Configuration.OPERATING_CONDITIONS
        self.assertEqual(conditions['temp_ambient_min'], 0)
        self.assertEqual(conditions['temp_ambient_max'], 50)
        self.assertGreater(conditions['temp_max_component'], conditions['temp_ambient_max'])

    def test_k1_signal_integrity_parameters(self):
        """Verify the signal integrity parameters for the K1 project."""
        sig_int = K1Configuration.SIGNAL_INTEGRITY
        # SPI clock should be high (inter-MCU communication)
        self.assertEqual(sig_int['spi_clock_max'], 40e6)
        # I2S clock for audio
        self.assertGreater(sig_int['i2s_clock'], 1e6)
        self.assertLess(sig_int['i2s_clock'], 10e6)

    def test_k1_test_requirements(self):
        """Verify the electrical test requirements for the K1 project (Class 2)."""
        test_reqs = K1Configuration.TEST_REQUIREMENTS
        self.assertEqual(test_reqs['hi_pot_voltage'], 250)
        self.assertEqual(test_reqs['insulation_resistance'], 100e6)
        self.assertTrue(test_reqs['electrical_test'])


# =============================================================================
# VALIDATION AND UTILITY TESTS
# =============================================================================

class TestValidationAndUtilities(unittest.TestCase):
    """Tests for validation and utility functions."""

    def test_validate_design_good(self):
        """Verify that a good design passes validation."""
        valid, message = validate_design(
            trace_width_mils=8.0,
            clearance_mils=5.0,
            voltage=3.3
        )
        self.assertTrue(valid)

    def test_validate_design_trace_too_narrow(self):
        """Verify that a design with too narrow traces fails validation."""
        valid, message = validate_design(
            trace_width_mils=2.0,
            clearance_mils=5.0,
            voltage=3.3
        )
        self.assertFalse(valid)
        self.assertIn('Trace width', message)

    def test_validate_design_clearance_too_small(self):
        """Verify that a design with insufficient clearance fails validation."""
        valid, message = validate_design(
            trace_width_mils=8.0,
            clearance_mils=2.0,
            voltage=3.3
        )
        self.assertFalse(valid)
        self.assertIn('Clearance', message)

    def test_validate_design_voltage_too_high(self):
        """Verify that a design with voltage exceeding specifications fails validation."""
        valid, message = validate_design(
            trace_width_mils=8.0,
            clearance_mils=5.0,
            voltage=24.0
        )
        self.assertFalse(valid)
        self.assertIn('Voltage', message)

    def test_ipc_reporter_generates_report(self):
        """Verify that the IPCReporter generates a complete report."""
        report = IPCReporter.generate_pcb_design_report()
        self.assertIn('K1 Lightwave PCB Design Report', report)
        self.assertIn('PCB CLASS SELECTION', report)
        self.assertIn('POWER DOMAIN ANALYSIS', report)
        self.assertIn('DESIGN RULES SUMMARY', report)


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration(unittest.TestCase):
    """Integration tests that combine multiple IPC standards."""

    def test_k1_complete_design_workflow(self):
        """Verify the complete design workflow for the K1 project."""
        # 1. Select PCB class
        pcb_class = K1Configuration.DESIGN_RULES['pcb_class']
        self.assertEqual(pcb_class, PCBClass.CLASS_2)

        # 2. Calculate trace widths for each power domain
        trace_widths = {}
        for domain_name in K1Configuration.POWER_DOMAINS.keys():
            width = K1Configuration.get_recommended_trace_width(domain_name)
            trace_widths[domain_name] = width

        # 3. Get clearance requirements
        clearances = {}
        for domain_name in K1Configuration.POWER_DOMAINS.keys():
            clearances[domain_name] = K1Configuration.get_clearance_for_domain(domain_name)

        # 4. Validate all designs
        for domain_name, width in trace_widths.items():
            valid, _ = validate_design(width, 5.0)
            self.assertTrue(valid)

        print(f"\nK1 Design Summary:")
        print(f"  PCB Class: {pcb_class.name}")
        for domain_name, width in trace_widths.items():
            print(f"  {domain_name}: {width} mils trace width")

    def test_trace_width_vs_current_scaling(self):
        """Verify that the calculated trace width scales correctly with current."""
        currents = [100, 500, 1000, 2000, 5000]
        widths = []

        for current_ma in currents:
            width, _ = IPC2221A.calculate_trace_width(
                current_ma=current_ma,
                temp_rise=TemperatureRise.POWER_EXTERNAL,
                is_external=True,
            )
            widths.append(width)

        # Verify monotonic increase (more current = wider trace)
        for i in range(len(widths) - 1):
            self.assertLess(widths[i], widths[i + 1])

        print(f"\nCurrent to Trace Width Scaling:")
        for current, width in zip(currents, widths):
            print(f"  {current}mA: {width:.2f} mils")

    def test_copper_thickness_impact(self):
        """Verify the impact of copper thickness on trace width calculations."""
        current_ma = 2000

        results = {}
        for oz in [0.5, 1.0, 2.0]:
            width, _ = IPC2221A.calculate_trace_width(
                current_ma=current_ma,
                temp_rise=TemperatureRise.POWER_EXTERNAL,
                is_external=True,
                copper_oz=oz,
            )
            results[oz] = IPC2221A.round_trace_width(width)

        # Verify that thicker copper allows narrower traces
        self.assertGreater(results[0.5], results[1.0])
        self.assertGreater(results[1.0], results[2.0])

        print(f"\nCopper Thickness Impact ({current_ma}mA):")
        for oz, width in results.items():
            print(f"  {oz}oz: {width} mils")


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)
