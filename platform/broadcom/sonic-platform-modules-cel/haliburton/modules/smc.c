/*
 * smc.c - The CPLD driver for E1031 System Management.
 * The driver implement sysfs to access CPLD register on the E1031 via LPC bus.
 * Copyright (C) 2018 Celestica Corp.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 */

#include <linux/interrupt.h>
#include <linux/module.h>
#include <linux/pci.h>
#include <linux/kernel.h>
#include <linux/stddef.h>
#include <linux/delay.h>
#include <linux/ioport.h>
#include <linux/init.h>
#include <linux/i2c.h>
#include <linux/acpi.h>
#include <linux/io.h>
#include <linux/dmi.h>
#include <linux/slab.h>
#include <linux/wait.h>
#include <linux/err.h>
#include <linux/platform_device.h>
#include <linux/types.h>
#include <uapi/linux/stat.h>
#include <linux/string.h>

// Changed: (opt) Add LED control sysfs
// Changed: Add PSU status sysfs*
// Changed: Add SFP mod ctrl sysfs*
// TODO: (opt) Add fan LED sysfs
// TODO: (opt) Add fan direction sysfs

#define DRIVER_NAME "e1031.smc"

/**
 * CPLD register address for read and write.
 */
#define VERSION         0x0200
#define SCRATCH         0x0201
#define BROAD_ID        0x0202

/* PSU STATUS
 * [7]  PSUR_ACOK
 * [6]  PSUR_PWOK
 * [5]  PSUR_ALRT
 * [4]  PSUR_PRS
 * [3]  PSUL_ACOK
 * [2]  PSUL_PWOK
 * [1]  PSUL_ALRT
 * [0]  PSUL_PRS
 */
#define PSU_STAT        0x0204
#define PSUR_ACOK       7
#define PSUR_PWOK       6
#define PSUR_ALRT       5
#define PSUR_PRS        4
#define PSUL_ACOK       3
#define PSUL_PWOK       2
#define PSUL_ALRT       1
#define PSUL_PRS        0

/* FAN LED CTRL
 * [7:3]  RESERVED
 * [2:0]  LED CTRL
 */
#define FAN_LED_1       0x0205
#define FAN_LED_2       0x0206
#define FAN_LED_3       0x0207

enum FAN_LED {
    fan_led_grn = 0,
    fan_led_grn_bnk,
    fan_led_amb,
    fan_led_amb_bnk,
    fan_led_off
} fan_led;

#define LED_OPMOD       0x0208
#define LED_TEST        0x0209

/* SYSTEM LED
 * [7:4] RESERVED
 * [3:2] STATUS LED
 * [1:0] MASTER LED
 */
#define LED_FPS         0x020a

enum STAT_LED {
    stat_led_off = 0,
    stat_led_grn,
    stat_led_grn_bnk
} stat_led;

enum MASTER_LED {
    master_led_off = 0,
    master_led_grn,
    master_led_amb
} master_led;

/* FAN DIRECTION STAT
 * [7:4] RESERVED
 * [3]   USB HUB STAT
 * [2:0] FAN_DIR
 */
#define DEV_STAT        0x020c
#define FAN_3           2
#define FAN_2           1
#define FAN_1           0

/* SFP PORT STATUS
 * [7:4] RESERVED
 * [3:0] TX_FAULT / MODABS / RXLOS
 */
#define SFP_TXFAULT     0x0242
#define SFP_MODABS      0x0243
#define SFP_RXLOS       0x0244

/* SFP PORT CTRL
 * [7:4] RATE SEL (RS0/RS1)
 * [3:0] TX_DIS
 */
#define SFP_TXCTRL      0x0255

/* SFP PORT BIT OFFSET */
#define SFP4            3
#define SFP3            2
#define SFP2            1
#define SFP1            0

struct cpld_data {
    struct mutex       cpld_lock;
    uint16_t           read_addr;
    struct device      *fpp_node;
    struct device      *sfp_devices[4];
};

struct sfp_device_data {
    int portid;
};

struct class *celplatform;
struct cpld_data *cpld_data;

static ssize_t scratch_show(struct device *dev, struct device_attribute *devattr,
                            char *buf)
{
    unsigned char data = 0;
    mutex_lock(&cpld_data->cpld_lock);
    data = inb(SCRATCH);
    mutex_unlock(&cpld_data->cpld_lock);
    return sprintf(buf, "0x%2.2x\n", data);
}

static ssize_t scratch_store(struct device *dev, struct device_attribute *devattr,
                             const char *buf, size_t count)
{
    unsigned long data;
    char *last;

    mutex_lock(&cpld_data->cpld_lock);
    data = (uint16_t)strtoul(buf, &last, 16);
    if (data == 0 && buf == last) {
        mutex_unlock(&cpld_data->cpld_lock);
        return -EINVAL;
    }
    outb(data, SCRATCH);
    mutex_unlock(&cpld_data->cpld_lock);
    return count;
}
static DEVICE_ATTR_RW(scratch);


static ssize_t version_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    int len = 0;
    mutex_lock(&cpld_data->cpld_lock);
    len = sprintf(buf, "0x%2.2x\n", inb(VERSION));
    mutex_unlock(&cpld_data->cpld_lock);
    return len;
}
static DEVICE_ATTR_RO(version);

static ssize_t getreg_store(struct device *dev, struct device_attribute *devattr,
                            const char *buf, size_t count)
{
    uint16_t addr;
    char *last;

    addr = (uint16_t)strtoul(buf, &last, 16);
    if (addr == 0 && buf == last) {
        return -EINVAL;
    }
    cpld_data->read_addr = addr;
    return count;
}

static ssize_t getreg_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    int len = 0;
    mutex_lock(&cpld_data->cpld_lock);
    len = sprintf(buf, "0x%2.2x\n", inb(cpld_data->read_addr));
    mutex_unlock(&cpld_data->cpld_lock);
    return len;
}
static DEVICE_ATTR_RW(getreg);

static ssize_t setreg_store(struct device *dev, struct device_attribute *devattr,
                            const char *buf, size_t count)
{
    uint16_t addr;
    uint8_t value;
    char *tok;
    char clone[count];
    char *pclone = clone;
    char *last;

    strcpy(clone, buf);

    mutex_lock(&cpld_data->cpld_lock);
    tok = strsep((char**)&pclone, " ");
    if (tok == NULL) {
        mutex_unlock(&cpld_data->cpld_lock);
        return -EINVAL;
    }
    addr = (uint16_t)strtoul(tok, &last, 16);
    if (addr == 0 && tok == last) {
        mutex_unlock(&cpld_data->cpld_lock);
        return -EINVAL;
    }

    tok = strsep((char**)&pclone, " ");
    if (tok == NULL) {
        mutex_unlock(&cpld_data->cpld_lock);
        return -EINVAL;
    }
    value = (uint8_t)strtoul(tok, &last, 16);
    if (value == 0 && tok == last) {
        mutex_unlock(&cpld_data->cpld_lock);
        return -EINVAL;
    }

    outb(value, addr);
    mutex_unlock(&cpld_data->cpld_lock);
    return count;
}
static DEVICE_ATTR_WO(setreg);

/**
 * Show status led
 * @param  dev     kernel device
 * @param  devattr kernel device attribute
 * @param  buf     buffer for get value
 * @return         led state - off/on/blink
 */
static ssize_t status_led_show(struct device *dev, struct device_attribute *devattr,
                               char *buf)
{
    unsigned char data = 0;
    mutex_lock(&cpld_data->cpld_lock);
    data = inb(LED_FPS);
    mutex_unlock(&cpld_data->cpld_lock);
    data = data & 0xc;
    return sprintf(buf, "%s\n",
                   data == stat_led_grn ? "on" : data == stat_led_grn_bnk ? "blink" : "off");
}

/**
 * Set the status led
 * @param  dev     kernel device
 * @param  devattr kernel device attribute
 * @param  buf     buffer of set value - off/on/blink
 * @param  count   number of bytes in buffer
 * @return         number of bytes written, or error code < 0.
 */
static ssize_t status_led_store(struct device *dev, struct device_attribute *devattr,
                                const char *buf, size_t count)
{
    unsigned char led_status, data;

    if (sysfs_streq(buf, "off")) {
        led_status = stat_led_off;
    } else if (sysfs_streq(buf, "on")) {
        led_status = stat_led_grn;
    } else if (sysfs_streq(buf, "blink")) {
        led_status = stat_led_grn_bnk;
    } else {
        count = -EINVAL;
        return count;
    }
    mutex_lock(&cpld_data->cpld_lock);
    data = inb(LED_FPS);
    data = data & ~(0xc);
    data = data | ( led_status << 2 );
    outb(data, LED_FPS);
    mutex_unlock(&cpld_data->cpld_lock);
    return count;
}
static DEVICE_ATTR_RW(status_led);


/**
 * Show master led
 * @param  dev     kernel device
 * @param  devattr kernel device attribute
 * @param  buf     buffer for get value
 * @return         led state - off/green/amber
 */
static ssize_t master_led_show(struct device *dev, struct device_attribute *devattr,
                               char *buf)
{
    unsigned char data = 0;
    mutex_lock(&cpld_data->cpld_lock);
    data = inb(LED_FPS);
    mutex_unlock(&cpld_data->cpld_lock);
    data = data & 0x3;
    return sprintf(buf, "%s\n",
                   data == master_led_grn ? "on" : data == master_led_amb ? "amber" : "off");
}

/**
 * Set the master led
 * @param  dev     kernel device
 * @param  devattr kernel device attribute
 * @param  buf     buffer of set value - off/green/amber
 * @param  count   number of bytes in buffer
 * @return         number of bytes written, or error code < 0.
 */
static ssize_t master_led_store(struct device *dev, struct device_attribute *devattr,
                                const char *buf, size_t count)
{
    unsigned char led_status, data;

    if (sysfs_streq(buf, "off")) {
        led_status = master_led_off;
    } else if (sysfs_streq(buf, "green")) {
        led_status = master_led_grn;
    } else if (sysfs_streq(buf, "amber")) {
        led_status = master_led_amb;
    } else {
        count = -EINVAL;
        return count;
    }
    mutex_lock(&cpld_data->cpld_lock);
    data = inb(LED_FPS);
    data = data & ~(0x3);
    data = data | led_status;
    outb(data, LED_FPS);
    mutex_unlock(&cpld_data->cpld_lock);
    return count;
}
static DEVICE_ATTR_RW(master_led);

static ssize_t psuL_prs_show(struct device *dev, struct device_attribute *devattr,
                             char *buf)
{
    unsigned char data = 0;
    mutex_lock(&cpld_data->cpld_lock);
    data = inb(PSU_STAT);
    mutex_unlock(&cpld_data->cpld_lock);
    return sprintf(buf, "%d\n", ~(data >> PSUL_PRS) & 1U);
}
static DEVICE_ATTR_RO(psuL_prs);

static ssize_t psuR_prs_show(struct device *dev, struct device_attribute *devattr,
                             char *buf)
{
    unsigned char data = 0;
    mutex_lock(&cpld_data->cpld_lock);
    data = inb(PSU_STAT);
    mutex_unlock(&cpld_data->cpld_lock);
    return sprintf(buf, "%d\n", ~(data >> PSUR_PRS) & 1U);
}
static DEVICE_ATTR_RO(psuR_prs);

static ssize_t psuL_status_show(struct device *dev, struct device_attribute *devattr,
                                char *buf)
{
    unsigned char data = 0;
    mutex_lock(&cpld_data->cpld_lock);
    data = inb(PSU_STAT);
    mutex_unlock(&cpld_data->cpld_lock);
    data = ( data >> PSUL_PWOK ) & 0x3;
    return sprintf(buf, "%d\n", data == 0x3 );
}
static DEVICE_ATTR_RO(psuL_status);

static ssize_t psuR_status_show(struct device *dev, struct device_attribute *devattr,
                                char *buf)
{
    unsigned char data = 0;
    mutex_lock(&cpld_data->cpld_lock);
    data = inb(PSU_STAT);
    mutex_unlock(&cpld_data->cpld_lock);
    data = ( data >> PSUR_PWOK ) & 0x3;
    return sprintf(buf, "%d\n", data == 0x3 );
}
static DEVICE_ATTR_RO(psuR_status);


static struct attribute *cpld_attrs[] = {
    &dev_attr_version.attr,
    &dev_attr_scratch.attr,
    &dev_attr_getreg.attr,
    &dev_attr_setreg.attr,
    // LEDS
    &dev_attr_status_led.attr,
    &dev_attr_master_led.attr,
    // PSUs
    &dev_attr_psuL_prs.attr,
    &dev_attr_psuR_prs.attr,
    &dev_attr_psuL_status.attr,
    &dev_attr_psuR_status.attr,
    NULL,
};

static struct attribute_group cpld_attrs_grp = {
    .attrs = cpld_attrs,
};

static ssize_t sfp_txfault_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    unsigned char data;
    struct sfp_device_data *dev_data = dev_get_drvdata(dev);
    unsigned int port_bit = dev_data->portid - 1;

    mutex_lock(&cpld_data->cpld_lock);
    data = inb(SFP_TXFAULT);
    mutex_unlock(&cpld_data->cpld_lock);
    return sprintf(buf, "%d\n", (data >> port_bit ) & 1U);
}
static DEVICE_ATTR_RO(sfp_txfault);

static ssize_t sfp_modabs_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    unsigned char data;
    struct sfp_device_data *dev_data = dev_get_drvdata(dev);
    unsigned int port_bit = dev_data->portid - 1;

    mutex_lock(&cpld_data->cpld_lock);
    data = inb(SFP_MODABS);
    mutex_unlock(&cpld_data->cpld_lock);
    return sprintf(buf, "%d\n", (data >> port_bit ) & 1U);
}
static DEVICE_ATTR_RO(sfp_modabs);

static ssize_t sfp_rxlos_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    unsigned char data;
    struct sfp_device_data *dev_data = dev_get_drvdata(dev);
    unsigned int port_bit = dev_data->portid - 1;

    mutex_lock(&cpld_data->cpld_lock);
    data = inb(SFP_RXLOS);
    mutex_unlock(&cpld_data->cpld_lock);
    return sprintf(buf, "%d\n", (data >> port_bit ) & 1U);
}
static DEVICE_ATTR_RO(sfp_rxlos);

static ssize_t sfp_txdis_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    unsigned char data;
    struct sfp_device_data *dev_data = dev_get_drvdata(dev);
    unsigned int port_bit = dev_data->portid - 1;
    mutex_lock(&cpld_data->cpld_lock);
    data = inb(SFP_TXCTRL);
    mutex_unlock(&cpld_data->cpld_lock);
    return sprintf(buf, "%d\n", (data >> port_bit ) & 1U);
}

static ssize_t sfp_txdis_store(struct device *dev, struct device_attribute *attr, const char *buf, size_t size)
{
    long value;
    ssize_t status;
    unsigned char data;
    struct sfp_device_data *dev_data = dev_get_drvdata(dev);
    unsigned int port_bit = dev_data->portid - 1;

    mutex_lock(&cpld_data->cpld_lock);
    status = kstrtol(buf, 0, &value);
    if (status == 0) {
        // check if value is 0, clear
        data = inb(SFP_TXCTRL);
        if (!value)
            data = data & ~( 1U << port_bit);
        else
            data = data | ( 1U << port_bit);
        outb(data, SFP_TXCTRL);
        status = size;
    }
    mutex_unlock(&cpld_data->cpld_lock);
    return status;
}
static DEVICE_ATTR_RW(sfp_txdis);

static ssize_t sfp_rs_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    unsigned char data;
    struct sfp_device_data *dev_data = dev_get_drvdata(dev);
    unsigned int port_bit = dev_data->portid - 1;

    // High nibble
    port_bit = port_bit + 4;
    mutex_lock(&cpld_data->cpld_lock);
    data = inb(SFP_TXCTRL);
    mutex_unlock(&cpld_data->cpld_lock);
    return sprintf(buf, "%d\n", (data >> port_bit ) & 1U);
}

static ssize_t sfp_rs_store(struct device *dev, struct device_attribute *attr, const char *buf, size_t size)
{
    long value;
    ssize_t status;
    unsigned char data;
    struct sfp_device_data *dev_data = dev_get_drvdata(dev);
    unsigned int port_bit = dev_data->portid - 1;

    // High nibble
    port_bit = port_bit + 4;
    mutex_lock(&cpld_data->cpld_lock);
    status = kstrtol(buf, 0, &value);
    if (status == 0) {
        // check if value is 0, clear
        data = inb(SFP_TXCTRL);
        if (!value)
            data = data & ~( 1U << port_bit);
        else
            data = data | ( 1U << port_bit);
        outb(data, SFP_TXCTRL);
        status = size;
    }
    mutex_unlock(&cpld_data->cpld_lock);
    return status;
}
static DEVICE_ATTR_RW(sfp_rs);

static struct attribute *sfp_attrs[] = {
    // SFP
    &dev_attr_sfp_txfault.attr,
    &dev_attr_sfp_modabs.attr,
    &dev_attr_sfp_rxlos.attr,
    &dev_attr_sfp_txdis.attr,
    &dev_attr_sfp_rs.attr,
    NULL,
};

static struct attribute_group sfp_attr_grp = {
    .attrs = sfp_attrs,
};

static const struct attribute_group *sfp_attr_grps[] = {
    &sfp_attr_grp,
    NULL
};

static struct resource cpld_resources[] = {
    {
        .start  = 0x0200,
        .end    = 0x0255,
        .flags  = IORESOURCE_IO,
    },
};

static struct device * sfp_init(int portid) {
    struct sfp_device_data *new_data;
    struct device *new_device;

    new_data = kzalloc(sizeof(*new_data), GFP_KERNEL);
    if (!new_data) {
        printk(KERN_ALERT "Cannot alloc sff device data @port%d", portid);
        return NULL;
    }
    /* Front panel port ID start from 1 */
    new_data->portid = portid + 1;
    new_device = device_create_with_groups(celplatform, cpld_data->fpp_node, MKDEV(0, 0), new_data, sfp_attr_grps, "SFP%d", new_data->portid);
    if (IS_ERR(new_device)) {
        printk(KERN_ALERT "Cannot create sff device @port%d", portid);
        kfree(new_data);
        return NULL;
    }
    return new_device;
}

static void cpld_dev_release( struct device * dev)
{
    return;
}

static struct platform_device cpld_dev = {
    .name           = DRIVER_NAME,
    .id             = -1,
    .num_resources  = ARRAY_SIZE(cpld_resources),
    .resource       = cpld_resources,
    .dev = {
        .release = cpld_dev_release,
    }
};

static int cpld_drv_probe(struct platform_device *pdev)
{
    struct resource *res;
    int err, i = 0;

    cpld_data = devm_kzalloc(&pdev->dev, sizeof(struct cpld_data),
                             GFP_KERNEL);
    if (!cpld_data)
        return -ENOMEM;

    mutex_init(&cpld_data->cpld_lock);

    cpld_data->read_addr = VERSION;

    res = platform_get_resource(pdev, IORESOURCE_IO, 0);
    if (unlikely(!res)) {
        printk(KERN_ERR "Specified Resource Not Available...\n");
        return -ENODEV;
    }

    err = sysfs_create_group(&pdev->dev.kobj, &cpld_attrs_grp);
    if (err) {
        printk(KERN_ERR "Cannot create sysfs for SMC.\n");
        return err;
    }

    celplatform = class_create(THIS_MODULE, "celplatform");
    if (IS_ERR(celplatform)) {
        printk(KERN_ERR "Failed to register device class\n");
        sysfs_remove_group(&pdev->dev.kobj, &cpld_attrs_grp);
        return PTR_ERR(celplatform);
    }

    cpld_data->fpp_node = device_create(celplatform, NULL, MKDEV(0, 0), NULL, "optical_ports");
    if (IS_ERR(cpld_data->fpp_node)) {
        class_destroy(celplatform);
        sysfs_remove_group(&pdev->dev.kobj, &cpld_attrs_grp);
        return PTR_ERR(cpld_data->fpp_node);
    }

    err = sysfs_create_link(&pdev->dev.kobj, &cpld_data->fpp_node->kobj, "SFP");
    if (err != 0) {
        put_device(cpld_data->fpp_node);
        device_unregister(cpld_data->fpp_node);
        class_destroy(celplatform);
        sysfs_remove_group(&pdev->dev.kobj, &cpld_attrs_grp);
        return err;
    }

    // Creae SFP devices
    for ( i = 0; i < 4; i++) {
        cpld_data->sfp_devices[i] = sfp_init(i);
    }
    return 0;
}

static int cpld_drv_remove(struct platform_device *pdev)
{
    struct sfp_device_data *rem_data;
    int i;

    for ( i = 0; i < 4; i++) {
        rem_data = dev_get_drvdata(cpld_data->sfp_devices[i]);
        put_device(cpld_data->sfp_devices[i]);
        device_unregister(cpld_data->sfp_devices[i]);
        kzfree(rem_data);
    }
    put_device(cpld_data->fpp_node);
    device_unregister(cpld_data->fpp_node);
    sysfs_remove_group(&pdev->dev.kobj, &cpld_attrs_grp);
    class_destroy(celplatform);
    return 0;
}

static struct platform_driver cpld_drv = {
    .probe  = cpld_drv_probe,
    .remove = __exit_p(cpld_drv_remove),
    .driver = {
        .name   = DRIVER_NAME,
    },
};

int cpld_init(void)
{
    // Register platform device and platform driver
    platform_device_register(&cpld_dev);
    platform_driver_register(&cpld_drv);
    return 0;
}

void cpld_exit(void)
{
    // Unregister platform device and platform driver
    platform_driver_unregister(&cpld_drv);
    platform_device_unregister(&cpld_dev);
}

module_init(cpld_init);
module_exit(cpld_exit);


MODULE_AUTHOR("Celestica Inc.");
MODULE_DESCRIPTION("Celestica E1031 SMC driver");
MODULE_VERSION("0.0.1");
MODULE_LICENSE("GPL");
