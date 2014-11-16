#computes euclidean distance between two vectors

import numpy as np
import math

def compute_euclidean_distance(x, y):
    length = 0;
    for k in range (len(x)):
        length = length + math.sqrt(math.pow((x[k] - y[k]), 2))
    print(length)
    return length



def compute_error_matrix(x, M):

    M_transpose = np.transpose(M)
    vector = [0]*len(x)
    for i in range (len(M)):
        for j in range (len(x)):
            vector[j] = M_transpose[j][i]
        compute_euclidean_distance(x, vector)    
    

#Testing purposes
#if __name__ == '__main__':
    #M = ([100, 2, 3, 1],[0, 60, 25, 1], [50, 140, 60, 1])
    #avg = np.array([0, 50, 100, 250])
    #x = np.array([0, 50, 100, 250])
    #y = np.array([10, 40, 110, 200])
    #compute_euclidean_distance(avg, x)
    #compute_error_matrix(x, M)
