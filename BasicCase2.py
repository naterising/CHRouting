# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 15:07:05 2021

@author: nater
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 20:48:22 2021

@author: nater
"""
import cvxpy as cp
import numpy as np
from Inputs import *
from Functions import *

# Code as Simple TSP in CVXPY 

# define start time
START_TIME = getStartTime()

# identify parameters
locs = getLocationsList() # list of locations, with home location as first element
D = distMatrix(locs) # distance coefficient matrix based on list of locations
N = len(locs) #number of locations based on list of locations



# Decision Variables -- X[i,j] defines whether or not location j is travelled
# to directly from location i
X = cp.Variable((N,N), boolean = True)

# U to be used for elminiating subroutines
U = cp.Variable(N)

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
    
#ensure that the first U is equal to 1
constraints.append(U[0] == 1)
    
#ensure all other U's are greater than 1 (the value of U[0])  
for k in range(1,N):
    constraints.append(U[k] >= 2)
    
# set up sub-loop elimination constraint
for i in range(1,N):
    for j in range(1,N):
            constraints.append(U[i] - U[j] + N*X[i,j] <= N - 1)
        
        
# Solve
problem = cp.Problem(cp.Minimize(objectiveFunction), constraints)

problem.solve(solver=cp.GUROBI, verbose = True)

print("Objective Function =")
print(objectiveFunction.value)
print("x =")
print(X.value)
print("u = ")
print(U.value)

printRouteAndSchedule(X.value, locs,D,START_TIME)

