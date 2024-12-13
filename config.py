import numpy as np


N = 50  # There're 1225 edges
T = 50  # Walker jumps T times on average 

# # Low frequency, independent evolving
# lam1 = 0.05 
# lam0 = 2*lam1 
# mu1 = lam1 
# mu0 = lam0 

# # High frequency, independent evolving
# lam1 = 0.5 
# lam0 = 2*lam1
# mu1 = lam1 
# mu0 = lam0 

# # Low frequency, dependent evolving
# lam1 = 0.05 
# lam0 = 2*lam1
# mu1 = 5*lam1 
# mu0 = 5*lam0 

# High frequency, dependent evolving
lam1 = 0.5 
lam0 = 2*lam1
mu1 = 5*lam1 
mu0 = 5*lam0 

Y0 = np.zeros((N, N))

for i in range(N):
    for j in range(i):
        Y0[i, j] = 1

P0 = np.zeros((N, N))

for i in range(N):
    for j in range(i):
        P0[i, j] = lam1