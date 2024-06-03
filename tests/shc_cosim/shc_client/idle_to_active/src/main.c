/*
 * Copyright (c) 2024 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/sys/util.h>
#include <zephyr/sys/printk.h>
#include <inttypes.h>

#define SLEEP_TIME_MS	1

#define GWU0_NODE DT_ALIAS(gwu0)
#if !DT_NODE_HAS_STATUS(GWU0_NODE, okay)
#error "Error: gwu0 devicetree alias is not defined"
#endif

#define EXT_LED_NODE DT_NODELABEL(ext_led0)

static const struct gpio_dt_spec wakeupPin = GPIO_DT_SPEC_GET(GWU0_NODE, gpios);
static struct gpio_callback wakeupPin_cb_data;

static const struct gpio_dt_spec ext_led = GPIO_DT_SPEC_GET(EXT_LED_NODE, gpios);

volatile bool blinkFlag = false;


void wakeup_cb(const struct device *dev, struct gpio_callback *cb,
			uint32_t pins)
{
	printk("Rising edge detected\n");
	blinkFlag = true;
	gpio_pin_toggle_dt(&ext_led);
}

int main(void)
{
	int ret;

	if (!gpio_is_ready_dt(&wakeupPin)) {
		printk("Error: wake-up gpio device %s is not ready\n",
		       wakeupPin.port->name);
		return 0;
	}

	if (!gpio_is_ready_dt(&ext_led)) {
		printk("Error: external LED is not ready\n");
        return 0;
    }

	ret = gpio_pin_configure_dt(&wakeupPin, GPIO_INPUT | GPIO_PULL_DOWN | GPIO_INT_WAKEUP);
	if (ret != 0) {
		printk("Error %d: failed to configure %s pin %d\n",
		       ret, wakeupPin.port->name, wakeupPin.pin);
		return 0;
	}

	ret = gpio_pin_interrupt_configure_dt(&wakeupPin,
					      GPIO_INT_EDGE_TO_ACTIVE);
	if (ret != 0) {
		printk("Error %d: failed to configure interrupt on %s pin %d\n",
			ret, wakeupPin.port->name, wakeupPin.pin);
		return 0;
	}

	gpio_init_callback(&wakeupPin_cb_data, wakeup_cb, BIT(wakeupPin.pin));
	gpio_add_callback(wakeupPin.port, &wakeupPin_cb_data);
	printk("Wake-up set at %s pin %d\n", wakeupPin.port->name, wakeupPin.pin);

	ret = gpio_pin_configure_dt(&ext_led, GPIO_OUTPUT_ACTIVE);
    if (ret < 0) {
        return 0;
    }
	gpio_pin_set_dt(&ext_led, 0);

	while (1) {
		if (blinkFlag) {
			ret = gpio_pin_toggle_dt(&ext_led);
			k_usleep(50);
		} else {
			k_msleep(100);
		}
	}
	return 0;
}
