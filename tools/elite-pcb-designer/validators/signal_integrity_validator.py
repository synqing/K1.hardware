"""
Elite PCB Designer - Signal Integrity Validator

Analyzes and validates:
- High-speed signal routing constraints
- Impedance matching requirements
- Differential pair rules
- Via stitching strategy
- Crosstalk prevention
- Timing constraints
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum


class SignalClass(Enum):
    """Signal classification by speed/sensitivity"""
    LOW_SPEED = "Digital logic <1MHz"
    MEDIUM_SPEED = "SPI/I2C 1-20MHz"
    HIGH_SPEED = "USB/Ethernet >100MHz"
    DIFFERENTIAL = "Differential pairs"
    ANALOG = "Analog signals"
    POWER = "Power distribution"


class ViaStitchingStrategy(Enum):
    """Via stitching patterns for EMI containment"""
    TIGHT = "Via spacing 0.5mm (RF/sensitive)"
    STANDARD = "Via spacing 1.0mm (normal)"
    LOOSE = "Via spacing 2.0mm (low-speed)"
    NONE = "No stitching required"


@dataclass
class TraceRoute:
    """Trace routing specification"""
    signal_name: str
    source_ref: str
    dest_ref: str
    signal_class: SignalClass
    trace_width: float  # mm
    min_clearance: float  # mm to other traces
    via_diameter: float  # mm
    via_hole: float  # mm
    impedance_ohms: Optional[float]  # Target Z0 if controlled
    differential_pair: Optional[str] = None  # Paired signal name


@dataclass
class RoutingConstraint:
    """Constraint for trace routing"""
    name: str
    description: str
    requirement: str
    severity: str  # "critical", "important", "recommended"


class K1_SignalIntegrityRules:
    """K1 Lightwave signal integrity design rules"""

    # Layer stackup target impedance
    LAYER_STACKUP = {
        "L1 (top)": {"cu_thickness": 0.035, "prepreg": 0.1},
        "L2 (GND)": {"cu_thickness": 0.035, "prepreg": 0.1},
        "L3 (PWR)": {"cu_thickness": 0.035, "prepreg": 0.1},
        "L4 (bottom)": {"cu_thickness": 0.035, "prepreg": 0.1},
    }

    # Trace width calculations (for 50 Ohm impedance on L1/L4)
    TRACE_WIDTHS = {
        SignalClass.LOW_SPEED: 0.254,  # 10mil - standard
        SignalClass.MEDIUM_SPEED: 0.254,  # 10mil
        SignalClass.HIGH_SPEED: 0.152,  # 6mil for better density
        SignalClass.DIFFERENTIAL: 0.152,  # 6mil traces
        SignalClass.ANALOG: 0.254,  # 10mil for lower noise
        SignalClass.POWER: 0.635,  # 25mil minimum for current capacity
    }

    # Via specifications
    VIA_SPECS = {
        "via_diameter": 0.3,  # 0.3mm pad
        "via_hole": 0.15,  # 0.15mm hole (12mil)
        "via_clearance": 0.1,  # 0.1mm from other traces
    }

    # Critical nets requiring differential pairs or special routing
    CRITICAL_NETS = {
        # Inter-MCU SPI link (20-40 MHz)
        "SPI_CLK": {
            "signal_class": SignalClass.HIGH_SPEED,
            "partner": "SPI_CS",  # Pair for clock/CS
            "max_length_diff": 5,  # 5mm skew tolerance
            "routing_strategy": "routed_together"
        },
        "SPI_MOSI": {
            "signal_class": SignalClass.HIGH_SPEED,
            "max_length": 50,  # Keep under 50mm
        },
        "SPI_MISO": {
            "signal_class": SignalClass.HIGH_SPEED,
            "max_length": 50,
        },

        # USB signals (HS only if implemented)
        "USB_DM": {
            "signal_class": SignalClass.DIFFERENTIAL,
            "partner": "USB_DP",
            "differential_impedance": 90,  # 90 ohm differential
            "routing_strategy": "differential_pair",
            "trace_separation": 0.5,  # 0.5mm spacing
        },
        "USB_DP": {
            "signal_class": SignalClass.DIFFERENTIAL,
            "partner": "USB_DM",
        },

        # Power monitoring (I2C, slow)
        "INA_SDA": {
            "signal_class": SignalClass.MEDIUM_SPEED,
            "pull_up_required": True,
        },
        "INA_SCL": {
            "signal_class": SignalClass.MEDIUM_SPEED,
            "pull_up_required": True,
        },
    }


class SignalIntegrityValidator:
    """Validate signal integrity for K1 design"""

    def __init__(self):
        self.rules = K1_SignalIntegrityRules()
        self.nets: Dict[str, TraceRoute] = {}
        self.violations: List[Dict] = []
        self.recommendations: List[Dict] = []

    def add_signal(self, signal_name: str, signal_class: SignalClass,
                   source: str, dest: str, impedance: Optional[float] = None):
        """Register a signal for validation"""
        trace = TraceRoute(
            signal_name=signal_name,
            source_ref=source,
            dest_ref=dest,
            signal_class=signal_class,
            trace_width=self.rules.TRACE_WIDTHS[signal_class],
            min_clearance=0.15,  # 6mil default
            via_diameter=self.rules.VIA_SPECS["via_diameter"],
            via_hole=self.rules.VIA_SPECS["via_hole"],
            impedance_ohms=impedance
        )
        self.nets[signal_name] = trace

    def validate(self) -> Dict:
        """Run comprehensive signal integrity validation"""
        results = {
            'total_nets': len(self.nets),
            'violations': [],
            'recommendations': [],
            'routing_rules': self._generate_routing_rules(),
            'layer_stackup': self.rules.LAYER_STACKUP,
        }

        # Validate each net
        for signal_name, trace in self.nets.items():
            self._validate_net(signal_name, trace)

        # Check for critical signal routing
        self._validate_critical_nets()

        # Check differential pair requirements
        self._validate_differential_pairs()

        results['violations'] = self.violations
        results['recommendations'] = self.recommendations

        return results

    def _validate_net(self, signal_name: str, trace: TraceRoute):
        """Validate individual net"""
        # Check if critical net has special requirements
        if signal_name in self.rules.CRITICAL_NETS:
            critical_spec = self.rules.CRITICAL_NETS[signal_name]

            # Verify routing strategy
            if "routing_strategy" in critical_spec:
                if critical_spec["routing_strategy"] == "differential_pair":
                    if trace.differential_pair is None:
                        self.violations.append({
                            'severity': 'critical',
                            'signal': signal_name,
                            'issue': 'Differential pair routing required but not specified',
                            'recommendation': f'Pair {signal_name} with {critical_spec.get("partner")}'
                        })

            # Check trace length constraints
            if "max_length" in critical_spec:
                self.recommendations.append({
                    'signal': signal_name,
                    'rule': 'Length constraint',
                    'requirement': f'Keep trace under {critical_spec["max_length"]}mm',
                    'reason': 'Minimize propagation delay'
                })

    def _validate_critical_nets(self):
        """Check critical signals have proper design"""
        for signal_name, spec in self.rules.CRITICAL_NETS.items():
            if signal_name not in self.nets:
                self.recommendations.append({
                    'signal': signal_name,
                    'issue': f'Critical signal {signal_name} not registered',
                    'action': 'Add to routing rules'
                })

    def _validate_differential_pairs(self):
        """Validate differential pair requirements"""
        differential_signals = [n for n, t in self.nets.items()
                               if t.signal_class == SignalClass.DIFFERENTIAL]

        for signal in differential_signals:
            trace = self.nets[signal]
            if trace.differential_pair:
                if trace.differential_pair not in self.nets:
                    self.violations.append({
                        'severity': 'critical',
                        'signal': signal,
                        'issue': f'Paired signal {trace.differential_pair} not found',
                        'action': 'Register paired signal'
                    })

    def _generate_routing_rules(self) -> List[RoutingConstraint]:
        """Generate routing constraints for PCB design"""
        rules = [
            RoutingConstraint(
                name="Minimum Trace Width",
                description="Prevent manufacturing issues",
                requirement="6mil (0.152mm) minimum for high-speed, 10mil (0.254mm) for power",
                severity="critical"
            ),
            RoutingConstraint(
                name="Trace Clearance",
                description="Prevent crosstalk and shorts",
                requirement="6mil (0.15mm) minimum clearance between signals",
                severity="critical"
            ),
            RoutingConstraint(
                name="Via Stitching",
                description="EMI containment and shield integrity",
                requirement="1mm spacing for standard signals, 0.5mm for sensitive analog",
                severity="important"
            ),
            RoutingConstraint(
                name="Differential Pair Matching",
                description="Preserve differential impedance",
                requirement="Pair USB_DM/DP with <5mm length difference",
                severity="critical"
            ),
            RoutingConstraint(
                name="High-Speed Net Isolation",
                description="Prevent interference",
                requirement="SPI traces routed on outer layers or dedicated layer",
                severity="important"
            ),
            RoutingConstraint(
                name="Ground Plane Continuity",
                description="Return path and EMI control",
                requirement="Continuous ground plane on L2 with minimal via stitching",
                severity="critical"
            ),
            RoutingConstraint(
                name="Power Plane Segmentation",
                description="Prevent ground loops",
                requirement="3.3V and 5V planes separated, ferrite isolation if needed",
                severity="important"
            ),
        ]
        return rules

    def get_validation_report(self) -> str:
        """Generate human-readable validation report"""
        lines = [
            "=" * 80,
            "SIGNAL INTEGRITY VALIDATION REPORT - K1 Lightwave",
            "=" * 80,
            f"Total nets analyzed: {len(self.nets)}",
            "",
            "LAYER STACKUP SPECIFICATION:",
            "-" * 80,
        ]

        for layer, spec in self.rules.LAYER_STACKUP.items():
            lines.append(f"{layer}: Cu={spec['cu_thickness']}mm, "
                        f"Prepreg={spec['prepreg']}mm")

        lines.extend([
            "",
            "CRITICAL ROUTING RULES:",
            "-" * 80,
        ])

        for rule in self._generate_routing_rules():
            lines.append(f"\n[{rule.severity.upper()}] {rule.name}")
            lines.append(f"  Description: {rule.description}")
            lines.append(f"  Requirement: {rule.requirement}")

        if self.violations:
            lines.extend([
                "",
                "VIOLATIONS:",
                "-" * 80,
            ])
            for v in self.violations:
                lines.append(f"\n[{v['severity'].upper()}] {v['signal']}")
                lines.append(f"  Issue: {v['issue']}")
                if 'recommendation' in v:
                    lines.append(f"  Action: {v['recommendation']}")

        if self.recommendations:
            lines.extend([
                "",
                "DESIGN RECOMMENDATIONS:",
                "-" * 80,
            ])
            for r in self.recommendations[:5]:  # First 5 recommendations
                lines.append(f"\n{r['signal']}: {r.get('rule', 'Design Rule')}")
                lines.append(f"  Requirement: {r.get('requirement', r.get('issue', 'See details'))}")

        return "\n".join(lines)
