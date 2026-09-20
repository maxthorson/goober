// SPDX-License-Identifier: GPL-2.0-or-later
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
