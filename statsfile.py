import numpy as np

#Statistics
def linear_variation(path):
    increments = np.diff(path)
    return np.sum(np.abs(increments))

def quadratic_variation(path):
    increments = np.diff(path)
    return np.sum(increments ** 2)

def cubic_variation(path):
    increments = np.diff(path)
    return np.sum(np.abs(increments ** 3))

#average statistic over 2d numpy array:

def avg_stat(statistic, paths):
    if paths.size == 0:
        return 0
    else:
        return round((sum(statistic(path) for path in paths) / len(paths)), 2)
     


