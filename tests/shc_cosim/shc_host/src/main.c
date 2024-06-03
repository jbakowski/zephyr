/*
 * Copyright (c) 2024 Intel Corporation.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdio.h>
#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/drivers/gpio.h>
#include <string.h>

#define UART_DEVICE_NODE DT_CHOSEN(zephyr_shell_uart)

#define MSG_SIZE 32

// holds up to 10 commands to be executed
K_MSGQ_DEFINE(uart_msgq, MSG_SIZE, 10, 4);

static const struct device *const uart_dev = DEVICE_DT_GET(UART_DEVICE_NODE);
static char rx_buf[MSG_SIZE];
static int rx_buf_pos;

#ifdef CONFIG_GPIO
static const struct device *const gpio_dev = DEVICE_DT_GET(DT_NODELABEL(gpiof));
#endif

#ifdef CONFIG_I2C
static const struct device *const i2c = DEVICE_DT_GET(DT_NODELABEL(i2c));
#endif

void uart_fifo_callback(const struct device *dev, void *user_data) {
    ARG_UNUSED(user_data);
    uint8_t c;

    if (!uart_irq_update(uart_dev)) {
        return;
    }
    if (!uart_irq_rx_ready(uart_dev)) {
        return;
    }

    while (uart_fifo_read(uart_dev, &c, 1) == 1) {
        if ((c == '\n' || c == '\r') && rx_buf_pos > 0) {
            rx_buf[rx_buf_pos] = '\0';
            k_msgq_put(&uart_msgq, &rx_buf, K_NO_WAIT);
            rx_buf_pos = 0;
        } else if (rx_buf_pos < (sizeof(rx_buf)) - 1) {
            rx_buf[rx_buf_pos++] = c;
        }
    }
}

void uart_init(const struct device *uart_dev) {
    int ret;
    if (!device_is_ready(uart_dev)) {
        printk("UART device not found!\n");
        return;
    }

    ret = uart_irq_callback_user_data_set(uart_dev, uart_fifo_callback, NULL);
    if (ret < 0) {
        if (ret == -ENOTSUP) {
            printk("Interrupt-driven UART API support not enabled\n");
        } else if (ret == -ENOSYS) {
            printk("UART device does not support interrupt-driven API\n");
        } else {
            printk("Error setting UART callback: %d\n", ret);
        }
        return;
    }

    uart_irq_rx_enable(uart_dev);
}

void gpio_init(const struct device *gpio_dev) {
    int ret;

    if (!device_is_ready(gpio_dev)) {
        printk("GPIO device not found!\n");
        return;
    }

    // TODO: unhardcode this later and implement commands for dynamic pin setup
    ret = gpio_pin_configure(gpio_dev, 4, GPIO_OUTPUT_INACTIVE | GPIO_PULL_DOWN);
    if (ret > 0) {
        printk("Error %d: failed to configure GPIO pin %d\n", ret, 4);
        return;
    }
}

void parse_command(char* cmd_ptr) {
    int ret;
    char *device;
    char *action;

    device = strtok(cmd_ptr, ":");
    action = strtok(NULL, ":");
    printk("[DBG] Device: %s\n", device);
    printk("[DBG] Action: %s\n", action);

    // TODO: find a more readable way to do this
    // find an appropriate device, then look for an associated action call

    // GPIO
    if (strcmp(device, "gpio") == 0) {
        printk("Device: GPIO, looking for a function call...\n");
        if (strcmp(action, "ON") == 0) {
            printk("Executing GPIO ON call!\n");
            ret = gpio_pin_set(gpio_dev, 4, 1);
        } else if (strcmp(action, "OFF") == 0) {
            printk("Executing GPIO OFF call!\n");
            ret = gpio_pin_set(gpio_dev, 4, 0);
        }
    // I2C
    } else if (strcmp(device, "i2c")) {
        // and so on, and so on
    }
    // ANOTHER DEVICE
}

int main() {
    char command[MSG_SIZE];

    gpio_init(gpio_dev);
    uart_init(uart_dev);

    while (k_msgq_get(&uart_msgq, &command, K_FOREVER) == 0) {
        parse_command(command);
    }
}
