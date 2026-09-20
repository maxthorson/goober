# Validation record — Goober Rev A.1

Digital checks completed on 5 September 2026. This record concerns the supplied files, not a built physical device.

| Check | Result | Evidence |
|---|---|---|
| KiCad 10.0.5 schematic ERC | 0 violations | `validation/schematic-erc.json` |
| KiCad PCB DRC, all track errors | 0 violations, 0 unconnected items | `validation/pcb-final.json` |
| KiCad schematic/PCB parity | 0 issues | `validation/pcb-final.json` |
| Independent pin comparison | 141 unique connected pads, 33 functional nets agree across schematic, PCB and contract | `validation/connectivity.json` |
| Firmware/hardware GPIO map | Keys, encoder, lighting and OLED assignments agree | `validation/connectivity.json` |
| QMK build | Success for `goober/rev_a:default` | `validation/firmware-build.log` |
| UF2 format | RP2040 family, block sequence, address range and magic values verified | `validation/firmware.json` |
| Exported fabrication files | Seven Gerber layers and both drill files parse | `validation/gerber-parse.json` |
| Board geometry | 80 × 96 mm nominal; drill separation preserved; nine LED openings present | Gerbers and board drawings |
| STL base / lid / knob | Watertight, one connected body each | `validation/case-meshes.json` |
| STL coupon | Watertight, two intentional separate test pieces | `validation/case-meshes.json` |
| Nominal case intersections | No positive-volume collision with rounded PCB, controller PCB, USB connector, OLED PCB or encoder-body proxies | `validation/mechanical-clearances.json` |
| Visual review | Actual CAD assembly, exploded render, schematic, PCB and exported Gerber drawings inspected | `mockups/` |

KiCad's normal non-electrical ignored-check defaults are recorded in its report. No reported shorts, open connections, copper clearances or schematic parity errors were waived to obtain the result. The schematic uses module-style symbols; ERC is not an analog circuit simulation.

Gerbonara 1.6.3 accepted the Excellon and Gerber exports. It noted KiCad's placement of G90 after the Excellon header and an unused macro argument, plus the absence of optional paste layers when making previews. These did not prevent parsing; the fabrication ZIP intentionally contains the bare-board layers, not a solder-paste stencil order.

The mechanical intersection checks use nominal bounding proxies, not supplier STEP models for every part. They do not include solder fillets, wire bends, header tolerances, keycap travel, switch-clip forces or print shrinkage. The fit coupon and first assembled prototype must resolve those.

Still to measure physically: rail voltages and current, LED colors and timing, USB enumeration and suspend/wake, encoder direction and detent count, OLED alignment, port/cable access, switch fit and retention, screw/insert fit, solderability and sustained-use temperature. No USB/EMC compliance testing, physical prototype build or supplier DFM approval has been performed.

The AI appearance concept is illustrative. CAD/STL and PCB dimensions govern construction; the actual firmware screen is the status display described in the guide.
