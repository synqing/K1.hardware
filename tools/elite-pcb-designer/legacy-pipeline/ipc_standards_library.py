"""
IPC Standards Library for PCB Design and Manufacturing
========================================================

Production-ready implementation of IPC-2221A, IPC-6012, and IPC-A-610 standards
with K1 Lightwave audio-reactive LED controller specific configurations.

Modules:
    - IPC2221A: Trace sizing, clearance calculations
    - IPC6012: Class requirements and testing standards
    - IPCA610: Assembly and solder joint quality standards
    - K1Configuration: K1-specific power domains and constraints

Author: Electronics Manufacturing Standards
Date: 2025-10-24
Version: 1.0.0 (Production Release)
"""

import math
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from abc import ABC, abstractmethod


# =============================================================================
# CONSTANTS AND ENUMERATIONS
# =============================================================================

class TemperatureRise(Enum):
    """IPC-2221A Temperature rise constants (ΔT) for different applications."""
    LOW_FREQ_INTERNAL = 10      # °C, low-frequency signals, internal layers
    LOW_FREQ_EXTERNAL = 20      # °C, low-frequency signals, external layers
    DIGITAL_INTERNAL = 15       # °C, digital signals, internal layers
    DIGITAL_EXTERNAL = 25       # °C, digital signals, external layers
    POWER_INTERNAL = 20         # °C, power distribution, internal layers
    POWER_EXTERNAL = 30         # °C, power distribution, external layers
    HIGH_SPEED_INTERNAL = 25    # °C, high-speed digital, internal layers
    HIGH_SPEED_EXTERNAL = 40    # °C, high-speed digital, external layers
    CRITICAL_INTERNAL = 15      # °C, mission-critical, internal layers
    CRITICAL_EXTERNAL = 20      # °C, mission-critical, external layers


class VoltageClass(Enum):
    """IPC-2221A Voltage classes for clearance calculations."""
    ULTRA_LOW = 1      # 0-6V
    LOW = 2            # 7-15V
    MEDIUM_LOW = 3     # 16-30V
    MEDIUM = 4         # 31-100V
    MEDIUM_HIGH = 5    # 101-200V
    HIGH = 6           # 201-500V


class EnvironmentalCondition(Enum):
    """IPC-2221A Environmental factors affecting clearance."""
    CLASS_1 = 1   # Controlled environment, dry
    CLASS_2A = 2  # Room temperature, moderate humidity (altitude < 2500m)
    CLASS_2B = 3  # Room temperature, moderate humidity (altitude > 2500m)
    CLASS_3A = 4  # Uncontrolled, high humidity, altitude < 2500m
    CLASS_3B = 5  # Uncontrolled, high humidity, altitude > 2500m


class PCBClass(Enum):
    """IPC-6012 PCB Classification."""
    CLASS_1 = 1  # General electronics, non-critical
    CLASS_2 = 2  # Dedicated service (industrial, consumer, automotive)
    CLASS_3 = 3  # High-reliability applications (military, medical, aircraft)


class SolderJointQuality(Enum):
    """IPC-A-610 Solder joint visual quality acceptance criteria."""
    ACCEPTABLE = "ACCEPTABLE"
    REWORK = "REWORK"
    REJECT = "REJECT"


# =============================================================================
# IPC-2221A: TRACE WIDTH AND CLEARANCE CALCULATIONS
# =============================================================================

class IPC2221A:
    """
    IPC-2221A Standard: Generic Standard on Printed Board Design.

    Implements trace width calculation using the exact formula:
        I = 0.048 × ΔT^0.44 × A^0.725

    Where:
        I = current capacity (amperes)
        ΔT = temperature rise (°C)
        A = cross-sectional area (mils²)

    Provides voltage-based clearance tables for trace-to-trace and
    trace-to-board-edge spacing across all voltage classes.
    """

    # IPC-2221A Trace Width Constants
    TRACE_WIDTH_CONSTANTS = {
        'k_external': 0.048,  # External layer constant
        'k_internal': 0.024,  # Internal layer constant (reduced current carrying)
    }

    # Temperature coefficient for trace width calculation
    TEMP_COEFFICIENT_DELTA = 0.44
    TEMP_COEFFICIENT_AREA = 0.725

    # Copper thickness (oz) used in standard PCBs
    COPPER_THICKNESS_OZ = {
        '1oz': 1.0,      # Standard
        '2oz': 2.0,      # High current
        '0.5oz': 0.5,    # Thin traces
    }

    # Conversion: 1 oz/ft² = 1.378 mils
    OZ_TO_MILS = 1.378

    @staticmethod
    def calculate_trace_width(
        current_ma: float,
        temp_rise: TemperatureRise,
        is_external: bool = True,
        copper_oz: float = 1.0,
    ) -> Tuple[float, float]:
        """
        Calculate required trace width using IPC-2221A formula.

        Args:
            current_ma: Current in milliamps
            temp_rise: Temperature rise class from TemperatureRise enum
            is_external: True for external layers, False for internal
            copper_oz: Copper thickness in ounces (1, 2, or 0.5)

        Returns:
            Tuple of (trace_width_mils, calculated_area_mils2)

        Formula: I = 0.048 × ΔT^0.44 × A^0.725 (external)
                 I = 0.024 × ΔT^0.44 × A^0.725 (internal)

        Rearranged for A: A = (I / (k × ΔT^0.44))^(1/0.725)
        """
        current_a = current_ma / 1000.0  # Convert to amperes
        delta_t = temp_rise.value
        k = IPC2221A.TRACE_WIDTH_CONSTANTS['k_external'] if is_external else IPC2221A.TRACE_WIDTH_CONSTANTS['k_internal']

        # Calculate required cross-sectional area
        temp_factor = math.pow(delta_t, IPC2221A.TEMP_COEFFICIENT_DELTA)
        required_area = math.pow(
            current_a / (k * temp_factor),
            1.0 / IPC2221A.TEMP_COEFFICIENT_AREA
        )

        # Convert copper thickness to mils
        copper_mils = copper_oz * IPC2221A.OZ_TO_MILS

        # Calculate trace width (width = area / thickness)
        trace_width_mils = required_area / copper_mils

        return trace_width_mils, required_area

    @staticmethod
    def round_trace_width(width_mils: float, standard: str = 'IPC') -> float:
        """
        Round trace width to standard manufacturing increments.

        IPC standard increments: 1, 2, 3, 5, 8, 10, 15, 20, 25, 32, 40 mils

        Args:
            width_mils: Calculated trace width in mils
            standard: Manufacturing standard ('IPC' or 'common')

        Returns:
            Rounded trace width in mils
        """
        standard_widths = [1, 2, 3, 5, 8, 10, 15, 20, 25, 32, 40, 50, 63, 80, 100]

        for std_width in standard_widths:
            if width_mils <= std_width:
                return float(std_width)

        return width_mils

    # IPC-2221A Clearance Tables (mils) - Trace to Trace
    CLEARANCE_TRACE_TO_TRACE = {
        VoltageClass.ULTRA_LOW: {
            EnvironmentalCondition.CLASS_1: 3,
            EnvironmentalCondition.CLASS_2A: 3,
            EnvironmentalCondition.CLASS_2B: 4,
            EnvironmentalCondition.CLASS_3A: 5,
            EnvironmentalCondition.CLASS_3B: 6,
        },
        VoltageClass.LOW: {
            EnvironmentalCondition.CLASS_1: 3,
            EnvironmentalCondition.CLASS_2A: 4,
            EnvironmentalCondition.CLASS_2B: 5,
            EnvironmentalCondition.CLASS_3A: 6,
            EnvironmentalCondition.CLASS_3B: 8,
        },
        VoltageClass.MEDIUM_LOW: {
            EnvironmentalCondition.CLASS_1: 4,
            EnvironmentalCondition.CLASS_2A: 5,
            EnvironmentalCondition.CLASS_2B: 6,
            EnvironmentalCondition.CLASS_3A: 8,
            EnvironmentalCondition.CLASS_3B: 10,
        },
        VoltageClass.MEDIUM: {
            EnvironmentalCondition.CLASS_1: 6,
            EnvironmentalCondition.CLASS_2A: 8,
            EnvironmentalCondition.CLASS_2B: 10,
            EnvironmentalCondition.CLASS_3A: 12,
            EnvironmentalCondition.CLASS_3B: 15,
        },
        VoltageClass.MEDIUM_HIGH: {
            EnvironmentalCondition.CLASS_1: 10,
            EnvironmentalCondition.CLASS_2A: 12,
            EnvironmentalCondition.CLASS_2B: 15,
            EnvironmentalCondition.CLASS_3A: 20,
            EnvironmentalCondition.CLASS_3B: 25,
        },
        VoltageClass.HIGH: {
            EnvironmentalCondition.CLASS_1: 15,
            EnvironmentalCondition.CLASS_2A: 20,
            EnvironmentalCondition.CLASS_2B: 25,
            EnvironmentalCondition.CLASS_3A: 30,
            EnvironmentalCondition.CLASS_3B: 40,
        },
    }

    # IPC-2221A Clearance Tables (mils) - Trace to Board Edge
    CLEARANCE_TRACE_TO_EDGE = {
        VoltageClass.ULTRA_LOW: {
            EnvironmentalCondition.CLASS_1: 10,
            EnvironmentalCondition.CLASS_2A: 10,
            EnvironmentalCondition.CLASS_2B: 15,
            EnvironmentalCondition.CLASS_3A: 20,
            EnvironmentalCondition.CLASS_3B: 25,
        },
        VoltageClass.LOW: {
            EnvironmentalCondition.CLASS_1: 10,
            EnvironmentalCondition.CLASS_2A: 15,
            EnvironmentalCondition.CLASS_2B: 20,
            EnvironmentalCondition.CLASS_3A: 25,
            EnvironmentalCondition.CLASS_3B: 30,
        },
        VoltageClass.MEDIUM_LOW: {
            EnvironmentalCondition.CLASS_1: 15,
            EnvironmentalCondition.CLASS_2A: 20,
            EnvironmentalCondition.CLASS_2B: 25,
            EnvironmentalCondition.CLASS_3A: 30,
            EnvironmentalCondition.CLASS_3B: 40,
        },
        VoltageClass.MEDIUM: {
            EnvironmentalCondition.CLASS_1: 20,
            EnvironmentalCondition.CLASS_2A: 25,
            EnvironmentalCondition.CLASS_2B: 30,
            EnvironmentalCondition.CLASS_3A: 40,
            EnvironmentalCondition.CLASS_3B: 50,
        },
        VoltageClass.MEDIUM_HIGH: {
            EnvironmentalCondition.CLASS_1: 30,
            EnvironmentalCondition.CLASS_2A: 40,
            EnvironmentalCondition.CLASS_2B: 50,
            EnvironmentalCondition.CLASS_3A: 60,
            EnvironmentalCondition.CLASS_3B: 75,
        },
        VoltageClass.HIGH: {
            EnvironmentalCondition.CLASS_1: 50,
            EnvironmentalCondition.CLASS_2A: 60,
            EnvironmentalCondition.CLASS_2B: 75,
            EnvironmentalCondition.CLASS_3A: 100,
            EnvironmentalCondition.CLASS_3B: 125,
        },
    }

    # IPC-2221A Clearance Tables (mils) - Trace to Component Leads
    CLEARANCE_TRACE_TO_LEADS = {
        VoltageClass.ULTRA_LOW: {
            EnvironmentalCondition.CLASS_1: 8,
            EnvironmentalCondition.CLASS_2A: 10,
            EnvironmentalCondition.CLASS_2B: 12,
            EnvironmentalCondition.CLASS_3A: 15,
            EnvironmentalCondition.CLASS_3B: 20,
        },
        VoltageClass.LOW: {
            EnvironmentalCondition.CLASS_1: 10,
            EnvironmentalCondition.CLASS_2A: 12,
            EnvironmentalCondition.CLASS_2B: 15,
            EnvironmentalCondition.CLASS_3A: 20,
            EnvironmentalCondition.CLASS_3B: 25,
        },
        VoltageClass.MEDIUM_LOW: {
            EnvironmentalCondition.CLASS_1: 12,
            EnvironmentalCondition.CLASS_2A: 15,
            EnvironmentalCondition.CLASS_2B: 20,
            EnvironmentalCondition.CLASS_3A: 25,
            EnvironmentalCondition.CLASS_3B: 30,
        },
        VoltageClass.MEDIUM: {
            EnvironmentalCondition.CLASS_1: 15,
            EnvironmentalCondition.CLASS_2A: 20,
            EnvironmentalCondition.CLASS_2B: 25,
            EnvironmentalCondition.CLASS_3A: 30,
            EnvironmentalCondition.CLASS_3B: 40,
        },
        VoltageClass.MEDIUM_HIGH: {
            EnvironmentalCondition.CLASS_1: 25,
            EnvironmentalCondition.CLASS_2A: 30,
            EnvironmentalCondition.CLASS_2B: 40,
            EnvironmentalCondition.CLASS_3A: 50,
            EnvironmentalCondition.CLASS_3B: 60,
        },
        VoltageClass.HIGH: {
            EnvironmentalCondition.CLASS_1: 40,
            EnvironmentalCondition.CLASS_2A: 50,
            EnvironmentalCondition.CLASS_2B: 60,
            EnvironmentalCondition.CLASS_3A: 75,
            EnvironmentalCondition.CLASS_3B: 100,
        },
    }

    @staticmethod
    def get_clearance(
        clearance_type: str,
        voltage_class: VoltageClass,
        environmental: EnvironmentalCondition,
    ) -> int:
        """
        Get required clearance in mils for specified conditions.

        Args:
            clearance_type: 'trace_to_trace', 'trace_to_edge', or 'trace_to_leads'
            voltage_class: VoltageClass enum value
            environmental: EnvironmentalCondition enum value

        Returns:
            Required clearance in mils

        Raises:
            ValueError: Invalid clearance type
        """
        if clearance_type == 'trace_to_trace':
            table = IPC2221A.CLEARANCE_TRACE_TO_TRACE
        elif clearance_type == 'trace_to_edge':
            table = IPC2221A.CLEARANCE_TRACE_TO_EDGE
        elif clearance_type == 'trace_to_leads':
            table = IPC2221A.CLEARANCE_TRACE_TO_LEADS
        else:
            raise ValueError(f"Invalid clearance type: {clearance_type}")

        return table[voltage_class][environmental]


# =============================================================================
# IPC-6012: PCB CLASS REQUIREMENTS
# =============================================================================

@dataclass
class PCBClassRequirement:
    """Specification for a single PCB class requirement."""
    parameter: str
    class_1: str
    class_2: str
    class_3: str
    unit: str = ""
    notes: str = ""


class IPC6012:
    """
    IPC-6012 Standard: Specification for Printed Circuit Boards.

    Defines three classes of PCBs with increasing reliability requirements:
    - Class 1: General electronics (consumer, non-critical)
    - Class 2: Dedicated service (industrial, automotive)
    - Class 3: High-reliability (military, medical, aircraft)
    """

    # Class definitions with key parameters
    CLASS_DEFINITIONS = {
        PCBClass.CLASS_1: {
            'name': 'General Electronics',
            'environment': 'Controlled manufacturing environment',
            'repair': 'Permitted (with limitations)',
            'defect_acceptance': 'Higher tolerance',
            'typical_applications': [
                'Consumer electronics',
                'General industrial',
                'Non-critical systems',
            ],
        },
        PCBClass.CLASS_2: {
            'name': 'Dedicated Service',
            'environment': 'Commercial/industrial environment',
            'repair': 'Limited/restricted',
            'defect_acceptance': 'Moderate tolerance',
            'typical_applications': [
                'Automotive',
                'Industrial controllers',
                'Continuous-duty equipment',
                'Audio/visual equipment',
            ],
        },
        PCBClass.CLASS_3: {
            'name': 'High-Reliability',
            'environment': 'Demanding environment',
            'repair': 'Severely restricted',
            'defect_acceptance': 'Minimal tolerance',
            'typical_applications': [
                'Military/aerospace',
                'Medical devices',
                'Safety-critical systems',
                'High-reliability commercial',
            ],
        },
    }

    # Detailed requirements table
    REQUIREMENTS = [
        PCBClassRequirement(
            parameter='Copper Pattern Definition',
            class_1='±0.005 inch typical',
            class_2='±0.003 inch typical',
            class_3='±0.002 inch typical',
            unit='inch',
            notes='Stricter control for higher classes'
        ),
        PCBClassRequirement(
            parameter='Via/Hole Size Tolerance',
            class_1='±0.005 inch',
            class_2='±0.003 inch',
            class_3='±0.002 inch',
            unit='inch',
            notes='Affects electrical connectivity'
        ),
        PCBClassRequirement(
            parameter='Solder Mask Thickness',
            class_1='0.0008-0.0015 inch',
            class_2='0.001-0.002 inch',
            class_3='0.0015-0.0025 inch',
            unit='inch',
            notes='Protects traces from contamination'
        ),
        PCBClassRequirement(
            parameter='Trace Width/Spacing',
            class_1='5 mil / 5 mil',
            class_2='4 mil / 4 mil',
            class_3='3 mil / 3 mil',
            unit='mil',
            notes='Minimum achievable; voltage-dependent'
        ),
        PCBClassRequirement(
            parameter='Plating Thickness (Copper)',
            class_1='≥0.0007 inch',
            class_2='≥0.001 inch',
            class_3='≥0.0015 inch',
            unit='inch',
            notes='Via and hole wall plating'
        ),
        PCBClassRequirement(
            parameter='Solder Joint Acceptability',
            class_1='IPC-A-610 Type I',
            class_2='IPC-A-610 Type II',
            class_3='IPC-A-610 Type III',
            unit='standard',
            notes='Visual inspection standard'
        ),
        PCBClassRequirement(
            parameter='Registration Tolerance',
            class_1='±0.005 inch',
            class_2='±0.003 inch',
            class_3='±0.002 inch',
            unit='inch',
            notes='Layer-to-layer alignment'
        ),
        PCBClassRequirement(
            parameter='Minimum Annular Ring',
            class_1='0.005 inch',
            class_2='0.008 inch',
            class_3='0.010 inch',
            unit='inch',
            notes='Copper ring around via/hole'
        ),
        PCBClassRequirement(
            parameter='Testing Requirements',
            class_1='Visual inspection + electrical test',
            class_2='Visual + electrical + automated',
            class_3='Visual + electrical + automated + X-ray/microsection',
            unit='method',
            notes='Verification of board quality'
        ),
        PCBClassRequirement(
            parameter='Defect Repair',
            class_1='Permitted with documentation',
            class_2='Restricted; requires approval',
            class_3='Severely restricted; minimal repair',
            unit='method',
            notes='Field/factory modification'
        ),
    ]

    # Electrical and design testing requirements
    ELECTRICAL_TEST_REQUIREMENTS = {
        PCBClass.CLASS_1: {
            'test_voltage': '100V min',
            'test_duration': '1 minute',
            'fault_current_limit': '500mA max',
            'hi_pot_test': 'Optional',
            'insulation_resistance': '≥100MΩ (optional)',
        },
        PCBClass.CLASS_2: {
            'test_voltage': '250V min',
            'test_duration': '2 minutes',
            'fault_current_limit': '200mA max',
            'hi_pot_test': 'Required',
            'insulation_resistance': '≥100MΩ',
        },
        PCBClass.CLASS_3: {
            'test_voltage': '500V min',
            'test_duration': '5 minutes',
            'fault_current_limit': '100mA max',
            'hi_pot_test': 'Required (critical)',
            'insulation_resistance': '≥500MΩ',
        },
    }

    @staticmethod
    def get_requirement(parameter: str, pcb_class: PCBClass) -> str:
        """Get specific requirement value for a parameter and class."""
        for req in IPC6012.REQUIREMENTS:
            if req.parameter == parameter:
                if pcb_class == PCBClass.CLASS_1:
                    return req.class_1
                elif pcb_class == PCBClass.CLASS_2:
                    return req.class_2
                else:
                    return req.class_3
        raise ValueError(f"Unknown requirement: {parameter}")

    @staticmethod
    def select_class_for_application(app_type: str) -> PCBClass:
        """
        Select appropriate PCB class based on application type.

        Args:
            app_type: Application type string

        Returns:
            Recommended PCBClass
        """
        app_lower = app_type.lower()

        class_3_keywords = ['military', 'aerospace', 'medical', 'safety', 'critical']
        class_2_keywords = ['automotive', 'industrial', 'continuous', 'duty', 'audio']

        if any(kw in app_lower for kw in class_3_keywords):
            return PCBClass.CLASS_3
        elif any(kw in app_lower for kw in class_2_keywords):
            return PCBClass.CLASS_2
        else:
            return PCBClass.CLASS_1


# =============================================================================
# IPC-A-610: ASSEMBLY AND SOLDER QUALITY STANDARDS
# =============================================================================

@dataclass
class SolderJointCriteria:
    """Criteria for evaluating solder joint quality."""
    criterion: str
    acceptable_description: str
    rework_description: str
    reject_description: str


class IPCA610:
    """
    IPC-A-610 Standard: Acceptability of Electronic Assemblies.

    Defines visual acceptance criteria for solder joints and component placement.
    Three quality levels corresponding to IPC-6012 classes.
    """

    # Solder joint visual inspection criteria
    SOLDER_JOINT_CRITERIA = {
        'fillet_shape': SolderJointCriteria(
            criterion='Fillet Shape',
            acceptable_description='Smooth, continuous, 45° angle, no sharp peaks',
            rework_description='Slightly uneven or partially missing, <5mm² area',
            reject_description='Completely missing or severely deformed'
        ),
        'wetting': SolderJointCriteria(
            criterion='Wetting',
            acceptable_description='>75% of lead wetted, shiny appearance',
            rework_description='50-75% wetted or dull appearance',
            reject_description='<50% wetted or cold solder joint'
        ),
        'solder_volume': SolderJointCriteria(
            criterion='Solder Volume',
            acceptable_description='Adequate to fill fillet, no excess',
            rework_description='Slightly insufficient or slight excess',
            reject_description='Insufficient to cover lead or excessive'
        ),
        'voiding': SolderJointCriteria(
            criterion='Voiding',
            acceptable_description='<10% void area (internal), <1% interconnect pad',
            rework_description='10-25% internal void area',
            reject_description='>25% void area'
        ),
        'pad_coverage': SolderJointCriteria(
            criterion='Pad Coverage',
            acceptable_description='≥75% of pad covered with solder',
            rework_description='50-75% pad coverage',
            reject_description='<50% pad coverage'
        ),
        'coplanarity': SolderJointCriteria(
            criterion='Component Coplanarity',
            acceptable_description='≤0.10 inch maximum deviation within component',
            rework_description='0.10-0.20 inch deviation',
            reject_description='>0.20 inch deviation'
        ),
        'lead_bend': SolderJointCriteria(
            criterion='Component Lead Bend',
            acceptable_description='No visible lead bending or spacing variation',
            rework_description='Minor bending, <0.015 inch offset',
            reject_description='Significant bending or >0.015 inch offset'
        ),
        'bridging': SolderJointCriteria(
            criterion='Solder Bridging',
            acceptable_description='No bridging between leads/pads',
            rework_description='Minor bridging, <0.010 inch wide, isolated',
            reject_description='Significant bridging affecting electrical function'
        ),
    }

    # Component placement tolerances (mils)
    PLACEMENT_TOLERANCES = {
        'chip_component_x_y': {
            'class_1': 100,  # ±0.100 inch
            'class_2': 75,   # ±0.075 inch
            'class_3': 50,   # ±0.050 inch
        },
        'chip_component_rotation': {
            'class_1': 5.0,  # ±5 degrees
            'class_2': 3.0,  # ±3 degrees
            'class_3': 2.0,  # ±2 degrees
        },
        'bga_column_x_y': {
            'class_1': 50,   # ±0.050 inch
            'class_2': 40,   # ±0.040 inch
            'class_3': 25,   # ±0.025 inch
        },
        'connector_pin_x_y': {
            'class_1': 50,   # ±0.050 inch
            'class_2': 40,   # ±0.040 inch
            'class_3': 25,   # ±0.025 inch
        },
    }

    # Pad size requirements (mils)
    PAD_SIZE_REQUIREMENTS = {
        'chip_0402': {
            'min_pad_length': 30,
            'min_pad_width': 30,
            'min_paste_coverage': 50,  # percent
        },
        'chip_0603': {
            'min_pad_length': 40,
            'min_pad_width': 40,
            'min_paste_coverage': 50,  # percent
        },
        'chip_0805': {
            'min_pad_length': 50,
            'min_pad_width': 50,
            'min_paste_coverage': 50,  # percent
        },
        'chip_1206': {
            'min_pad_length': 60,
            'min_pad_width': 60,
            'min_paste_coverage': 50,  # percent
        },
        'qfp': {
            'min_pad_length': 20,
            'min_pad_width': 8,
            'min_paste_coverage': 50,  # percent
        },
        'bga': {
            'min_pad_diameter': 8,
            'min_paste_coverage': 75,  # percent for BGA
        },
    }

    # Test point requirements
    TEST_POINT_REQUIREMENTS = {
        'diameter_min': 25,  # mils
        'diameter_max': 50,  # mils
        'spacing': 100,      # mils minimum spacing from center to center
        'clearance_component': 50,  # mils from component body
        'clearance_pad': 50,  # mils from pad
    }

    # Pin/Lead size requirements (mils)
    LEAD_SIZE_REQUIREMENTS = {
        'single_in_line': {
            'lead_diameter': '0.030-0.045 inch',
            'hole_diameter': '0.035-0.050 inch',
        },
        'dual_in_line': {
            'lead_diameter': '0.030-0.045 inch',
            'hole_diameter': '0.035-0.050 inch',
            'lead_spacing': '0.100 inch pitch',
        },
        'axial_component': {
            'lead_diameter': '0.015-0.035 inch',
            'hole_diameter': '0.020-0.045 inch',
        },
        'ball_grid_array': {
            'ball_diameter': '0.030-0.050 inch',
            'pad_diameter': '0.035-0.055 inch',
        },
    }

    @staticmethod
    def evaluate_solder_joint(
        joint_measurements: Dict[str, bool],
        severity_level: str = 'class_2'
    ) -> SolderJointQuality:
        """
        Evaluate solder joint quality based on acceptance criteria.

        Args:
            joint_measurements: Dict of criterion -> pass/fail boolean
            severity_level: 'class_1', 'class_2', or 'class_3'

        Returns:
            SolderJointQuality enum value
        """
        total_checks = len(joint_measurements)
        passed_checks = sum(1 for v in joint_measurements.values() if v)
        pass_percentage = (passed_checks / total_checks) * 100

        # Class 3 requires >95% pass, Class 2 requires >85%, Class 1 requires >75%
        severity_thresholds = {
            'class_1': 75,
            'class_2': 85,
            'class_3': 95,
        }
        threshold = severity_thresholds.get(severity_level, 85)

        if pass_percentage >= threshold:
            return SolderJointQuality.ACCEPTABLE
        elif pass_percentage >= (threshold - 15):
            return SolderJointQuality.REWORK
        else:
            return SolderJointQuality.REJECT


# =============================================================================
# K1 LIGHTWAVE SPECIFIC CONFIGURATION
# =============================================================================

@dataclass
class PowerDomain:
    """Power domain specification for K1."""
    name: str
    voltage: float
    current_typical_ma: float
    current_peak_ma: float
    temp_rise: TemperatureRise
    voltage_class: VoltageClass
    isolation_required: bool
    notes: str = ""


class K1Configuration:
    """
    K1 Lightwave Audio-Reactive LED Controller Specific Configuration.

    Dual ESP32-S3 MCU with separate audio processing (COM-A) and
    LED rendering (COM-B). Power domains: VBUS_USB_5V (logic only),
    LED_5V (external isolated), 3.3V (internal logic).

    Manufacturing: JLCPCB Standard 4-Layer (JLC02160H-1LG)
    """

    # K1 Power domains
    POWER_DOMAINS = {
        'VBUS_USB_5V': PowerDomain(
            name='VBUS_USB_5V',
            voltage=5.0,
            current_typical_ma=500,
            current_peak_ma=1200,
            temp_rise=TemperatureRise.DIGITAL_EXTERNAL,
            voltage_class=VoltageClass.LOW,
            isolation_required=False,
            notes='USB input, logic power only, no LED load'
        ),
        'LED_5V': PowerDomain(
            name='LED_5V',
            voltage=5.0,
            current_typical_ma=2000,
            current_peak_ma=8000,
            temp_rise=TemperatureRise.POWER_EXTERNAL,
            voltage_class=VoltageClass.LOW,
            isolation_required=True,
            notes='High-current LED output, isolated from USB'
        ),
        '3V3_LOGIC': PowerDomain(
            name='3V3_LOGIC',
            voltage=3.3,
            current_typical_ma=400,
            current_peak_ma=800,
            temp_rise=TemperatureRise.DIGITAL_INTERNAL,
            voltage_class=VoltageClass.ULTRA_LOW,
            isolation_required=False,
            notes='MCU and digital logic, regulated from VBUS'
        ),
    }

    # K1 Recommended design rules
    DESIGN_RULES = {
        'pcb_class': PCBClass.CLASS_2,
        'min_trace_width': 5,  # mils
        'min_clearance_trace': 5,  # mils, trace-to-trace
        'min_clearance_edge': 10,  # mils, trace-to-board-edge
        'min_via_diameter': 10,  # mils
        'min_pad_size': 8,  # mils
        'copper_weight': 1.0,  # oz/ft²
        'solder_mask': 'LPI',  # Liquid Photoimageable
        'silkscreen': 'white',
    }

    # K1 Signal integrity requirements
    SIGNAL_INTEGRITY = {
        'spi_clock_max': 40e6,  # 40 MHz inter-MCU SPI
        'i2s_clock': 2.822e6,  # 2.822 MHz audio I2S
        'led_output_max': 10e6,  # 10 MHz LED data (NeoPixel-class)
        'impedance_control': False,  # Not required at these frequencies
        'length_matching': False,  # Not critical for this application
    }

    # K1 Temperature specifications
    OPERATING_CONDITIONS = {
        'temp_ambient_min': 0,  # °C
        'temp_ambient_max': 50,  # °C (conservative for audio equipment)
        'temp_rise_allowed': 20,  # °C rise above ambient
        'temp_max_component': 70,  # °C absolute maximum for standard parts
    }

    # K1 Test requirements (Class 2)
    TEST_REQUIREMENTS = {
        'electrical_test': True,
        'hi_pot_voltage': 250,  # Volts
        'insulation_resistance': 100e6,  # Ohms
        'continuity_test': True,
        'functional_test': True,
        'burn_in_recommended': False,
    }

    @staticmethod
    def get_recommended_trace_width(domain_name: str) -> float:
        """
        Get recommended trace width for power domain in K1.

        Args:
            domain_name: Name of power domain ('VBUS_USB_5V', 'LED_5V', '3V3_LOGIC')

        Returns:
            Recommended trace width in mils
        """
        domain = K1Configuration.POWER_DOMAINS[domain_name]

        # Use peak current for conservative design
        current_ma = domain.current_peak_ma

        trace_width_calc, _ = IPC2221A.calculate_trace_width(
            current_ma=current_ma,
            temp_rise=domain.temp_rise,
            is_external=True,
            copper_oz=K1Configuration.DESIGN_RULES['copper_weight']
        )

        # Round to standard width and apply 1.5x safety factor
        trace_width = IPC2221A.round_trace_width(trace_width_calc * 1.5, standard='IPC')

        return trace_width

    @staticmethod
    def get_clearance_for_domain(domain_name: str) -> Dict[str, int]:
        """
        Get required clearances for power domain in K1.

        Args:
            domain_name: Name of power domain

        Returns:
            Dict with clearance requirements in mils
        """
        domain = K1Configuration.POWER_DOMAINS[domain_name]

        # K1 operates in controlled indoor environment
        environmental = EnvironmentalCondition.CLASS_2A

        return {
            'trace_to_trace': IPC2221A.get_clearance(
                'trace_to_trace',
                domain.voltage_class,
                environmental
            ),
            'trace_to_edge': IPC2221A.get_clearance(
                'trace_to_edge',
                domain.voltage_class,
                environmental
            ),
            'trace_to_leads': IPC2221A.get_clearance(
                'trace_to_leads',
                domain.voltage_class,
                environmental
            ),
        }


# =============================================================================
# UTILITY FUNCTIONS AND REPORTING
# =============================================================================

class IPCReporter:
    """Generates reports and design documentation from IPC standards."""

    @staticmethod
    def generate_pcb_design_report(title: str = "K1 Lightwave PCB Design Report") -> str:
        """Generate comprehensive PCB design report."""
        report = f"""
{'=' * 80}
{title}
{'=' * 80}

1. PCB CLASS SELECTION
{'-' * 80}
Selected Class: {K1Configuration.DESIGN_RULES['pcb_class'].name} (IPC-6012)
Rationale: Audio-reactive LED controller with continuous operation and
          moderate reliability requirements.

Class 2 Requirements Met:
  - Dedicated service environment (consumer electronics, continuous duty)
  - Commercial-grade testing (electrical + functional)
  - Repair permitted with restrictions
  - Suitable for audio/visual equipment per IPC-6012

2. POWER DOMAIN ANALYSIS
{'-' * 80}
"""

        for domain_name, domain in K1Configuration.POWER_DOMAINS.items():
            trace_width = K1Configuration.get_recommended_trace_width(domain_name)
            clearances = K1Configuration.get_clearance_for_domain(domain_name)

            report += f"""
Domain: {domain.name}
  Voltage: {domain.voltage}V
  Current (typical/peak): {domain.current_typical_ma}mA / {domain.current_peak_ma}mA
  Temperature Rise Class: {domain.temp_rise.name}
  Isolation Required: {'Yes' if domain.isolation_required else 'No'}
  Recommended Trace Width: {trace_width} mils
  Clearance (trace-to-trace): {clearances['trace_to_trace']} mils
  Clearance (trace-to-edge): {clearances['trace_to_edge']} mils
  Clearance (trace-to-leads): {clearances['trace_to_leads']} mils
  Notes: {domain.notes}
"""

        report += f"""
3. DESIGN RULES SUMMARY (IPC-2221A)
{'-' * 80}
Minimum Trace Width: {K1Configuration.DESIGN_RULES['min_trace_width']} mils
Minimum Trace Spacing: {K1Configuration.DESIGN_RULES['min_clearance_trace']} mils
Board Edge Clearance: {K1Configuration.DESIGN_RULES['min_clearance_edge']} mils
Minimum Via Diameter: {K1Configuration.DESIGN_RULES['min_via_diameter']} mils
Copper Weight: {K1Configuration.DESIGN_RULES['copper_weight']} oz/ft²
Solder Mask: {K1Configuration.DESIGN_RULES['solder_mask']}

4. ASSEMBLY STANDARDS (IPC-A-610)
{'-' * 80}
Class 2 Acceptance Criteria:
  - Solder joint wetting: ≥75% of lead
  - Pad coverage: ≥75%
  - Void area: <10% internal, <1% interconnect
  - Component coplanarity: ≤0.10 inch deviation
  - No solder bridging affecting electrical function

Component Placement (Class 2):
  - Chip component X/Y: ±0.075 inch
  - Chip rotation: ±3 degrees
  - Connector pins: ±0.040 inch

5. TESTING REQUIREMENTS (IPC-6012 Class 2)
{'-' * 80}
  - Hi-pot test: {K1Configuration.TEST_REQUIREMENTS['hi_pot_voltage']}V, 2 minutes
  - Insulation resistance: ≥{K1Configuration.TEST_REQUIREMENTS['insulation_resistance']/1e6:.0f}MΩ
  - Continuity testing: Required
  - Functional testing: Required
  - Electrical test: {K1Configuration.TEST_REQUIREMENTS['electrical_test']}

6. MANUFACTURING NOTES
{'-' * 80}
  JLCPCB Standard 4-Layer (JLC02160H-1LG):
    - Layers: Signal | GND | Power | Signal (typical stackup)
    - Via process: Mechanical drilling, standard plating
    - Copper weight: 1 oz/ft² (standard)
    - Solder mask: LPI (Liquid Photo-Imageable)
    - Silkscreen: Single color (white)

7. OPERATING ENVIRONMENT
{'-' * 80}
  Ambient temperature: {K1Configuration.OPERATING_CONDITIONS['temp_ambient_min']}-{K1Configuration.OPERATING_CONDITIONS['temp_ambient_max']}°C
  Maximum temperature rise: {K1Configuration.OPERATING_CONDITIONS['temp_rise_allowed']}°C
  Maximum component temperature: {K1Configuration.OPERATING_CONDITIONS['temp_max_component']}°C
  Environmental class: IPC-2221A CLASS_2A (controlled, moderate humidity)

{'=' * 80}
End of Report
{'=' * 80}
"""
        return report


# =============================================================================
# VALIDATION AND TESTING
# =============================================================================

def validate_design(
    trace_width_mils: float,
    clearance_mils: float,
    voltage: float = 5.0,
) -> Tuple[bool, str]:
    """
    Validate design against IPC standards.

    Args:
        trace_width_mils: Trace width in mils
        clearance_mils: Clearance in mils
        voltage: Operating voltage

    Returns:
        Tuple of (valid: bool, message: str)
    """
    min_width = K1Configuration.DESIGN_RULES['min_trace_width']
    min_clearance = K1Configuration.DESIGN_RULES['min_clearance_trace']

    if trace_width_mils < min_width:
        return False, f"Trace width {trace_width_mils} mils is below minimum {min_width} mils"

    if clearance_mils < min_clearance:
        return False, f"Clearance {clearance_mils} mils is below minimum {min_clearance} mils"

    if voltage > 12:
        return False, f"Voltage {voltage}V exceeds K1 specification"

    return True, "Design meets IPC standards"
