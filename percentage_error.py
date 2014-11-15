#computes percentage error

import numpy as np

def compute_percentage_error(x, y):

    e = 0
    diff = [abs(x[i] - y[i]) for i in range(len(x))]

    for i in range (0, len(diff)):
        e += diff[i]

    e = ((e * 100)/ 255)
    return e
	
#Testing purposes
if __name__ == '__main__':
    avg = np.array([0, 50, 100, 250])
    x = np.array([0, 70, 30, 120])
    y = np.array([10, 40, 110, 200])
    print(compute_percentage_error(avg, y))    

