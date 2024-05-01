from current_analyzer import currentRMS

def test_active_state(current_measurement_output):
    average_expected_value = 0.005669083770115426
    tolerance = 0.2
    measured_rms = currentRMS("measurementData.csv")
    assert (measured_rms > (1-tolerance)*average_expected_value) and (measured_rms < (1+tolerance)*average_expected_value)
