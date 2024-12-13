import numpy as np
import multiprocessing
import time
import matplotlib.pyplot as plt
from collections import Counter

from scipy.stats import ecdf
from helper import *


# def continuous_W(x, y):
#     return (x**2 + y**2)/2

def continuous_W(x, y):
    if (x-1/4)*(y-1/4)>0:
        return 5
    return 1

p0 = np.random.uniform(size=N)
p0 = p0/np.sum(p0)
W_N = sample_W(N, continuous_W)

def my_func(i):
    print(f"==== Start run {i} ====")
    Xt = sample_Xt(p0, W_N)
    print(f"====  End run {i}  ====")
    return Xt/N

if __name__ == '__main__':
    # multiprocessing pool object
    pool = multiprocessing.Pool()

    num_trials = 500  # 10*N
    inputs = range(num_trials)

    now = time.time()

    Xts = pool.map(my_func, inputs)
    print(f"Time used: {time.time() - now}")

    ecdf_data = ecdf(Xts)
    F_hat = ecdf_data.cdf
    
    p = solve_PDE(p0, W_N)
    F = np.cumsum(p)

    # print(F_hat.quantiles) 
    sum = 0
    for i, q in enumerate(F_hat.quantiles):
        x = int(N*q)
        sum += (F[x] - F_hat.probabilities[i])**2

    print(f"MSE: {sum/N}")

    alpha = 0.05
    eps = np.sqrt(np.log(2/alpha)/(2*num_trials))
    F_hat.plot(label="EDF")
    plt.step(F_hat.quantiles, F_hat.probabilities - eps, label='Lower Bound')
    plt.step(F_hat.quantiles, F_hat.probabilities + eps, label='Upper Bound')

    plt.plot([x/N for x in range(N)], F, label="CDF")
    plt.xlabel('Position')
    _ = plt.xticks([x/N for x in range(0, N, 10)])
    _ = plt.yticks(np.arange(0, 1.1, 0.1))
    plt.ylabel('Frequency')
    plt.legend()

    # plt.savefig("low-ind-block") 
    # plt.savefig("high-ind-block")  
    # plt.savefig("low-dep-block")
    plt.savefig("high-dep-block")

    plt.show()

    