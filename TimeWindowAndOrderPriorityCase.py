# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 19:41:57 2021

@author: nater
"""

from DataAndFunctions import *
import cvxpy as cp
import numpy as np

#Determine manual Order priority:
# Visit first index first index second, and so on
# 2 represents the location @ index 2 of the locaitons list built from data I/O
##############################HARDCODED FOR NOW...WE NEED DATA I/O FOR THIS####
#orderPriority = [2,3,1] #Test example
orderPriority = []

# time --> integer conversion
# Inputs: time (as dt.time()), start time (as dt.datetime())
# Output: integer representing the number of minutes from the start time
def timeDiffInMinAsInt(time, startTime):
    startTimeMin = startTime.hour*60 + startTime.minute
    timeMin = time.hour*60 + time.minute
    if(timeMin < startTimeMin):
        return 0
    else:
        return timeMin - startTimeMin

# define start time
START_TIME_HOUR = 8
START_TIME_MINUTES = 30
START_TIME = dt.datetime(dt.datetime.today().year,month = dt.datetime.today().month,day = dt.datetime.today().day,hour = START_TIME_HOUR,minute = START_TIME_MINUTES)

# identify parameters
locs = locationsList() # list of locations, with home location as first element
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

# implement manual order priority constraints
for i in range(len(orderPriority)):
    if(i == 0):
        constraints.append(X[0,orderPriority[i]] == 1)
    else:
        constraints.append(X[orderPriority[i-1],orderPriority[i]] == 1)

# Solve
problem = cp.Problem(cp.Minimize(objectiveFunction), constraints)

problem.solve(solver=cp.GUROBI, verbose = True)

print("Objective Function =")
print(objectiveFunction.value)
print("x =")
print(X.value)
print("t = ")
print(T.value)

printRouteAndSchedule(X.value, locs,D,START_TIME)


