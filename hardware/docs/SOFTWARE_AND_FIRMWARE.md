# Mac software and firmware

The design tools have already been installed for this project. **You do not need additional software to flash the supplied firmware.** Finder can copy the UF2 to the RP2040 bootloader drive.

| Tool | Location on this Mac | When you need it |
|---|---|---|
| KiCad 10.0.5 | `/Users/maxthorson/Applications/KiCad/KiCad.app` | Open the PCB project, inspect Gerbers or make electrical changes |
| OpenSCAD 2026.08.27 | `/Users/maxthorson/Applications/OpenSCAD.app` | Open `case/goober.scad`, change dimensions and export STL parts |
| QMK CLI 1.2.0 | `Goober/tools/venv` | Rebuild firmware after editing macros or lighting |
| Arm GNU toolchain 13.3.Rel1 | `Goober/tools/arm-gnu-toolchain-13.3.rel1-darwin-arm64-arm-none-eabi` | Compiler used by the build script |
| Git / Python / Homebrew / VS Code | Already present | Optional code editing and dependency management |
| Printer-specific slicer | Not installed by this project | Only needed if you print at home; a print service takes STL files |

QMK Toolbox, Arduino IDE and Raspberry Pi OS are not needed for this design. Official download pages for another machine are in `DESIGN_PLAN.md`. On a different machine, follow QMK's setup guide for the CLI/compiler; the firmware build script uses system-installed tools if project-local copies are absent. OpenSCAD's installed version is a development snapshot; the generated STL files can be used without it.

## Flash the supplied binary

Hold the RP2040-Zero's BOOT button while connecting its USB-C data cable. In Finder, copy `firmware/build/goober-rev-a-default.uf2` to **RPI-RP2**. The drive disappears when flashing finishes and the module reboots. No flashing tool, account or API key is required.

The compiled image has an 86,016-byte UF2 container and a 43,008-byte flash payload. The exact SHA-256 is recorded in `validation/firmware.json` and the release checksums. It is built for RP2040, not RP2350/Pico 2.

## Edit and rebuild

The source you normally edit is `firmware/goober/rev_a/keymaps/default/keymap.c`. Key order is top-left to bottom-right, followed by the encoder's push switch. `COPY`, `PASTE`, `UNDO` and `SHOT` are Mac shortcuts; replace those with the shortcuts you want. F13 and F14 are available for app assignments.

From Terminal:

```sh
cd /Users/maxthorson/Goober
./firmware/build.sh
```

The script copies the editable keyboard files into the local QMK checkout, builds them and refreshes `firmware/build/goober-rev-a-default.uf2`. It expects upstream QMK revision `e6a31e474a931060412bb72c4c48131f58ac4bbc`. On a fresh copy, it downloads that checkout and its required submodules. It refuses to silently change an existing checkout at a different revision. Reflash the new UF2 after a successful build.

The local upstream source lives in `tools/qmk_firmware`. The delivery ZIP contains the complete Goober-specific firmware sources and a pinned build script; the large installed tools/checkouts are kept separately on this Mac. QMK's source and dependency licenses remain in its checkout, and license notices are also included with this project.

## Controls and display

The shipped key layout is:

| | Left | Middle | Right |
|---|---|---|---|
| Top | Copy | Paste | Undo |
| Middle | Previous track | Play/pause | Next track |
| Bottom | Screenshot selection | F13 | Tap F14 / hold LIGHTS |

Turn the knob for volume; press it for mute. Hold bottom-right to change the knob to brightness. On the LIGHTS layer, top-left toggles RGB, top-middle/right changes effects, middle-left/bottom-left changes hue, middle-middle/bottom-middle changes saturation, and middle-right raises brightness. Lighting settings use QMK's persistent settings. There is no separate configuration app in this version.

The OLED reports the current layer, lighting enable/brightness and last command. It is monochrome, 128 × 32 pixels. It does not receive the Mac's actual volume percentage. QMK effects drive the nine LEDs individually; reactive effects use the matching switch positions.

For custom per-key colors, use QMK's `rgb_matrix_indicators_user` hook and `rgb_matrix_set_color(index, r, g, b)` in the keymap. LED indices 0–8 follow reading order. If adding a custom hook, explicitly honor the chosen brightness cap and RGB enable state—direct color writes can bypass a theme's normal brightness scaling. The included default uses the standard QMK effects and controls.

## Hardware pin map

| RP2040 GPIO | Function |
|---|---|
| GP0–GP8 | Nine switches, each closes directly to ground |
| GP9 | LED power enable, active high |
| GP10 / GP11 | Encoder A / B |
| GP12 | Encoder press, closes to ground |
| GP13 | RGB data through the 5 V AHCT buffer |
| GP14 / GP15 | OLED SDA / SCL, 3.3 V I²C |

RGB brightness is capped at 64/255, default 32. The switched LED rail is off before USB configuration and while suspended. The buffer is disabled when the lighting rail is off. GPIO16's LED on the controller module is not used by this keyboard.

The USB VID/PID (`FEED:0901`) are development placeholders, not an assigned commercial USB identity. Hardware testing and a suitable USB identity remain necessary before turning this into a distributed product.
