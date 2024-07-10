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

    for i in np.arange(0.95, 1.0, 0.02):
      low_pass = i
      print("Low pass: " + str(low_pass))
      plt.plot(accel_y)
      med_y = median(accel_y, 9)
      plt.plot(med_y)
      low_pass_y = lowPass(med_y, low_pass)
      plt.plot(low_pass_y)
      plt.legend(["Raw", "Median", "Median + Low pass"])
      plt.show()
      plt.clf()
      
if __name__ == "__main__":
  main()

