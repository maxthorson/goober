# Goober revision A

Personal RP2040-Zero macro pad. See the project assembly guide for the hardware pin contract.

Build: `qmk compile -kb goober/rev_a -km default`

Bootloader: hold the module BOOT button while connecting USB, or hold the top-left key while connecting USB (Bootmagic). Copy the UF2 onto RPI-RP2. The USB VID/PID are development identifiers, not an assigned production USB identity.
