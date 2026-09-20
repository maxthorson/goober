# Parts and cost — Goober Rev A

This is the purchasing list for one prototype. Budget roughly **US$50–100 plus shipping and tax** for a small PCB order, parts and a basic print if you already have soldering tools. This is a planning allowance, not a live supplier quote. Small-order shipping and switch/keycap choices can dominate the total. A soldering service or purchased tools add cost.

Buy spare LEDs, sockets and small components; quantities below are what one board uses. The design intentionally uses a ready-made USB-C controller and two PCB layers to keep the first build manageable. There is no hub or charging passthrough in this revision.

| Ref | Qty | Buy this | Package / selection detail |
|---|---:|---|---|
| PCB | 1 | Goober Rev A.1 carrier | 80 × 96 mm, 2 layers, 1.6 mm FR-4; Gerber ZIP supplied |
| U1 | 1 | Waveshare **RP2040-Zero** | USB-C, 18 × 23.5 mm; get the unpopulated-header version so mounting height can be set |
| SW1–SW9 | 9 | Kailh **CPG151101S11** MX hot-swap sockets | Original MX style; Choc/low-profile sockets do not fit |
| D1–D9 | 9 | OPSCO **SK6812MINI-E-012** | Reverse mount, 3.2 × 2.8 mm, 12 mA/channel version; order 12–15. LCSC C5149201 is the source used for the datasheet |
| ENC1 | 1 | Alps Alpine **EC11E15244G1** | Push switch, 30 detents/15 pulses, 20 mm actuator. A generic EC11 may have a different height or pulse count |
| OLED | 1 | Waveshare **0.91inch OLED Module**, SKU 14657 | SSD1306, I²C, 128 × 32, monochrome white, 36 × 12.5 mm board; 3.3 V operation |
| U2 | 1 | Texas Instruments **SN74AHCT125D** or **SN74AHCT125DR** | SOIC-14, 3.9 mm body / 1.27 mm pitch. The D/DR package matters; do not substitute HC or AHC |
| Q1 | 1 | Alpha & Omega **AO3401A** | P-channel MOSFET, SOT-23, pin 1 gate / 2 source / 3 drain |
| Q2 | 1 | onsemi **MMBT3904LT1G** | NPN, SOT-23, pin 1 base / 2 emitter / 3 collector |
| F1 | 1 | Littelfuse **1206L050YR** | 0.5 A hold resettable PTC, 1206 footprint |
| C1–C10 | 10 | 100 nF ceramic, 16 V or higher, X7R | 0805 imperial / 2012 metric. C1–C9 on bottom; C10 on top |
| C11 | 1 | 4.7 µF ceramic, 16 V, X5R or X7R | 0805 imperial / 2012 metric |
| R1, R3 | 2 | 100 kΩ, 1%, ≥0.125 W | 0805 imperial / 2012 metric |
| R2 | 1 | 10 kΩ, 1%, ≥0.125 W | 0805 |
| R4 | 1 | 330 Ω, 1%, ≥0.125 W | 0805 |
| R5, R6, R9 | 3 | 4.7 kΩ, 1%, ≥0.125 W | 0805 |
| R7, R8 | 2 | 3.3 kΩ, 1%, ≥0.125 W | 0805 |
| J1 wiring | 1 set | Four flexible insulated wires, 28–30 AWG, about 50 mm each | Solder directly into J1 pads; **do not install a tall pin header under the OLED cradle**. Use the OLED's included harness or its labeled solder holes |
| U1 interconnect | 23 pins | 2.54 mm pitch, 0.64 mm square breakaway pin strips | Cut into 2 × 9-pin and 1 × 5-pin strips; enough pin length for both boards plus a **3.0 mm gap**. Soldered module; not a plug-in socket |
| Switches | 9 | MX-compatible, standard-height, 3-pin or 5-pin | Choose translucent/RGB-compatible housing and your preferred feel. The switch must suit a 1.5 mm plate |
| Keycaps | 9 | 1u MX-stem keycaps | Uniform profile is simplest; shine-through or translucent sides show more light |
| Case | 1 set | Printed base + lid | STL and editable OpenSCAD source included |
| Knob | 1 | Printed Goober knob | 6 mm D-shaft fit. The supplied knob is 20 mm diameter × 14 mm tall |
| Inserts | 4 | M2.5 brass heat-set inserts | Nominal OD 3.8 mm × 4.0 mm long; test the coupon with the actual brand |
| Front screws | 2 | M2.5 × 12 mm machine screws | Pan/button head, not countersunk; front is the key side |
| Rear screws | 2 | M2.5 × 18 mm machine screws | Pan/button head; rear is the OLED/encoder side |
| Feet | 4 | 8 mm adhesive rubber feet | Thickness ≥1 mm; recess is 0.6 mm deep |
| OLED attachment | small amount | Thin electronics-safe double-sided tape | Only under PCB edges on the cradle ledges; do not press or tape the display glass |
| Cable | 1 | USB-C data cable to suit the Mac | Charging-only cables cannot send keys; plug body should fit the 14 × 8 mm rear opening |

The hot-swap feature applies to the **nine switches**. The sockets, LEDs, encoder, controller and other electronics are soldered permanently in this low-cost prototype.

## Tools you need physically

Temperature-controlled fine-tip soldering iron, solder, flux, fine tweezers, solder wick, magnification, flush cutters, multimeter, calipers, a small screwdriver and a switch puller. Use ventilation for soldering. Heat-set inserts need a suitable iron tip. A USB current meter is useful for testing; a current-limited 5 V supply or current-limited USB test adapter helps with first power-up. A PCB assembly service can handle the small surface-mount parts if you prefer.

Use your own printer and its slicer, or send the STLs to a print service. You do not need to buy a printer.

## Source pages used for component selection

- [Waveshare RP2040-Zero](https://www.waveshare.com/wiki/RP2040-Zero)
- [Waveshare OLED](https://www.waveshare.com/product/ai/0.91inch-oled-module.htm)
- [Alps encoder specification](https://tech.alpsalpine.com/e/products/detail/EC11E15244G1/)
- [TI buffer](https://www.ti.com/product/SN74AHCT125)
- [AO3401A datasheet](https://www.aosmd.com/pdfs/datasheet/AO3401A.pdf)
- [onsemi transistor datasheet](https://www.onsemi.com/pdf/datasheet/mmbt3904lt1-d.pdf)
- [SK6812MINI-E-012 datasheet](../hardware/sk6812mini-e.pdf)

Check the exact part and package at checkout. A listing that only says “Pico,” “0.91 OLED,” “EC11” or “SK6812” does not establish compatibility with these files.
