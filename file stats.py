from os import listdir
from csv_parser import read_data, get_data
import statistics
import matplotlib.pyplot as plt

DATA_FOLDER = "data"

def main():
  files = listdir(DATA_FOLDER)
  print("Data files found:")
  print(files)

  for file in files:
    print("-------------------")
    print("Analyzing file: " + file)
    data = read_data(DATA_FOLDER + "/" + file)
    accel_x, accel_y, of_x, of_y, heading = get_data(data)

    print("Accelerometer X")
    print("Mean: " + str(statistics.mean(accel_x)))
    print("Standard deviation: " + str(statistics.stdev(accel_x)))
    plt.figure("Accel X")
    plt.plot(accel_x)

    print("Accelerometer Y")
    print("Mean: " + str(statistics.mean(accel_y)))
    print("Standard deviation: " + str(statistics.stdev(accel_y)))
    plt.figure("Accel Y")
    plt.plot(accel_y)

    print("Optical flow X")
    print("Mean: " + str(statistics.mean(of_x)))
    print("Standard deviation: " + str(statistics.stdev(of_x)))
    plt.figure("OF X")
    plt.plot(of_x)

    print("Optical flow Y")
    print("Mean: " + str(statistics.mean(of_y)))
    print("Standard deviation: " + str(statistics.stdev(of_y)))
    plt.figure("OF Y")
    plt.plot(of_y)
    plt.show()

    pos_x = 0
    pos_y = 0
    for i in range(len(of_x)):
        pos_x += of_x[i] * 0.01
        pos_y += of_y[i] * 0.01
    print("No filter position: " + str(pos_x) + ", " + str(pos_y))
    


if __name__ == "__main__":
  main()
