"""
K1 Expert PCB Design Agent.

Modular architecture for end-to-end PCB design:
  - drivers: KiCad CLI, IPC, plugin bridges
  - kicad: domain knowledge (layers, netlist, rules)
  - routing: DSN/SES, FreeRouting
  - dfm: Design for Manufacturing checks
  - thermal: Thermal analysis
  - impedance: High-speed impedance control
  - orchestrator: 7-phase pipeline
  - configs: Project configuration
"""

__version__ = "1.0.0"
__author__ = "K1 Expert PCB Agent"
