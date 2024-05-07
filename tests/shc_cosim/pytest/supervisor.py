import serial
import time
import subprocess

class Supervisor():
    def __init__(self, host_port, host_baud):
        self.host_port = host_port
        self.host_baud = host_baud
        self.host_serial_device = serial.Serial(self.host_port, self.host_baud, timeout=1)
        print(host_port)
        print(host_baud)

    def execute_supervisor_action(self, device, action):
        with open("supervisor_log.txt", 'a+') as file:
            if device == "print":
                file.write(action + '\n')
            elif device == "delay":
                time.sleep(float(action))

    def send_command_via_uart(self, command):
        #self.host_serial_device.write(command.encode())
        #subprocess.run(["echo", command, ">", "/dev/serial/by-id/usb-STMicroelectronics_STLINK-V3_004800483137510D33333639-if02"], shell=True, check=True)
        device_path = "/dev/serial/by-id/usb-STMicroelectronics_STLINK-V3_004800483137510D33333639-if02"
        with open(device_path, 'w') as device_file:
            subprocess.run(["echo", command], stdout=device_file, check=True)
        print(f"Sent command '{command}' via UART")

    def parse_commands(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(':')
                if len(parts) != 3:
                    print(f"Invalid command format: {line}")
                    continue

                entity, device, action = parts

                if entity == 'supervisor':
                    self.execute_supervisor_action(device, action)
                elif entity == 'host':
                    self.send_command_via_uart(device + ":" + action)
                elif entity == 'client':
                    pass
                else:
                    print(f"Unknown entity: {entity}")

    def close_uart(self):
        if self.host_serial_device.is_open:
            self.host_serial_device.close()