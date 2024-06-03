import pytest
import logging
import subprocess
import os
import json
import re
import serial
import threading
import time
from powershield import PowerShield
from supervisor import Supervisor

def pytest_addoption(parser):
    parser.addoption("--host-uuid",
            help="Host's probe UUID.")
    parser.addoption("--client-uuid",
            help="Client's probe UUID.")
    parser.addoption("--client-board",
            help="Board name of the client.")
    parser.addoption("--host-board",
            help="Board name of the host.")
    parser.addoption("--powershield",
            help="Path to PowerShield device")

@pytest.fixture(scope='session', autouse=True)
def build_and_flash_host(request):
    host_board = request.config.getoption('--host-board')
    host_uuid = request.config.getoption('--host-uuid')
    host_path = "../shc_host"
    subprocess.run(["west", "build", "-b", str(host_board)], cwd=host_path, check=True)
    print("Host binary built!")
    subprocess.run(["west", "flash", "-r", "pyocd", "--dev-id", host_uuid], cwd=host_path, check=True)
    print("Host binary flashed!")

@pytest.fixture(scope="module")
def current_measurement_output(request, module_path):
    powershield_device = request.config.getoption("--powershield")
    SupVis = Supervisor(powershield_device, 115200)
    supervisor_thread = threading.Thread(target=SupVis.parse_commands, args=(module_path + "simulationPlan.txt",))
    supervisor_thread.start()
    PwSh = PowerShield("1k", 10)
    while not PwSh.acqComplete:
        time.sleep(1)
    PwSh.pwsh.close()
    return "measurementData.csv"

@pytest.fixture(scope="session", autouse=True)
def clean_up(request):
    yield
    if os.path.exists("rawData.csv"):
        os.remove("rawData.csv")
    if os.path.exists("sanitizedData.csv"):
        os.remove("sanitizedData.csv")
    if os.path.exists("measurementData.csv"):
        os.remove("measurementData.csv")
    if os.path.exists("supervisor_log.txt"):
        os.remove("supervisor_log.txt")