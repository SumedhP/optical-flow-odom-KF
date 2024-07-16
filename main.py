from filter import KalmanFilterWrapper
from csv_parser import read_data, get_data
from math_utils import rotateVector, alphaBeta, lowPass
from os import listdir
import matplotlib.pyplot as plt
from tqdm import tqdm


DATA_FOLDER = "data"

of_alpha = 0.03
of_beta = 0.001

accel_alpha = 0.01
dt = 0.01

def main():
    files = listdir(DATA_FOLDER)
    print("Data files found:")
    print(files)

    for file in files:
        print("-------------------")
        print("Analyzing file: " + file)
        data = read_data(DATA_FOLDER + "/" + file)
        accel_x, accel_y, of_x, of_y, heading = get_data(data)
        
        # of_scalar = 10
        # for i in range(len(of_x)):
        #     of_x[i] *= of_scalar
        #     of_y[i] *= of_scalar

        # of_x, _ = alphaBeta(of_x, dt, of_alpha, of_beta)
        # of_y, _ = alphaBeta(of_y, dt, of_alpha, of_beta)
        # accel_x, _ = alphaBeta(accel_x, dt, accel_alpha)
        # accel_y, _ = alphaBeta(accel_y, dt, accel_alpha)
        
        x_kf = KalmanFilterWrapper(dt)
        y_kf = KalmanFilterWrapper(dt)
        for i in tqdm (range(len(of_x)), desc="Processing data", unit="Data points"):
              of_x[i], of_y[i] = rotateVector(of_x[i], of_y[i], 0) # Replace with heading[i]
              accel_x[i], accel_y[i] = rotateVector(accel_x[i], accel_y[i], 0)
              x_kf.update([of_x[i], accel_x[i]])
              y_kf.update([of_y[i], accel_y[i]])
        
        print("\nFinal state")
        print("X: " + str(x_kf.getState()))
        print("Y: " + str(y_kf.getState()))
        magntiude = (x_kf.getState()[0] ** 2 + y_kf.getState()[0] ** 2) ** 0.5
        print("Magnitude: " + str(magntiude))

        p_x, v_x, a_x = x_kf.getRecordedStates()
        p_y, v_y, a_y = y_kf.getRecordedStates()
        # makePlots(p_x, p_y, v_x, v_y, a_x, a_y)

def makePlots(p_x, p_y, v_x, v_y, a_x, a_y):
    plt.figure("Position estimate")
    plt.plot(p_x)
    plt.plot(p_y)
    plt.legend(["X", "Y"])

    plt.figure("Velocity estimate")
    plt.plot(v_x)
    plt.plot(v_y)
    plt.legend(["X", "Y"])

    plt.figure("Acceleration estimate")
    plt.plot(a_x)
    plt.plot(a_y)
    plt.legend(["X", "Y"])

    plt.show()

if __name__ == "__main__":
    main()
