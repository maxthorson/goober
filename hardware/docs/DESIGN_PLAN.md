# Goober — revision A design plan

Status: revision A.1 digital design completed; physical prototype testing pending. USB hub/passthrough is deferred at the owner's request. One USB-C device connection remains.

## Product

- Nine MX mechanical switches in a 3×3 grid at 19.05 mm pitch.
- Kailh CPG151101S11 hot-swap sockets. Both 3-pin and 5-pin MX switches; select an RGB-compatible translucent switch housing.
- One reverse-mount SK6812MINI-E RGB LED per key, with a 5 V logic buffer and a switched lighting supply.
- One 128×32 SSD1306 I²C OLED. Shows layer, lighting state and last action.
- One detented encoder with push switch: clockwise volume up, counterclockwise volume down, press mute.
- Waveshare RP2040-Zero module: RP2040, flash, oscillator, USB-C and regulator on a small replaceable assembly.
- QMK firmware, editable source, compiled UF2, no Mac application required for normal operation.
- Two-layer FR-4 carrier PCB, 1.6 mm nominal, with printable case and removable top/plate.

The screen will report volume commands rather than an invented Mac volume percentage. Standard keyboard media reports do not return the host's actual volume.

## Design sequence and acceptance checks

1. Freeze component references and electrical pin assignments.
2. Create the schematic, PCB footprints, routing and BOM. Check the controller header orientation and every LED's power/data pinout against source drawings.
3. Run schematic electrical checks and PCB design-rule checks. Resolve shorts, open connections, copper clearance and outline errors.
4. Export copper, mask, silkscreen, outline and plated/non-plated drill files; inspect the exported geometry.
5. Build the enclosure around the same switch centers, PCB holes, controller port and encoder coordinates. Keep the switch plate thickness and height consistent with MX switch seating.
6. Compile the QMK target with the pinned source revision. Include default macros, lighting controls, display, encoder and bootloader access.
7. Deliver editable sources, prototype fabrication exports, printable geometry, mockups, parts list and assembly/test instructions.
8. Build and physically test a prototype before considering the design production validated.

## Power

USB-powered, with a 500 mA descriptor budget. Lighting brightness is capped in firmware. The LED rail is enabled only after USB configuration and is switched off during suspend. Brightness limiting is a design budget, not a measured current certification. Check startup, steady-state and suspend current on hardware.

The RP2040 GPIOs use 3.3 V logic. The OLED uses 3.3 V and pull-ups to 3.3 V. Addressable LEDs use 5 V; a TTL-input buffer translates their data signal. No accessory charging output, battery, USB 3 hub or laptop charging circuitry is in revision A.

## User's physical tasks

1. Choose nine compatible switches, keycaps and the enclosure color. Default concept: graphite case, light keycaps, silver knob.
2. Order the exact electronics from the BOM and a small batch of prototype boards after reviewing the delivered validation notes.
3. Order or print the case; print the fit coupon first if using an FDM printer.
4. Solder the permanent components, inspect joints, and check for shorts before connecting the controller.
5. Flash the supplied UF2 through the RP2040 bootloader.
6. Fit the plate, insert the hot-swap switches while supporting the sockets, and assemble the enclosure.
7. Run the supplied functional and power checks. Record any fit or electrical corrections for revision B.

## Software on the Mac

- KiCad: PCB/schematic editing, Gerber viewing, DRC and fabrication exports. https://www.kicad.org/download/macos/
- OpenSCAD: parametric case editing and STL export. https://openscad.org/downloads.html
- QMK CLI and Arm compiler: firmware builds. https://docs.qmk.fm/newbs_getting_started
- Printer-specific slicer only if printing at home. A print service can accept STL files directly.
- Homebrew, Git, Python and VS Code were already present.

Project-local firmware dependencies are installed under `tools/`. KiCad and OpenSCAD are installed under the user's Applications directory. QMK Toolbox and Arduino IDE are not required for UF2 drag-and-drop flashing.

## Sources

- RP2040 module and schematic: https://www.waveshare.com/wiki/RP2040-Zero
- OLED dimensions/interface: https://www.waveshare.com/product/ai/0.91inch-oled-module.htm
- QMK processor support: https://docs.qmk.fm/platformdev_rp2040
- QMK lighting: https://docs.qmk.fm/features/rgb_matrix
- QMK encoder: https://docs.qmk.fm/features/encoders
- QMK OLED: https://docs.qmk.fm/features/oled_driver
- Hot-swap socket: https://www.kailhswitch.com/info/kailh-switch-pcb-hot-swapping-socket-33463528.html
- Keyboard footprints: https://github.com/ebastler/marbastlib
