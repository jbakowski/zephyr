west flash -r pyocd --dev-id

twister --device-testing --device-serial /dev/ttyACM1 -p stm32l562e_dk -s pm.state_transition_idle_to_active -v --west-flash
twister --device-testing --hardware-map map.yaml -p stm32l562e_dk -s pm.state_transition_idle_to_active -v --west-flash
twister --device-testing --hardware-map map.yaml -s pm.state_transition_idle_to_active -vv --west-flash

# raw pytest
pytest --host-uuid=004800483137510D33333639 --client-uuid=004E003F3137510B33333639 --host-board=stm32l562e_dk --client-board=stm32l562e_dk --powershield=/dev/serial/by-id/usb-STMicroelectronics_STLINK-V3_004800483137510D33333639-if02

# twister
twister --device-testing --device-serial /dev/ttyACM1 -p stm32l562e_dk -s pm.state_transition_idle_to_active --west-flash

# CLIENT:
usb-STMicroelectronics_PowerShield__Virtual_ComPort_in_FS_Mode__FFFFFFFEFFFF-if00
usb-STMicroelectronics_STLINK-V3_004E003F3137510B33333639-if02

# HOST:
usb-STMicroelectronics_STLINK-V3_004800483137510D33333639-if02