"""
KiCad Footprint Hunter - Claude Code Skill

Integrates footprint resolution into Claude Code as a callable Skill.

Usage from Claude Code:
    /kicad-footprint-hunt <netlist_file> [--confidence 0.5] [--auto]
"""

from pathlib import Path
from typing import Dict, Optional, Any
import json

# Import core modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.footprint_hunter import FootprintHunter
from core.netlist_parser import NetlistParser


class KiCadFootprintSkill:
    """Claude Code Skill for KiCad footprint hunting"""

    def __init__(self, project_root: Optional[str] = None):
        """
        Initialize skill

        Args:
            project_root: Optional project root for context
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()

    def hunt_footprints(self, netlist_path: str, confidence_threshold: float = 0.5,
                        auto_assign: bool = False) -> Dict[str, Any]:
        """
        Hunt for footprints in a netlist and optionally assign them

        Args:
            netlist_path: Path to KiCad netlist file (.net)
            confidence_threshold: Minimum confidence for matches (0.0-1.0)
            auto_assign: Automatically assign top matches above threshold

        Returns:
            Resolution result dictionary
        """
        netlist = Path(netlist_path)

        if not netlist.exists():
            return {
                'status': 'error',
                'error': f'Netlist file not found: {netlist_path}'
            }

        try:
            # Create hunter
            hunter = FootprintHunter(netlist_path=str(netlist))

            # Run workflow
            report = hunter.run(
                min_confidence=confidence_threshold,
                auto_assign=auto_assign
            )

            # Return structured result
            return {
                'status': 'success',
                'netlist': str(netlist),
                'summary': hunter.get_resolution_summary(),
                'report': report,
                'unresolved': hunter.get_unresolved_components()
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def analyze_netlist(self, netlist_path: str) -> Dict[str, Any]:
        """
        Analyze a netlist without resolving footprints

        Args:
            netlist_path: Path to KiCad netlist file (.net)

        Returns:
            Analysis result with component inventory
        """
        netlist = Path(netlist_path)

        if not netlist.exists():
            return {
                'status': 'error',
                'error': f'Netlist file not found: {netlist_path}'
            }

        try:
            parser = NetlistParser()
            components = parser.parse_file(str(netlist))
            summary = parser.get_component_summary()
            missing = parser.get_missing_footprints()

            return {
                'status': 'success',
                'netlist': str(netlist),
                'components': {
                    'total': len(components),
                    'with_footprints': summary['with_footprints'],
                    'missing_footprints': summary['missing_footprints'],
                    'coverage_percent': summary['coverage_percent']
                },
                'by_type': summary['by_type'],
                'missing_refs': sorted(missing.keys())
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def get_resolution_status(self, netlist_path: str) -> Dict[str, Any]:
        """
        Quick check of resolution status for a netlist

        Args:
            netlist_path: Path to netlist file

        Returns:
            Status summary
        """
        netlist = Path(netlist_path)

        if not netlist.exists():
            return {
                'status': 'error',
                'error': f'Netlist file not found: {netlist_path}'
            }

        try:
            parser = NetlistParser()
            parser.parse_file(str(netlist))
            summary = parser.get_component_summary()

            return {
                'status': 'success',
                'netlist': str(netlist),
                'coverage_percent': summary['coverage_percent'],
                'components': {
                    'total': summary['total_components'],
                    'assigned': summary['with_footprints'],
                    'missing': summary['missing_footprints']
                },
                'progress': self._get_progress_bar(
                    summary['with_footprints'],
                    summary['total_components']
                )
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    @staticmethod
    def _get_progress_bar(current: int, total: int) -> str:
        """Generate ASCII progress bar"""
        if total == 0:
            return "[Empty]"

        percent = current / total
        filled = int(percent * 20)
        bar = "█" * filled + "░" * (20 - filled)
        return f"[{bar}] {percent:.1%}"


# Singleton instance for use as Skill
_skill_instance = None


def get_skill() -> KiCadFootprintSkill:
    """Get singleton skill instance"""
    global _skill_instance
    if _skill_instance is None:
        _skill_instance = KiCadFootprintSkill()
    return _skill_instance


# Claude Code integration
def hunt_footprints(netlist_path: str, confidence: float = 0.5,
                    auto: bool = False) -> str:
    """
    Claude Code Skill: Hunt for KiCad footprints

    Resolves missing footprints in a KiCad netlist by searching:
    - KiCad standard libraries
    - Component type patterns
    - Available database entries

    Args:
        netlist_path: Path to .net file
        confidence: Minimum confidence threshold (0.0-1.0)
        auto: Auto-assign footprints above threshold

    Returns:
        Formatted result string
    """
    skill = get_skill()
    result = skill.hunt_footprints(
        netlist_path=netlist_path,
        confidence_threshold=confidence,
        auto_assign=auto
    )

    if result['status'] != 'success':
        return f"Error: {result.get('error', 'Unknown error')}"

    # Format output
    summary = result['summary']
    lines = [
        "✓ Footprint Resolution Complete",
        f"  Total Components: {summary['total_components']}",
        f"  Resolved: {summary['resolved']}/{summary['missing_footprints']}",
        f"  Success Rate: {summary['resolution_rate']}",
    ]

    unresolved = result['unresolved']
    if unresolved:
        lines.append(f"\n⚠ {len(unresolved)} Unresolved Components:")
        for ref in sorted(unresolved.keys())[:5]:
            comp = unresolved[ref]
            lines.append(f"  {ref} ({comp['value']}) - {comp['library']}")
        if len(unresolved) > 5:
            lines.append(f"  ... and {len(unresolved) - 5} more")

    return "\n".join(lines)


def analyze_netlist(netlist_path: str) -> str:
    """
    Claude Code Skill: Analyze KiCad netlist

    Inventories components and reports footprint coverage.

    Args:
        netlist_path: Path to .net file

    Returns:
        Formatted analysis string
    """
    skill = get_skill()
    result = skill.analyze_netlist(netlist_path=netlist_path)

    if result['status'] != 'success':
        return f"Error: {result.get('error', 'Unknown error')}"

    comps = result['components']
    lines = [
        f"Netlist Analysis: {Path(netlist_path).name}",
        f"  Total Components: {comps['total']}",
        f"  With Footprints: {comps['with_footprints']}",
        f"  Missing: {comps['missing_footprints']}",
        f"  Coverage: {comps['coverage_percent']:.1f}%",
        "",
        "By Type:"
    ]

    for comp_type, count in sorted(result['by_type'].items()):
        lines.append(f"  {comp_type}: {count}")

    return "\n".join(lines)
