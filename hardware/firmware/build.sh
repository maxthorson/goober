#!/bin/bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
QMK_DIR="${GOOBER_QMK_DIR:-$PROJECT_ROOT/tools/qmk_firmware}"
PIN=e6a31e474a931060412bb72c4c48131f58ac4bbc
if [ ! -d "$QMK_DIR/.git" ]; then
  git clone https://github.com/qmk/qmk_firmware.git "$QMK_DIR"
  git -C "$QMK_DIR" checkout "$PIN"
fi
if [ "$(git -C "$QMK_DIR" rev-parse HEAD)" != "$PIN" ]; then
  echo "This build expects QMK $PIN. Use a separate checkout at that revision."
  exit 1
fi
git -C "$QMK_DIR" submodule update --init lib/chibios lib/chibios-contrib lib/printf lib/pico-sdk lib/lufa
export PATH="$PROJECT_ROOT/tools/venv/bin:$PROJECT_ROOT/tools/arm-gnu-toolchain-13.3.rel1-darwin-arm64-arm-none-eabi/bin:$PATH"
mkdir -p "$QMK_DIR/keyboards/goober/rev_a" "$PROJECT_ROOT/firmware/build"
cp -R "$PROJECT_ROOT/firmware/goober/rev_a/." "$QMK_DIR/keyboards/goober/rev_a/"
cd "$QMK_DIR"
qmk compile -kb goober/rev_a -km default
cp goober_rev_a_default.uf2 "$PROJECT_ROOT/firmware/build/goober-rev-a-default.uf2"
