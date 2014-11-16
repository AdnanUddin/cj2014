#computes percentage error

import numpy as np


def compute_percentage_error(x, y):

    e = 0
    diff = [abs(x[i] - y[i]) for i in range(len(x))]

    for i in range (0, len(diff)):
        e += diff[i]

    e = ((e * 100)/ 255)
    print(e)
    return e

def compute_error_matrix(x, M):

    M_transpose = np.transpose(M)
    vector = [0]*len(x)
    for i in range (len(M)):
        for j in range (0, len(x)):
            vector[j] = M_transpose[j][i]
        compute_percentage_error(x, vector)    
    

#Testing purposes
if __name__ == '__main__':
    M = ([100, 2, 3],[0, 60, 25], [50, 140, 60])
    avg = np.array([0, 50, 100, 250])
    x = np.array([0, 70, 30])
    y = np.array([10, 40, 110, 200])
    #compute_percentage_error(avg, x)
    compute_error_matrix(x, M)
