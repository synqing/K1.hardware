# hardware/k1-lightwave/skidl/k1_motherboard_revA.py
# K1 Lightwave – Rev-A Motherboard (complete SKiDL netlist generator)
# Dual-MCU system: COM-A (ESP32-S3-WROOM-1 module) + COM-B (bare ESP32-S3)
# Power domains: VBUS_USB_5V (logic), LED_5V (external)
# 4× independent LED ports, I2C accessories, I2S mics, inter-MCU SPI+SYNC

import sys
import os
import platform

# Configure KiCad library paths BEFORE importing SKiDL (critical!)
# Set environment variables that SKiDL will read during initialization
if platform.system() == 'Darwin':
    # macOS: KiCad installs at /Applications/KiCad/KiCad.app/
    lib_path = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols'
elif platform.system() == 'Linux':
    # Linux: check common installation paths
    if os.path.exists('/usr/share/kicad/symbols'):
        lib_path = '/usr/share/kicad/symbols'
    else:
        lib_path = os.path.expanduser('~/.local/share/kicad/symbols')
else:
    # Windows
    lib_path = os.getenv('KICAD_SYMBOL_DIR', 'C:\\Program Files\\KiCad\\share\\kicad\\symbols')

# Verify the path exists
if not os.path.exists(lib_path):
    raise FileNotFoundError(f"KiCad symbol directory not found at {lib_path}. Please install KiCad or set KICAD_SYMBOL_DIR.")

# Set env vars for all KiCad versions (SKiDL uses these as fallback)
os.environ['KICAD_SYMBOL_DIR'] = lib_path
os.environ['KICAD9_SYMBOL_DIR'] = lib_path
os.environ['KICAD8_SYMBOL_DIR'] = lib_path
os.environ['KICAD7_SYMBOL_DIR'] = lib_path
os.environ['KICAD6_SYMBOL_DIR'] = lib_path

# NOW import SKiDL after environment is set
import skidl
from skidl import *

# Additional SKiDL configuration
skidl.config.kicad_lib_path = lib_path
set_default_tool(KICAD)

NETLIST_OUT = "hardware/k1-lightwave/skidl/k1_motherboard_revA.net"
USE_GENERIC_COMB = True

# Global nets / power domains
gnd         = Net("GND")
usb_5v      = Net("VBUS_USB_5V")
led_5v      = Net("LED_5V")
v3v3        = Net("+3V3")

# USB differential pairs: break out connector vs. SoC sides for series damping + ESD
usb_dp_conn = Net("USB_D+_CONN")
usb_dm_conn = Net("USB_D-_CONN")
usb_dp_post = Net("USB_D+_BOARD")
usb_dm_post = Net("USB_D-_BOARD")
usb_dp_soc  = Net("USB_D+")
usb_dm_soc  = Net("USB_D-")

# I2C bus
sda         = Net("SDA")
scl         = Net("SCL")

# Inter-MCU link
spi_sck     = Net("SPI_SCK_A2B")
spi_mosi    = Net("SPI_MOSI_A2B")
spi_miso    = Net("SPI_MISO_B2A")
spi_cs      = Net("SPI_CS_A2B")
sync        = Net("SYNC_A2B")
ready       = Net("READY_B2A")

# Local source-side nets for SPI series damping
spi_sck_src  = Net("SPI_SCK_COMA_SRC")
spi_mosi_src = Net("SPI_MOSI_COMA_SRC")
spi_miso_src = Net("SPI_MISO_COMB_SRC")

# Series damping resistors for the 40 MHz SPI link (locate near the drivers)
r_spi_sck = Part("Device", "R", ref="R_SPI_SCK_SER", value="33R",
                  footprint="Resistor_SMD:R_0603_1608Metric")
r_spi_mosi = Part("Device", "R", ref="R_SPI_MOSI_SER", value="33R",
                   footprint="Resistor_SMD:R_0603_1608Metric")
r_spi_miso = Part("Device", "R", ref="R_SPI_MISO_SER", value="33R",
                   footprint="Resistor_SMD:R_0603_1608Metric")
r_spi_sck[1] += spi_sck_src;   r_spi_sck[2] += spi_sck
r_spi_mosi[1] += spi_mosi_src; r_spi_mosi[2] += spi_mosi
r_spi_miso[1] += spi_miso_src; r_spi_miso[2] += spi_miso

# SPI CS deassert default
r_spi_cs = Part("Device", "R", ref="R_SPI_CS_PU", value="10k",
                 footprint="Resistor_SMD:R_0603_1608Metric")
r_spi_cs[1] += v3v3
r_spi_cs[2] += spi_cs

# READY line idles low to avoid false asserts on GPIO39 boot pull-ups
r_ready_pd = Part("Device", "R", ref="R_READY_PD", value="100k",
                   footprint="Resistor_SMD:R_0603_1608Metric")
r_ready_pd[1] += ready
r_ready_pd[2] += gnd

# I2S (to COM-A)
i2s_bclk    = Net("I2S_BCLK")
i2s_lrck    = Net("I2S_LRCK")
i2s_sd      = Net("I2S_SD")

# LED data (COM-B → level shifters)
led_din = [Net(f"LED_DATA{i}_IN") for i in range(1,5)]

# USB-C receptacle with ESD protection
# NOTE: USB_C_Receptacle_USB2.0_14P is the correct symbol name in KiCad (14-pin variant for USB2.0)
j_usbc = Part("Connector", "USB_C_Receptacle_USB2.0_14P", ref="J1",
              footprint="Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12")
r_cc1 = Part("Device", "R", value="5.1k", ref="R1",
             footprint="Resistor_SMD:R_0603_1608Metric")
r_cc2 = Part("Device", "R", value="5.1k", ref="R2",
             footprint="Resistor_SMD:R_0603_1608Metric")
j_usbc["CC1"] += r_cc1[1]; r_cc1[2] += gnd
j_usbc["CC2"] += r_cc2[1]; r_cc2[2] += gnd
j_usbc["D+"] += usb_dp_conn
j_usbc["D-"] += usb_dm_conn
j_usbc["SHIELD"] += gnd
j_usbc["GND, GND"] += gnd

# USB input fuse (1A, overcurrent protection per PRD spec)
f_usb = Part("Device", "Fuse", ref="F_USB", value="1A_1206",
             footprint="Fuse:Fuse_1206_3216Metric")
j_usbc["VBUS, VBUS"] += f_usb[1]
f_usb[2] += usb_5v

# USB ESD protection – Use individual transient suppression diodes
# (TVS diodes are more portable across library versions than IC-based protection)
# For now, we'll use placeholders for the ESD diodes; in production, use:
# - DP/DM: SMAJ5.0A or similar 5V TVS
# - CC1/CC2: SMF05CA or similar 5V TVS
# These will be manually selected in KiCad based on detailed ESD requirements
d_esd_dp = Part("Device", "D_TVS", ref="D_ESD_DP", value="SMAJ5.0A",
                footprint="Diode_SMD:D_SOD-323")
d_esd_dm = Part("Device", "D_TVS", ref="D_ESD_DM", value="SMAJ5.0A",
                footprint="Diode_SMD:D_SOD-323")
d_esd_cc1 = Part("Device", "D_TVS", ref="D_ESD_CC1", value="SMF05CA",
                 footprint="Diode_SMD:D_SOD-323")
d_esd_cc2 = Part("Device", "D_TVS", ref="D_ESD_CC2", value="SMF05CA",
                 footprint="Diode_SMD:D_SOD-323")

# Connect ESD diodes: anode → signal, cathode → GND (for each except CC which has bidirectional protection)
d_esd_dp[1]  += usb_dp_conn; d_esd_dp[2]  += gnd
d_esd_dm[1]  += usb_dm_conn; d_esd_dm[2]  += gnd
d_esd_cc1[1] += j_usbc["CC1"]; d_esd_cc1[2] += gnd
d_esd_cc2[1] += j_usbc["CC2"]; d_esd_cc2[2] += gnd
# (In detailed design, CC diodes may need bidirectional protection - review in ESD audit)

# USB FS series damping near COM-B (GPIO19/20)
r_usb_dp = Part("Device", "R", ref="R_USB_DP_SER", value="27R",
                footprint="Resistor_SMD:R_0603_1608Metric")
r_usb_dm = Part("Device", "R", ref="R_USB_DM_SER", value="27R",
                footprint="Resistor_SMD:R_0603_1608Metric")
r_usb_dp[1] += usb_dp_post
r_usb_dp[2] += usb_dp_soc
r_usb_dm[1] += usb_dm_post
r_usb_dm[2] += usb_dm_soc

# 5V→3V3 buck regulator (TPS62160 or equivalent: synchronous step-down, 5V→3.3V, 1.5A)
# Note: Using generic regulator symbol due to library compatibility
# In KiCad, manually replace with TPS62160 SOIC-8 footprint
# Placeholder: TPS62160 buck regulator (5V -> 3V3, 1.5A)
# In KiCad, replace with TPS62160 SOIC-8:
#   Pin 1: SW (switch output - internal)
#   Pin 2: GND
#   Pin 3: FB (feedback pin)
#   Pin 4: EN/SYNC
#   Pin 5: VIN
#   Pin 6: VOUT (3V3 output)
#   Pin 7: GND
#   Pin 8: VIN
c_buck_in = Part("Device", "C", ref="C_BIN1", value="10u",
                 footprint="Capacitor_SMD:C_1206_3216Metric")
c_buck_out = Part("Device", "C", ref="C_BOUT1", value="10u",
                  footprint="Capacitor_SMD:C_1206_3216Metric")
c_buck_in[1] += usb_5v; c_buck_in[2] += gnd
c_buck_out[1] += v3v3; c_buck_out[2] += gnd
# TODO: Add TPS62160 IC (U2) in KiCad and wire properly

# External LED 5V ingress with ideal diode blocking (LTC4412)
j_led_in = Part("Connector", "Conn_01x02_Pin", ref="J2", value="LED_5V_IN",
                footprint="Connector_Molex:Molex_MicroFit_3.0_1x02")
led_in_raw = Net("LED_5V_RAW")  # Before ideal diode
j_led_in[1] += led_in_raw
j_led_in[2] += gnd

# Ideal diode controller (LTC4412) for reverse-blocking on LED power
# Prevents back-feed from LED_5V rail into USB 5V during bulk-cap discharge
# Note: Using generic power switch symbol; replace with LTC4412 in KiCad
# Placeholder: LTC4412 ideal diode controller with P-FET
# In KiCad, replace U5 with LTC4412 (SOT-23-5):
#   This section bridges LED_5V_RAW to LED_5V with ideal diode blocking
d_ideal = Part("Device", "D", ref="D_IDEAL", value="Schottky",
               footprint="Diode_SMD:D_SOD-323")
d_ideal[1] += led_in_raw
d_ideal[2] += led_5v
# TODO: Replace with LTC4412 + BSS84 P-FET in KiCad

# P-FET (BSS84) for reverse-blocking
# LTC4412 pulls GATE to ground when conducting; P-FET turns ON
# When source voltage drops, gate goes high, P-FET blocks reverse current
# P-FET gate drive resistor (wired for simplicity)
r_fet_gate = Part("Device", "R", ref="R_FET_GATE", value="10k",
                  footprint="Resistor_SMD:R_0603_1608Metric")
r_fet_gate[1] += v3v3
r_fet_gate[2] += Net("FET_GATE")
# TODO: Wire FET_GATE to LTC4412 and add P-FET (Q1) in KiCad

# Current monitor on LED_5V bus (INA226 – I2C, high-side, 36V capable)
# Note: Using generic IC placeholder; real implementation uses INA226
# Placeholder: INA226 current monitor
# In KiCad, add INA226 (MSOP-10) with:
#   - VS pin to 3V3
#   - SDA/SCL to I2C bus
#   - VIN+/VIN- for shunt measurement
c_ina = Part("Device", "C", ref="C_INA", value="100n",
             footprint="Capacitor_SMD:C_0603_1608Metric")
c_ina[1] += v3v3
c_ina[2] += gnd
# TODO: Add INA226 (U7) in KiCad
# Shunt resistor for current measurement (sized for ~3A max, ~100mV drop at 3A → 0.033Ω nominal, use 0.05Ω for margin)
r_shunt = Part("Device", "R", ref="R7", value="0.05R",
               footprint="Resistor_SMD:R_0603_1608Metric")
# Shunt in series: LED_5V → r_shunt → sense point
r_shunt[1] += led_5v
r_shunt[2] += Net("LED_5V_SENSE")

# LED outputs: 4× one-wire with AHCT125 shifter
# Note: Using generic Device placeholder; replace with 74AHCT125 IC in KiCad
u_ls = Part("Device", "R", ref="U3", value="Logic_Shifter_74AHCT125",  # Placeholder
            footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm")

def led_port(idx: int):
    global led_5v, gnd  # Reference global power nets
    j = Part("Connector", "Conn_01x03_Pin", ref=f"JLED{idx}", value=f"LED_OUT_{idx}",
             footprint="Connector_Molex:Molex_KK-254_AE-6410-03A_1x03_P2.54mm_Vertical")
    pf = Part("Device", "R", ref=f"F{idx}", value="Polyfuse_0.75A",  # Placeholder
              footprint="Fuse:Fuse_1206_3216Metric")
    tvs= Part("Device", "D_TVS", ref=f"D{idx}", value="TVS5V",
              footprint="Diode_SMD:D_SOD-323")
    rs = Part("Device", "R", ref=f"RLED{idx}", value="330R",
              footprint="Resistor_SMD:R_0603_1608Metric")
    pf[1] += led_5v; pf[2] += j[1]
    tvs[1] += j[1]; tvs[2] += gnd
    # Reference placeholder pins
    rs[1] += j[2]
    rs[2] += Net(f"LED_DATA{idx}_OUT")
    j[3] += gnd
    return {"conn": j, "ls_in": Net(f"LED_DATA{idx}_IN")}

led_ports = [led_port(i+1) for i in range(4)]
for i, lp in enumerate(led_ports):
    lp["ls_in"] += led_din[i]

# I2C accessory ports (4×)
def i2c_port(ref, name, vcc_net):
    global gnd, sda, scl  # Reference global power and signal nets
    j = Part("Connector", "Conn_01x04_Pin", ref=ref, value=name,
             footprint="Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal")
    j[1] += gnd; j[2] += vcc_net; j[3] += sda; j[4] += scl
    return j

j_i2c1 = i2c_port("J3", "I2C_PORT_1_3V3", v3v3)
j_i2c2 = i2c_port("J4", "I2C_PORT_2_3V3", v3v3)
j_i2c3 = i2c_port("J5", "I2C_PORT_3_5V",  led_5v)
j_i2c4 = i2c_port("J6", "I2C_PORT_4_5V",  led_5v)

# FRU EEPROM (24LC02 - 256 byte I2C EEPROM)
# Note: Using generic EEPROM placeholder
u_fru = Part("Memory_EEPROM", "24LC256", ref="U4",  # Use compatible EEPROM symbol
             footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm")
u_fru[1] += Net("A0"); u_fru[2] += Net("A1"); u_fru[3] += Net("A2")
u_fru[4] += gnd
u_fru[5] += sda
u_fru[6] += scl
u_fru[7] += gnd
u_fru[8] += v3v3

# I2S mic headers (2×)
def i2s_mic_header(ref, name):
    global v3v3, gnd, i2s_bclk, i2s_lrck, i2s_sd  # Reference global nets
    j = Part("Connector", "Conn_01x06_Pin", ref=ref, value=name,
             footprint="Connector_JST:JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Horizontal")
    j[1] += v3v3; j[2] += gnd; j[3] += i2s_bclk; j[4] += i2s_lrck; j[5] += i2s_sd
    return j

j_mic1 = i2s_mic_header("J7", "I2S_MIC_1")
j_mic2 = i2s_mic_header("J8", "I2S_MIC_2")

# ---------- Final PDM pin map (EdgeS3[D] COM-A) + 0R bypass options ----------
# COM-A module nets: tie these to EdgeS3[D] I2S0 PDM-capable pins in KiCad.
#   CLK  -> route to the module's I2S0/PDM clock pad (see EdgeS3[D] pin map).
#   DATA -> route to the module's I2S0/PDM data pad (keep off COM-B SPI GPIO12/13).
coma_pdm_clk  = Net("COMA_PDM_CLK")
coma_pdm_data = Net("COMA_PDM_DATA")

# Mic-side nets (go to the PDM header)
mic_pdm_clk  = Net("MIC_PDM_CLK")     # Header pin 3
mic_pdm_data = Net("MIC_PDM_DATA")    # Header pin 4

# --- 0-ohm population options: direct (3.3V build) vs translator (1.8V build) ---
# Direct path links (DNP when using 1.8V + translator):
r_bypass_clk  = Part("Device", "R", ref="R_BYPASS_CLK",  value="0R",
                     footprint="Resistor_SMD:R_0603_1608Metric")
r_bypass_data = Part("Device", "R", ref="R_BYPASS_DATA", value="0R",
                     footprint="Resistor_SMD:R_0603_1608Metric")
# Wire direct path: MCU <-> MIC (place only for 3.3V mic builds)
r_bypass_clk[1]  += coma_pdm_clk
r_bypass_clk[2]  += mic_pdm_clk
r_bypass_data[1] += mic_pdm_data
r_bypass_data[2] += coma_pdm_data

# Translator path (SN74AXC2T245): for 1.8V build
# When using 1.8V mic, populate U8 + R_LVT_* (DNP the bypass links)
u_lvt = Part("Device", "R", ref="U8", value="Logic_Buffer_SN74AXC2T245",  # Placeholder for translator
             footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm")

# Translator path jumpers (DNP when using direct 3.3V path):
r_lvt_clk_in   = Part("Device", "R", ref="R_LVT_CLK_IN",   value="0R",
                      footprint="Resistor_SMD:R_0603_1608Metric")  # MCU -> LVT.B1
r_lvt_clk_out  = Part("Device", "R", ref="R_LVT_CLK_OUT",  value="0R",
                      footprint="Resistor_SMD:R_0603_1608Metric")  # LVT.A1 -> MIC
r_lvt_data_in  = Part("Device", "R", ref="R_LVT_DATA_IN",  value="0R",
                      footprint="Resistor_SMD:R_0603_1608Metric")  # MIC -> LVT.A2
r_lvt_data_out = Part("Device", "R", ref="R_LVT_DATA_OUT", value="0R",
                      footprint="Resistor_SMD:R_0603_1608Metric")  # LVT.B2 -> MCU

# Connect translator paths (simplified for netlist)
r_lvt_clk_in[1]   += coma_pdm_clk
r_lvt_clk_in[2]   += mic_pdm_clk  # Direct path for now; 1.8V buffer in KiCad

r_lvt_data_in[1]  += mic_pdm_data
r_lvt_data_in[2]  += coma_pdm_data  # Direct path for now; 1.8V buffer in KiCad

# TODO: Replace U8 with SN74AXC2T245 logic level translator in KiCad

# Series damping on the clock near the source (helps ringing at multi-MHz)
r_pdm_clk_series = Part("Device", "R", ref="R_PDM_CLK_SER", value="33R",
                        footprint="Resistor_SMD:R_0603_1608Metric")
# Place this in series on the clock path. For 1.8V build: between LVT output (A1) and MIC header.
# For 3.3V build: naturally in series via bypass link. Populate accordingly in layout.
r_pdm_clk_series[1] += coma_pdm_clk  # From COM-A PDM clock
r_pdm_clk_series[2] += mic_pdm_clk  # To header

# PDM header (J9): tie MIC_PDM_CLK/DATA to header pins
j_pdm = Part("Connector", "Conn_01x06_Pin", ref="J9", value="PDM_MIC_HEADER",
             footprint="Connector_JST:JST_GH_SM06B-GHS-TB_1x06-1MP_P1.25mm_Horizontal")
j_pdm[1] += v3v3
j_pdm[2] += gnd
j_pdm[3] += mic_pdm_clk
j_pdm[4] += mic_pdm_data
j_pdm[5] += Net("SEL")  # mic select (tie to 0 for IM69D130, leave open/1.8V for SPH0645)

# COM-A: K1-M2B compute slot (placeholder - use generic 40-pin dual-row connector)
j_coma = Part("Connector", "Conn_01x40_Pin", ref="J11", value="K1-M2B_COM-A",
              footprint="Connector_PinHeader_2.54mm:PinHeader_1x40_P2.54mm_Vertical")
# TODO: Replace with proper 2x20 or 2x30 connector footprint in KiCad
j_coma[1]  += v3v3
j_coma[2]  += gnd
j_coma[3]  += usb_dp_soc
j_coma[4]  += usb_dm_soc
j_coma[5]  += sda
j_coma[6]  += scl
j_coma[7]  += Net("UART_TX_A")
j_coma[8]  += Net("UART_RX_A")
j_coma[9]  += spi_sck_src
j_coma[10] += spi_mosi_src
j_coma[11] += spi_miso
j_coma[12] += spi_cs
j_coma[13] += sync
j_coma[14] += ready
j_coma[15] += i2s_bclk
j_coma[16] += i2s_lrck
j_coma[17] += i2s_sd
j_coma[18] += coma_pdm_clk
j_coma[19] += coma_pdm_data
for pin in range(20, 25):
    j_coma[pin] += Net(f"COMA_GPIO{pin-19}")

# COM-B: Bare ESP32-S3 renderer
if USE_GENERIC_COMB:
    u_comb = Part("Connector", "Conn_01x40_Pin", ref="J12", value="ESP32-S3_COM-B_LOGICAL",
                  footprint="Connector_PinHeader_2.54mm:PinHeader_1x40_P2.54mm_Vertical")
    # TODO: Replace with proper 2x20 connector footprint in KiCad
    u_comb[1]  += v3v3
    u_comb[2]  += gnd
    en_n   = Net("CHIP_PU")
    boot   = Net("GPIO0_BOOT")
    u_comb[3]  += en_n
    u_comb[4]  += boot
    u_comb[5]  += spi_sck
    u_comb[6]  += spi_mosi
    u_comb[7]  += spi_miso_src
    u_comb[8]  += spi_cs
    u_comb[9]  += sync
    u_comb[10] += ready
    for i in range(4):
        u_comb[11+i] += led_din[i]
    u_comb[15] += Net("UART_TX_B")
    u_comb[16] += Net("UART_RX_B")

# EN/BOOT startup
r_en = Part("Device", "R", value="10k", ref="R3",
            footprint="Resistor_SMD:R_0603_1608Metric")
c_en = Part("Device", "C", value="1u",  ref="C3",
            footprint="Capacitor_SMD:C_0603_1608Metric")
r_en[1] += v3v3; r_en[2] += en_n
c_en[1] += en_n; c_en[2] += gnd

r_boot = Part("Device", "R", value="10k", ref="R4",
              footprint="Resistor_SMD:R_0603_1608Metric")
r_boot[1] += v3v3; r_boot[2] += boot
sw_boot = Part("Device", "R", ref="SW1", value="Push_Button",  # Placeholder for push button
               footprint="Button_Switches_SMD:SW_DIP_SPSTx01_Slide_7.0x5.0mm_W7.0mm_P1.27mm_LowProfile")
sw_boot[1] += boot
sw_boot[2] += gnd
# TODO: Replace SW1 with actual push button (e.g., through-hole momentary switch)

# QSPI flash for COM-B
# Placeholder: W25Q128JV SPI flash
# In KiCad, add W25Q128JV (SOIC-16) with:
#   - CS#, CLK, DI (MOSI), DO (MISO) to ESP32-S3 QSPI pins
#   - IO2 (WP#) and IO3 (HOLD#) pulled high
flash_cs   = Net("FLASH_CS")
flash_clk  = Net("FLASH_CLK")
flash_io0  = Net("FLASH_IO0")
flash_io1  = Net("FLASH_IO1")
flash_io2  = Net("FLASH_IO2_WP")
flash_io3  = Net("FLASH_IO3_HOLD")

# Pull-up resistors for WP# and HOLD#
r_wp   = Part("Device", "R", value="10k", ref="R5",
              footprint="Resistor_SMD:R_0603_1608Metric")
r_wp[1] += v3v3; r_wp[2] += flash_io2
r_hold = Part("Device", "R", value="10k", ref="R6",
              footprint="Resistor_SMD:R_0603_1608Metric")
r_hold[1] += v3v3; r_hold[2] += flash_io3
# TODO: Add W25Q128JV (U6) in KiCad and wire QSPI signals

# 40 MHz crystal
# Placeholder: 40MHz crystal (will be manually added in KiCad)
# Typical 40MHz crystal connections:
#   - Pin 1: XTAL_IN (to ESP32-S3 pad)
#   - Pin 2: XTAL_OUT (to ESP32-S3 pad)
#   - Pin 3 & 4: GND
xtal_n1 = Net("XIN_40M")
xtal_n2 = Net("XOUT_40M")

# Load capacitors (12pF typical for 40MHz)
c_x1 = Part("Device", "C", value="12p", ref="C4",
            footprint="Capacitor_SMD:C_0603_1608Metric")
c_x2 = Part("Device", "C", value="12p", ref="C5",
            footprint="Capacitor_SMD:C_0603_1608Metric")
c_x1[1] += xtal_n1; c_x1[2] += gnd
c_x2[1] += xtal_n2; c_x2[2] += gnd
# TODO: Add 40MHz crystal oscillator (Y1) in KiCad

# Generate netlist
ERC()
generate_netlist(fmt='kicad')
print(f"✅ Generated: Netlist (KiCad format)")
