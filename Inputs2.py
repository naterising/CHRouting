from Functions2 import *

# Function that allows users to hardcode locations that will be travelled to.
# Inputs: None. Hardcode data into this function
# Output: list of locations to deliver to, with START/END location as the first element
def getLocationsList():
    #initialize an empty list
    locationsList = []
    
    # add the start/stop location as the first element in the list
    # no specified delivery time, so use earliest as 0:00 and latest as 23:59
    # Use the address of Jesse Owens North as our test depot
    depot = Location("DEPOT (JON)", 2151, "Neil", "Ave","Columbus","OH",43210,dt.time(0,0),dt.time(23,59),0)
    locationsList.append(depot)
    
    # add the rest of the locations
    # if no specified delivery time, use 0:00 and 23:49 as defualt. Otherwise, 
    # fill in with customer-defined data
    loc1 = Location("E Dublin-Granville CVS", 2150, "East Dublin Granville", "Rd","Columbus","OH",43229,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc1)
    loc2 = Location("4400 Cleveland CVS", 4400, "Cleveland", "Ave","Columbus","OH",43224,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc2)
    loc3 = Location("Stelzer CVS", 2929, "Stelzer", "Rd","Columbus","OH",43219,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc3)
    loc4 = Location("2680 High CVS", 2680, "North High", "St","Columbus","OH",43202,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc4)
    loc5 = Location("759 Neil CVS", 759, "Neil", "Ave","Columbus","OH",43215,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc5)
    loc6 = Location("1634 Neil CVS", 1634, "Neil", "Ave","Columbus","OH",43201,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc6)
 
    #additional locations after initial small sample
    loc7 = Location("3424 High CVS", 3424, "South High", "Street","Columbus","OH",43207,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc7)
    
    loc8 = Location("Demorest CVS", 1159, "Demorest", "Road","Columbus","OH",43204,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc8)
    
    loc9 = Location("3355 Livingston CVS", 3355, "East Livingston", "Ave","Columbus","OH",43227,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc9)
    
    loc10 = Location("4548 Main CVS", 4548, "East Main", "Street","Columbus","OH",43213,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc10)
    
    loc11 = Location("Lockbourne CVS", 1500, "Lockbourne", "Road","Columbus","OH",43206,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc11)
    
    loc12 = Location("1515 Broad CVS", 1515, "West Broad", "Street","Columbus","OH",43222,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc12)
    
    loc13 = Location("591 Livingston CVS", 591, "East Livingston", "Ave","Columbus","OH",43215,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc13)
    
    loc14 = Location("109 High CVS", 109, "South High", "Ave","Columbus","OH",43215,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc14)
    
    loc15 = Location("Fifth Ave CVS", 1495, "West Fifth", "Ave","Columbus","OH",43212,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc15)
    
    loc16 = Location("Tremont CVS", 3282, "Tremont", "Road","Columbus","OH",43221,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc16)
    
    loc17 = Location("3100 Cleveland CVS", 3100, "Cleveland", "Ave","Columbus","OH",43224,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc17)
    
    loc18 = Location("Morse CVS", 1211, "Morse", "Road","Columbus","OH",43229,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc18)
    
    loc19 = Location("Olentangy CVS", 1717, "Olentangy River", "Road","Columbus","OH",43212,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc19)
    
    loc20 = Location("3955 Broad CVS", 3955, "East Broad", "Street","Columbus","OH",43213,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc20)
    
    loc21 = Location("Sawmill CVS", 6000, "Sawmill", "Road","Dublin","OH",43017,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc21)
    
    loc22 = Location("Park Mill Run CVS", 3883, "Park Mill Run", "Road","Hilliard","OH",43026,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc22)
    
    loc23 = Location("Clime CVS", 3499, "Clime", "Road","Columbus","OH",43223,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc23)
    
    loc24 = Location("Parsons CVS", 1400, "Parsons", "Ave","Columbus","OH",43206,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc24)
    
    
    #last round of new locations
    loc25 = Location("2160 High CVS", 2160, "North High", "Street","Columbus","OH",43201,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc25)
    
    loc26 = Location("1892 High CVS", 1892, "North High", "Street","Columbus","OH",43201,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc26)
    
    loc27 = Location("5445 High CVS", 5445, "North High", "Street","Columbus","OH",43214,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc27)
    
    loc28 = Location("2532 Main CVS", 2532, "East Main", "Street","Columbus","OH",43209,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc28)
    
    loc29 = Location("Trueman CVS", 4211, "Trueman", "Boulevard","Hilliard","OH",43026,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc29)
    
    loc30 = Location("Morse Crossing CVS", 4199, "Morse", "Crossing","Columbus","OH",43219,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc30)   
    
    loc31 = Location("Eakin CVS", 2020, "Eakin", "Road","Columbus","OH",43223,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc31) 
    
    loc32 = Location("Bethel CVS", 933, "Bethel", "Road","Columbus","OH",43214,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc32)
    
    loc33 = Location("Graceland CVS", 55, "Graceland", "Boulevard","Columbus","OH",43214,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc33)
    
    loc34 = Location("918 High CVS", 918, "High", "Street","Worthington","OH",43085,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc34)
    
    loc35 = Location("3307 Broad CVS", 3307, "East Broad", "Street","Columbus","OH",43213,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc35)
    
    loc36 = Location("4777 Sawmill CVS", 4777, "Sawmill", "Road","Columbus","OH",43220,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc36)
    
    loc37 = Location("Henderson CVS", 1885, "West Henderson", "Road","Columbus","OH",43220,dt.time(0,0),dt.time(23,59),10)
    locationsList.append(loc37)
    
    
    #return list of locaitons
    return locationsList

#Hardcode the start time by chaning the values of START_TIME_HOUR and START_TIME_MINUTES
def getStartTime():
    return dt.datetime.now()

def getOrderPriorityList():
    #orderPriority = [1,6,2,5,4] #test priority
    orderPriority = []
    return orderPriority