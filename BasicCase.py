# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 20:48:22 2021

@author: nater
"""
import cvxpy as cp
from DataAndFunctions import *
# Code as Simple TSP in CVXPY 

# identify parameters
locs = locationsList() # list of locations, with home location as first element
D = distMatrix(locs) # distance coefficient matrix based on list of locations
N = len(locs) #number of locations based on list of locations


# Decision Variables -- X[i,j] defines whether or not location j is travelled
# to directly from location i
X = cp.Variable((N,N), boolean = True)

# T to be used for elminiating subroutines
T = cp.Variable(N, integer = True)

# THIS IS POTENTIALLY CLEANER CODE...HAVEN'T VALIDATED IT YET
#Objective Function
#obj_func = cp.sum(D @ X)


# Objectve Function
objectiveFunction = 0
for i in range(N): 
    for j in range(N):
            objectiveFunction += D[i,j]*X[i,j]

# Constraints
constraints = []

#only arrive at each location once
for i in range(N):
    constraints.append(cp.sum(X[i,:]) == 1) 

#only depart from each location once
for j in range(N):
    constraints.append(cp.sum(X[:,j]) == 1) 
    
# eliminate subtours
    
#ensure that the first T is equal to 1
constraints.append(T[0] == 1)
    
#ensure all other T's are greater than or equal to 0    
for k in range(1,N):
    constraints.append(T[k] >= 2)
    
# set up sub-loop elimination constraint
for i in range(1,N):
    for j in range(1,N):
            constraints.append(T[i] - T[j] + N*X[i,j] <= N - 1)
        
        
# Solve
problem = cp.Problem(cp.Minimize(objectiveFunction), constraints)

problem.solve(solver=cp.GUROBI, verbose = True)

print("Objective Function =")
print(objectiveFunction.value)
print("x =")
print(X.value)
print("t = ")
print(T.value)

printRoute(X.value, locs,D)
