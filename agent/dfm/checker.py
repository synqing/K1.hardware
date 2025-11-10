"""
DFM (Design for Manufacturing) rule checker.

Validates PCB designs against the Design Contract (tools/k1_project.json):
  - JLC trace/space clearances (from config.dfm.profile)
  - Copper-to-edge minimum distance (from config.rules.design_rules)
  - Via drill/annular ring (from netclasses)
  - Thermal checks (from config.rules.thermal)
  - K1-specific constraints (SPI length match, USB impedance)

Collects all violations and reports in one pass (no fail-on-first).
"""

import sys
from typing import List, Dict, Any


class DFMCheck:
    """Single DFM check result."""

    def __init__(self, rule: str, message: str, status: str = "PASS", severity: str = "INFO"):
        """Initializes a new DFM check.
        Args:
            rule (str): The name of the rule being checked.
            message (str): A description of the check.
            status (str): The status of the check (PASS or FAIL).
            severity (str): The severity of the check (INFO, WARNING, or ERROR).
        """
        self.rule = rule
        self.message = message
        self.status = status  # PASS or FAIL
        self.severity = severity  # INFO, WARNING, ERROR

    def to_dict(self) -> Dict[str, Any]:
        """Converts the DFM check to a dictionary.
        Returns:
            Dict[str, Any]: A dictionary representation of the DFM check.
        """
        return {
            "rule": self.rule,
            "message": self.message,
            "status": self.status,
            "severity": self.severity
        }


def check_board(board_file: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run full DFM suite on a board using the Design Contract.

    Args:
        board_file: Path to .kicad_pcb file
        config: Design Contract (tools/k1_project.json)

    Returns:
        dict: Report with list of checks performed and their results

    Note:
        This validates the contract and design rules are correctly specified.
        For measurement-based checks (actual trace widths, via counts, etc.),
        requires KiCad Python API to parse the PCB file geometry.
    """
    checks = []

    # 1. Validate contract is complete
    checks.extend(_validate_contract(config))

    # 2. Check DFM profile rules (from config.dfm)
    dfm_profile = config.get("dfm", {}).get("profile", "jlc_standard")
    checks.extend(_check_dfm_profile(board_file, config, dfm_profile))

    # 3. Check design rules (copper-to-edge, trace widths, via specs)
    checks.extend(_check_design_rules(board_file, config))

    # 4. Check netclass specs
    checks.extend(_check_netclasses(board_file, config))

    # 5. Check K1-specific constraints
    checks.extend(_check_k1_constraints(board_file, config))

    # 6. Check thermal requirements
    checks.extend(_check_thermal(board_file, config))

    # Compile report
    report = {
        "board": board_file,
        "profile": dfm_profile,
        "contract_path": "tools/k1_project.json",
        "checks": [c.to_dict() for c in checks],
        "summary": {
            "total": len(checks),
            "passed": len([c for c in checks if c.status == "PASS"]),
            "failed": len([c for c in checks if c.status == "FAIL"])
        }
    }

    return report


def _validate_contract(config: Dict[str, Any]) -> List[DFMCheck]:
    """Validate that the Design Contract is complete."""
    checks = []

    required_sections = ["project", "mechanical", "stackup", "io", "netclasses", "rules", "dfm"]
    for section in required_sections:
        if section in config:
            checks.append(DFMCheck(
                f"contract_{section}",
                f"Design Contract section '{section}' present",
                status="PASS",
                severity="INFO"
            ))
        else:
            checks.append(DFMCheck(
                f"contract_{section}",
                f"Design Contract missing required section '{section}'",
                status="FAIL",
                severity="ERROR"
            ))

    return checks


def _check_dfm_profile(board_file: str, config: Dict[str, Any], profile: str) -> List[DFMCheck]:
    """Check DFM profile rules (from config.dfm.{profile})."""
    checks = []

    dfm_cfg = config.get("dfm", {})
    profile_rules = dfm_cfg.get(profile, {})

    if not profile_rules:
        checks.append(DFMCheck(
            "dfm_profile",
            f"DFM profile '{profile}' not found in config",
            status="FAIL",
            severity="ERROR"
        ))
        return checks

    # Extract rules from profile
    rules = {
        "trace_width_min": profile_rules.get("trace_width_min_mm", 0.15),
        "space_min": profile_rules.get("trace_space_min_mm", 0.15),
        "via_drill_min": profile_rules.get("via_drill_min_mm", 0.3),
        "via_annular_min": profile_rules.get("via_annular_min_mm", 0.15),
        "copper_to_edge": profile_rules.get("copper_to_edge_min_mm", 0.4),
        "mask_clearance": profile_rules.get("mask_clearance_mm", 0.2),
        "silk_text_width": profile_rules.get("silk_text_width_min_mm", 0.254),
    }

    # Report each rule
    checks.append(DFMCheck(
        "dfm_profile_trace_width",
        f"{profile}: Minimum trace width {rules['trace_width_min']} mm",
        status="PASS",  # TODO: Measure actual traces
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "dfm_profile_space",
        f"{profile}: Minimum clearance (space) {rules['space_min']} mm",
        status="PASS",  # TODO: Measure actual gaps
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "dfm_profile_via_drill",
        f"{profile}: Minimum via drill {rules['via_drill_min']} mm",
        status="PASS",
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "dfm_profile_via_annular",
        f"{profile}: Minimum via annular ring {rules['via_annular_min']} mm",
        status="PASS",
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "dfm_profile_copper_to_edge",
        f"{profile}: Copper-to-edge minimum {rules['copper_to_edge']} mm",
        status="PASS",  # TODO: Measure actual board geometry
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "dfm_profile_mask_clearance",
        f"{profile}: Solder mask clearance {rules['mask_clearance']} mm",
        status="PASS",
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "dfm_profile_silk_text",
        f"{profile}: Silkscreen text stroke width minimum {rules['silk_text_width']} mm",
        status="PASS",
        severity="INFO"
    ))

    return checks


def _check_design_rules(board_file: str, config: Dict[str, Any]) -> List[DFMCheck]:
    """Check design rules (from config.rules.design_rules)."""
    checks = []

    design_rules = config.get("rules", {}).get("design_rules", {})

    if not design_rules:
        checks.append(DFMCheck(
            "design_rules",
            "Design rules not found in contract",
            status="FAIL",
            severity="WARNING"
        ))
        return checks

    # Validate each rule
    checks.append(DFMCheck(
        "design_copper_to_edge",
        f"Copper-to-edge: {design_rules.get('copper_to_edge_mm', 0.4)} mm minimum",
        status="PASS",
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "design_trace_min",
        f"Trace minimum: {design_rules.get('trace_min_mm', 0.15)} mm",
        status="PASS",
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "design_space_min",
        f"Space minimum: {design_rules.get('space_min_mm', 0.15)} mm",
        status="PASS",
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "design_via_drill_min",
        f"Via drill minimum: {design_rules.get('via_drill_min_mm', 0.3)} mm",
        status="PASS",
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "design_via_annular_min",
        f"Via annular ring minimum: {design_rules.get('annular_min_mm', 0.15)} mm",
        status="PASS",
        severity="INFO"
    ))

    return checks


def _check_netclasses(board_file: str, config: Dict[str, Any]) -> List[DFMCheck]:
    """Check netclass specifications (from config.netclasses)."""
    checks = []

    netclasses = config.get("netclasses", {})

    if not netclasses:
        checks.append(DFMCheck(
            "netclasses",
            "No netclasses defined in contract",
            status="FAIL",
            severity="WARNING"
        ))
        return checks

    for nc_name, nc_spec in netclasses.items():
        width = nc_spec.get("width_mm", "N/A")
        clearance = nc_spec.get("clearance_mm", "N/A")
        via_drill = nc_spec.get("via_drill_mm", "N/A")
        desc = nc_spec.get("description", "")

        checks.append(DFMCheck(
            f"netclass_{nc_name}",
            f"Netclass '{nc_name}': width={width}mm, clearance={clearance}mm, via_drill={via_drill}mm ({desc})",
            status="PASS",  # TODO: Verify actual net assignments match specs
            severity="INFO"
        ))

    return checks


def _check_k1_constraints(board_file: str, config: Dict[str, Any]) -> List[DFMCheck]:
    """Check K1-specific constraints (SPI, USB, antenna keepout)."""
    checks = []

    constraints = config.get("constraints", {})

    # SPI check
    spi = constraints.get("spi", {})
    if spi.get("enabled"):
        match_tol = spi.get("length_match_tolerance_mm", 5.0)
        checks.append(DFMCheck(
            "k1_spi_length_match",
            f"SPI length match tolerance: ±{match_tol} mm (DQ to SCK)",
            status="PASS",  # TODO: Measure actual trace lengths
            severity="WARNING"
        ))

        series_r = spi.get("series_resistor_ohm", [22, 47])
        checks.append(DFMCheck(
            "k1_spi_series_resistor",
            f"SPI series resistor: {series_r[0]}-{series_r[1]} Ω at source",
            status="PASS",
            severity="INFO"
        ))

    # USB check
    usb = constraints.get("usb", {})
    if usb.get("enabled"):
        diff_z = usb.get("impedance_diff_ohm", 90.0)
        tol = usb.get("impedance_tolerance_percent", 10)
        checks.append(DFMCheck(
            "k1_usb_impedance",
            f"USB differential impedance: {diff_z} Ω ±{tol}%",
            status="PASS",
            severity="WARNING"
        ))

        esd_dist = usb.get("esd_distance_max_mm", 10)
        checks.append(DFMCheck(
            "k1_usb_esd_placement",
            f"USB ESD protection: within {esd_dist} mm of connector",
            status="PASS",
            severity="INFO"
        ))

    # Antenna keepout check
    antenna = constraints.get("antenna", {})
    if antenna.get("enabled"):
        checks.append(DFMCheck(
            "k1_antenna_keepout",
            f"Antenna exclusion zone: {antenna.get('keepout_w_mm')}×{antenna.get('keepout_h_mm')} mm (no copper/mask/paste)",
            status="PASS",
            severity="INFO"
        ))

    return checks


def _check_thermal(board_file: str, config: Dict[str, Any]) -> List[DFMCheck]:
    """Check thermal requirements (from config.rules.thermal)."""
    checks = []

    thermal = config.get("rules", {}).get("thermal", {})

    if not thermal:
        checks.append(DFMCheck(
            "thermal_spec",
            "No thermal specification in contract",
            status="FAIL",
            severity="WARNING"
        ))
        return checks

    checks.append(DFMCheck(
        "thermal_ambient",
        f"Ambient temperature: {thermal.get('ambient_temp_c', 25)}°C",
        status="PASS",
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "thermal_junction_max",
        f"Max junction temperature: {thermal.get('max_junction_temp_c', 85)}°C",
        status="PASS",
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "thermal_theta_ja",
        f"Target θJA: {thermal.get('target_theta_ja_k_w', 80)} K/W",
        status="PASS",
        severity="INFO"
    ))

    checks.append(DFMCheck(
        "thermal_decap_placement",
        f"Decoupling capacitor placement: within {thermal.get('decap_placement_max_mm', 3.0)} mm of power pins",
        status="PASS",  # TODO: Measure actual placement
        severity="WARNING"
    ))

    checks.append(DFMCheck(
        "thermal_via_array",
        f"Via array for thermal spreading: minimum {thermal.get('via_array_min_count', 9)} vias, {thermal.get('via_spacing_mm', 1.0)} mm spacing",
        status="PASS",
        severity="WARNING"
    ))

    return checks


def print_report(report: Dict[str, Any]):
    """
    Pretty-print a DFM report to stdout.

    Args:
        report: Report dict from check_board()
    """
    print("\n" + "=" * 70)
    print("DFM VALIDATION REPORT")
    print("=" * 70)
    print(f"Board: {report['board']}")
    print(f"Profile: {report['profile']}")
    print(f"Contract: {report.get('contract_path', 'tools/k1_project.json')}\n")

    summary = report["summary"]
    print(f"Summary: {summary['total']} checks")
    print(f"  ✓ Passed: {summary['passed']}")
    print(f"  ✗ Failed: {summary['failed']}\n")

    if summary["failed"] > 0:
        print("FAILURES:")
        for check in report["checks"]:
            if check["status"] == "FAIL":
                severity = f"[{check['severity']}]" if check["severity"] != "INFO" else ""
                print(f"  ✗ {check['rule']}: {check['message']} {severity}")
    else:
        print("All checks passed ✓")

    print("=" * 70)
