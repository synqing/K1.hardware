"""
FreeRouting headless autorouter wrapper.

FreeRouting is a powerful open-source PCB router that accepts KiCad DSN files
and outputs Specctra Session (SES) files with completed routing.

This module handles:
  - JAR availability checks
  - Process spawning with timeout/retry logic
  - Output verification (non-empty SES)
  - Error reporting with logs
"""

import subprocess
import os
import sys
from pathlib import Path


class FreeRoutingError(Exception):
    """Raised when FreeRouting operation fails."""


def route(jar_path, dsn_file, ses_output, timeout_s=1800, max_retries=1):
    """
    Run FreeRouting headless to route a board.

    Args:
        jar_path: Path to freerouting.jar
        dsn_file: Input Specctra DSN file
        ses_output: Output Specctra Session file path
        timeout_s: Timeout in seconds (default: 1800 = 30 min)
        max_retries: Number of retries on timeout (default: 1, so 2 total attempts)

    Returns:
        str: Path to the generated SES file

    Raises:
        FreeRoutingError: If routing fails, jar not found, or output invalid
    """
    if not os.path.exists(jar_path):
        raise FreeRoutingError(f"FreeRouting JAR not found: {jar_path}")

    if not os.path.exists(dsn_file):
        raise FreeRoutingError(f"DSN file not found: {dsn_file}")

    # Clean up any previous SES (we'll verify the new one is created)
    if os.path.exists(ses_output):
        os.remove(ses_output)

    args = ["java", "-jar", jar_path, "-de", dsn_file, "-do", ses_output]

    attempt = 0
    last_error = None

    while attempt <= max_retries:
        attempt += 1
        print(f"\n[FreeRouting] Attempt {attempt}/{max_retries + 1}: routing {os.path.basename(dsn_file)}", file=sys.stderr)

        try:
            result = subprocess.run(
                args,
                timeout=timeout_s,
                capture_output=True,
                text=True
            )

            # FreeRouting exits with 0 on success
            if result.returncode != 0:
                # Non-zero exit; may retry
                stderr = result.stderr or ""
                stdout = result.stdout or ""
                last_error = f"FreeRouting exit code {result.returncode}\nStderr: {stderr}\nStdout: {stdout}"
                print(f"[FreeRouting] Attempt {attempt} failed: {last_error}", file=sys.stderr)

                if attempt <= max_retries:
                    print(f"[FreeRouting] Retrying...", file=sys.stderr)
                    continue
                else:
                    raise FreeRoutingError(last_error)

            # Exit code 0; check for SES output
            if not os.path.exists(ses_output) or os.path.getsize(ses_output) < 1000:
                last_error = (
                    f"SES file missing or too small (possible silent failure)\n"
                    f"Expected: {ses_output}\n"
                    f"Size: {os.path.getsize(ses_output) if os.path.exists(ses_output) else 0} bytes"
                )
                print(f"[FreeRouting] Attempt {attempt} produced invalid output: {last_error}", file=sys.stderr)

                if attempt <= max_retries:
                    print(f"[FreeRouting] Retrying...", file=sys.stderr)
                    continue
                else:
                    raise FreeRoutingError(last_error)

            # Success
            size_mb = os.path.getsize(ses_output) / (1024 * 1024)
            print(f"[FreeRouting] SUCCESS: {os.path.basename(ses_output)} ({size_mb:.2f} MB)", file=sys.stderr)
            return ses_output

        except subprocess.TimeoutExpired:
            last_error = f"Timeout after {timeout_s}s"
            print(f"[FreeRouting] Attempt {attempt} timed out", file=sys.stderr)

            if attempt <= max_retries:
                print(f"[FreeRouting] Retrying...", file=sys.stderr)
                continue
            else:
                raise FreeRoutingError(last_error) from None

    # Should not reach here, but just in case
    raise FreeRoutingError(f"Routing failed after {max_retries + 1} attempts: {last_error}")


def check_jar_available(jar_path) -> bool:
    """
    Check if FreeRouting JAR exists and is readable.

    Args:
        jar_path: Path to freerouting.jar

    Returns:
        bool: True if JAR is available
    """
    return os.path.exists(jar_path) and os.path.isfile(jar_path)


def get_version_hint(jar_path) -> str:
    """
    Try to get FreeRouting version (best-effort).

    Args:
        jar_path: Path to freerouting.jar

    Returns:
        str: Version string or "unknown"
    """
    try:
        result = subprocess.run(
            ["java", "-jar", jar_path, "-h"],
            timeout=5,
            capture_output=True,
            text=True
        )
        # Look for version in output
        for line in result.stdout.split("\n") + result.stderr.split("\n"):
            if "version" in line.lower():
                return line.strip()
        return "unknown (JAR present and executable)"
    except Exception:
        return "unable to determine"
