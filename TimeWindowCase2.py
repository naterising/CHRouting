# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 15:09:02 2021

@author: nater
"""

from Inputs import *
from Functions import *
import cvxpy as cp
import numpy as np


# define start time
START_TIME = getStartTime()

# identify parameters
locs = getLocationsList() # list of locations, with home location as first element
D = distMatrix(locs) # distance coefficient matrix based on list of locations
N = len(locs) #number of locations based on list of locations

# build list of earliest arrival times possible (minutes form earliest arrval time)
E = []
for i in range(N):
    E.append(timeDiffInMinAsInt(locs[i].earliestDeliveryTime,START_TIME))
    
# build list of latest arrival times possible (minutes form earliest arrval time)
L = []
for i in range(N):
    L.append(timeDiffInMinAsInt(locs[i].latestDeliveryTime,START_TIME))  
    
# build list of droppoff times for each location 
DO = []
for i in range(N):
    DO.append(locs[i].dropoffTime) 

# CVXPY Formulation: 
    
# Decision Variables -- X[i,j] defines whether or not location j is travelled
# to directly from location i
X = cp.Variable((N,N), boolean = True)

# U to be used for elminiating subroutines
U = cp.Variable(N)

# S[i] is the time of arrival at location i
S = cp.Variable(N, nonneg=True)


# define objective function
# Objectve Function
objectiveFunction = 0
for i in range(N): 
    for j in range(N):
            objectiveFunction += D[i,j]*X[i,j]
    
# initialize list of constraints
constraints = []

#only arrive at each location once
for i in range(N):
    constraints.append(cp.sum(X[i,:]) == 1) 

#only depart from each location once
for j in range(N):
    constraints.append(cp.sum(X[:,j]) == 1) 
    
# Set up time window constraints
M = 1000000 #large number for constraint relaxation
for i in range(N):
    for j in range(1,N):
        if(i!=j):
            constraints.append(S[i] + DO[i] + D[i,j] <= S[j] + M*(1-X[i,j]))
            
for i in range(1,N):
    constraints.append(E[i] <= S[i])
    constraints.append(S[i] <= L[i])
    
constraints.append(S[0] == 0) 

# Keep subtour elimination constraints from simple TSP:
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


printRouteAndSchedule(X.value, locs,D,START_TIME)

