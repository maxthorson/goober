# Goober

Goober is a compact USB-C macro pad project with two connected halves:

- `website/` contains the public Next.js site for presenting the product, linking
  firmware resources, and experimenting with a hosted QMK configurator surface.
- `hardware/` contains the Rev A hardware package: KiCad PCB files, case models,
  QMK firmware, fabrication docs, mockups, validation notes, and release
  deliverables.

The hardware target is a 9-key RP2040-Zero macro pad with MX hot-swap switches,
an OLED display, a volume/mute knob, and individually addressable RGB lighting.
USB hub and charging passthrough are deferred.

## Project Status

Rev A.1 is a checked engineering prototype ready for a first fabrication and fit
test. It has not yet been built or electrically tested on physical hardware.

The hardware package passes schematic ERC, PCB DRC, and KiCad schematic/PCB
parity checks with zero issues. Firmware compiles, and the printable case
components validate as watertight single-body meshes.

## Repository Layout

| Folder | Purpose |
|---|---|
| `website/` | Next.js product site and QMK configurator integration |
| `hardware/case/` | OpenSCAD source and printable STL case files |
| `hardware/docs/` | Design, fabrication, assembly, firmware, and validation guides |
| `hardware/firmware/` | QMK board files, keymap, build script, and UF2 output |
| `hardware/hardware/` | KiCad schematic, PCB, Gerbers, BOM, and part references |
| `hardware/mockups/` | CAD renders, board images, and appearance concepts |
| `hardware/releases/` | Packaged Rev A prototype release archive |
| `hardware/tools/` | Project-owned helper scripts; large external tools are excluded |

## Start Here

For the site:

```bash
cd website
npm install
npm run dev
```

For the hardware:

1. Read `hardware/docs/DESIGN_PLAN.md` and
   `hardware/docs/PARTS_AND_COST.md`.
2. Use `hardware/docs/FABRICATION.md` to order a small PCB batch.
3. Print the fit coupon, then follow `hardware/docs/ASSEMBLY_AND_TEST.md`.
4. Flash the supplied UF2 or rebuild from `hardware/firmware/`.

## Notes

Large installed tools, virtual environments, downloaded toolchains, and upstream
source checkouts are intentionally not committed. License and provenance notes
for the hardware package are in `hardware/NOTICE.md`.
