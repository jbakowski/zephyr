import pytest
import logging
import subprocess
import os
import re
import serial
from time import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Board():
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud

        self.serial_device = serial.Serial("/" + port, self.baud, timeout=1)

    def wait_for_regex_in_line(self, regex, timeout_s=20, log=True):
        start_time = time()
        while True:
            self.serial_device.timeout=timeout_s
            line = self.serial_device.read_until().decode("utf-8", errors='replace').replace("\r\n", "")
            if line != "" and log:
                print(line)
            if time() - start_time > timeout_s:
                raise RuntimeError("timeout")
            regex_search = re.search(regex, line)
            if regex_search:
                return regex_search

@pytest.fixture(scope="session")
def host_board(host_port, host_baudrate):
    return Board(host_port, host_baudrate)

@pytest.fixture(scope="session")
def client_board(client_port, client_baudrate):
    return Board(client_port, client_baudrate)

def pytest_addoption(parser):
    parser.addoption("--host-port",
            help="The port to which the host device is attached (eg: /dev/ttyACM0)")
    parser.addoption("--host-baud", type=int, default=115200,
            help="Host's serial port baud rate (default: 115200)")
    parser.addoption("--client-port",
            help="The port to which the client device is attached (eg: /dev/ttyACM1)")
    parser.addoption("--client-baud", type=int, default=115200,
            help="Client's serial port baud rate (default: 115200)")

@pytest.fixture(scope="session")
def host_port(request):
    return request.config.getoption("--host-port")

@pytest.fixture(scope="session")
def host_baudrate(request):
    return request.config.getoption("--host-baud")

@pytest.fixture(scope="session")
def client_port(request):
    return request.config.getoption("--client-port")

@pytest.fixture(scope="session")
def client_baudrate(request):
    return request.config.getoption("--client-baud")

@pytest.fixture(scope="session", autouse=True)
def initialize_system(request):
    setup_supervisor_config()
    build_host_binary()
    build_client_binary()
    flash_host_binary()
    flash_client_binary()
    reset_devices()

    def finalize():
        deinit_system()

    request.addfinalizer(finalize)

def setup_supervisor_config():
    print("Supervisor configured")

def build_host_binary():
    print("Host binary built")

def build_client_binary():
    fw_dir = "../samples/hello_world"
    build_dir = fw_dir + "/build"
    board = "stm32l562e_dk"

    subprocess.run(["west", "build", "-p", "auto", "-b", board], cwd = fw_dir, check=True)
    binary_path = os.path.join(build_dir, "zephyr", "zephyr.bin")
    assert os.path.isfile(binary_path), "Build failed: client binary not found"

# TODO: specify ports for host and client, so we can differentiate between
# host and client, even if they are the same device
def flash_host_binary():
    print("Host binary flashed")
def flash_client_binary():
    fw_dir = "../samples/hello_world"

    subprocess.run(["west", "flash"], cwd = fw_dir, check=True)

def reset_devices():
    print("Devices reset")
def deinit_system():
    print("System deinitialized")