from filterpy.kalman import KalmanFilter  
import numpy as np

class KalmanFilterWrapper:
    def __init__(self):
        self.kf = KalmanFilter(dim_x=3, dim_z=2)
        self.dt = 0.01

        # State transition matrix
        self.kf.F = np.array([[1, self.dt, 0.5*self.dt**2],
                              [0, 1, self.dt],
                              [0, 0, 1]])
        
        # Measurement function
        self.kf.H = np.array([[0, 1, 0],
                              [0, 0, 1]])

        self.of_std = 0.009877928685029257
        self.accel_std = 0.022141264441937807

        self.kf.R = np.array([[self.of_std**2, 0],
                              [0, self.accel_std**2]])
        
        self.kf.Q = np.array([[1e-8, 0, 0],
                              [0, 1e-6, 0],
                              [0, 0, 1e-4]])
        
        self.kf.x = np.array([0, 0, 0])
        # tbh idk how changing this value will affect the filter
        self.kf.P = np.eye(3)

        self.predicted_p = list()
        self.predicted_v = list()
        self.predicted_a = list()

    def update(self, z):
        self.kf.predict()
        self.kf.update(z)
        self.predicted_p.append(self.kf.x[0])
        self.predicted_v.append(self.kf.x[1])
        self.predicted_a.append(self.kf.x[2])
      
    def getState(self):
        return self.kf.x
      
    def updateMeasurementErrorCovariance(self, R):
        self.kf.R = R

    def getRecordedStates(self):
        return self.predicted_p, self.predicted_v, self.predicted_a
    
    def reset(self):
        self.kf.x = np.array([0, 0, 0])
        self.kf.P = np.eye(3)
        self.predicted_p = list()
        self.predicted_v = list()
        self.predicted_a = list()
