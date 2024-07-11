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

of_alpha = 0.409 # 0.3916078431372548
of_beta = 0.026 # 0.05288235294117647

accel_alpha = 0.236 # 0.2885744680851064

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
    # for i in tqdm(range(0, len(accel_y) - 100, 100)):
    #     a, e = fitToDataJustAlpha(accel_y, i, i + 100)
    #     # print("Best alpha for accel_x: " + str(a))
    #     # print("Best error for accel_x: " + str(e))
    #     if a != 0:
    #        alphas.append(a)
    
    # print("Average alpha for accel_x: " + str(np.mean(alphas)))
    # plt.plot(alphas)
    # plt.show()

    alphas = []
    betas = []
    # look through 100 data point windows and fit to it
    delta = 100
    for i in tqdm(range(1800, len(of_y) - delta, int(delta/2))):
        a, b, e = fitToDataAlphaBeta(of_y, i, i + delta)
        # plt.plot(of_y[i:i+delta])
        # theirVal, _ = alphaBeta(of_y[i:i+delta], dt, a, b)
        # myVal, _ = alphaBeta(of_y[i:i+delta], dt, of_alpha, of_beta)
        # plt.plot(myVal)
        # plt.plot(theirVal)
        # plt.legend(["Raw", "mine", "Found"])
        # plt.show()
        # print("Best alpha for accel_x: " + str(a))
        # print("Best error for accel_x: " + str(e))
        if a != 0 and b != 0:
           alphas.append(a)
           betas.append(b)
    
    print("Average alpha for of_y: " + str(np.mean(alphas)))
    print("Average beta for of_y: " + str(np.mean(betas)))
    plt.plot(alphas)
    plt.plot(betas)
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

def fitToDataJustAlpha(data, start, end):
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
    for alpha in (np.arange(0, 0.5, 0.001)):
      v, a = alphaBeta(val, dt, alpha, 0)
      error = compareToPolynomial(v, poly_vals)
      if error < best_error:
          best_error = error
          best_alpha = alpha
    
    return best_alpha, best_error

def findBestAlphaBeta(val, poly_vals):
    best_alpha = 0
    best_beta = 0
    best_error = compareToPolynomial(val, poly_vals)
    for alpha in (np.arange(0, 0.5, 0.001)):
        for beta in (np.arange(0, 0.1, 0.001)):
            v, a = alphaBeta(val, dt, alpha, beta)
            error = compareToPolynomial(v, poly_vals)
            if error < best_error:
                best_error = error
                best_alpha = alpha
                best_beta = beta
    
    return best_alpha, best_beta, best_error

def fitToDataAlphaBeta(data, start, end):
    val = []
    for i in range(start, end):
        val.append(data[i])

    x = np.arange(len(val))

    # fit a 100th order polynomial to the data
    z = np.polyfit(x, val, 100)
    poly_vals = np.polyval(z, x) 
    
    # Account for some lag in the copmutation by shifting polynmial over by a bit
    poly_vals = np.roll(poly_vals, 1)

    best_alpha, best_beta, best_error = findBestAlphaBeta(val, poly_vals)
    return best_alpha, best_beta, best_error


def compareToPolynomial(vals, poly):
    error = 0
    for i in range(len(vals)):
        error += (vals[i] - poly[i]) ** 2
    return error

if __name__ == "__main__":
  main()

