"""
KiCad Footprint Hunter - Core Modules

Multi-source footprint resolver for KiCad netlists.
Searches KiCad libraries, GitHub repositories, and uses pattern matching
to automatically assign footprints to components.
"""

from .netlist_parser import NetlistParser, ComponentMetadata, ComponentType
from .footprint_scraper import (
    FootprintMatch, FootprintResolver, KiCadLibraryScraper,
    PatternBasedScraper, LCSCDatabaseScraper
)
from .footprint_hunter import FootprintHunter
from .pcb_updater import PCBUpdater, NetlistUpdater, SKiDLUpdater

__version__ = "1.0.0"
__all__ = [
    'NetlistParser',
    'ComponentMetadata',
    'ComponentType',
    'FootprintMatch',
    'FootprintResolver',
    'KiCadLibraryScraper',
    'PatternBasedScraper',
    'LCSCDatabaseScraper',
    'FootprintHunter',
    'PCBUpdater',
    'NetlistUpdater',
    'SKiDLUpdater',
]
