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
def initializeMatrix (): 
  n=4
  matrix = [[0 for x in range(n)] for y in range(n)]
  return matrix

# This function reads the locations from a file
def getLocations():
  locations = ""
  locations_filename = open('destinations.txt', 'r')
  locations = locations_filename.read().strip()
  return locations

# This function converts locations into correct format for API call
def formatLocations(locations):
  locations = locations.replace('\n', '|')
  locations = locations.replace('.', '')
  locations = locations.replace(',', '')
  locations = locations.replace(' ', '+')
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
def makeDistMatrix(response_json):
  matrix = initializeMatrix()
  for i in range(4):
    for j in range(4):
      distance_duration = response_json['rows'][i]['elements'][j]
      matrix[i][j] = distance_duration.get("duration_in_traffic").get("value")/60
      if matrix [i][j] < 0.15:
        matrix[i][j] = 0.0
  return matrix
    
def apiDistMatrix():  
  #get key
  key = getKey()

  #get locations, format them, and set to origin and destination
  locations = getLocations()
  locations = formatLocations(locations)
  origin, destination = setOriginDestination(locations)

  #make API call and format results
  response_json = callAPI(origin, destination, key)

  #create distance matrix
  distance_matrix = makeDistMatrix(response_json)

  #return distance matrix  
  return distance_matrix
