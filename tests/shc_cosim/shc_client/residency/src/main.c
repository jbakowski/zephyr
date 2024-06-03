/*
 * Copyright (c) 2012-2014 Wind River Systems, Inc.
 *
 * SPDX-License-Identifier: Apache-2.0
 */
#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <stdio.h>

#define EXT_LED_NODE DT_NODELABEL(ext_led0)
static const struct gpio_dt_spec ext_led = GPIO_DT_SPEC_GET(EXT_LED_NODE, gpios);

void stay_idle(uint32_t idle_time_us) {
	printk("Staying idle for %u microseconds\n", idle_time_us);
	k_usleep(idle_time_us);
}

uint32_t runningCounter = 0;

int main(void)
{
	int ret = 0;
	k_msleep(2000);
	ret = gpio_pin_configure_dt(&ext_led, GPIO_OUTPUT_ACTIVE);
	ret = gpio_pin_set_dt(&ext_led, 0);

	for (int i = 0; i < 623; i++) {
		k_usleep(70);
	}

	ret = gpio_pin_set_dt(&ext_led, 1);
	k_msleep(100);
	ret = gpio_pin_set_dt(&ext_led, 0);

	for (int i = 0; i < 534; i++) {
		k_usleep(80);
	}

	ret = gpio_pin_set_dt(&ext_led, 1);
	k_msleep(100);
	ret = gpio_pin_set_dt(&ext_led, 0);

	for (int i = 0; i < 445; i++) {
		k_usleep(90);
	}

	ret = gpio_pin_set_dt(&ext_led, 1);
	k_msleep(100);
	ret = gpio_pin_set_dt(&ext_led, 0);

	for (int i = 0; i < 500; i++) {
		k_msleep(1);
	}

	ret = gpio_pin_set_dt(&ext_led, 1);
	k_msleep(100);
	ret = gpio_pin_set_dt(&ext_led, 0);

	for (int i = 0; i < 500; i++) {
		k_msleep(1);
		k_usleep(10);
	}

	ret = gpio_pin_set_dt(&ext_led, 1);
	k_msleep(100);
	ret = gpio_pin_set_dt(&ext_led, 0);

	for (int i = 0; i < 500; i++) {
		k_msleep(1);
		k_usleep(20);
	}

	// since this test has no wake up sources
	// we have to keep the board active to not brick it
	ret = gpio_pin_set_dt(&ext_led, 1);
	while(true) {
		k_usleep(50);
		ret = gpio_pin_toggle_dt(&ext_led);
	};

	return 0;
}
