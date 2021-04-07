"""
Created on Wed Apr  7 13:34:13 2021

@author: patricksmith
"""

# importing required libraries 
import requests, json 
import urllib.request
import numpy

# This function reads API key from file
def getKey ():  
  file = open('key.txt', 'r')
  key = file.read().strip()
  return key

# This function initializes the matrix
def initializeMatrix (num_locs): 
  matrix = [[0 for x in range(num_locs)] for y in range(num_locs)]
  return matrix

# This function reads the locations from a file
def getLocations():
  locations = ""
  locations_filename = open('destinations.txt', 'r')
  locations = locations_filename.read().strip()
  return locations

# This function converts locations into correct format for API call
def formatLocations(locationsList):
  n = len(locationsList)
  locations = ""
  for i in range(n):
    temp = str(locationsList[i].addressNumber)
    temp += " "
    temp += str(locationsList[i].streetName)
    temp += " "
    temp += str(locationsList[i].streetSuffix)
    temp += " "
    temp += str(locationsList[i].city) 
    temp += " "
    temp += str(locationsList[i].state)
    temp += " "
    temp += str(locationsList[i].zipCode)
    if(i != n-1):
        temp += "|"
    temp = temp.replace('\n', '|')
    temp = temp.replace('.', '')
    temp = temp.replace(',', '')
    temp = temp.replace(' ', '+')
    locations = locations + temp
  return(locations)


# This function sets all locations as both origin and destination
def setOriginDestination(locations):
  origin = locations
  destination = locations
  return (origin, destination)

# This function makes the API call and formats the results
def callAPI (origin, destination, key):
  url = ('https://maps.googleapis.com/maps/api/distancematrix/json'
       + '?language=en-US&units=imperial'
       + '&origins={}'
       + '&destinations={}'
       + '&departure_time=now'
       + '&key={}'
       ).format(origin, destination, key)

  response = urllib.request.urlopen(url)
  response_json = json.loads(response.read())
  
  return response_json

# This function creates a distance matrix using times in minutes
def makeDistMatrix(response_json, num_locs):
  matrix = initializeMatrix(num_locs)
  for i in range(num_locs):
    for j in range(num_locs):
      distance_duration = response_json['rows'][i]['elements'][j]
      matrix[i][j] = distance_duration.get("duration_in_traffic").get("value")/60
      if matrix [i][j] < 0.15:
        matrix[i][j] = 0.0
  return matrix
    
def apiDistMatrix(locs):  

  #get number of locations
  num_locs = len(locs)  
  
  #get key
  key = getKey()

  #get locations, format them, and set to origin and destination
  #locations = getLocations()
  locations = formatLocations(locs)
  origin, destination = setOriginDestination(locations)
  
  #make API call and format results
  response_json = callAPI(origin, destination, key)
  
  #create distance matrix
  distance_matrix = makeDistMatrix(response_json, num_locs)

  #return distance matrix  
  return distance_matrix

