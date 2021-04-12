from Inputs2 import *
from Functions2 import *
import cvxpy as cp
import numpy as np
from api_distance_matrix2 import *

#Retrieve order priority from Inputs
orderPriority = getOrderPriorityList()

# define start time
START_TIME = getStartTime()

# identify parameters
locs = getLocationsList() # list of locations, with home location as first element
locsCopy = locs.copy()
#D = distMatrix(locs) # distance coefficient matrix based on list of locations
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
    
D = apiDistMatrix(locs)


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
            objectiveFunction += D[i][j]*X[i,j]
    
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
            constraints.append(S[i] + DO[i] + D[i][j] <= S[j] + M*(1-X[i,j]))
            
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

#problem.solve(solver=cp.GUROBI, verbose = True) #use true parameter for debugging
problem.solve(solver=cp.GUROBI, verbose = False)


#print statement helpful for debugging
#print("Objective Function =")
#print(objectiveFunction.value)
#print("x =")
#print(X.value)

printRouteAndSchedule(X.value, locsCopy,D,START_TIME)

##########################################################################
#now, after initial schedule, find shortest path from current node to next 
#to end node for all subsequent visits

#first, move the most recently visited location to the front of the list.
#Then, move the old start location (now at index 1/position 2) to the end
locs = locsCopy
visitOrder = visitList(X,locs)#get visit order from most recent trip
locs.insert(0,locs.pop(visitOrder[0])) #move the most recently visited location to front to be new start
locs.append(locs.pop(1))

while(len(locs)>1): 
    
    #update the number of locations and start time
    START_TIME = getStartTime()
    
    # update the earliest and latest arrival allowed lists by removing the elements
    # corresponding to the most recently visited location and then updating to 
    # reflect current list
    E.clear()
    L.clear()
    DO.clear()
    
    N = len(locs)
    
    for i in range(N):
        E.append(timeDiffInMinAsInt(locs[i].earliestDeliveryTime,START_TIME))
            
    for i in range(N):
        L.append(timeDiffInMinAsInt(locs[i].latestDeliveryTime,START_TIME))  
            
    for i in range(N):
        DO.append(locs[i].dropoffTime) 

    #get a new distance matrix with new locations order
    D = apiDistMatrix(locs)
        
   #force the route to end at the depot by making the distance from the depot 
   # to every location very large except to first location in the list. This 
   #will make an artificial last leg of the trip from the depot to the start 
   #location for this iteration, which will be ignored
    
    # Update the last row to have aritifically high distances,
    # except for the 2nd to last element in the last row which will stay 0
    i = len(D)-1
    D[i][0] = 0 #short distance from deopt to current first location
    for j in range(len(D)):
        if(j != 0):
            D[i][j] = 10000 #10000 is an artificially high number
            
    #get new parameters for TSP call
    N = len(locs)
    
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
                objectiveFunction += D[i][j]*X[i,j]
            
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
                    constraints.append(S[i] + DO[i] + D[i][j] <= S[j] + M*(1-X[i,j]))
                    
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
        
    #problem.solve(solver=cp.GUROBI, verbose = True) # use true parameter for debugging
    problem.solve(solver=cp.GUROBI, verbose = False)

    #print statements helpful for debugging   
    #print("Objective Function =")
    #print(objectiveFunction.value)
    #print("x =")
    #print(X.value)
        
    printRouteAndScheduleIterative(X.value, locs,D,START_TIME)
    
    #pare down locations list further to delete an already visited and left location
    visitOrder = visitList(X,locs)#get visit order from most recent trip
    temp = locs.pop(visitOrder[0])
    locs.insert(0,temp) #move the most recently visited location to front to be new start
    locs.pop(1) #remove the old start location (now at index 1)
    if(visitOrder[0] in orderPriority): #adjust the orderPriority list if needed
        orderPriority.remove(visitOrder[0])
        
    