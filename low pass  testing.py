from csv_parser import read_data, get_data
from os import listdir
import matplotlib.pyplot as plt
from math_utils import lowPass, median
import numpy as np
import statistics
DATA_FOLDER = "data"

vel_x = 0
vel_y = 0

dt = 0.01

low_pass = 0.1

def main():
  files = listdir(DATA_FOLDER)
  print("Data files found:")
  print(files)

  for file in files:
    print("-------------------")
    print("Analyzing file: " + file)
    data = read_data(DATA_FOLDER + "/" + file)
    accel_x, accel_y, of_x, of_y, heading = get_data(data)

    of_scalar = 10
    for i in range(len(of_x)):
        of_x[i] *= of_scalar
        of_y[i] *= of_scalar

    for i in np.arange(0.95, 1.0, 0.01):
      low_pass = i
      print("Low pass: " + str(low_pass))
      plt.figure("Low pass of " + str(low_pass))
      plt.plot(accel_y)
      low_x = lowPass(accel_y, low_pass)
      plt.plot(low_x)
      plt.legend(["Raw", "Low pass"])
    plt.show()


if __name__ == "__main__":
  main()

