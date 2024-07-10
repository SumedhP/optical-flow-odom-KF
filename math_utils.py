import math

# Angle in degrees
def rotateVector(x, y, angle):
    angle = math.radians(angle)
    temp_x = x
    x = x * math.cos(angle) - y * math.sin(angle)
    y = temp_x * math.sin(angle) + y * math.cos(angle)
    return x, y

def filterData(data):
    """
    Here for data filteration. Somethings I've read are:
    - Low pass on accel
    - Median filter on accel
    - Both of the above
    - Lowering trust on optical flow the greater the magnitude of the vector
    """
    pass


# Higher alpha means more weight to the previous value
def lowPassHelper(prev, current, alpha):
    return alpha * prev + (1 - alpha) * current

def lowPass(data, alpha):
    result = []
    prev = data[0]
    result.append(prev)
    for i in range(1, len(data)):
        prev = lowPassHelper(prev, data[i], alpha)
        result.append(prev)
    return result

import statistics
def median(data, window_size):
    result = []
    for i in range(len(data)):
        if i < window_size:
            result.append(data[i])
        else:
            result.append(statistics.median(data[i - window_size:i]))
    return result
