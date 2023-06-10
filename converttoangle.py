#this is a helper file used to convert raman shift to angle of crystal orientation, no changes needed by user

import numpy as np
import math
from scipy.optimize import curve_fit
import matplotlib.pylab as plt
import warnings
warnings.filterwarnings('ignore')

xdata = [0, 5, 15, 25, 35, 45, 55, 65, 75, 85, 90]
ydata = [570, 571, 574, 580, 589, 602, 610, 617, 622, 626, 626]

def sigEq(x, A, B, C, D):
    y = A + (B / (1 + np.exp(-1*C*(x - D))))
    return y

parameters2, covariance = curve_fit(sigEq, xdata, ydata, p0 = [570, 56, 0.1, 45], maxfev = 100000)

def convertEq(y, A = parameters2[0], B = parameters2[1], C = parameters2[2], D = parameters2[3]):
    x = (np.log((B / (y - A)) - 1) / (-1 * C)) + D
    return x


fit_y = sigEq(xdata, parameters2[0], parameters2[1], parameters2[2], parameters2[3])
print(parameters2)