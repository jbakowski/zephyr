import pytest
import subprocess
import shutil
from current_analyzer import current_RMS, detect_single_transition, detect_multiple_rising_edge, detect_multiple_falling_edge, measure_single_transition

@pytest.fixture(scope="module", autouse=True)
def setup_client(request):
    client_board = request.config.getoption('--client-board')
    client_uuid = request.config.getoption('--client-uuid')
    client_path = "../shc_client/residency"
    subprocess.run(["west", "build", "-b", str(client_board)], cwd=client_path, check=True)
    print("Client binary built!")
    subprocess.run(["west", "flash", "-r", "pyocd", "--dev-id", client_uuid], cwd=client_path, check=True)
    print("Client binary flashed!")

@pytest.fixture(scope="module", autouse=True)
def module_path(request):
    return "../shc_client/residency/"

@pytest.fixture(scope="module", autouse=True)
def move_measurement_data(module_path):
    yield
    shutil.move("measurementData.csv", module_path)
    shutil.move("supervisor_log.txt", module_path)

def test_expected_rms_residency(current_measurement_output):
    average_expected_value = 0.0056983115268326445
    tolerance = 0.2
    measured_rms = current_RMS("measurementData.csv")
    assert (measured_rms > (1-tolerance)*average_expected_value) and (measured_rms < (1+tolerance)*average_expected_value)

# # currently hardcoded for stm32l562e_dk residency time of 100us
# def test_entered_idle_state(current_measurement_output):
#     idle_periods = [70, 80, 90, 100, 110, 120]
#     expected_results = [False, False, False, True, True, True]
#     time_separator = 5000 # 500ms
#     actual_results = []




