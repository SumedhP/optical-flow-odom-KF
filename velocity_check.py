from csv_parser import read_data, get_data
from os import listdir
import matplotlib.pyplot as plt

DATA_FOLDER = "data"

DATA_START = 0
DATA_END = 1000


# Make something to plot raw data
# make something that computes average of velocity data from certain begin and end points

def main():
  files = listdir(DATA_FOLDER)
  print("Data files found:")
  print(files)

  for file in files:
    print("-------------------")
    print("Analyzing file: " + file)
    data = read_data(DATA_FOLDER + "/" + file)
    accel_x, accel_y, of_x, of_y, heading = get_data(data)
    plot_data(of_x, of_y)

def plot_data(vx, vy):
  plt.figure("Velocity")
  plt.plot(vx)
  plt.plot(vy)
  plt.legend(["X", "Y"])
  plt.show()


