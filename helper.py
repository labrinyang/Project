import numpy as np
import copy
from config import *


def sample_poisson(edge_rates, walker_rate = 1):
    rates = np.append(walker_rate, edge_rates.reshape(-1))
    rate_sum = np.sum(rates)
    t = np.random.exponential(1/rate_sum)
    U = np.random.rand()

    sum = 0

    for i in range(len(rates)):
        sum += rates[i]
        if U < sum/rate_sum:
            return t, i

def sample_W(N, graphon):
    W = np.zeros((N, N))

    for i in range(N):
        for j in range(N):
            W[i, j] = graphon(i/N, j/N)

    return W

def sample_Xt(p0, W_N, T=T):
    t = 0

    global Y0, P0, N, mu1, mu0, lam1, lam0
    Y = copy.deepcopy(Y0)
    P = copy.deepcopy(P0)

    X = np.random.choice(range(N), p=p0)

    for i in range(X):
        P[X, i] = mu1

    for i in range(X+1, N):
        P[i, X] = mu1

    while True:
        dt, i = sample_poisson(P)

        if i == 0:  # Walker jump
            connected_vertices = []
            
            for j in range(N):
                if j < X and Y[X, j] == 1:
                    connected_vertices.append(j)
                elif j > X and Y[j, X] == 1:
                    connected_vertices.append(j)

            if len(connected_vertices) == 0:
                # print(f"{round(t+dt, 2)}: No edge connected to walker at {X}.")
                continue

            new_X = np.random.choice(connected_vertices, p=W_N[X, connected_vertices]/sum(W_N[X, connected_vertices]))

            # print(f"{round(t+dt, 2)}: Walker jumps from {X} to {new_X}.")
            X = new_X

        else: 
            i -= 1
            row = int(i/N)
            col = i%N
            # print(f"{round(t+dt, 2)}: Edge ({row}, {col}) switches.")

            assert col < row
            
            if Y[row, col] == 0:
                Y[row, col] = 1
                P[row, col] = mu1 if (X == row or X == col) else lam1

            else:
                Y[row, col] = 0
                P[row, col] = mu0 if (X == row or X == col) else lam0

        t += dt 

        if t > T:
            break

    return X

def solve_PDE(p0, W_N, num_timesteps=10000, T=T):
    p = p0  # Initial value
    k_N = np.sum(W_N, axis=1)/N

    dt = T/num_timesteps
    
    for _ in range(num_timesteps):
        for i in range(N):  # Calculate at t + dt
            p[i] = (1-dt)*p[i] + dt * 1/N * np.sum(W_N[:, i]/k_N * p)

    return p