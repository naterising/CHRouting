# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 16:12:37 2021

@author: nater
"""

# import packages

import numpy as np
from math import radians, cos, sin, asin, sqrt
import cvxpy as cp
import math

# Define Location object
class Location:
    def __init__(self, compName, addressNumber,streetName, streetSuffix, city, state, zipCode):
        self.compName = compName
        self.addressNumber = addressNumber
        self.streetName = streetName        
        self.streetSuffix = streetSuffix
        self.city = city
        self.state = state
        self.zipCode = zipCode
        
    #define repr for debugging purposes
    def __repr__(self):
        return self.compName

    #basic print method for this class for testing and output
    def printLocation(self):
        print("Company Name: ", self.compName)
        print("Address Number: ", self.addressNumber)
        print("Street Name: ", self.streetName)
        print("Street Suffix: ", self.streetSuffix)
        print("City: ", self.city)
        print("State: ", self.state)
        print("Zip: ", self.zipCode)

# Function that allows users to hardcode locations that will be travelled to.
# Inputs: None. Hardcode data into this function
# Output: list of locations to deliver to, with START/END location as the first element
def locationsList():
    #initialize an empty list
    locationsList = []
    
    #add the start/stop location as the first element in the list
    home = Location("Cardinal Health", 2151, "Neil", "Ave","Columbus","OH",43210)
    locationsList.append(home)
    
    #add the rest of the locations
    loc1 = Location("Clipper's Stadium", 330, "Huntington Park", "Ln","Columbus","OH",43215)
    locationsList.append(loc1)
    loc2 = Location("RPAC", 337, "Annie & John Glenn", "Ave","Columbus","OH",43210)
    locationsList.append(loc2)
    loc3 = Location("Ohio Union", 1739, "High", "Street","Columbus","OH",43210)
    locationsList.append(loc3)
    loc4 = Location("Ohio Capitol", 1, "Capitol", "Square","Columbus","OH",43215)
    locationsList.append(loc4)
    loc5 = Location("MAPFRE Stadium", 10, "Black and Gold", "Blvd","Columbus","OH",43211)
    locationsList.append(loc5)
    
    #return list of locaitons
    return locationsList


# Distance Method between two Location objects
# Inputs: 2 Location objects
# Output: Distance, in minutes, between these 2 objects
#THIS IS WHAT WE NEED TO FIGURE OUT WITH GOOGLE API
#FIND THE DISTANCE BETWEEN TWO LOCATION OBJECTS IN MINUTES
def distanceAB(locationA,locationB):
    #random distance for now
    return (locationA.addressNumber+locationB.addressNumber) % 97


# Construct Distance Matrix
# input: list of locations used un the problem (1st element start/end location)
# output: pairwise matrix of distances (in minutes) between each location
def distMatrix(locationsList):
    numLocations = len(locationsList)
    dMx = np.ndarray(shape=(numLocations,numLocations))
    for i in range(numLocations):
        for j in range(numLocations):
            if i==j:
                dMx[i,j] = 0
            else:
                dMx[i,j] = distanceAB(locationsList[i], locationsList[j])
    
    return dMx

# function to print results of solving an optimization model
# inputs: solved Xij matrix, list of locations used for problem, distance matrix
#         used for problem
# output: print trip order and time for each leg to console
def printRoute(X, listOfLocations,distMX):
    n = len(listOfLocations)
    i = 0
    for k in range(n): #repeat for every trip
        j = 0
        while(X[i,j] != 1):
            j+=1
        print(listOfLocations[i].compName, " --> ", listOfLocations[j].compName, "(",distMX[i,j],"min )")
        i = j
    





