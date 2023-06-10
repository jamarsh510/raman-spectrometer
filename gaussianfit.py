#this file is used to fit the curve of individual spectra

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pylab as plt
import warnings
warnings.filterwarnings('ignore')

xdata = []
ydata = []
finalxdata = []
finalydata = []

filename = input("Enter the name of the file you would like to use for data (no extension): ")
lowerbound = input("Enter your lower boundary for wavelength: ")
upperbound = input("Enter your upper boundary for wavelength: ")

def gaussianEq(x, A, B, C, D):
    y = A * np.exp(-1*B*((x - C)**2)) + D
    return y

#the file name here should be changed to match your file containing the x-data you want to analyze
f1 = open('x-axis.txt', 'r')
for x in f1:
    l = f1.readline().strip()
    xdata.append(float(l))

filename = (f"{filename}.txt")
f2 = open(filename)
for x in f2:
    l = f2.readline().strip()
    ydata.append(float(l))

array = list(zip(xdata, ydata))

for x in array:
    if x[0] < lowerbound or x[0] > upperbound:
        continue
    else:
        finalxdata.append(x[0])
        finalydata.append(x[1])
            
parameters, covariance = curve_fit(gaussianEq, finalxdata, finalydata, p0 = [7000, 0.125, 549, 1000])

fit_y = gaussianEq(finalxdata, parameters[0], parameters[1], parameters[2], parameters[3])

plt.plot(finalxdata, finalydata, 'o', label = 'data')
plt.plot(finalxdata, fit_y, '-', label = 'fit')
plt.legend()
plt.show()