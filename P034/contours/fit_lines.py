import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def func_square(x, a, b, c):
    return a * (np.array(x) ** 2) + b * np.array(x) + c


def func_line(x, a, b):
    return a * np.array(x) + b


def fit_func_line(xdata, ydata):
    popt, pcov = curve_fit(func_line, np.array(xdata), np.array(ydata))
    return popt


def fit_func_square(xdata, ydata):
    # plt.plot(xdata, ydata, 'b-', label='data')

    popt, pcov = curve_fit(func_square, np.array(xdata), np.array(ydata))
    return popt
    # plt.plot(xdata, func_square(xdata, *popt), 'r-', label='fit: a=%5.3f, b=%5.3f c=%5.3f' % tuple(popt))
    #
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.legend()
    # plt.show()

