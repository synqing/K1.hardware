# hardware/k1-lightwave/skidl/k1_motherboard_revA.py
# K1 Lightwave – Rev-A Motherboard Skeleton (SKiDL)
# Purpose:
#   - Define power domains & connectors (USB-C 5V for logic; external LED_5V for LEDs)
#   - Instantiate 4x one-wire LED ports (level shifted), reserve pads for +4 and 2x SPI (later)
#   - Provide I2C accessory ports (Qwiic-compatible pin order) with dual-footprint intent
#   - Add slot FRU EEPROM (one shown; replicate per slot in layout phase)
#
# Notes:
#   - This generates a netlist only; KiCad symbols must be available locally.
#   - RefDes and values are illustrative; footprint binding happens in KiCad/KiBot.

from skidl import *

# ---------- Nets / Power domains ----------
gnd         = Net("GND")
usb_5v      = Net("VBUS_USB_5V")   # 5V from USB-C (controller-only domain)
led_5v      = Net("LED_5V")        # 5V from external supply (LED domain)
v3v3        = Net("+3V3")          # logic rail from buck converter

# ---------- USB-C sink (5V only; no PD) ----------
# USB-C receptacle (USB2.0-only symbol)
j_usbc = Part("Connector_USB", "USB_C_Receptacle_USB2.0", ref="J1", footprint="Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12")
# CC pull-downs (Rd ~5.1k) to advertise as Sink
r_cc1 = Part("Device", "R", value="5.1k", ref="R1")
r_cc2 = Part("Device", "R", value="5.1k", ref="R2")
# ESD protection (placeholder diode arrays)
d_esd_usbc = Part("Device", "ESD_Protection", ref="D1")

# Wire CC pins
j_usbc["CC1"] += r_cc1[1]
r_cc1[2]      += gnd
j_usbc["CC2"] += r_cc2[1]
r_cc2[2]      += gnd

# VBUS to controller domain; add input protection placeholders
# (In PCB: place ideal-diode/e-fuse + inrush limiter before feeding usb_5v.)
j_usbc["VBUS, VBUS"] += usb_5v
# USB data to MCU (left unconnected here; routed in compute card)
# j_usbc["D+, D-"] -> compute slot USB signals
# Shield & GND
j_usbc["SHIELD"] += gnd
j_usbc["GND, GND"] += gnd

# ---------- 5V->3V3 buck (symbol as placeholder regulator) ----------
u_buck = Part("Regulator_Switching", "TPS62133", ref="U2")  # example; swap per BOM
u_buck["VIN"] += usb_5v
u_buck["VOUT"] += v3v3
u_buck["GND"] += gnd

# ---------- External LED 5V input ----------
j_led_in = Part("Connector", "Conn_01x02", ref="J2", value="LED_5V_IN", footprint="Connector_Molex:Molex_MicroFit_3.0_1x02")
j_led_in[1] += led_5v
j_led_in[2] += gnd
# NOTE: In PCB, place ideal-diode/OR-FET here to block backfeed to USB 5V.

# ---------- Level shifter (AHCT125) for 4x LED DATA ----------
u_ls = Part("Logic_LevelTranslator", "SN74AHCT125", ref="U3")  # quad buffer; OE pins to +5V enable

# Per-port protection components (polyfuse + TVS), series resistor on DATA
def led_port(idx: int):
    # 3-pin LED output connector (5V, DATA, GND)
    j = Part("Connector", "Conn_01x03", ref=f"JLED{idx}", value=f"LED_OUT_{idx}", footprint="Connector_Molex:Molex_KK-254_1x03")
    # Polyfuse on 5V leg
    f = Part("Device", "Polyfuse_Small", ref=f"F{idx}", value="0.75A")
    # TVS diode on 5V to GND
    d = Part("Device", "D_TVS", ref=f"D{idx}", value="TVS5V")
    # Series resistor on DATA (damp ringing; 300–500Ω)
    r = Part("Device", "R", ref=f"RLED{idx}", value="330R")

    # Wire 5V path: LED_5V -> Polyfuse -> Connector V
    led_5v += f[1]
    f[2]    += j[1]
    # TVS: 5V to GND near connector
    d[1]    += j[1]
    d[2]    += gnd
    # DATA: AHCT125 output -> series R -> connector DATA
    # Map LS channels 1..4 to ports 1..4
    ls_out = u_ls["Y{}".format(idx)]
    ls_oe  = u_ls["OE{}".format(idx)]
    ls_in  = u_ls["A{}".format(idx)]
    # OE tied high to +5V (comes from LED_5V via local LDO if needed; use logic 5V rail in PCB)
    ls_oe += led_5v
    # Series resistor
    ls_out += r[1]
    r[2]   += j[2]
    # GND
    j[3]   += gnd

    return j, f, d, r, ls_in

# Instantiate 4x LED ports (DATA inputs to be driven by MCU GPIOs later)
ports = {}
for i in range(1, 5):
    j, f, d, r, ls_in = led_port(i)
    ports[i] = {"conn": j, "pfuse": f, "tvs": d, "rser": r, "ls_in": ls_in}

# ---------- Accessory I2C ports (Qwiic/STEMMA pin order: GND,VCC,SDA,SCL) ----------
def i2c_port(ref, name, vcc=v3v3):
    j = Part("Connector", "Conn_01x04", ref=ref, value=name, footprint="Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal")
    # GND, VCC, SDA, SCL
    j[1] += gnd
    j[2] += vcc
    j[3] += Net("SDA")
    j[4] += Net("SCL")
    return j

j_i2c1 = i2c_port("J3", "I2C_PORT_1_3V3", v3v3)
j_i2c2 = i2c_port("J4", "I2C_PORT_2_3V3", v3v3)
# Switchable 5V ports (label; in PCB add level-safe buffers or ensure devices are 5V-tolerant)
j_i2c3 = i2c_port("J5", "I2C_PORT_3_5V", led_5v)   # supply pin is 5V; data still referenced to 3V3 domain via level-shifter on board
j_i2c4 = i2c_port("J6", "I2C_PORT_4_5V", led_5v)

# ---------- FRU EEPROM on I2C (slot identity) ----------
u_fru = Part("Memory_EEPROM", "24LC02", ref="U4", footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm")
u_fru["VCC"] += v3v3
u_fru["GND"] += gnd
u_fru["SDA"] += Net("SDA")
u_fru["SCL"] += Net("SCL")
# Address pins: tie low for FRU#0
u_fru["A0, A1, A2"] += gnd

# ---------- Expose MCU LED DATA inputs so firmware knows where to wire ----------
# In layout: connect these to ESP32-S3 GPIOs on the compute card(s).
for i in range(1, 5):
    ports[i]["ls_in"] += Net(f"LED_DATA{i}_IN")

# ---------- ERC helpers ----------
ERC()
generate_netlist("k1_motherboard_revA.net")
