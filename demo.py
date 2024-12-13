import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy


def sample_poisson(edge_rates, walker_rate = 1):
    rates = np.append(edge_rates.reshape(-1), walker_rate)
    rate_sum = sum(rates)
    t = np.random.exponential(1/rate_sum)
    U = np.random.rand()

    for i in range(len(rates)):
        if U < np.cumsum(rates)[i]/rate_sum:
            return t, i
    
    return t, i+1

# CONSTANTS
N = 5

lam0 = 1
lam1 = 1
mu0 = 2
mu1 = 2

W = np.zeros((N, N))
for i in range(N):
    for j in range(i):
        W[i, j] = 1
        W[j, i] = 1

# INITIALIZE
Y = np.zeros((N, N))
X = 0

for i in range(N):
    for j in range(i):
        Y[i, j] = 1

P = np.zeros((N, N))

for i in range(N):
    for j in range(i):
        P[i, j] = mu1 if (X == i or X == j) else lam1

t = 0
T = 5
states = [copy.deepcopy((X, Y, t, 0))]

while True:
    dt, i = sample_poisson(P)

    if i == N**2:  # Walker jump
        connected_vertices = []
        
        for j in range(N):
            if j < X and Y[X, j] == 1:
                connected_vertices.append(j)
            elif j > X and Y[j, X] == 1:
                connected_vertices.append(j)

        if len(connected_vertices) == 0:
            print(f"No edge connected to walker at {X}.")
            print(Y)
            continue

        new_X = np.random.choice(connected_vertices, p=W[X, connected_vertices]/sum(W[X, connected_vertices]))

        print(f"Walker jumps from {X} to {new_X}.")
        X = new_X

    else: 
        row = int(i/N)
        col = i%N
        print(f"Edge ({row}, {col}) switches.")

        assert col < row
        
        if Y[row, col] == 0:
            Y[row, col] = 1
            P[row, col] = mu1 if (X == row or X == col) else lam1

        else:
            Y[row, col] = 0
            P[row, col] = mu0 if (X == row or X == col) else lam0

    t += dt 

    states.append(copy.deepcopy((X, Y, t, dt)))

    if t > T:
        break

# REGULAR POLYGON COORDINATES
import shapely.geometry as sg
import math

def regular_polygon_coordinates(n, center_x, center_y, radius):
    polygon = sg.Polygon([(center_x + radius * math.cos(2 * math.pi * i / n),
                            center_y + radius * math.sin(2 * math.pi * i / n))
                           for i in range(n)])
    return [(x, y) for x, y in polygon.exterior.coords]

n = N  # number of sides
center_x = 0
center_y = 0
radius = 10
coords = regular_polygon_coordinates(n, center_x, center_y, radius)
x = [coord[0] for coord in coords]
y = [coord[1] for coord in coords]

# PLOT

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time


def plot_graph(ax, state):
    ax.clear()
    X, Y, t = state[0], state[1], state[2]
    time.sleep(state[3])

    for i in range(N):
        for j in range(i):
            if Y[i,j] == 1:
                ax.plot([x[i], x[j]], [y[i], y[j]], '-ok', mfc = 'C1', mec='C1')
    ax.plot(x[X], y[X], 'o', ms=10)
    ax.plot(x[X], y[X], 'ro', ms=20)
    
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_title(f"Time {round(t, 2)}")

fig, ax = plt.subplots()


def update_plot(frame):
    plot_graph(ax, states[frame])

ani = animation.FuncAnimation(fig, update_plot, frames=len(states), interval=1)

plt.show()
