# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:57:50 2021

@author: nater
"""

from Functions import *

# Function that allows users to hardcode locations that will be travelled to.
# Inputs: None. Hardcode data into this function
# Output: list of locations to deliver to, with START/END location as the first element
def getLocationsList():
    #initialize an empty list
    locationsList = []
    
    # add the start/stop location as the first element in the list
    # no specified delivery time, so use earliest as 0:00 and latest as 23:59
    home = Location("Jesse Owens North", 2151, "Neil", "Ave","Columbus","OH",43210,dt.time(0,0),dt.time(23,59),0)
    locationsList.append(home)
    
    # add the rest of the locations
    # if no specified delivery time, use 0:00 and 23:49 as defualt. Otherwise, 
    # fill in with customer-defined data
    loc1 = Location("E Dublin-Granville CVS", 2150, "East Dublin Granville", "Rd","Columbus","OH",43229,dt.time(0,0),dt.time(23,59),15)
    locationsList.append(loc1)
    loc2 = Location("Cleveland CVS", 4400, "Cleveland", "Ave","Columbus","OH",43224,dt.time(0,0),dt.time(23,59),15)
    locationsList.append(loc2)
    loc3 = Location("Stelzer CVS", 2929, "Stelzer", "Rd","Columbus","OH",43219,dt.time(0,0),dt.time(23,59),15)
    locationsList.append(loc3)
    loc4 = Location("High Street CVS", 2680, "North High", "St","Columbus","OH",43202,dt.time(0,0),dt.time(23,59),15)
    locationsList.append(loc4)
    loc5 = Location("759 Neil CVS", 759, "Neil", "Ave","Columbus","OH",43215,dt.time(0,0),dt.time(23,59),15)
    locationsList.append(loc5)
    loc6 = Location("1634 Neil CVS", 1634, "Neil", "Ave","Columbus","OH",43201,dt.time(0,0),dt.time(23,59),15)
    locationsList.append(loc6)
 
    #return list of locaitons
    return locationsList

#Hardcode the start time by chaning the values of START_TIME_HOUR and START_TIME_MINUTES
def getStartTime():
    #START_TIME_HOUR = 8
    #START_TIME_MINUTES = 30
    #return dt.datetime(dt.datetime.today().year,month = dt.datetime.today().month,day = dt.datetime.today().day,hour = START_TIME_HOUR,minute = START_TIME_MINUTES)

    return dt.datetime.now()

def getOrderPriorityList():
    #orderPriority = [1,6,2,5,4] #test priority
    orderPriority = []
    return orderPriority