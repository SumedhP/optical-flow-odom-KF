import math
import scipy

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
