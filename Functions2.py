# import packages
import numpy as np
import cvxpy as cp
import math
import datetime as dt
from api_distance_matrix import *

# Define Location object: each object has attributes for address, as well as time
# attributes regarding earliest possible dropoff time, latest possible dropoff time
# and the time each delivery is expected to take once the driver has arrived at
# the delivery site
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
    
# function to print results and estimeated delivery times for a solved route
# optimization model
# inputs: -solved X[i,j] matrix (from solver) that shows whether or not location
#         j is traveled to from location i
#         -list of locations used for problem formulation
#         -distance matrix (time in mins from location i to location
#         j) used in problem formulation as determined by Google API call
#          -start time
# output: print trip order and time for each leg to console
# note: assume delivery strts t 8:00 am
def printRouteAndSchedule(X, listOfLocations, distMX, startTime):
    #loop over the deliveries based on the results of X and print the routes   
    n = len(listOfLocations)
    i = 0
    print("Delivery Start: "+simpleTimeString(startTime))
    time = startTime # variable to store total expected delivery times
    for k in range(n): 
        j = 0
        while(X[i,j] != 1):
            j+=1
        print("Leg ",k+1,": ")
        print("\t",listOfLocations[i].compName, " --> ", listOfLocations[j].compName, "(",int(distMX[i][j]),"min )")
        time = incTime(time,distMX[i][j]) #increment time due to travel
        print("\t Expected Arrival: ",simpleTimeString(time))
        if(k!=n-1):
            time = incTime(time,listOfLocations[j].dropoffTime) # increment time to reflect 
            print("\t Dropoff: ", listOfLocations[j].dropoffTime," min")
            print("\t Expected Departure: ", simpleTimeString(time))
        i = j
        
        
# exact same function as printRouteAndSchedule, except ingnoring the final leg
# since in the iterative case this is a "dummy" trip enforced to reuse the TSP
# code instead of implementing a shortest path algorithm
def printRouteAndScheduleIterative(X, listOfLocations, distMX, startTime):   
    n = len(listOfLocations)
    i = 0
    print("Delivery Start: "+simpleTimeString(startTime))
    time = startTime 
    for k in range(n-1):  # n-1 not n to skip last leg
        j = 0
        while(X[i,j] != 1):
            j+=1
        print("Leg ",k+1,": ")
        print("\t",listOfLocations[i].compName, " --> ", listOfLocations[j].compName, "(",int(distMX[i][j]),"min )")
        time = incTime(time,distMX[i][j]) #increment time due to travel
        print("\t Expected Arrival: ",simpleTimeString(time))
        if(k!=n-1):
            time = incTime(time,listOfLocations[j].dropoffTime) # increment time to reflect 
            print("\t Dropoff: ", listOfLocations[j].dropoffTime," min")
            print("\t Expected Departure: ", simpleTimeString(time))
        i = j
        
        
#inputs: -t, a date time variable
#output: -string in HH:MM AM/PM format
def simpleTimeString(t):
    #determine the hour and minute and AM/PM of the start time for cleaner 
    #printing to the console. The dt object is on military time, so if the hour
    #is over 12, subtract 12
    am_pm = "AM"
    hour = t.hour
    if(hour >=12 and hour <24): am_pm = "PM"
    if(hour>12): hour = hour - 12
    if(hour == 0): hour = 12
    mins = t.minute
    minsStr = str(mins)
    if(mins <=9): minsStr = "0"+minsStr
    return str(hour)+":"+minsStr+" "+am_pm


#input: result matrix from CVXPY optimization, list of location objects used in formulation
#output: list for which the value of element i is the index in the locations 
#        list (input parameter) of the place visited ith (i.e 1st, 2nd, ..., last)
def visitList(X, locs):
    n = len(locs)
    visitOrder = [0]*n
    row = 0
    for k in range(n):
        column = 0
        while(X.value[row,column] == 0):
            column+=1
        visitOrder[k] = column
        row = column
    return visitOrder

     
# function to increment a datetime object by a certain number of minutes
# inputs: number of minutes to increment datetime object
# outputs: updated datetime object (by value NOT reference)
def incTime(time, mins):
    return (time + dt.timedelta(minutes=mins))


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
