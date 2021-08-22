'''
    API: "http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api"
    Weather: "http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/weather/ID/city"
    Cities: "http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/cities/"
'''

import requests
import statistics as stat

# Appends ID and city onto base api url
def customURL(url,ID,city):
    return url+"/weather/"+str(ID)+"/"+city


# Checks for bad field input
def suitableField(res,field,day='friday'):
    typeTest = res.json()[day][0][field] 
    if (type(typeTest) != int and type(typeTest) != float):
        #print("Error: Field is not of a suitable type")
        return False
    else:
        return True


# Returns value of a given weather attribute in city at day/ time 
def q1(url,ID,city,day,time,field):
    res = requests.get(customURL(url,ID,city))
    return(res.json()[day][time][field])


# Checks if weather attribute drops below limit for city/ day
def q2(url,ID,city,day,limit,field):
    res = requests.get(customURL(url,ID,city))

    if(not suitableField(res,field,day)): return -1
    
    for time in res.json()[day]:
        if(time[field]<limit):
           return True 
    return False


# Returns median value for weather attribute across the week for a given city
def q3(url,ID,city,field):
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    data = []
    res = requests.get(customURL(url,ID,city))

    if(not suitableField(res,field)): return -1
    
    for day in days:
        data += [time[field] for time in res.json()[day]]   
    #print(len(data)/7) # should equal 24    
    return stat.median(data)


# Return the city which has the highest wind speed value
# (Return alphabetically first city if multiple have same value)
def q4(url,ID,field):
    
    cities = requests.get(url+"/cities/").json()['cities']
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    
    if(not suitableField(requests.get(customURL(url,ID,cities[0])),field)): return -1

    # Find highest field value for each city
    maxTimes = []
    for city in cities:
        res = requests.get(customURL(url,ID,city))
        maxTimes.append(max([time[field] for day in days for time in res.json()[day]]))
    highestVal = max(maxTimes)

    cityVals = sorted(list(zip(cities,maxTimes)))

    # Returns alphabetically first city with highest value of provided field
    for pair in cityVals:
        if(pair[1] == highestVal):
            return pair[0]
        
    return -1


# TESTING
url = "http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api"
ID = 2
# Passes base test
assert q1(url,ID,'bath','wednesday',10,'temperature') == -2
# Can obtain data for different field/ city/ day
assert q1(url,ID,'cardiff','friday',0,'humidity') == 78

# Passes base tests
assert q2(url,ID,'edinburgh','friday',1000,'pressure') == False
assert q2(url,ID,'edinburgh','friday',2000,'pressure') == True
# Provides correct response for different field
assert q2(url,ID,'cardiff','monday',1,'precipitation') == True
# Provides correct response on threshold
assert q2(url,ID,'cardiff','monday',0,'precipitation') == False
# Doesn't accept fields with non-numeric values
assert q2(url,ID,'edinburgh','friday',2000,'wind_direction') == -1

q3Sol = q3(url,ID,'cardiff','temperature')
q4Sol = q4(url,ID,'wind_speed')




   
