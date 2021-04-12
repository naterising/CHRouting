# importing required libraries 
import requests, json 
import urllib.request
import numpy
from Inputs2 import *
from Functions2 import *

def getKey ():  
  return 'AIzaSyCyT9_RPfcizA4GtPtwcoUvwqZP-JTOGCs'

# This function initializes the matrix (all zeros)
def initializeMatrix (I,J): 
  matrix = [[0 for y in range(J)] for x in range(I)]
  return matrix


# This function converts locations into correct format for API call
def formatLocations(locationsList):
  n = len(locationsList)
  locations = ""
  for i in range(n):
    temp = locationsList[i].compName
    temp += " "
    temp += str(locationsList[i].addressNumber)
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
def makeDistMatrix(response_json, I,J):
  matrix = initializeMatrix(I,J)
  for i in range(I):
    for j in range(J):
      distance_duration = response_json['rows'][i]['elements'][j]
      matrix[i][j] = distance_duration.get("duration_in_traffic").get("value")/60
  return matrix

    
def apiDistMatrix(locs):  
  #if more than 10 locations, repeated api calls will have to be made since
  # 10x10 is max allowed return matrix size
  n = math.ceil(len(locs)/10) #number of submatrices will be n^2
  
  #get key
  key = getKey()
  
  #split the list into sublists no greater than 10 elements
  #the length of sLocs will be n
  locsCopy = locs.copy()
  sLocs = splitList(locsCopy,10)
  
  distMatrixRows = [] #fill in matrix rows for every i for-loop iteration, to be concatenated later   
  for i in range(n):
      for j in range(n):
          origins = formatLocations(sLocs[i])
          destinations = formatLocations(sLocs[j])
  
          #make API call and format results
          response_json = callAPI(origins, destinations, key)
          if(j==0):
              tempRow = makeDistMatrix(response_json, len(sLocs[i]),len(sLocs[j]))
              tempRow = listMatrixToNumpyMatrix(tempRow)
              distMatrixRows.append(tempRow)
          else:
              tempRow2 = makeDistMatrix(response_json, len(sLocs[i]),len(sLocs[j])) 
              tempRow2 = listMatrixToNumpyMatrix(tempRow2)
              tempRow = distMatrixRows[i]
              tempRow = np.concatenate((tempRow, tempRow2), axis = 1)
              distMatrixRows[i] = tempRow
              
  distance_matrix = distMatrixRows.pop(0)
  for i in range(len(distMatrixRows)):
     distance_matrix = np.concatenate((distance_matrix, distMatrixRows[i]), axis = 0)
  
  #ensure diagonal elements are 0
  I,J = distance_matrix.shape
  for i in range(I):
      for j in range(J):
          if i == j:
                distance_matrix[i,j] = 0.0 #distance from a location to itself is always 0  
    
  #return distance matrix  
  return numpyMatrixToListMatrix(distance_matrix)

def splitList(l,n):
    l #make a copy of the locations list to avoid reference issues
    l2 = []
    while(len(l) > 0):
        tempElement = []
        for i in range(n):
            if(len(l) > 0):
                tempElement.append(l.pop(0))
        l2.append(tempElement)
    return l2

# convert a list matrix to a numpy matrix
def listMatrixToNumpyMatrix(m):
    rows = len(m)
    columns = len(m[0])
    m2 = np.empty([rows,columns])
    for i in range(rows):
        for j in range(columns):
            m2[i,j] = m[i][j]
    return m2

# convert a numpy matrix to a list matrix   
def numpyMatrixToListMatrix(m):
    rows = m.shape[0]
    columns = m.shape[1]
    m2 = [ [ 0 for j in range(columns) ] for i in range(rows) ]
    
    for i in range(rows):
        for j in range(columns):
            m2[i][j] = m[i,j]
    return m2

               
