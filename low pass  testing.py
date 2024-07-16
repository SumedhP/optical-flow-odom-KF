from csv_parser import read_data, get_data
from os import listdir
import matplotlib.pyplot as plt
from math_utils import lowPass, median, alphaBeta
import numpy as np
from tqdm import tqdm

DATA_FOLDER = "data"

dt = 0.002

# of_alpha = 0.409 # 0.3916078431372548
# of_beta = 0.026 # 0.05288235294117647

of_alpha = 0.03
of_beta = 0.001

accel_alpha = 0.01 # 0.2885744680851064

data_start = 6700
data_end = 7250

def main():
  files = listdir(DATA_FOLDER)
  print("Data files found:")
  print(files)

  for file in files:
    print("-------------------")
    print("Analyzing file: " + file)
    data = read_data(DATA_FOLDER + "/" + file)
    accel_x, accel_y, of_x, of_y, heading = get_data(data)

    # Raw data output
    pos_x = 0
    pos_y = 0
    for i in range(len(of_x)):
        pos_x += of_x[i] * dt
        pos_y += of_y[i] * dt
    magntiude = (pos_x ** 2 + pos_y ** 2) ** 0.5
    print("No filter position: " + str(pos_x) + ", " + str(pos_y) + ", " + str(magntiude))

    accel_pos_x = 0
    accel_vel_x = 0
    accel_pos_y = 0
    accel_vel_y = 0
    for i in range(len(accel_x)):
        accel_vel_x += accel_x[i] * dt
        accel_vel_y += accel_y[i] * dt
        accel_pos_x += accel_vel_x * dt
        accel_pos_y += accel_vel_y * dt
    magntiude = (accel_pos_x ** 2 + accel_pos_y ** 2) ** 0.5
    print("Accel position: " + str(accel_pos_x) + ", " + str(accel_pos_y) + ", " + str(magntiude))

    of_x, _ = alphaBeta(of_x, dt, of_alpha, of_beta)
    of_y, _ = alphaBeta(of_y, dt, of_alpha, of_beta)
    accel_x, _ = alphaBeta(accel_x, dt, accel_alpha)
    accel_y, _ = alphaBeta(accel_y, dt, accel_alpha)

    pos_x = 0
    pos_y = 0
    for i in range(len(of_x)):
        pos_x += of_x[i] * dt
        pos_y += of_y[i] * dt
    magntiude = (pos_x ** 2 + pos_y ** 2) ** 0.5
    print("Final position: " + str(pos_x) + ", " + str(pos_y) + ", " + str(magntiude))

    accel_pos_x = 0
    accel_vel_x = 0
    accel_pos_y = 0
    accel_vel_y = 0
    for i in range(len(accel_x)):
        accel_vel_x += accel_x[i] * dt
        accel_vel_y += accel_y[i] * dt
        accel_pos_x += accel_vel_x * dt
        accel_pos_y += accel_vel_y * dt
    magntiude = (accel_pos_x ** 2 + accel_pos_y ** 2) ** 0.5
    print("Final accel position: " + str(accel_pos_x) + ", " + str(accel_pos_y) + ", " + str(magntiude))

    plt.figure("Accel data for " + file)
    plt.plot(accel_x)
    plt.plot(accel_y)

  plt.show()



def fitToDataJustAlpha(data, start, end):
    val = []
    for i in range(start, end):
        val.append(data[i])

    x = np.arange(len(val))

    # fit a 10th order polynomial to the data
    z = np.polyfit(x, val, 100)
    poly_vals = np.polyval(z, x) 
    
    # # Account for some lag in the copmutation by shifting polynmial over by a bit
    # poly_vals = np.roll(poly_vals, 1)

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
    for alpha in tqdm (np.arange(0, 0.5, 0.001)):
        for beta in (np.arange(0, 0.05, 0.001)):
            v, a = alphaBeta(val, dt, alpha, beta)
            error = compareToPolynomial(v, poly_vals)
            if error < best_error:
                best_error = error
                best_alpha = alpha
                best_beta = beta
    
    return best_alpha, best_beta, best_error

def fitToDataAlphaBeta(data, start, end):
    val = np.array(data)[start:end]

    x = np.arange(len(val))

    # fit a 100th order polynomial to the data
    z = np.polyfit(x, val, 15)
    poly_vals = np.polyval(z, x)
    
    # Account for some lag in the copmutation by shifting polynmial over by a bit
    poly_vals = np.roll(poly_vals, 1)
    # plt.plot(val)
    # plt.plot(poly_vals)
    # plt.show()

    best_alpha, best_beta, best_error = findBestAlphaBeta(val, poly_vals)
    return best_alpha, best_beta, best_error


def compareToPolynomial(vals, poly):
    error = 0
    for i in range(len(vals)):
        error += (vals[i] - poly[i]) ** 2
    return error

if __name__ == "__main__":
  main()

