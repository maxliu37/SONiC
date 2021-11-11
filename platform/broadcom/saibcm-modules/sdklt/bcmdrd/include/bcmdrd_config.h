/*
 * $Copyright: Copyright 2018-2021 Broadcom. All rights reserved.
 * The term 'Broadcom' refers to Broadcom Inc. and/or its subsidiaries.
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License 
 * version 2 as published by the Free Software Foundation.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * A copy of the GNU General Public License version 2 (GPLv2) can
 * be found in the LICENSES folder.$
 *
 * DO NOT EDIT THIS FILE!
 * This file will be auto-generated in the near future.
 *
 * This config file defines all compilation-time specifications for
 * the BCMDRD.
 *
 * Reasonable defaults are provided for all configuration options
 * where appropriate.
 *
 * You need not edit this file directly to change your configuration,
 * nor is modifying this file advised -- so doing will require
 * manually merging whenever the BCMDRD is upgraded.
 *
 * You should provide your own configuration options or overrides
 * through a combination of:
 *
 *      1. The compiler command line, such as -D{OPTION}={VALUE}
 *
 *      2. Create your own custom configuration file:
 *         a) Create a file called 'bcmdrd_custom_config.h'
 *         b) Define all custom settings, using this file as
 *            the reference
 *         c) Add -DBCMDRD_INCLUDE_CUSTOM_CONFIG to your
 *            compilation
 *         d) Make sure the compilation include path includes
 *            'bcmdrd_custom_config.h'
 *
 */

#ifndef BCMDRD_CONFIG_H
#define BCMDRD_CONFIG_H


/*
 * Include system config file if specified:
 */
#ifdef BCMDRD_INCLUDE_CUSTOM_CONFIG
#include <bcmdrd_custom_config.h>
#endif


/*
 * OPTIONAL configuration and feature values.
 * Defaults are provided for all non-specified values.
 */

/* Maximum number of chips supported */
#ifndef BCMDRD_CONFIG_MAX_UNITS
#define BCMDRD_CONFIG_MAX_UNITS                    8
#endif

/* Maximum number of ports per chip supported */
#ifndef BCMDRD_CONFIG_MAX_PORTS
#define BCMDRD_CONFIG_MAX_PORTS                    848
#endif

/* Maximum number of SCHAN polls */
#ifndef BCMDRD_CONFIG_SCHAN_MAX_POLLS
#define BCMDRD_CONFIG_SCHAN_MAX_POLLS              100000
#endif

/* Maximum number of MIIM polls */
#ifndef BCMDRD_CONFIG_MIIM_MAX_POLLS
#define BCMDRD_CONFIG_MIIM_MAX_POLLS               100000
#endif

/* Direct access to memory-mapped registers */
#ifndef BCMDRD_CONFIG_MEMMAP_DIRECT
#define BCMDRD_CONFIG_MEMMAP_DIRECT                0
#endif

/*
 * Include chip symbol tables for the debug shell.
 *
 * No symbolic debugging (register/memory names) will be available
 * without this defined.
 *
 * You should enable at least these symbols if you can afford the
 * space.
 *
 * This define is required to get any symbols at all.
 *
 * If you only wish to include symbols for a subset of chips in the
 * system (probably for code space reasons), you can define the
 * following for each chip whose symbols you wish to EXCLUDE:
 *
 *       BCMDRD_CONFIG_EXCLUDE_CHIP_SYMBOLS_<CHIP>
 *
 */
#ifndef BCMDRD_CONFIG_INCLUDE_CHIP_SYMBOLS
#define BCMDRD_CONFIG_INCLUDE_CHIP_SYMBOLS         1
#endif

/*
 * Include register and memory field information for the debug shell.
 *
 * This provides encoding, decoding, and displaying individual field
 * values for each register and memory.
 *
 * Requires more code space than just the chip symbols alone.
 *
 * The per-chip exclusion define
 * (BCMDRD_CONFIG_EXCLUDE_FIELD_INFO_<CHIP>) also applies.
 */
#ifndef BCMDRD_CONFIG_INCLUDE_FIELD_INFO
#define BCMDRD_CONFIG_INCLUDE_FIELD_INFO           1
#endif

/*
 * Include alternative symbol names for registers and memories.
 *
 * Mainly for internal Broadcom use, so you can safely leave this
 * option off.
 */
#ifndef BCMDRD_CONFIG_INCLUDE_ALIAS_NAMES
#define BCMDRD_CONFIG_INCLUDE_ALIAS_NAMES          1
#endif

#endif /* BCMDRD_CONFIG_H */

#ifdef CONFIG_OPTION
#ifdef BCMDRD_INCLUDE_CUSTOM_CONFIG
CONFIG_OPTION(BCMDRD_INCLUDE_CUSTOM_CONFIG)
#endif
#ifdef BCMDRD_CONFIG_MAX_UNITS
CONFIG_OPTION(BCMDRD_CONFIG_MAX_UNITS)
#endif
#ifdef BCMDRD_CONFIG_MAX_PORTS
CONFIG_OPTION(BCMDRD_CONFIG_MAX_PORTS)
#endif
#ifdef BCMDRD_CONFIG_SCHAN_MAX_POLLS
CONFIG_OPTION(BCMDRD_CONFIG_SCHAN_MAX_POLLS)
#endif
#ifdef BCMDRD_CONFIG_MIIM_MAX_POLLS
CONFIG_OPTION(BCMDRD_CONFIG_MIIM_MAX_POLLS)
#endif
#ifdef BCMDRD_CONFIG_MEMMAP_DIRECT
CONFIG_OPTION(BCMDRD_CONFIG_MEMMAP_DIRECT)
#endif
#ifdef BCMDRD_CONFIG_INCLUDE_CHIP_SYMBOLS
CONFIG_OPTION(BCMDRD_CONFIG_INCLUDE_CHIP_SYMBOLS)
#endif
#ifdef BCMDRD_CONFIG_INCLUDE_FIELD_INFO
CONFIG_OPTION(BCMDRD_CONFIG_INCLUDE_FIELD_INFO)
#endif
#ifdef BCMDRD_CONFIG_INCLUDE_ALIAS_NAMES
CONFIG_OPTION(BCMDRD_CONFIG_INCLUDE_ALIAS_NAMES)
#endif
#endif /* CONFIG_OPTION */
#include "bcmdrd_config_chips.h"
