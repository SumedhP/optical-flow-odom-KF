from filterpy.kalman import KalmanFilter
import numpy as np
import csv
import scipy
import matplotlib.pyplot as plt

# Create a Kalman Filter
kf = KalmanFilter(dim_x=3, dim_z=2)

dt = 0.01 # time delta between measurements

# Define the state transition matrix
kf.F = np.array([[1, dt, 0.5*dt**2],
                 [0, 1, dt],
                 [0, 0, 1]])

# Define the measurement function
kf.H = np.array([[0, 1, 0],
                 [0, 0, 1]])

# Define the measurement noise covariance matrix
of_std = 0.009877928685029257
accel_std = 0.022141264441937807
kf.R = np.array([[of_std**2, 0],
                 [0, accel_std**2]])

# Define the process noise covariance matrix
# 1,1 should 1e-8, 2,2 1e-6, 3,3 1e-4
kf.Q = np.array([[1e-8, 0, 0],
                  [0, 1e-6, 0],
                  [0, 0, 1e-4]])

# Define the initial state
kf.x = np.array([0, 0, 0])

# Define the initial state covariance
kf.P = np.eye(3) * 0.0000001

# ok start importing data
file_values = open("OF_data/oldAccelBetterOFMountdataFlashlight.csv", 'r')
reader = csv.reader(file_values)
data = list(reader)

# OF x is 10, accel x is 2
of_x = list()
accel_x = list()
for i in range(1, len(data)):
  of_x.append(float(data[i][10]))
  accel_x.append(float(data[i][2]))

print("Last line of data values")
print(of_x[-1])
print(accel_x[-1])

# plot the accel values
plt.figure("Accel values")
plt.plot(accel_x, color='blue')
# now median filter the accel values
accel_x = scipy.signal.medfilt(accel_x, kernel_size=5)
plt.plot(accel_x, color='red')
plt.legend(['Raw accel', 'Filtered accel'])
plt.show()



print("Made kalman filter")

# Now we can start the Kalman filter
pred_x = list()
pred_v = list()
pred_a = list()
for i in range(len(of_x)):
  kf.predict()
  kf.update([of_x[i], accel_x[i]])
  pred_x.append(kf.x[0])
  pred_v.append(kf.x[1])
  pred_a.append(kf.x[2])

# print final state
print(kf.x)


# Plot the results

# Plot the input data
# plt.plot(of_x, label='OF x')
# plt.plot(accel_x, label='Accel x')

plt.figure(1)
plt.plot(pred_x, label='Predicted x')
plt.figure(2)
plt.plot(pred_v, label='Predicted v')
plt.figure(3)
plt.plot(pred_a, label='Predicted a')
lg = plt.legend()
for line in lg.get_lines():
    line.set_linewidth(0.1)
# plt.show()
