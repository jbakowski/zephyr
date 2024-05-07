west flash -r pyocd --dev-id

twister --device-testing --device-serial /dev/ttyACM1 -p stm32l562e_dk -s pm.state_transition_idle_to_active -v --west-flash

CLIENT:
usb-STMicroelectronics_PowerShield__Virtual_ComPort_in_FS_Mode__FFFFFFFEFFFF-if00
usb-STMicroelectronics_STLINK-V3_004E003F3137510B33333639-if02

HOST:
usb-STMicroelectronics_STLINK-V3_004800483137510D33333639-if02

###

twister --device-testing --device-serial /dev/ttyACM0 -p stm32l562e_dk -s pm.state.transition_idle_to_active -v --west-flash="-r pyocd --dev-id usb-STMicroelectronics_STLINK-V3_004E003F3137510B33333639-if02"

twister --device-testing --device-serial /dev/ttyACM2 --device-id  -p stm32l562e_dk -s pm.state.transition_idle_to_active -v --west-flash