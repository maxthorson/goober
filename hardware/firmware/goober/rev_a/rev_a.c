// SPDX-License-Identifier: GPL-2.0-or-later
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
