# Source and license notices

Goober-specific design files were prepared for Max Thorson's project. This package does not impose a new public release license on the original PCB circuitry, case or documentation. Third-party material retains its own notices and license terms.

- **Firmware:** Goober QMK board/keymap files are marked GPL-2.0-or-later. Upstream QMK is pinned to `e6a31e474a931060412bb72c4c48131f58ac4bbc`, from https://github.com/qmk/qmk_firmware. See `licenses/QMK-GPL-2.0.txt`. The complete upstream checkout, including the initialized build dependencies and their notices, is installed locally at `tools/qmk_firmware`; the portable build script retrieves the pinned sources when needed. Retain corresponding upstream/dependency source and notices with any firmware redistribution.
- **MX hot-swap footprint:** `SW_MX_HS_CPG151101S11_1u.kicad_mod` is from ebastler's marbastlib, https://github.com/ebastler/marbastlib, under CERN-OHL-P-2.0. See `licenses/marbastlib-CERN-OHL-P-2.0.txt`. Its geometry is unmodified; placement is flipped to the carrier underside.
- **Other stock footprints:** From the KiCad community libraries distributed with KiCad 10.0.5, under CC-BY-SA-4.0 with the KiCad design exception. See `licenses/KiCad-footprints-LICENSE.md`. The local reverse-mount SK6812MINI-E footprint has its long pad dimension reduced from 1.35 to 1.30 mm. Other copied footprint geometries are unchanged.
- **RP2040-Zero header footprint:** Generated from Waveshare's published 18 × 23.5 mm module drawing and header/pinout data. The module itself is purchased separately; the carrier does not reproduce its internal PCB.
- **Manufacturer reference documents/images:** Remain the property of their respective manufacturers. They are included as engineering references for the exact selected parts; source links are in the project documents. They are not original Goober artwork.
- **Appearance concept:** AI-generated from the mechanical CAD reference; labeled as a concept. It does not replace fabrication dimensions or represent a photograph of a built prototype.

The supplied project library is self-contained for electrical editing. Optional KiCad 3D model paths refer to the installed KiCad library; the case assembly renders use simplified component shapes. The printed case files do not depend on those optional models.
