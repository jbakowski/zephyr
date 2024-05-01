import numpy as np

def currentRMS(file_path):
    data = np.genfromtxt(file_path, delimiter=None)
    rms = np.sqrt(np.mean(np.square(data)))
    return rms