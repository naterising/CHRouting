# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 16:29:20 2021

@author: nater
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 15:44:21 2021

@author: nater
"""

#Patrick's Code:
# importing required libraries 
import requests, json 
import urllib.request
from Functions import *
from Inputs import *

def distUsingAPI(loc1,loc2):
    # enter your api key here 
    #file = open('key.txt', 'r')
    #key = file.read().strip()
    key = 'AIzaSyCyT9_RPfcizA4GtPtwcoUvwqZP-JTOGCs'
    
    # Take origin as input and remove periods and commas and replace with +
    origin = loc1.compName+"+"+str(loc1.addressNumber)+"+"+loc1.streetName+"+"+loc1.streetSuffix+"+"+loc1.city+"+"+loc1.state+"+"+str(loc1.zipCode)
    origin = origin.replace('.', '')
    origin = origin.replace(',', '')
    origin = origin.replace(' ', '+')
    print(origin)
    
    # Take destination as input 
    destination = loc2.compName+"+"+str(loc2.addressNumber)+"+"+loc2.streetName+"+"+loc2.streetSuffix+"+"+loc2.city+"+"+loc2.state+"+"+str(loc2.zipCode)
    destination = destination.replace('.', '')
    destination = destination.replace(',', '')
    destination = destination.replace(' ', '+')
    print(destination)
      
    # Get method of requests module 
    # return response object 
    # could also download google maps library and use distance_matrix function 
    
    url = ('https://maps.googleapis.com/maps/api/distancematrix/json'
           + '?language=en-US&units=imperial'
           + '&origins={}'
           + '&destinations={}'
           + '&departure_time=now'
           + '&key={}'
           ).format(origin, destination, key)
    
    # json method of response object 
    # return json format result 
    response = urllib.request.urlopen(url)
    response_json = json.loads(response.read())
    print(response_json)
    distance_duration = response_json['rows'][0]['elements'][0]
    
    ## print the value of response_json 
    ## use "text" for value as a string, use value for time in seconds
    duration = distance_duration.get("duration_in_traffic").get("value")
    duration /=60
    return duration
    




