import numpy as np
from scipy import signal
from skimage.restoration import denoise_tv_chambolle

def current_RMS(file_path):
    data = np.genfromtxt(file_path, delimiter=None)
    rms = np.sqrt(np.mean(np.square(data)))
    return rms

# works only if there is one transition in the signal
def detect_single_transition(file_path):
    data = np.genfromtxt(file_path, delimiter=None)
    data_std = (data - data.mean()) / data.std()
    data_denoised = denoise_tv_chambolle(data_std, weight=3)
    data_step = -2*np.cumsum(data_denoised)
    step_indicator = data_step == data_step.max()
    if True in step_indicator:
        return True
    else:
        return False

def measure_single_transition(file_path):
    data = np.genfromtxt(file_path, delimiter=None)
    data_std = (data - data.mean()) / data.std()
    data_denoised = denoise_tv_chambolle(data_std, weight=3)
    data_step = -2*np.cumsum(data_denoised)
    step_indicator = data_step == data_step.max()

    # linear search is good enough for small enough datasets
    # might want to swap to a binary search for larger datasets, if performance suffers
    transition_start = None
    transition_end = None

    for i, value in enumerate(step_indicator):
        if value == True:
            if transition_start == None:
                transition_start = i
            transition_end = i

    return (transition_start, transition_end)

# returns the amount of rising edges detected
def detect_multiple_rising_edge(file_path):
    data = np.genfromtxt(file_path, delimiter=None)
    dary = np.array(data)
    dary -= np.average(dary)

    step = np.hstack((np.ones(len(dary)), -1*np.ones(len(dary))))
    dary_step = np.convolve(dary, step, mode='valid')

    peaks = signal.find_peaks(dary_step, width=20)[0]

    return len(peaks)

# returns the amount of falling edges detected
def detect_multiple_falling_edge(file_path):
    data = np.genfromtxt(file_path, delimiter=None)
    dary = np.array(data)
    dary -= np.average(dary)

    step = np.hstack((np.ones(len(dary)), -1*np.ones(len(dary))))
    dary_step = np.convolve(dary, step, mode='valid')

    peaks = signal.find_peaks(-dary_step, width=20)[0]

    return len(peaks)
