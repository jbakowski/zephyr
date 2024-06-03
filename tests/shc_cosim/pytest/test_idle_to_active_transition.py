import pytest
import subprocess
import time
import os
import shutil
from current_analyzer import current_RMS, detect_single_transition, detect_multiple_rising_edge, detect_multiple_falling_edge, measure_single_transition

@pytest.fixture(scope="module", autouse=True)
def setup_client(request):
    client_board = request.config.getoption('--client-board')
    client_uuid = request.config.getoption('--client-uuid')
    client_path = "../shc_client/idle_to_active"
    subprocess.run(["west", "build", "-b", str(client_board)], cwd=client_path, check=True)
    print("Client binary built!")
    subprocess.run(["west", "flash", "-r", "pyocd", "--dev-id", client_uuid], cwd=client_path, check=True)
    print("Client binary flashed!")

@pytest.fixture(scope="module", autouse=True)
def module_path(request):
    return "../shc_client/idle_to_active/"

@pytest.fixture(scope="module", autouse=True)
def move_measurement_data(module_path):
    yield
    shutil.move("measurementData.csv", module_path)
    shutil.move("supervisor_log.txt", module_path)

def test_expected_rms(current_measurement_output):
    average_expected_value = 0.00725440798118475988888888888889
    tolerance = 0.2
    measured_rms = current_RMS("measurementData.csv")
    assert (measured_rms > (1-tolerance)*average_expected_value) and (measured_rms < (1+tolerance)*average_expected_value)

def test_detect_state_transition(current_measurement_output):
    assert detect_single_transition("measurementData.csv")

def test_detect_rising_edges(current_measurement_output):
    assert detect_multiple_rising_edge("measurementData.csv") == 1

def test_detect_falling_edges(current_measurement_output):
    assert detect_multiple_falling_edge("measurementData.csv") == 0

def test_state_transition_start(current_measurement_output):
    (transition_start, transition_end) = measure_single_transition("measurementData.csv")
    average_expected_value = 2531
    # 5ms tolerance
    tolerance = 5
    assert (transition_start > (1-tolerance)*average_expected_value) and (transition_start < (1+tolerance)*average_expected_value)

def test_measure_state_transition(current_measurement_output):
    (transition_start, transition_end) = measure_single_transition("measurementData.csv")
    # (end_of_transition - start_of_transition) * sampling_frequency = length of transition
    # (2531 - 2531) * 1000
    # in this specific example, our time resolution is not good enough, because the transition
    # is sub 1ms
    result = (transition_end - transition_start) * 1000
    assert result == 0