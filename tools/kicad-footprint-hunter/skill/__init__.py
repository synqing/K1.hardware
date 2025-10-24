"""
KiCad Footprint Hunter - Claude Code Skill

Provides Claude Code integration for footprint resolution.
"""

from .kicad_footprint_skill import (
    KiCadFootprintSkill,
    hunt_footprints,
    analyze_netlist,
    get_skill
)

__all__ = [
    'KiCadFootprintSkill',
    'hunt_footprints',
    'analyze_netlist',
    'get_skill'
]
