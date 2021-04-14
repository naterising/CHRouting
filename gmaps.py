# ordered dropoffs according to our optimized route
order_list = visitList(X, locs)

# create map visual
# create a list of coordinates to pass to gmaps
coord_list = []

key = getKey()

address = ''

# call geocode api to create convert addresses to coordinates
for i in range(N):
    order = order_list[i]
    address = str(locs[order].addressNumber)
    address += " "
    address += str(locs[order].streetName)
    address += " "
    address += str(locs[order].streetSuffix)
    address += " "
    address += str(locs[order].city) 
    address += " "
    address += str(locs[order].state)
    address += " "
    address += str(locs[order].zipCode)
    
    params = {
        'key': key,
        'address': address
    }
    
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(base_url, params=params).json()
    response.keys()
    
    if response['status'] == 'OK':
        geometry = response['results'][0]['geometry']
        lat = geometry['location']['lat']
        lon = geometry['location']['lng']
        
    coord_list.append((lat,lon))
    coord_list

# gmaps call
now = datetime.now()

#set start and end to JON
start = coord_list[len(coord_list)-1]
end = coord_list[len(coord_list)-1]

# set waypoints to all other locations
waypoints = coord_list[0:len(coord_list)-1]

gmaps.configure(api_key=key)
#create the map
fig = gmaps.figure()
#create the layer
#layer = gmaps.directions.Directions(start, end, waypoints = waypoints, optimize_waypoints=True,
#                                   mode='car',api_key=key,departure_time = now)

layer = gmaps.directions_layer(start, end, waypoints = waypoints)

#Add the layers
fig.add_layer(layer)
#Add traffic layer
fig.add_layer(gmaps.traffic_layer())
fig
