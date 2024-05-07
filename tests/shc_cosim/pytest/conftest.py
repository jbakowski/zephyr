import pytest
import logging
import subprocess
import os
import json
import re
import serial
import threading
from time import time
from powershield import PowerShield
from supervisor import Supervisor
from twister_harness import DeviceAdapter

def pytest_addoption(parser):
    parser.addoption("--host-uuid",
            help="Host's probe UUID.")
    parser.addoption("--client-uuid",
            help="Client's probe UUID.")


@pytest.fixture(scope="session")
def host_uuid(request):
    return request.config.getoption('--host-uuid')

@pytest.fixture(scope="session")
def client_uuid(request):
    return request.config.getoption('--client-uuid')

@pytest.fixture(scope="session")
def current_measurement_output(request):
    SupVis = Supervisor("/dev/serial/by-id/usb-STMicroelectronics_STLINK-V3_004800483137510D33333639-if02", 115200)
    supervisor_thread = threading.Thread(target=SupVis.parse_commands, args=("simulationPlan.txt",))
    supervisor_thread.start()
    PwSh = PowerShield("1k", 5)
    while not PwSh.acqComplete:
        time.sleep(1)
    return "measurementData.csv"

@pytest.fixture(scope="session", autouse=True)
def initialize_system(request, dut: DeviceAdapter):
    client_uuid_val = request.config.getoption("--client-uuid")
    host_uuid_val = request.config.getoption("--host-uuid")

    setup_supervisor_config()
    flash_host_binary(host_uuid_val)
    #flash_client_binary(client_uuid_val)

    def finalize():
        deinit_system()

    request.addfinalizer(finalize)

def setup_supervisor_config():
    print("Supervisor configured")

def flash_host_binary(host_uuid):
    testplan_json = "twister-out/testplan.json"
    with open(testplan_json, 'r') as file:
        data = json.load(file)
        platform = data['testsuites'][0]['platform']
        testsuite_name = data['testsuites'][0]['name']
        build_dir = "twister-out/" + platform + '/' + testsuite_name
    subprocess.run(["west", "flash", "--domain", "shc_host", "-r", "pyocd", "--dev-id", host_uuid], cwd=build_dir, check=True)
    print("Host binary flashed")
    # west flash -r pyocd --dev-id

def flash_client_binary(client_uuid):
    print("Client binary flashed")

def reset_devices():
    print("Devices reset")

def deinit_system():
    print("System deinitialized")
    # if os.path.exists("rawData.csv"):
    #      os.remove("rawData.csv")
    # if os.path.exists("sanitizedData.csv"):
    #      os.remove("sanitizedData.csv")
    # if os.path.exists("measurementData.csv"):
    #      os.remove("measurementData.csv")
    # if os.path.exists("supervisor_log.txt"):
    #      os.remove("supervisor_log.txt")