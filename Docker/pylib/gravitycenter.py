import numpy as np


def gravitycenter(data, height, width):
    _data = np.squeeze(data)
    if _data.ndim != 2:
        return [0, 0]
    _total = np.sum(_data)
    _sum_Y = np.sum(_data, axis=1)
    _total_Y = 0
    for i in range(height):
        _total_Y += i*_sum_Y[i]
    gravity_Y = int(_total_Y/_total)
    _sum_X = np.sum(_data, axis=0)
    _total_X = 0
    for j in range(width):
        _total_X += j*_sum_X[j]
    gravity_X = int(_total_X/_total)
    return [gravity_Y, gravity_X]
