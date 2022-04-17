import math as m
import numpy as np
import matplotlib.pyplot as plt


def logify(data):
    return [m.log(i) for i in data]

ydata = [1.0, 1.2, 1.2, 1.6, 1.2, 2.2, 2.6, 1.6, 2.2, 1.8, 3.8, 2.8, 2.2, 2.8, 4.2, 2.0, 2.6, 2.0, 1.8, 2.6, 3.2, 2.2, 4.0, 3.2, 3.4, 2.4, 5.4, 2.2, 4.2, 5.0, 4.2, 4.2, 3.6, 5.4, 4.8, 5.8, 5.6, 4.6, 6.2, 6.6, 6.8, 7.0, 3.4, 4.0, 6.2, 6.4, 7.6, 6.6, 4.6, 5.2, 8.6, 6.6, 7.2, 8.4, 7.6, 8.4, 5.0, 7.4, 7.0, 6.8, 6.2, 6.4, 11.0, 7.0, 6.8, 7.6, 3.6, 8.8, 6.4, 5.0, 8.8, 6.8, 9.4, 11.4, 4.2, 12.8, 6.6, 12.0, 8.6, 7.4, 8.4, 5.0, 8.6, 9.6, 7.4, 13.6, 5.2, 4.6, 12.2, 5.4, 8.4, 10.6, 12.2, 8.4, 6.8, 10.0, 15.4, 9.4, 6.6, 12.6, 9.8, 8.4, 6.8, 9.0, 11.8]

betterydata = [1.0, 1.4, 1.4, 1.2, 1.8, 1.2, 1.2, 1.8, 3.0, 2.0, 3.0, 3.4, 3.0, 2.6, 3.2, 2.0, 3.6, 3.6, 4.0, 2.4, 4.0, 6.0, 6.0, 3.2, 4.4, 4.0, 6.6, 5.6, 5.6, 3.4, 2.8, 3.6, 7.2, 5.4, 5.8, 4.4, 6.4, 5.0, 6.4, 4.2, 8.2, 4.8, 5.6, 4.6, 6.2, 4.2, 7.4, 5.6, 8.2, 7.2, 6.6, 5.4, 4.6, 7.6, 7.6, 8.8, 9.0, 7.4, 6.4, 11.0, 10.0, 9.6, 7.2, 6.8, 10.2, 8.6, 8.4, 7.6, 13.8, 9.2, 7.4, 8.6, 9.8, 3.2, 8.0, 11.0, 12.4, 6.6, 9.4, 8.2, 8.8, 9.2, 12.4, 12.2, 14.6, 8.8, 9.6, 6.8, 7.8, 9.6, 7.6, 14.6, 11.2, 9.8, 9.0, 10.2, 13.4, 13.2, 6.4, 10.8, 9.8, 12.6, 14.0, 9.2, 8.4]

xdata = [i for i in range(1,len(betterydata) +1)]



plt.plot(xdata,betterydata, label = "Trial Number: 200")
plt.plot(xdata,ydata, label = "Trial Number: 1s00")


b_0 = -0.4947338467209428
b_1 = 0.582393430356382
b_0 = -0.8
b_1 = 2/3

y_data_pred = [0.5 * m.pow(x,2/3) for x in xdata]


plt.plot(xdata,y_data_pred, label = "Modelled")

plt.legend()
plt.show()

ydata = logify(ydata)
xdata = logify(xdata)

def estimate_coef(x, y):
    # number of observations/points
    n = np.size(x)

    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x

    return (b_0, b_1)

def plot_regression_line(x, y, b):
    # plotting the actual points as scatter plot
    plt.plot(x, y, color = "m")

    # predicted response vector
    y_pred = b[0] + b[1]*x

    # plotting the regression line
    plt.plot(x, y_pred, color = "g")

    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')

    # function to show plot
    plt.show()

def main():
    # observations / data
    x = np.array(xdata)
    y = np.array(ydata)

    # estimating coefficients
    b = estimate_coef(x, y)
    print("Estimated coefficients:\nb_0 = {}  \
          \nb_1 = {}".format(b[0], b[1]))

    # plotting regression line
    plot_regression_line(x, y, b)
