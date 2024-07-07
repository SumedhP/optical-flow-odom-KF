import csv

# Assume csv is in following format: Index, time, Ax, Ay, OF x, OF y, heading

def read_data(file_name):
    file_values = open(file_name, 'r')
    reader = csv.reader(file_values)
    data = list(reader)
    return data

def get_data(data):
    accel_x = list()
    accel_y = list()
    of_x = list()
    of_y = list()
    heading = list()
    for i in range(1, len(data)):
        accel_x.append(float(data[i][2]))
        accel_y.append(float(data[i][3]))
        of_x.append(float(data[i][4]))
        of_y.append(float(data[i][5]))
        heading.append(float(data[i][6]))
    return accel_x, accel_y, of_x, of_y, heading
