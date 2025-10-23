# hardware/k1-lightwave/skidl/k1_motherboard_revA.py
# K1 Lightwave – Rev-A Motherboard (complete SKiDL netlist generator)
# Dual-MCU system: COM-A (ESP32-S3-WROOM-1 module) + COM-B (bare ESP32-S3)
# Power domains: VBUS_USB_5V (logic), LED_5V (external)
# 4× independent LED ports, I2C accessories, I2S mics, inter-MCU SPI+SYNC

import skidl
from skidl import *
import sys
import os

# Configure KiCad library paths (cross-platform)
import platform
if platform.system() == 'Darwin':
    skidl.config.kicad_lib_path = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols'
else:
    # Linux/Ubuntu
    skidl.config.kicad_lib_path = os.getenv('KICAD_SYMBOL_DIR', '/usr/share/kicad/symbols')

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
r_spi_sck = Part("Device", "R", ref="R_SPI_SCK_SER", value="33R")
r_spi_mosi = Part("Device", "R", ref="R_SPI_MOSI_SER", value="33R")
r_spi_miso = Part("Device", "R", ref="R_SPI_MISO_SER", value="33R")
r_spi_sck[1] += spi_sck_src;   r_spi_sck[2] += spi_sck
r_spi_mosi[1] += spi_mosi_src; r_spi_mosi[2] += spi_mosi
r_spi_miso[1] += spi_miso_src; r_spi_miso[2] += spi_miso

# SPI CS deassert default
r_spi_cs = Part("Device", "R", ref="R_SPI_CS_PU", value="10k")
r_spi_cs[1] += v3v3
r_spi_cs[2] += spi_cs

# READY line idles low to avoid false asserts on GPIO39 boot pull-ups
r_ready_pd = Part("Device", "R", ref="R_READY_PD", value="100k")
r_ready_pd[1] += ready
r_ready_pd[2] += gnd

# I2S (to COM-A)
i2s_bclk    = Net("I2S_BCLK")
i2s_lrck    = Net("I2S_LRCK")
i2s_sd      = Net("I2S_SD")

# LED data (COM-B → level shifters)
led_din = [Net(f"LED_DATA{i}_IN") for i in range(1,5)]

# USB-C receptacle with ESD protection
j_usbc = Part("Connector_USB", "USB_C_Receptacle_USB2.0", ref="J1",
              footprint="Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12")
r_cc1 = Part("Device", "R", value="5.1k", ref="R1")
r_cc2 = Part("Device", "R", value="5.1k", ref="R2")
j_usbc["CC1"] += r_cc1[1]; r_cc1[2] += gnd
j_usbc["CC2"] += r_cc2[1]; r_cc2[2] += gnd
j_usbc["D+"] += usb_dp_conn
j_usbc["D-"] += usb_dm_conn
j_usbc["SHIELD"] += gnd
j_usbc["GND, GND"] += gnd

# USB input fuse (1A, overcurrent protection per PRD spec)
f_usb = Part("Device", "Fuse", ref="F_USB", value="1A_1206")
j_usbc["VBUS, VBUS"] += f_usb[1]
f_usb[2] += usb_5v

# USB ESD protection (TPD4E05U06 – 4-channel, < 0.5 pF for USB2.0 compliance)
u_esd = Part("Protection", "TPD4E05U06", ref="U1", value="TPD4E05U06")
u_esd["VCC"]     += v3v3
u_esd["GND"]     += gnd
u_esd["IN_A"]    += usb_dp_conn
u_esd["OUT_A"]   += usb_dp_post
u_esd["IN_B"]    += usb_dm_conn
u_esd["OUT_B"]   += usb_dm_post
u_esd["IN_C"]    += j_usbc["CC1"]
u_esd["OUT_C"]   += j_usbc["CC1"]
u_esd["IN_D"]    += j_usbc["CC2"]
u_esd["OUT_D"]   += j_usbc["CC2"]

# USB FS series damping near COM-B (GPIO19/20)
r_usb_dp = Part("Device", "R", ref="R_USB_DP_SER", value="27R")
r_usb_dm = Part("Device", "R", ref="R_USB_DM_SER", value="27R")
r_usb_dp[1] += usb_dp_post
r_usb_dp[2] += usb_dp_soc
r_usb_dm[1] += usb_dm_post
r_usb_dm[2] += usb_dm_soc

# 5V→3V3 buck (TPS62160: synchronous step-down, 5V→3.3V, 1.5A)
u_buck = Part("Regulator_Switching", "TPS62160", ref="U2")
u_buck["VIN"]  += usb_5v
u_buck["VOUT"] += v3v3
u_buck["GND"]  += gnd

# External LED 5V ingress with ideal diode blocking (LTC4412)
j_led_in = Part("Connector", "Conn_01x02", ref="J2", value="LED_5V_IN",
                footprint="Connector_Molex:Molex_MicroFit_3.0_1x02")
led_in_raw = Net("LED_5V_RAW")  # Before ideal diode
j_led_in[1] += led_in_raw
j_led_in[2] += gnd

# Ideal diode controller (LTC4412) + external P-FET for reverse-blocking on LED power
# Prevents back-feed from LED_5V rail into USB 5V during bulk-cap discharge
u_ideal_diode = Part("Power_Management", "LTC4412", ref="U5", value="LTC4412")
u_ideal_diode["IN"]  += led_in_raw
u_ideal_diode["OUT"] += led_5v
u_ideal_diode["GND"] += gnd
# P-FET (BSS84) gate drive for logic-level reverse-blocking
# LTC4412 pulls GATE to ground when conducting; P-FET (gate at GND) turns ON
# When source voltage drops, gate goes high via pull-up, P-FET blocks reverse current
p_fet = Part("Transistor_FET", "BSS84", ref="Q1", value="BSS84")
u_ideal_diode["GATE"] += p_fet["G"]
p_fet["S"] += led_5v    # Source tied to output (LED_5V)
p_fet["D"] += led_in_raw  # Drain tied to input (LED_5V_RAW)

# Current monitor on LED_5V bus (INA226 – I2C, high-side, 36V capable)
u_ina226 = Part("Sensor_Current", "INA226", ref="U7", value="INA226")
u_ina226["VS"]  += v3v3
u_ina226["GND"] += gnd
u_ina226["SDA"] += sda
u_ina226["SCL"] += scl
u_ina226["VBUS"] += led_5v  # Power supply for INA226 (floating or rail voltage)
# Shunt resistor for current measurement (sized for ~3A max, ~100mV drop at 3A → 0.033Ω nominal, use 0.05Ω for margin)
r_shunt = Part("Device", "R", ref="R7", value="0.05R", footprint="Resistor_SMD:R_2512_6332Metric_Pad1.52x3.35mm_HandSolder")
# Shunt in series: LED_5V → r_shunt → INA226[VIN+]; INA226[VIN-] → GND
r_shunt[1] += led_5v
r_shunt[2] += u_ina226["VIN+"]
u_ina226["VIN-"] += gnd

# LED outputs: 4× one-wire with AHCT125 shifter
u_ls = Part("Logic_74xx", "74AHCT125", ref="U3")

def led_port(idx: int):
    j = Part("Connector", "Conn_01x03", ref=f"JLED{idx}", value=f"LED_OUT_{idx}",
             footprint="Connector_Molex:Molex_KK-254_1x03")
    pf = Part("Device", "Polyfuse_Small", ref=f"F{idx}", value="0.75A")
    tvs= Part("Device", "D_TVS", ref=f"D{idx}", value="TVS5V")
    rs = Part("Device", "R", ref=f"RLED{idx}", value="330R")
    led_5v += pf[1]; pf[2] += j[1]
    tvs[1] += j[1]; tvs[2] += gnd
    y = u_ls[f"Y{idx}"]; oe = u_ls[f"OE{idx}"]; a = u_ls[f"A{idx}"]
    oe += led_5v
    y  += rs[1]; rs[2] += j[2]
    j[3] += gnd
    return {"conn": j, "ls_in": a}

led_ports = [led_port(i+1) for i in range(4)]
for i, lp in enumerate(led_ports):
    lp["ls_in"] += led_din[i]

# I2C accessory ports (4×)
def i2c_port(ref, name, vcc_net):
    j = Part("Connector", "Conn_01x04", ref=ref, value=name,
             footprint="Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal")
    j[1] += gnd; j[2] += vcc_net; j[3] += sda; j[4] += scl
    return j

j_i2c1 = i2c_port("J3", "I2C_PORT_1_3V3", v3v3)
j_i2c2 = i2c_port("J4", "I2C_PORT_2_3V3", v3v3)
j_i2c3 = i2c_port("J5", "I2C_PORT_3_5V",  led_5v)
j_i2c4 = i2c_port("J6", "I2C_PORT_4_5V",  led_5v)

# FRU EEPROM
u_fru = Part("Memory_EEPROM", "24LC02", ref="U4")
u_fru["VCC"] += v3v3; u_fru["GND"] += gnd
u_fru["SDA"] += sda;  u_fru["SCL"] += scl
u_fru["A0, A1, A2"] += gnd

# I2S mic headers (2×)
def i2s_mic_header(ref, name):
    j = Part("Connector", "Conn_01x06", ref=ref, value=name,
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
r_bypass_clk  = Part("Device", "R", ref="R_BYPASS_CLK",  value="0R")
r_bypass_data = Part("Device", "R", ref="R_BYPASS_DATA", value="0R")
# Wire direct path: MCU <-> MIC (place only for 3.3V mic builds)
r_bypass_clk[1]  += coma_pdm_clk
r_bypass_clk[2]  += mic_pdm_clk
r_bypass_data[1] += mic_pdm_data
r_bypass_data[2] += coma_pdm_data

# Translator path (SN74AXC2T245): for 1.8V build
# When using 1.8V mic, populate U8 + R_LVT_* (DNP the bypass links)
u_lvt = Part("Logic_Buffers", "SN74AXC2T245", ref="U8", value="SN74AXC2T245")

# Translator path jumpers (DNP when using direct 3.3V path):
r_lvt_clk_in   = Part("Device", "R", ref="R_LVT_CLK_IN",   value="0R")  # MCU -> LVT.B1
r_lvt_clk_out  = Part("Device", "R", ref="R_LVT_CLK_OUT",  value="0R")  # LVT.A1 -> MIC
r_lvt_data_in  = Part("Device", "R", ref="R_LVT_DATA_IN",  value="0R")  # MIC -> LVT.A2
r_lvt_data_out = Part("Device", "R", ref="R_LVT_DATA_OUT", value="0R")  # LVT.B2 -> MCU

# Connect translator pins: Channel1 for CLK (B1 ↔ A1), Channel2 for DATA (A2 ↔ B2)
r_lvt_clk_in[1]   += coma_pdm_clk
r_lvt_clk_in[2]   += u_lvt["B1"]
r_lvt_clk_out[1]  += u_lvt["A1"]
r_lvt_clk_out[2]  += mic_pdm_clk

r_lvt_data_in[1]  += mic_pdm_data
r_lvt_data_in[2]  += u_lvt["A2"]
r_lvt_data_out[1] += u_lvt["B2"]
r_lvt_data_out[2] += coma_pdm_data

# Direction straps (1.8V logic domain):
u_lvt["DIR1"] += v3v3    # logic '1' (B->A) for CLK
u_lvt["DIR2"] += gnd     # logic '0' (A->B) for DATA
u_lvt["OE"]   += v3v3    # enable
u_lvt["VCC_A"] += v3v3   # 3.3V side (COM-B)
u_lvt["VCC_B"] += Net("MIC_1V8")  # 1.8V side (mic domain); tie to 1.8V buck output
u_lvt["GND"]  += gnd

# Series damping on the clock near the source (helps ringing at multi-MHz)
r_pdm_clk_series = Part("Device", "R", ref="R_PDM_CLK_SER", value="33R")
# Place this in series on the clock path. For 1.8V build: between LVT output (A1) and MIC header.
# For 3.3V build: naturally in series via bypass link. Populate accordingly in layout.
r_pdm_clk_series[1] += u_lvt["A1"]  # Translator output (1.8V side)
r_pdm_clk_series[2] += mic_pdm_clk  # To header

# PDM header (J9): tie MIC_PDM_CLK/DATA to header pins
j_pdm = Part("Connector", "Conn_01x06", ref="J9", value="PDM_MIC_HEADER",
             footprint="Connector_JST:JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Horizontal")
j_pdm[1] += v3v3
j_pdm[2] += gnd
j_pdm[3] += mic_pdm_clk
j_pdm[4] += mic_pdm_data
j_pdm[5] += Net("SEL")  # mic select (tie to 0 for IM69D130, leave open/1.8V for SPH0645)

# COM-A: K1-M2B compute slot
j_coma = Part("Connector_Generic", "Conn_02x30_Odd_Even", ref="J11", value="K1-M2B_COM-A")
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
    u_comb = Part("Connector_Generic", "Conn_02x20_Odd_Even", ref="J12", value="ESP32-S3_COM-B_LOGICAL")
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
r_en = Part("Device", "R", value="10k", ref="R3")
c_en = Part("Device", "C", value="1u",  ref="C3")
r_en[1] += v3v3; r_en[2] += en_n
c_en[1] += en_n; c_en[2] += gnd

r_boot = Part("Device", "R", value="10k", ref="R4")
r_boot[1] += v3v3; r_boot[2] += boot
sw_boot = Part("Switch", "SW_Push", ref="SW1", value="BOOT_SW")
sw_boot[1] += boot; sw_boot[2] += gnd

# QSPI flash for COM-B
u_flash = Part("Memory_Flash", "W25Q128JV", ref="U6")
flash_cs   = Net("FLASH_CS")
flash_clk  = Net("FLASH_CLK")
flash_io0  = Net("FLASH_IO0")
flash_io1  = Net("FLASH_IO1")
flash_io2  = Net("FLASH_IO2_WP")
flash_io3  = Net("FLASH_IO3_HOLD")
u_flash["CS#"]  += flash_cs
u_flash["CLK"]  += flash_clk
u_flash["DO"]   += flash_io1
u_flash["DI"]   += flash_io0
u_flash["IO2"]  += flash_io2
u_flash["IO3"]  += flash_io3
u_flash["VCC"]  += v3v3
u_flash["GND"]  += gnd
r_wp   = Part("Device", "R", value="10k", ref="R5"); r_wp[1] += v3v3; r_wp[2] += flash_io2
r_hold = Part("Device", "R", value="10k", ref="R6"); r_hold[1] += v3v3; r_hold[2] += flash_io3

# 40 MHz crystal
xtal = Part("Device", "Crystal_GND2", ref="Y1", value="40MHz")
c_x1 = Part("Device", "C", value="12p", ref="C4")
c_x2 = Part("Device", "C", value="12p", ref="C5")
xtal_n1 = Net("XIN_40M")
xtal_n2 = Net("XOUT_40M")
xtal[1] += xtal_n1; xtal[2] += xtal_n2; xtal["GND"] += gnd
c_x1[1] += xtal_n1; c_x1[2] += gnd
c_x2[1] += xtal_n2; c_x2[2] += gnd

# Generate netlist
ERC()
generate_netlist(NETLIST_OUT)
print(f"✅ Generated: {NETLIST_OUT}")
