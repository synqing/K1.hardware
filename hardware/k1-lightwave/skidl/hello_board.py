#!/usr/bin/env python3
"""
SKiDL hello_board.py — Minimal example schematic generator for K1 Lightwave.

This generates a trivial netlist with:
- ESP32-S3-WROOM-1 MCU header
- 2× LED power connectors
- 2× mic inputs (SPH0645 / IM69D130)
- Decoupling caps on 3.3V rail
- Power connectors (5V, GND)

Run: skidl_gen_netlist("hardware/k1-lightwave/skidl/hello_board.py", out_net="hello.net")
Output: hello.net (KiCad S-expression netlist, importable into KiCad)

Docs: https://devbisme.github.io/skidl/
"""

from skidl import *

# Define simple components (no footprints for this demo; use generic symbols)
# In real use, you'd import from KiCad symbol libraries

# Reset circuit
reset()

# Create a simple schematic:
# - ESP32-S3 MCU (placeholder)
# - Power rails (5V, 3.3V, GND)
# - Decoupling capacitors
# - LED connectors
# - Mic connectors

# Nets
GND = Net('GND')
VCC_5V = Net('VCC_5V')
VCC_3V3 = Net('VCC_3V3')
I2S_BCLK = Net('I2S_BCLK')
I2S_LRCLK = Net('I2S_LRCLK')
I2S_SD = Net('I2S_SD')
LED_DATA = Net('LED_DATA')
LED_CLK = Net('LED_CLK')

# Simple header/connector placeholders (footprint: Conn_01x40_Pin, etc.)
# In real design, replace with actual KiCad symbols

# MCU Power
C1 = Part('Device', 'C', value='100uF', footprint='C_1206')
C1[1] += VCC_3V3
C1[2] += GND

C2 = Part('Device', 'C', value='10uF', footprint='C_0805')
C2[1] += VCC_3V3
C2[2] += GND

C3 = Part('Device', 'C', value='100nF', footprint='C_0603')
C3[1] += VCC_5V
C3[2] += GND

# LED Power connectors (placeholders)
LED1 = Part('Connector', 'Conn_01x03_Pin', footprint='Conn_JST-XH_3UCON_1x03_P2.50mm_Horizontal')
LED1[1] += GND
LED1[2] += VCC_5V
LED1[3] += LED_DATA

LED2 = Part('Connector', 'Conn_01x02_Pin', footprint='Conn_JST-XH_2UCON_1x02_P2.50mm_Horizontal')
LED2[1] += LED_CLK
LED2[2] += GND

# Mic inputs (SPH0645 / IM69D130 — digital I2S)
MIC1 = Part('Connector', 'Conn_01x04_Pin', footprint='Conn_01x04_Pin')
MIC1[1] += VCC_3V3
MIC1[2] += GND
MIC1[3] += I2S_SD
MIC1[4] += I2S_BCLK

MIC2 = Part('Connector', 'Conn_01x03_Pin', footprint='Conn_01x03_Pin')
MIC2[1] += I2S_LRCLK
MIC2[2] += GND
MIC2[3] += VCC_3V3

# MCU placeholder header
MCU = Part('Connector', 'Conn_01x40_Pin', footprint='Conn_01x40_Pin')
# Just wire up a few key pins for demo
MCU[1] += VCC_3V3
MCU[2] += GND
MCU[3] += I2S_BCLK
MCU[4] += I2S_LRCLK
MCU[5] += I2S_SD
MCU[6] += LED_DATA
MCU[7] += LED_CLK

# Bypass capacitor on 3.3V
C4 = Part('Device', 'C', value='100nF', footprint='C_0603')
C4[1] += VCC_3V3
C4[2] += GND

# Power connectors
PWR_IN = Part('Connector', 'Conn_01x02_Pin', footprint='Conn_JST-PH_2UCON_1x02_P2.00mm_Horizontal')
PWR_IN[1] += VCC_5V
PWR_IN[2] += GND

# Generate netlist
# This will be called by: skidl_gen_netlist(...) → generates hello.net

if __name__ == "__main__":
    # For standalone testing
    generate_netlist()
