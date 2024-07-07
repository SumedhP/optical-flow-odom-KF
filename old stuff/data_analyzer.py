# files = ['accelOFData_run2.csv', 'accelOFData_run3.csv', 'oldAccelBetterOFMountdata_run1.csv', 'oldAccelBEtterOFMountdata_run1.csv'
#          'oldAccelBEtterOFMountdataFlashlight.csv']
# indicies = [2,3,5,6,10,11]


# Uncomment the following lines and comment out the above lines
# Then go and uncomment the very bottom line with the plt.show() to see the plots
# Look at the X-axis to see the difference
#########################################

files = ['accelOFData_run2.csv', 'accelOFData_run3.csv', 'oldAccelBetterOFMountdata_run1.csv',
         'oldAccelBEtterOFMountdataFlashlight.csv']
indicies = [2]

#########################################

import csv
import statistics
import matplotlib.pyplot as plt


index_values = {2: 'Ax', 3: 'Ay', 5: 'Raw OF x', 6: 'Raw OF y', 10: 'OF x m/s', 11: 'OF y m/s'}
distance = 4
OF_quality = 9
pos_x = 7
pos_y = 8

for file in files:
  file_values = open("OF_data/" + file, 'r')
  reader = csv.reader(file_values)
  data = list(reader)

  print("Opened file:" + file)

  # Go through certain indexes and find their mean and std deviation
  for index in indicies:
    values = list()
    for i in range(1, len(data)):
      values.append(float(data[i][index]))
    stdev = statistics.stdev(values)
    mean = statistics.mean(values)
    plot = plt.figure(file + " " + index_values[index])
    plt.hist(values, bins=50, edgecolor='black')
    # plt.plot(values)
    print(index_values[index] + " has mean: " + str(mean) + " and std deviation: " + str(stdev))
  
  # Find average of distance and optical flow quality
  distance_values = list()
  OF_quality_values = list()
  for i in range(1, len(data)):
    distance_values.append(float(data[i][distance]))
    OF_quality_values.append(float(data[i][OF_quality]))
  distance_mean = statistics.mean(distance_values)
  quality_mean = statistics.mean(OF_quality_values)
  print("Average distance: " + str(distance_mean))
  print("Average OF quality: " + str(quality_mean))

  # Position over time graphs
  pos_x_values = list()
  pos_y_values = list()
  for i in range(1, len(data)):
    pos_x_values.append(float(data[i][pos_x]))
    pos_y_values.append(float(data[i][pos_y]))
  
  # x = plt.figure(file + " X Position over time")
  # plt.plot(pos_x_values)
  # y = plt.figure(file + " Y Position over time")
  # plt.plot(pos_y_values) 

  print("")

# VVVVVVVVVVVVVV
plt.show()
#^^^^^^^^ UNCOMMENT THIS LINE TO SEE THE PLOTS ^^^^^^^
