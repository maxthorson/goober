"""Generate the Goober QMK target from the revision-A pin contract."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'firmware' / 'goober' / 'rev_a'
(out / 'keymaps' / 'default').mkdir(parents=True, exist_ok=True)
config = {
    'keyboard_name': 'Goober Rev A', 'manufacturer': 'Goober',
    'maintainer': 'maxthorson', 'processor': 'RP2040', 'bootloader': 'rp2040',
    'usb': {'vid': '0xFEED', 'pid': '0x0901', 'device_version': '0.1.0', 'max_power': 500},
    'features': {'bootmagic': True, 'extrakey': True, 'nkro': True,
                 'encoder': True, 'oled': True, 'rgb_matrix': True},
    'matrix_pins': {'direct': [['GP0','GP1','GP2'], ['GP3','GP4','GP5'],
                               ['GP6','GP7','GP8'], ['GP12',None,None]]},
    'encoder': {'rotary': [{'pin_a':'GP10','pin_b':'GP11','resolution':2}]},
    'ws2812': {'pin':'GP13','driver':'vendor'},
    'rgb_matrix': {'driver':'ws2812', 'animations': {
        'cycle_all':True, 'cycle_left_right':True, 'breathing':True,
        'solid_reactive_simple':True, 'gradient_left_right':True},
        'layout':[{'matrix':[r,c], 'x':112*c,'y':32*r,'flags':4}
                  for r in range(3) for c in range(3)]},
    'layouts': {'LAYOUT': {'layout':
        [{'matrix':[r,c], 'x':c,'y':r+1} for r in range(3) for c in range(3)] +
        [{'matrix':[3,0],'x':2,'y':0}]}},
    'debounce':5
}
(out/'keyboard.json').write_text(json.dumps(config, indent=2)+'\n')
(out/'rules.mk').write_text('BOARD = GENERIC_RP_RP2040\nOLED_DRIVER = ssd1306\nOLED_TRANSPORT = i2c\n')
(out/'config.h').write_text('''// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#define I2C_DRIVER I2CD1
#define I2C1_SDA_PIN GP14
#define I2C1_SCL_PIN GP15
#define I2C1_CLOCK_SPEED 400000
#define OLED_DISPLAY_128X32
#define OLED_DISPLAY_ADDRESS 0x3C
#define OLED_TIMEOUT 30000
#define RGB_MATRIX_MAXIMUM_BRIGHTNESS 64
#define RGB_MATRIX_DEFAULT_VAL 32
#define RGB_MATRIX_DEFAULT_MODE RGB_MATRIX_CYCLE_LEFT_RIGHT
#define RGB_MATRIX_SLEEP
#define RGB_MATRIX_KEYPRESSES
#define RGB_MATRIX_LED_FLUSH_LIMIT 20
#define GOOBER_LED_POWER GP9
#define TAPPING_TERM 200
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET
''')
(out/'halconf.h').write_text('#pragma once\n#define HAL_USE_I2C TRUE\n#include_next <halconf.h>\n')
(out/'mcuconf.h').write_text('#pragma once\n#include_next <mcuconf.h>\n#undef RP_I2C_USE_I2C1\n#define RP_I2C_USE_I2C1 TRUE\n')
(out/'rev_a.c').write_text('''// SPDX-License-Identifier: GPL-2.0-or-later
#include QMK_KEYBOARD_H
#include "usb_device_state.h"

static void update_led_power(void) {
    bool on = usb_device_state_get_configure_state() == USB_DEVICE_STATE_CONFIGURED
              && rgb_matrix_is_enabled();
    gpio_write_pin(GOOBER_LED_POWER, on);
}

void keyboard_pre_init_kb(void) {
    gpio_write_pin_low(GOOBER_LED_POWER);
    gpio_set_pin_output(GOOBER_LED_POWER);
    keyboard_pre_init_user();
}

void housekeeping_task_kb(void) {
    update_led_power();
    housekeeping_task_user();
}

void notify_usb_device_state_change_kb(struct usb_device_state state) {
    update_led_power();
    notify_usb_device_state_change_user(state);
}

void suspend_power_down_kb(void) {
    gpio_write_pin_low(GOOBER_LED_POWER);
    oled_off();
    suspend_power_down_user();
}

void suspend_wakeup_init_kb(void) {
    update_led_power();
    suspend_wakeup_init_user();
}
''')
(out/'keymaps/default/keymap.c').write_text('''// SPDX-License-Identifier: GPL-2.0-or-later
#include QMK_KEYBOARD_H

enum layers { MACROS, LIGHTS };
#define COPY LGUI(KC_C)
#define PASTE LGUI(KC_V)
#define UNDO LGUI(KC_Z)
#define SHOT LGUI(LSFT(KC_4))

// Order: nine physical keys in reading order, then the encoder push switch.
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [MACROS] = LAYOUT(
        COPY,    PASTE,   UNDO,
        KC_MPRV, KC_MPLY, KC_MNXT,
        SHOT,    KC_F13,  LT(LIGHTS, KC_F14),
        KC_MUTE
    ),
    [LIGHTS] = LAYOUT(
        RM_TOGG, RM_NEXT, RM_PREV,
        RM_HUEU, RM_SATU, RM_VALU,
        RM_HUED, RM_SATD, KC_TRNS,
        KC_MUTE
    )
};

static const char *last_action = "Ready";

bool encoder_update_user(uint8_t index, bool clockwise) {
    if (index != 0) return false;
    if (layer_state_is(LIGHTS)) {
        if (clockwise) rgb_matrix_increase_val();
        else rgb_matrix_decrease_val();
        last_action = clockwise ? "Brightness +" : "Brightness -";
    } else {
        tap_code(clockwise ? KC_VOLU : KC_VOLD);
        last_action = clockwise ? "Volume +" : "Volume -";
    }
    return false;
}

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    if (!record->event.pressed) return true;
    switch (keycode) {
        case COPY: last_action = "Copy"; break;
        case PASTE: last_action = "Paste"; break;
        case UNDO: last_action = "Undo"; break;
        case KC_MPRV: last_action = "Previous track"; break;
        case KC_MPLY: last_action = "Play / pause"; break;
        case KC_MNXT: last_action = "Next track"; break;
        case SHOT: last_action = "Select screenshot"; break;
        case KC_F13: last_action = "F13 macro"; break;
        case KC_MUTE: last_action = "Mute toggle"; break;
        default: last_action = layer_state_is(LIGHTS) ? "Lighting adjusted" : "Key pressed";
    }
    return true;
}

bool oled_task_user(void) {
    oled_set_cursor(0,0);
    oled_write_ln_P(PSTR("GOOBER / REV A       "), false);
    oled_write_ln_P(layer_state_is(LIGHTS) ? PSTR("LAYER: LIGHTS       ") : PSTR("LAYER: MACROS       "), false);
    oled_write_P(rgb_matrix_is_enabled() ? PSTR("RGB: ON  ") : PSTR("RGB: OFF "), false);
    oled_write(get_u8_str(rgb_matrix_get_val(), ' '), false);
    oled_write_ln_P(PSTR(" /64   "), false);
    oled_write_P(PSTR("                     "), false);
    oled_set_cursor(0,3);
    oled_write(last_action, false);
    return false;
}
''')
(out/'readme.md').write_text('''# Goober revision A

Personal RP2040-Zero macro pad. See the project assembly guide for the hardware pin contract.

Build: `qmk compile -kb goober/rev_a -km default`

Bootloader: hold the module BOOT button while connecting USB, or hold the top-left key while connecting USB (Bootmagic). Copy the UF2 onto RPI-RP2. The USB VID/PID are development identifiers, not an assigned production USB identity.
''')
print(out)
