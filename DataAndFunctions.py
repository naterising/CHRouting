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
import datetime as dt

# Define Location object
class Location:
    def __init__(self, compName, addressNumber,streetName, streetSuffix, city, state, zipCode, earliestDeliveryTime, latestDeliveryTime,dropoffTime):
        self.compName = compName
        self.addressNumber = addressNumber
        self.streetName = streetName        
        self.streetSuffix = streetSuffix
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.earliestDeliveryTime = earliestDeliveryTime
        self.latestDeliveryTime = latestDeliveryTime
        self.dropoffTime = dropoffTime
        
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
    
    # add the start/stop location as the first element in the list
    # no specified delivery time, so use earliest as 0:00 and latest as 23:59
    home = Location("Cardinal Health", 2151, "Neil", "Ave","Columbus","OH",43210,dt.time(0,0),dt.time(23,59),0)
    locationsList.append(home)
    
    # add the rest of the locations
    # if no specified delivery time, use 0:00 and 23:49 as defualt. Otherwise, 
    # fill in with customer-defined data
    loc1 = Location("AAAAA", 330, "Huntington Park", "Ln","Columbus","OH",43215,dt.time(0,0),dt.time(23,59),5)
    locationsList.append(loc1)
    loc2 = Location("BBBBB", 337, "Annie & John Glenn", "Ave","Columbus","OH",43210,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc2)
    loc3 = Location("CCCCC", 1739, "High", "Street","Columbus","OH",43210,dt.time(0,0),dt.time(23,59),15)
    locationsList.append(loc3)
 
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

# function to print results of solving a route ptimization model
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
    
# function to print results and estimeated delivery times for a solved route
# optimization model
# inputs: solved Xij matrix, list of locations used for problem, distance matrix
#         used for problem
# output: print trip order and time for each leg to console
# note: assume delivery strts t 8:00 am
def printRouteAndSchedule(X, listOfLocations, distMX, startTime):
    n = len(listOfLocations)
    i = 0
    time = startTime
    print("Delivery Start: ", time)
    for k in range(n): #repeat for every trip
        j = 0
        while(X[i,j] != 1):
            j+=1
        print("Leg ",k+1,": ")
        print("\t",listOfLocations[i].compName, " --> ", listOfLocations[j].compName, "(",distMX[i,j],"min )")
        time = incTime(time,distMX[i,j]) #increment time due to travel
        print("\t Expected Arrival: ",time)
        if(k!=n-1):
            time = incTime(time,listOfLocations[j].dropoffTime) # increment time to reflect 
            print("\t Dropoff: ", listOfLocations[j].dropoffTime," min")
            print("\t Expected Departure: ", time)
        i = j
    
# function to return a datetime object with today's date and a specified hour/min start
# inputs: hour to start deliveries, minute to start deliveries
# output: datetime object with today's date and delivery start time as specified by inputs
def startTime(h,m):
    return dt.datetime(dt.datetime.today().year, dt.datetime.today().month,day = dt.datetime.today().day,hour=h,minute=m)
     
# function to increment a datetime object by a certain number of minutes
# inputs: number of minutes to increment datetime object
# outputs: updated datetime object (by value NOT reference)
def incTime(time, mins):
    return (time + dt.timedelta(minutes=mins))
