import cvxpy as cp
import numpy as np
from Inputs2 import *
from Functions2 import *
from api_distance_matrix2 import *


# Code as Simple TSP in CVXPY 

# define start time
START_TIME = getStartTime()

# identify parameters
locs = getLocationsList() # list of locations, with home location as first element
N = len(locs) #number of locations based on list of locations
D = apiDistMatrix(locs)


# Decision Variables -- X[i,j] defines whether or not location j is travelled
# to directly from location i
X = cp.Variable((N,N), boolean = True)

# U to be used for elminiating subroutines
U = cp.Variable(N)

# Objectve Function
objectiveFunction = 0
for i in range(N): 
    for j in range(N):
            objectiveFunction += D[i][j]*X[i,j]

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
#problem.solve(solver=cp.GUROBI, verbose = False)


print("Objective Function =")
print(objectiveFunction.value)
print("x =")
print(X.value)
print("u = ")
print(U.value)

printRouteAndSchedule(X.value, getLocationsList(),D,START_TIME)

