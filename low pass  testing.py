from csv_parser import read_data, get_data
from os import listdir
import matplotlib.pyplot as plt
from math_utils import lowPass, median, alphaBeta
import numpy as np
from tqdm import tqdm

DATA_FOLDER = "data"

vel_x = 0
vel_y = 0

dt = 0.01

low_pass = 0.1

of_alpha = 0.409
of_beta = 0.026

accel_alpha = 0.28

# data_start = 1829
# data_end = data_start + 200
data_start = 1829 - 100
data_end = data_start + 100


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

    alphas = []

    print(len(accel_y))

    # look through 100 data point windows and fit to it
    for i in tqdm(range(0, len(accel_y) - 100, 100)):
        a, e = fitToData(accel_y, i, i + 100)
        # print("Best alpha for accel_x: " + str(a))
        # print("Best error for accel_x: " + str(e))
        if a != 0:
           alphas.append(a)
    
    print("Average alpha for accel_x: " + str(np.mean(alphas)))
    plt.plot(alphas)
    plt.show()
    


    # val = []
    # for i in range(data_start, data_end):
    #     val.append(accel_y[i])

    # x = np.arange(len(val))

    # # fit a 10th order polynomial to the data
    # z = np.polyfit(x, val, 100)
    # print(z)
    # poly_vals = np.polyval(z, x) 
    
    # # Account for some lag in the copmutation by shifting polynmial over by a bit
    # poly_vals = np.roll(poly_vals, 1)

    # plt.figure("Raw data OF Y but alpha beta")
    # plt.plot(val)
    # plt.plot(poly_vals)
    # v,a = alphaBeta(val, dt, 0.3, 0.01)
    # plt.plot(v)
    # plt.legend(["Raw", "Poly", "Mine"])
    # plt.show()

    # best_alpha, best_error = findBestAlpha(val, poly_vals)
    # best_beta = 0
    
    # print("Best alpha: " + str(best_alpha))
    # print("Best beta: " + str(best_beta))
    # print("Best error: " + str(best_error))

    # v, a = alphaBeta(val, dt, best_alpha, best_beta)
    # plt.figure("Raw data OF Y but alpha beta")
    # plt.plot(val)
    # plt.plot(v)
    # v,a = alphaBeta(val, dt, 0.3, 0.005)
    # plt.plot(v)
    # plt.plot(poly_vals)
    # plt.legend(["Raw", "Found", "Mine" ,"Poly"])
    # plt.show()

def fitToData(data, start, end):
    val = []
    for i in range(start, end):
        val.append(data[i])

    x = np.arange(len(val))

    # fit a 10th order polynomial to the data
    z = np.polyfit(x, val, 100)
    poly_vals = np.polyval(z, x) 
    
    # Account for some lag in the copmutation by shifting polynmial over by a bit
    poly_vals = np.roll(poly_vals, 1)

    best_alpha, best_error = findBestAlpha(val, poly_vals)
    return best_alpha, best_error

def findBestAlpha(val, poly_vals):
    best_alpha = 0
    best_error = compareToPolynomial(val, poly_vals)
    for alpha in (np.arange(0, 0.5, 0.0001)):
      v, a = alphaBeta(val, dt, alpha, 0)
      error = compareToPolynomial(v, poly_vals)
      if error < best_error:
          best_error = error
          best_alpha = alpha
    
    return best_alpha, best_error


def compareToPolynomial(vals, poly):
    error = 0
    for i in range(len(vals)):
        error += (vals[i] - poly[i]) ** 2
    return error

if __name__ == "__main__":
  main()

