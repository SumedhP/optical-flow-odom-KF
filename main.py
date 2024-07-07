from filter import KalmanFilterWrapper
from csv_parser import read_data, get_data
from os import listdir
import matplotlib.pyplot as plt
from tqdm import tqdm


DATA_FOLDER = "data"

def main():
    print("Starting")
    files = listdir(DATA_FOLDER)
    print("Data files found:")
    print(files)
    print("-------------------\n")

    for file in files:
        print("Analyzing file: " + file)
        data = read_data(DATA_FOLDER + "/" + file)
        accel_x, accel_y, of_x, of_y, heading = get_data(data)
        x_kf = KalmanFilterWrapper()
        y_kf = KalmanFilterWrapper()
        for i in tqdm (range(len(of_x)), desc="Processing data", unit="Data points"):
              x_kf.update([of_x[i], accel_x[i]])
              y_kf.update([of_y[i], accel_y[i]])
        
        print("\nFinal state")
        print(x_kf.getState())
        print(y_kf.getState())

        p_x, v_x, a_x = x_kf.getRecordedStates()
        p_y, v_y, a_y = y_kf.getRecordedStates()
        makePlots(p_x, p_y, v_x, v_y, a_x, a_y)

def makePlots(p_x, p_y, v_x, v_y, a_x, a_y):
    plt.figure("Position estimate")
    plt.plot(p_x)
    plt.plot(p_y)

    plt.figure("Velocity estimate")
    plt.plot(v_x)
    plt.plot(v_y)

    plt.figure("Acceleration estimate")
    plt.plot(a_x)
    plt.plot(a_y)

    plt.show()

if __name__ == "__main__":
    main()
