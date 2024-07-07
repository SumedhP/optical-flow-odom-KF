import vector
import math
import scipy

def rotateVector(x, y, angle):
    """
    Rotate a vector by a given angle (radians)
    """
    vec = vector.obj(x=x, y=y).rotateZ(math.radians(angle))
    return vec.x, vec.y

def filterData(data):
    """
    Here for data filteration. Somethings I've read are:
    - Low pass on accel
    - Median filter on accel
    - Both of the above
    - Lowering trust on optical flow the greater the magnitude of the vector
    """
    pass
