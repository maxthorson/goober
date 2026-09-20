# Build and test your Goober

The files are an **engineering prototype release**. The schematic and PCB pass automated electrical checks, the firmware compiles, and the case meshes pass digital checks. An assembled board has not yet been powered or physically fitted. Start with one build and use the checks below before ordering a larger batch.

## 1. Review and order

Read `PARTS_AND_COST.md` and `FABRICATION.md`. Upload `hardware/Goober-Rev-A-Gerbers.zip` to a PCB fabricator, select two layers, 1.6 mm FR-4 and 1 oz copper, and check the preview for the outside shape and all nine LED windows. Order the exact controller, encoder, OLED, LEDs and sockets in the parts list. Choose nine switches/keycaps and a case color.

The PCB is 80 × 96 mm. The assembled case is 86 × 102 mm, 18 mm high over the key plate, 24 mm over the control hood, and approximately 40 mm overall with the supplied knob, excluding feet. Keycap height varies with the chosen set.

## 2. Print the fit coupon, then the enclosure

All STLs use **millimetres**. Print at 100% scale. The coupon deliberately contains two separate pieces: a switch plate and an insert block. It tests 13.9, 14.0 and 14.1 mm switch openings in that order, and 3.3, 3.4 and 3.5 mm insert pilots. Use the same printer, material and settings as the case.

The supplied lid uses a 14.1 mm switch opening and a 1.5 mm plate. Check that your switch snaps in, sits flat and can be removed without breaking the clips. Test an insert in the 3.4 mm pilot. Adjust `switch_cut` or `insert_hole` in `case/goober.scad` and re-export if needed; do not scale the entire enclosure, because that moves every mounting hole.

Starting print settings: PLA or PETG, 0.4 mm nozzle, 0.15 mm layers (so the plate is ten layers), four walls and 25–35% infill. Print the base floor-down, knob bore-down, coupon flat. The lid has a raised roof and projecting spacers: orient it with the control roof toward the bed and use supports under the key plate and other overhangs. Inspect the slicer's layer preview and remove supports carefully from switch openings, OLED ledges and screw bores. A print service can choose an equivalent process and orientation.

Install four heat-set inserts into the base bosses from above, ending flush with the boss tops. Let them cool before fitting screws. Do not melt the bosses down or allow an insert to protrude into the PCB seating surface. The actual insert manufacturer's pilot recommendation and the coupon govern fit.

## 3. Solder and inspect the carrier PCB

“Top” is the side the switches and encoder enter. The controller, nine hot-swap sockets, nine LEDs and C1–C9 go on the **bottom**. Use the PCB drawings and reference labels to locate parts; the bottom drawing is mirrored as viewed from below.

1. Solder the small top-side parts first: R1–R9, C10–C11, F1, Q1, Q2 and U2. Check values and orientation. R and C parts are non-polarized. U2's pin-1 mark must match pin 1 in KiCad; Q1 and Q2 are different parts despite sharing a package.
2. Solder C1–C9 and reverse-mount LEDs on the bottom. Each LED's emitting body goes into its milled PCB window and shines upward toward the switch. **LED pin 1 is GND, pin 2 is data in, pin 3 is +5 V, pin 4 is data out.** Compare the physical package marking and datasheet with the numbered pads in KiCad; do not guess orientation from the word “LED.” D9's data-out pad is intentionally unconnected.
3. Solder all nine hot-swap sockets on the bottom, flush to the PCB. Their plastic bodies and contacts must align with the corresponding switch holes. Do not fill the switch contact holes with solder.
4. Solder the encoder on top, fully seated, including both mechanical tabs. It needs the exact shaft height in the BOM.
5. Solder four flexible wires directly into J1. Keep wire exits low and route the harness away from the switch holes and screw bosses. Leave about 50 mm to connect the OLED under the removable lid. A tall vertical header and Dupont plugs would interfere with the cradle.
6. Inspect every joint for bridges or loose solder. With power disconnected, check resistance between USB 5 V and ground, 3.3 V and ground, and the switched LED rail and ground. Capacitors can cause a brief changing reading; a persistent near-zero reading must be investigated. Compare continuity between representative pads with the schematic.

The socket footprint has multiple pads with the same pin number; these are one electrical contact. Nine direct GPIO inputs mean there are no matrix diodes to fit.

## 4. Flash and fit the controller

Flash the loose RP2040-Zero before soldering it into the carrier:

1. Hold the controller's **BOOT** button while plugging its USB-C port into the Mac with a data cable.
2. Release BOOT when the removable drive **RPI-RP2** appears.
3. Copy `firmware/build/goober-rev-a-default.uf2` onto that drive. It should disappear as the module reboots into the keyboard firmware.
4. Unplug USB before soldering.

Fit the controller on the carrier's **underside, with its components and USB-C connector facing away from the carrier toward the case floor**. The USB-C end points out of the rear board edge. Use 23 header pins in two nine-pin rows and one five-pin row. Use a removable 3.0 mm gauge while soldering so the separation between the carrier underside and the controller's bare back surface is **3.0 mm**. Soldered pin strips are the intended mounting method, not stackable female sockets.

Before soldering all pins, verify with the module labels: viewed from the carrier top, GP0 is at x20.38/y1.59, and 5V is at x35.62/y1.59. Viewed from below those are mirrored. Tack opposite corners, check height and port alignment in the base, then solder the rest. Trim sharp pin ends where necessary without damaging joints.

U1's 5 V connection is supplied by its USB port. Do not connect another power source to that rail while USB is connected.

## 5. Connect and mount the OLED

Wire by **signal name**, regardless of harness color or connector order:

| Carrier J1 pad | Carrier signal | OLED terminal |
|---|---|---|
| 1, square pad | GND | GND |
| 2 | 3.3 V | VCC |
| 3 | SCL / GP15 | SCL |
| 4 | SDA / GP14 | SDA |

J1 runs from x10 to x17.62 on the carrier top drawing, with pin 1 at x10. The OLED is powered at 3.3 V. Its I²C address is 0x3C. Do not use a 5 V-powered substitute with pull-ups to 5 V.

The exact 36 × 12.5 mm Waveshare module sits in the lid's cradle with its display facing out through the window. The underside connector is toward the cradle's open end. Use thin tape on the PCB support ledges, avoiding glass and components. Dry-fit before taping: the window must show the active area, the connector must have clearance, and the module must not flex when the lid is closed.

## 6. First electrical test

Keep the assembly out of the case on an insulating surface. Use a current-limited USB test source for initial power if available. With a supply that provides power but no USB enumeration, the LEDs should remain off. Check approximately 5 V at U1's USB rail and 3.3 V at J1 VCC. If a supply immediately hits its limit or a part warms unexpectedly, disconnect and inspect the corresponding rail.

After the short checks and rail measurements pass, connect to the Mac. The Goober should enumerate as a keyboard, the OLED should show the Goober status, and lighting should start after USB configuration. If macOS opens Keyboard Setup Assistant, you can close it; this is a macro pad and has no full keyboard layout to identify.

Test one compatible switch first while supporting the socket from below. Then fit the lid/plate and the other eight switches while the base is still open. Ensure the metal switch pins are straight before pushing. Support the socket under each switch; otherwise insertion force can tear its solder pads from the PCB. The switches snap into the plate and their electrical pins engage the sockets.

## 7. Functional checklist

Use disposable text for the clipboard tests, and start with the Mac's volume low.

| Test | Expected result | Record |
|---|---|---|
| Top-left / top-middle / top-right | Command-C / Command-V / Command-Z | Pass / fail |
| Middle-left / middle / middle-right | Previous track / play-pause / next track in a compatible media app | Pass / fail |
| Bottom-left | Command-Shift-4 screenshot selection | Pass / fail |
| Bottom-middle | F13 | Pass / fail |
| Bottom-right tap | F14 | Pass / fail |
| Bottom-right hold (>200 ms) | LIGHTS layer on screen while held | Pass / fail |
| Encoder turn | Clockwise volume up, counterclockwise down; about one event per detent | Pass / fail |
| Encoder press | Mute toggle | Pass / fail |
| Hold bottom-right, turn encoder | Adjust LED brightness between 0 and 64 | Pass / fail |
| Hold bottom-right, press top-left | Toggle all key lighting | Pass / fail |
| Hold bottom-right, press top-middle/right | Next/previous lighting effect | Pass / fail |
| Hold bottom-right, middle-left / bottom-left | Hue up/down | Pass / fail |
| Hold bottom-right, middle-middle / bottom-middle | Saturation up/down | Pass / fail |
| Hold bottom-right, middle-right | Brightness up; use encoder counterclockwise for down | Pass / fail |
| Color sweep | All nine LEDs change color, in reading order; no flicker | Pass / fail |
| Several simultaneous keys | No missing keys or stuck modifiers | Pass / fail |
| Unplug / replug; reverse USB-C plug | Works both orientations and retains saved lighting settings | Pass / fail |
| Mac sleep / wake | LED rail switches off while suspended, then recovers after wake | Pass / fail |
| OLED activity | Layer and last action update; no claimed host-volume percentage | Pass / fail |
| Hot-swap replacement, power unplugged | One switch can be replaced without soldering; socket stays secure | Pass / fail |

F13/F14 may have no visible effect until assigned in macOS or an application. An event viewer or app shortcut assignment can confirm them. Volume media commands may be ignored for certain digital audio outputs; test with the Mac's built-in speakers before treating that as a PCB fault.

Measure USB current before configuration, during maximum permitted white lighting, and during suspend. Record actual readings. The descriptor requests up to 500 mA and firmware caps RGB brightness at 64/255. The power budget and suspend behavior are **not hardware certified**; the controller module's regulator and onboard LEDs also contribute. Do not raise the brightness cap until measurements justify it.

If the encoder direction is reversed on the actual part, swap `pin_a` and `pin_b` in `firmware/goober/rev_a/keyboard.json` and rebuild. If it emits two steps per detent or misses alternating detents, verify the exact encoder and its resolution setting (2 for this selected 15-pulse/30-detent part).

## 8. Close the case

Seat the PCB on the four base bosses. Tuck the OLED wires clear of screw paths and switch pins. Check the USB-C opening against the actual cable before tightening anything. Fit the lid with two **12 mm** M2.5 screws at the front key side and two **18 mm** screws at the rear control side. Tighten gently until seated; the PCB and printed spacers set the stack height.

Press the printed D-shaft knob onto the encoder without forcing it. It should retain at least a small clearance above the hood and move through the 0.5 mm push stroke without rubbing. Sand/adjust the bore from the fit of the actual shaft if needed. Add four rubber feet and repeat the controls test after closing.

To recover firmware later, unplug USB and hold the top-left key while reconnecting (QMK Bootmagic). If that does not work, open the case and use the module's physical BOOT button. The base is removable for service.

Keep a build log with part variants, print settings, measurements and any needed fit changes. Those results determine whether a revision B is needed before further production.
