## Power (Rev-A)
- **Primary input:** **USB-C, 5 V (sink), up to 3 A**. Type-C current mode; no PD negotiation required.
- **Usage:** powers **controller logic only** (compute cards, radios, codecs, accessories).
- **LED power:** **external 5 V supply required** for LED loads. Routed through baseboard; never back-feeds USB-C.
- **LED power ingress:** locking high-current connector (Micro-Fit 3.0 / XT30). Ideal-diode/OR-FET on LED 5 V input prevents reverse feed into USB 5 V.
- **Per-port protection:** polyfuse + low-cap TVS on LED 5 V, ESD on DATA, 300–500 Ω series resistor at the driver.

## LED Outputs (Rev-A)
- **Populated now:** **4× one-wire** (WS2812/SK6812), 5 V level-shifted (SN74AHCT125).
- **Reserved (DNP):** **+4× one-wire** and **2× SPI (HD108)** headers with matched-length stubs & keepouts.
- **Throughput targets:** one-wire @800 kHz ≈30 µs/LED → **60 FPS ≈ 555 LED/port**, **120 FPS ≈ 277 LED/port** (margin excludes reset). SPI (future) targets **≥ 300 FPS** at similar counts.

## USB-C
- **Sink policy:** 5 V only, up to 3 A if advertised; otherwise 1.5 A.  
- **Protection:** input fuse or e-fuse, ideal-diode, ESD (CC/D+/D–), inrush limiting.

## Accessory Ports
- **Electrical:** I²C, pin order **GND, VCC, SDA, SCL**; **3.3 V default**; **two ports switchable to 5 V** (level-safe).  
- **Mechanical:** dual-footprints per port (DNP one): **JST-SH 1.0 mm** (Qwiic) and **JST-GH 1.25 mm** (latching).  
- **Bus hygiene:** 100 kHz default, 400 kHz on short chains; optional I²C mux to segment long runs.

## Environment & Thermal
- **Ambient:** **0–50 °C** nominal.  
- **Thermal policy:** derate LED current above **60 °C** PCB; warn > 70 °C; cutback on LED-bus sag < 4.6 V.

## Compliance & DFM
- **EMC/ESD:** CISPR-32 Class B pre-scan; ±8 kV air / ±4 kV contact on user IO.  
- **Panelization:** KiKit — V-cuts when panel ≥ 70×70 mm, else mouse-bites; 5 mm rails; global + per-board fiducials.
- **CI artifacts:** ERC/DRC (JSON), Gerbers, Drill, **iBOM**, **STEP**, **GLB** on every PR.
