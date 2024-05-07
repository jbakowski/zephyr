# Copyright (c) 2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

set(HOST_APP shc_host)
set(HOST_APP_SRC_DIR ${ZEPHYR_BASE}/tests/shc_cosim/${HOST_APP})

ExternalZephyrProject_Add(
	APPLICATION ${HOST_APP}
	SOURCE_DIR  ${HOST_APP_SRC_DIR}
	BOARD       ${SB_CONFIG_HOST_BOARD}
)

sysbuild_add_dependencies(FLASH shc_cosim shc_host)