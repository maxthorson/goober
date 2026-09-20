# PCB fabrication — revision A.1

Upload **`hardware/Goober-Rev-A-Gerbers.zip`** as the bare-board fabrication file. This ZIP contains seven Gerber layers, two Excellon drill files and the KiCad job metadata. It does not order components or assembly.

| Setting | Value |
|---|---|
| Board outline | 80 × 96 mm, rounded corners, radius 3 mm |
| Material / thickness | FR-4, **1.6 mm** |
| Copper layers | **2** |
| Copper weight | 1 oz finished nominal |
| Finish | Lead-free HASL for cost; ENIG optional |
| Solder mask | Both sides; any color |
| Silkscreen | Both sides |
| Minimum copper clearance / signal trace | 0.20 mm / 0.20 mm |
| Smallest plated drill / via land | 0.30 mm / 0.60 mm |
| Minimum copper-to-routed-edge | 0.25 mm |
| Impedance control | Not required; USB data routing is entirely on the bought controller module |
| Castellations / edge plating | None on this carrier |
| Panelization | Single board outline; let the fabricator handle their process panel |

Keep plated and non-plated drill files separate. The switch contact holes are intentionally plated. The center and plastic-leg switch holes, and the four mounting holes, are non-plated. Two encoder mechanical holes are plated routed slots.

**The nine internal LED windows on Edge.Cuts must be milled through the PCB.** They are not printed graphics. Check that the fabricator's upload viewer recognizes one outer contour and nine internal contours; request confirmation of the internal routing if the preview omits it. The cutouts include rounded reliefs. The board also has 31 non-plated drill hits and 90 plated drill/slot objects in the independent export check.

Gerber mapping:

| File | Purpose |
|---|---|
| `goober-F_Cu.gtl` / `goober-B_Cu.gbl` | Top / bottom copper |
| `goober-F_Mask.gts` / `goober-B_Mask.gbs` | Top / bottom solder-mask openings |
| `goober-F_Silkscreen.gto` / `goober-B_Silkscreen.gbo` | Top / bottom printing |
| `goober-Edge_Cuts.gm1` | Outside shape and nine LED openings |
| `goober-PTH.drl` | Plated holes and slots |
| `goober-NPTH.drl` | Non-plated holes |

The exact editable project is `hardware/goober.kicad_pro`, with the adjacent schematic, PCB and local libraries. Keep those files together. The schematic uses labeled component blocks with every pin shown; it is electrically connected and linked to the PCB. Routed power nets use the same named net connectivity as the schematic.

The bottom side carries U1, SW1–SW9, D1–D9 and C1–C9. Other small parts and the encoder are on top. J1 is a low-profile wire connection in the assembly, despite using a standard header footprint. `BOM.csv` is a manual build list, not a pre-approved factory assembly order. Through-hole module installation and OLED wiring need the assembly guide.

The SK6812MINI-E footprint is based on KiCad's reverse-mount footprint. Its SMD lands were reduced from 1.35 to **1.30 mm** in the long dimension to meet the 0.25 mm copper-to-milled-edge clearance. The supplied local library includes this change. Do not replace it with the stock footprint without rechecking clearance.

These are prototype fabrication outputs. Automated rule checks do not verify solderability, real component tolerances, USB compliance, current consumption or the feel of the assembled device. Build and validate one prototype before larger orders.
