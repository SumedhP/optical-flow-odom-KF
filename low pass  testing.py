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

alpha = 0.409
beta = 0.026

data_start = 1829
# data_end = 3000
data_end = data_start + 200
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

    val = []
    for i in range(data_start, data_end):
        val.append(accel_y[i])

    x = np.arange(len(val))

    # fit a 10th order polynomial to the data
    z = np.polyfit(x, val, 100)
    print(z)
    poly_vals = np.polyval(z, x) 
    
    # Account for some lag in the copmutation by shifting polynmial over by a bit
    poly_vals = np.roll(poly_vals, 1)

    plt.figure("Raw data OF Y but alpha beta")
    plt.plot(val)
    plt.plot(poly_vals)
    v,a = alphaBeta(val, dt, 0.3, 0.01)
    plt.plot(v)
    plt.legend(["Raw", "Poly", "Mine"])
    plt.show()




    # Brute force a bunch of alpha beta values to see which has least error to the polynomial values
    best_alpha = 0
    best_beta = 0
    best_error = 1000000000000000
    for alpha in tqdm (np.arange(0, 1, 0.001)):
        for beta in np.arange(0.001, 1, 0.001):
            v, a = alphaBeta(val, dt, alpha, beta)
            error = compareToPolynomial(v, poly_vals)
            if error < best_error:
                best_error = error
                best_alpha = alpha
                best_beta = beta
    
    print("Best alpha: " + str(best_alpha))
    print("Best beta: " + str(best_beta))
    print("Best error: " + str(best_error))

    v, a = alphaBeta(val, dt, best_alpha, best_beta)
    plt.figure("Raw data OF Y but alpha beta")
    plt.plot(val)
    plt.plot(v)
    v,a = alphaBeta(val, dt, 0.3, 0.005)
    plt.plot(v)
    plt.plot(poly_vals)
    plt.legend(["Raw", "Found", "Mine" ,"Poly"])
    plt.show()


def compareToPolynomial(vals, poly):
    error = 0
    for i in range(len(vals)):
        error += (vals[i] - poly[i]) ** 2
    return error

if __name__ == "__main__":
  main()

