"""
Elite PCB Designer - DFM (Design for Manufacturability) Validator

Checks:
- PCB manufacturing constraints
- Assembly capability
- Cost optimization
- Yield improvement
- Test point requirements
"""

from typing import List, Dict, Optional


class ManufacturingConstraint:
    """Manufacturing design rule"""

    def __init__(self, name: str, limit: float, unit: str, severity: str):
        self.name = name
        self.limit = limit
        self.unit = unit
        self.severity = severity  # "critical", "important", "recommended"


class K1_ManufacturingRules:
    """K1 Lightwave DFM rules (JLCPCB compatible)"""

    # PCB manufacturing
    PCB_CONSTRAINTS = {
        "min_trace_width": ManufacturingConstraint("Min trace width", 0.15, "mm", "critical"),
        "min_trace_spacing": ManufacturingConstraint("Min trace spacing", 0.15, "mm", "critical"),
        "min_via_diameter": ManufacturingConstraint("Min via diameter", 0.3, "mm", "critical"),
        "min_hole_diameter": ManufacturingConstraint("Min hole diameter", 0.15, "mm", "critical"),
        "min_annular_ring": ManufacturingConstraint("Min annular ring", 0.05, "mm", "critical"),
        "max_aspect_ratio": ManufacturingConstraint("Max via aspect ratio", 10, "H:D", "important"),
        "min_copper_to_edge": ManufacturingConstraint("Min copper to edge", 0.2, "mm", "important"),
    }

    # Assembly constraints (pick and place)
    ASSEMBLY_CONSTRAINTS = {
        "min_component_spacing": ManufacturingConstraint("Min component spacing", 2.0, "mm", "important"),
        "max_bga_pitch": ManufacturingConstraint("Max BGA pitch", 0.5, "mm", "important"),
        "qfp_pad_size": ManufacturingConstraint("QFP pad size", 0.25, "mm", "important"),
        "0603_min_spacing": ManufacturingConstraint("0603 footprint spacing", 0.5, "mm", "recommended"),
    }

    # Solder paste stencil
    STENCIL_CONSTRAINTS = {
        "min_aperture": ManufacturingConstraint("Min stencil aperture", 0.15, "mm", "critical"),
        "max_aperture": ManufacturingConstraint("Max stencil aperture", 0.8, "mm", "recommended"),
        "solder_volume": ManufacturingConstraint("Solder volume (0603)", 4, "mm³", "important"),
    }

    # Reflow and thermal
    THERMAL_CONSTRAINTS = {
        "max_reflow_temp": ManufacturingConstraint("Max reflow temperature", 260, "°C", "critical"),
        "min_lead_free_solder": ManufacturingConstraint("Lead-free solder melting", 217, "°C", "critical"),
        "thermal_shock_rate": ManufacturingConstraint("Thermal shock rate", 6, "°C/sec", "important"),
    }

    # Cost factors (for optimization)
    COST_FACTORS = {
        "layer_count": [
            {"layers": 2, "cost_multiplier": 1.0},
            {"layers": 4, "cost_multiplier": 2.5},
            {"layers": 6, "cost_multiplier": 4.5},
        ],
        "component_count": {
            "up_to_50": 1.0,
            "50_to_100": 1.2,
            "100_to_200": 1.5,
            "over_200": 2.0,
        },
        "panelization": {
            "single_board": 1.0,
            "2x2_panel": 0.65,  # 35% savings
            "4x4_panel": 0.5,   # 50% savings
        },
    }


class DFMValidator:
    """Validate design for manufacturability"""

    def __init__(self):
        self.rules = K1_ManufacturingRules()
        self.violations: List[Dict] = []
        self.warnings: List[Dict] = []
        self.recommendations: List[Dict] = []

    def validate_pcb_design(self) -> Dict:
        """Validate PCB manufacturing feasibility"""
        results = {
            'status': 'PASS',
            'violations': [],
            'warnings': [],
            'manufacturing_readiness': 0,
        }

        # Check critical constraints
        results['violations'].extend(self._check_pcb_constraints())
        results['warnings'].extend(self._check_assembly_constraints())
        results['warnings'].extend(self._check_stencil_constraints())

        # Calculate readiness
        total_checks = len(results['violations']) + len(results['warnings'])
        passed_checks = total_checks - len(results['violations']) - len(results['warnings'])
        results['manufacturing_readiness'] = int(100 * passed_checks / max(1, total_checks))

        if results['violations']:
            results['status'] = 'FAIL'
        elif results['warnings']:
            results['status'] = 'PASS WITH WARNINGS'

        results['recommendations'] = self._generate_recommendations()

        return results

    def _check_pcb_constraints(self) -> List[Dict]:
        """Check PCB manufacturing constraints"""
        violations = []

        # Trace width check
        # For K1: minimum 0.15mm for all traces
        violations.append({
            'rule': 'Trace Width',
            'requirement': f'Min {self.rules.PCB_CONSTRAINTS["min_trace_width"].limit}mm',
            'status': 'VERIFY',
            'severity': 'critical',
        })

        # Via checks
        violations.append({
            'rule': 'Via Diameter',
            'requirement': f'Min {self.rules.PCB_CONSTRAINTS["min_via_diameter"].limit}mm pad',
            'status': 'VERIFY',
            'severity': 'critical',
        })

        return violations

    def _check_assembly_constraints(self) -> List[Dict]:
        """Check assembly constraints"""
        warnings = []

        warnings.append({
            'rule': 'Component Spacing',
            'requirement': f'Min {self.rules.ASSEMBLY_CONSTRAINTS["min_component_spacing"].limit}mm between centers',
            'status': 'VERIFY',
            'severity': 'important',
            'reason': 'Allows pick-and-place head clearance',
        })

        warnings.append({
            'rule': 'BGA Pitch',
            'requirement': f'Max {self.rules.ASSEMBLY_CONSTRAINTS["max_bga_pitch"].limit}mm for safe soldering',
            'status': 'VERIFY',
            'severity': 'important',
        })

        return warnings

    def _check_stencil_constraints(self) -> List[Dict]:
        """Check solder paste stencil constraints"""
        constraints = []

        constraints.append({
            'rule': 'Stencil Aperture Size',
            'requirement': f'0.15-0.8mm for 0603 footprints',
            'optimization': 'Use 0.7mm aperture for balanced solder volume',
            'severity': 'recommended',
        })

        return constraints

    def _generate_recommendations(self) -> List[Dict]:
        """Generate manufacturing recommendations"""
        recommendations = [
            {
                'category': 'Panelization',
                'recommendation': 'Design for 2x2 or 4x4 panel (35-50% cost savings)',
                'impact': 'Cost reduction',
            },
            {
                'category': 'Test Points',
                'recommendation': 'Add test points for all power and ground nets',
                'details': 'Required for ICT (In-Circuit Test)',
            },
            {
                'category': 'Fiducials',
                'recommendation': 'Place 3 fiducial marks on board',
                'details': 'For automatic placement calibration',
            },
            {
                'category': 'Edge Clearance',
                'recommendation': 'Maintain 0.2mm clearance from board edge',
                'details': 'Prevents component damage during depanelization',
            },
            {
                'category': 'Silkscreen',
                'recommendation': 'Include reference designators and voltage labels',
                'details': 'Aids assembly and rework',
            },
        ]

        return recommendations

    def calculate_assembly_cost_estimate(self, component_count: int,
                                         layer_count: int = 4,
                                         panel_config: str = "single_board") -> Dict:
        """Estimate assembly cost"""
        factors = self.rules.COST_FACTORS

        # Base PCB cost multiplier for layer count
        layer_multiplier = 1.0
        for config in factors['layer_count']:
            if config['layers'] == layer_count:
                layer_multiplier = config['cost_multiplier']

        # Component count multiplier
        count_multiplier = 1.0
        if component_count <= 50:
            count_multiplier = factors['component_count']['up_to_50']
        elif component_count <= 100:
            count_multiplier = factors['component_count']['50_to_100']
        elif component_count <= 200:
            count_multiplier = factors['component_count']['100_to_200']
        else:
            count_multiplier = factors['component_count']['over_200']

        # Panelization savings
        panel_multiplier = factors['panelization'].get(panel_config, 1.0)

        # Estimate (relative units, normalized to 4-layer, 65 components, single board = 1.0)
        base_cost = 1.0
        pcb_cost = base_cost * layer_multiplier * panel_multiplier
        assembly_cost = base_cost * count_multiplier * (1.0 if layer_count >= 4 else 1.5)

        return {
            'pcb_cost_relative': pcb_cost,
            'assembly_cost_relative': assembly_cost,
            'total_cost_relative': pcb_cost + assembly_cost,
            'cost_optimization': {
                'recommendation': f'Use {layer_count}-layer with {panel_config}',
                'potential_savings': f'{(1 - panel_multiplier) * 100:.0f}% from panelization',
            },
        }

    def get_dfm_report(self) -> str:
        """Generate DFM validation report"""
        results = self.validate_pcb_design()
        cost_est = self.calculate_assembly_cost_estimate(65, 4, "single_board")

        lines = [
            "=" * 80,
            "DFM (DESIGN FOR MANUFACTURABILITY) REPORT - K1 Lightwave",
            "=" * 80,
            f"Manufacturing Readiness: {results['manufacturing_readiness']}%",
            f"Status: {results['status']}",
            "",
            "CRITICAL CONSTRAINTS:",
            "-" * 80,
        ]

        for v in results['violations'][:5]:
            lines.append(f"\n{v['rule']}")
            lines.append(f"  Requirement: {v['requirement']}")
            lines.append(f"  Status: {v['status']}")

        lines.extend([
            "",
            "ASSEMBLY GUIDELINES:",
            "-" * 80,
        ])

        for w in results['warnings'][:3]:
            lines.append(f"\n{w['rule']}")
            lines.append(f"  Requirement: {w['requirement']}")
            if 'reason' in w:
                lines.append(f"  Reason: {w['reason']}")

        lines.extend([
            "",
            "COST OPTIMIZATION:",
            "-" * 80,
            f"PCB Cost Factor: {cost_est['pcb_cost_relative']:.2f}x",
            f"Assembly Cost Factor: {cost_est['assembly_cost_relative']:.2f}x",
            f"Total Cost Factor: {cost_est['total_cost_relative']:.2f}x",
        ])

        if 'potential_savings' in cost_est['cost_optimization']:
            lines.append(f"Potential Savings: {cost_est['cost_optimization']['potential_savings']}")

        lines.extend([
            "",
            "RECOMMENDATIONS:",
            "-" * 80,
        ])

        for rec in results['recommendations'][:5]:
            lines.append(f"\n{rec['category']}")
            lines.append(f"  {rec['recommendation']}")

        return "\n".join(lines)
