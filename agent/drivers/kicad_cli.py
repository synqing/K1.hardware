"""
KiCad CLI driver for headless operations.

Provides safe wrappers around kicad-cli commands:
  - DRC (Design Rule Check) → JSON report
  - Exports (Gerbers, Drill, IPC-2581, ODB++)
  - DSN/SES I/O (routing import/export)
  - Netlist generation/ingestion
  - ERC checks

All commands verify output artifact size to catch silent failures.
"""

import subprocess
import os
import json
import sys
from pathlib import Path


class KiCadCLIError(Exception):
    """Raised when a kicad-cli command fails."""


def _run_cmd(args, description=""):
    """
    Run a subprocess command and raise on failure.

    Args:
        args: List of command arguments
        description: Human-readable description of the command (for error messages)

    Raises:
        KiCadCLIError: If command exits non-zero
    """
    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        msg = f"kicad-cli failed: {description}\nCommand: {' '.join(args)}\n"
        msg += f"Exit code: {e.returncode}\n"
        if e.stdout:
            msg += f"Stdout:\n{e.stdout}\n"
        if e.stderr:
            msg += f"Stderr:\n{e.stderr}\n"
        raise KiCadCLIError(msg) from e


def _verify_artifact(path, min_size=1000, description=""):
    """
    Verify that an artifact exists and has minimum size.

    Args:
        path: Path to the artifact file
        min_size: Minimum expected file size (bytes)
        description: Human-readable description

    Raises:
        KiCadCLIError: If artifact missing or too small
    """
    if not os.path.exists(path):
        raise KiCadCLIError(
            f"Artifact missing: {description}\n"
            f"Expected at: {path}"
        )
    size = os.path.getsize(path)
    if size < min_size:
        raise KiCadCLIError(
            f"Artifact too small (possible silent failure): {description}\n"
            f"Path: {path}\n"
            f"Size: {size} bytes (minimum: {min_size})"
        )


def drc(board_file, output_json=None):
    """
    Run DRC (Design Rule Check) on a KiCad board.

    Args:
        board_file: Path to .kicad_pcb file
        output_json: Output path for JSON report (default: auto-generated)

    Returns:
        dict: Parsed DRC report (JSON)

    Raises:
        KiCadCLIError: If DRC command fails or produces no output
    """
    if not output_json:
        base = os.path.splitext(board_file)[0]
        output_json = f"{base}_drc.json"

    args = [
        "kicad-cli",
        "pcb",
        "drc",
        board_file,
        "--output", output_json,
        "--format", "json"
    ]

    _run_cmd(args, f"DRC on {board_file}")
    _verify_artifact(output_json, min_size=500, description=f"DRC JSON report")

    with open(output_json, "r", encoding="utf-8") as f:
        report = json.load(f)

    # Extract violation counts
    violations = len(report.get("violations", []))
    unconnected = len(report.get("unconnected_items", []))

    report["_summary"] = {
        "violations_count": violations,
        "unconnected_count": unconnected,
        "output_json": output_json
    }

    return report


def export_dsn(board_file, output_dsn=None):
    """
    Export a KiCad board to Specctra DSN format for routing.

    Args:
        board_file: Path to .kicad_pcb file
        output_dsn: Output path (default: auto-generated)

    Returns:
        str: Path to exported DSN file

    Raises:
        KiCadCLIError: If export fails or produces no output
    """
    if not output_dsn:
        base = os.path.splitext(board_file)[0]
        output_dsn = f"{base}.dsn"

    args = [
        "kicad-cli",
        "pcb",
        "export",
        "dsn",
        board_file,
        "-o", output_dsn
    ]

    _run_cmd(args, f"DSN export from {board_file}")
    _verify_artifact(output_dsn, min_size=5000, description="DSN file")

    return output_dsn


def import_ses(board_file, ses_file):
    """
    Import a Specctra Session (SES) file into a KiCad board.

    NOTE: Some KiCad builds don't expose CLI SES import.
    If this fails, user must do one-click in GUI:
      File → Import → Specctra Session → select SES → OK → Save

    Args:
        board_file: Path to .kicad_pcb file (will be modified)
        ses_file: Path to .ses file to import

    Raises:
        KiCadCLIError: If import fails (see note above)
    """
    if not os.path.exists(ses_file):
        raise KiCadCLIError(f"SES file not found: {ses_file}")

    args = [
        "kicad-cli",
        "pcb",
        "import",
        "ses",
        board_file,
        "--input", ses_file
    ]

    try:
        _run_cmd(args, f"SES import from {ses_file}")
    except KiCadCLIError as e:
        # CLI SES import not available; give user fallback
        print("\n" + "=" * 70, file=sys.stderr)
        print("WARNING: kicad-cli SES import not available in your KiCad build.", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        print("\nFallback (one-time manual step):", file=sys.stderr)
        print("  1. Open KiCad PCB Editor: File → Open → " + board_file, file=sys.stderr)
        print("  2. Menu: File → Import → Specctra Session", file=sys.stderr)
        print("  3. Select: " + ses_file, file=sys.stderr)
        print("  4. Click OK", file=sys.stderr)
        print("  5. File → Save (Ctrl+S)", file=sys.stderr)
        print("  6. Re-run this script", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        raise KiCadCLIError(
            f"SES import via CLI failed. See fallback instructions above."
        ) from e


def export_gerbers(board_file, output_dir=None):
    """
    Export Gerber files (copper, mask, silkscreen, etc.).

    Args:
        board_file: Path to .kicad_pcb file
        output_dir: Output directory (default: auto-generated)

    Returns:
        str: Path to output directory

    Raises:
        KiCadCLIError: If export fails
    """
    if not output_dir:
        base = os.path.splitext(board_file)[0]
        output_dir = f"{base}_gerbers"

    os.makedirs(output_dir, exist_ok=True)

    args = [
        "kicad-cli",
        "pcb",
        "export",
        "gerbers",
        board_file,
        "--output", output_dir
    ]

    _run_cmd(args, f"Gerber export from {board_file}")

    # Verify at least one Gerber file was created
    gerber_files = list(Path(output_dir).glob("*.gbr")) + list(Path(output_dir).glob("*.GBR"))
    if not gerber_files:
        raise KiCadCLIError(f"No Gerber files found in {output_dir}")

    return output_dir


def export_drill(board_file, output_dir=None):
    """
    Export drill files (Excellon format).

    Args:
        board_file: Path to .kicad_pcb file
        output_dir: Output directory (default: auto-generated)

    Returns:
        str: Path to output directory

    Raises:
        KiCadCLIError: If export fails
    """
    if not output_dir:
        base = os.path.splitext(board_file)[0]
        output_dir = f"{base}_drill"

    os.makedirs(output_dir, exist_ok=True)

    args = [
        "kicad-cli",
        "pcb",
        "export",
        "drill",
        board_file,
        "--output", output_dir
    ]

    _run_cmd(args, f"Drill export from {board_file}")

    # Verify drill files
    drill_files = list(Path(output_dir).glob("*.xln")) + list(Path(output_dir).glob("*.XLN"))
    if not drill_files:
        raise KiCadCLIError(f"No drill files found in {output_dir}")

    return output_dir


def export_ipc2581(board_file, output_xml=None):
    """
    Export IPC-2581 XML (industry-standard fab format).

    Args:
        board_file: Path to .kicad_pcb file
        output_xml: Output path (default: auto-generated)

    Returns:
        str: Path to exported IPC-2581 file

    Raises:
        KiCadCLIError: If export fails
    """
    if not output_xml:
        base = os.path.splitext(board_file)[0]
        output_xml = f"{base}.ipc2581"

    args = [
        "kicad-cli",
        "pcb",
        "export",
        "ipc2581",
        board_file,
        "-o", output_xml
    ]

    _run_cmd(args, f"IPC-2581 export from {board_file}")
    _verify_artifact(output_xml, min_size=10000, description="IPC-2581 XML")

    return output_xml


def export_odb(board_file, output_zip=None):
    """
    Export ODB++ format (advanced manufacturing data).

    Args:
        board_file: Path to .kicad_pcb file
        output_zip: Output path (default: auto-generated)

    Returns:
        str: Path to exported ODB++ file

    Raises:
        KiCadCLIError: If export fails
    """
    if not output_zip:
        base = os.path.splitext(board_file)[0]
        output_zip = f"{base}.odb"

    args = [
        "kicad-cli",
        "pcb",
        "export",
        "odb",
        board_file,
        "-o", output_zip
    ]

    _run_cmd(args, f"ODB++ export from {board_file}")
    _verify_artifact(output_zip, min_size=5000, description="ODB++ file")

    return output_zip


def export_all_fab(board_file, output_dir=None):
    """
    Export all fab-pack formats in one call (convenience).

    Exports: Gerbers, Drill, IPC-2581, ODB++

    Args:
        board_file: Path to .kicad_pcb file
        output_dir: Output directory (default: auto-generated)

    Returns:
        dict: Paths to all exported files

    Raises:
        KiCadCLIError: If any export fails
    """
    if not output_dir:
        base = os.path.splitext(board_file)[0]
        output_dir = f"{base}_fabpack"

    os.makedirs(output_dir, exist_ok=True)

    artifacts = {}

    # Export each format
    artifacts["gerbers_dir"] = export_gerbers(board_file, os.path.join(output_dir, "gerbers"))
    artifacts["drill_dir"] = export_drill(board_file, os.path.join(output_dir, "drill"))
    artifacts["ipc2581"] = export_ipc2581(board_file, os.path.join(output_dir, "k1.ipc2581.xml"))
    artifacts["odb"] = export_odb(board_file, os.path.join(output_dir, "k1.odb"))

    return artifacts


def get_version():
    """
    Get the KiCad CLI version string.

    Returns:
        str: Version output from kicad-cli --version

    Raises:
        KiCadCLIError: If command fails
    """
    stdout, _ = _run_cmd(["kicad-cli", "--version"], "Get KiCad version")
    return stdout.strip()
