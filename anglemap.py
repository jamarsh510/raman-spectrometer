import numpy as np
from scipy.optimize import curve_fit
import seaborn as sns
import matplotlib.pylab as plt
import warnings
from converttoangle import convertEq

warnings.filterwarnings('ignore')

#Set the dimensions of the scan here
dimx = 75
dimy = 32

#Choice 1 means spectra data that only has intensities, i.e. 1 column.  Choice means spectra data that has two columns, wavelength and intensity
choice = 0

method = 0
xdata = []
ydata = []

def linearEq(x, A, B):
    y = A + B*x
    return y

def gaussianEq(x, A, B, C, D):
    y = A * np.exp(-1*B*((x - C)**2)) + D
    return y

userinput = input("Choose the method used for data storage (1 or 2): ")
if userinput == '1':
    method = 'spec'
    choice = 1
if userinput == '2':
    method = 'data'
    choice = 2

if choice == 1:
    f1 = open('x-axis.txt', 'r')
    for x in f1:
        l = f1.readline().strip()
        xdata.append(float(l))

if choice == 2:
    array = np.loadtxt("data_1_1.txt")
    xdata = array[:,0]

print(f"Wavelength Minimum: {xdata[0]}")
print(f"Wavelength Maximum: {xdata[-1]}")

lowerbound = float(input("Enter a lower boundary: "))
upperbound = float(input("Enter an upper boundary: "))
a = float(input("Enter a guess for A: "))
b = float(input("Enter a guess for B: "))
c = float(input("Enter a guess for C: "))
d = float(input("Enter a guess for D: "))

arr = [[0 for x in range(dimy)] for y in range(dimx)]
arr2 = [[0 for x in range(dimy)] for y in range(dimx)]

for i in range(0, dimx):
    for j in range(0, dimy):
        ydata = []
        finalarray = []
        xdatafinal = []
        ydatafinal = []
        if choice == 1:
            filename = (f"{method}_{i}_{j}.txt")
            f2 = open(filename)
            for x in f2:
                l = f2.readline().strip()
                ydata.append(float(l))
            
            array = list(zip(xdata, ydata))
        

        if choice == 2:
            filename = (f"{method}_{i + 1}_{j + 1}.txt")
            array = np.loadtxt(filename)
            xdata = array[:,0]
            ydata = array[:,1]

        for x in array:
            if x[0] < lowerbound or x[0] > upperbound:
                continue
            else:
                xdatafinal.append(x[0])
                ydatafinal.append(x[1])
                finalarray.append(x)

        parameters, covariance = curve_fit(gaussianEq, xdatafinal, ydatafinal, p0 = [a, b, c, d], maxfev = 100000)
        arr[i][j] = parameters[2]

for i in range(0, dimx):
    for j in range(0, dimy):
        shift = 10**7 * ((1 / 531.45) - (1 / arr[i][j]))
        
        angle = convertEq(shift)
        arr2[i][j] = angle

ax = sns.heatmap(arr2, linewidth=0)
plt.show()