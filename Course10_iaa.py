# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 22:11:05 2025

@author: iabio

"""
# =============================================================================
# 
# 
# !pip install requests
# !pip install pandas
# !pip install numpy
# =============================================================================

# Requests allows us to make HTTP requests which we will use to get data from an API
import requests
# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Datetime is a library that allows us to represent dates
import datetime

# Setting this option will print all collumns of a dataframe
pd.set_option('display.max_columns', None)
# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth', None)



# Takes the dataset and uses the rocket column to call the API and append the data to the list
def getBoosterVersion(data):
    for x in data['rocket']:
       if x:
        response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
        BoosterVersion.append(response['name'])
        
        
        
# Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(data):
    for x in data['launchpad']:
       if x:
         response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
         Longitude.append(response['longitude'])
         Latitude.append(response['latitude'])
         LaunchSite.append(response['name'])
         
# Takes the dataset and uses the payloads column to call the API and append the data to the lists
def getPayloadData(data):
    for load in data['payloads']:
       if load:
        response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])         
        
        
        
        
# Takes the dataset and uses the cores column to call the API and append the data to the lists
def getCoreData(data):
    for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])        
        
        
        


spacex_url="https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)
print(response.content)

xd = pd.json_normalize(response.json())
xd.head(n=5)








static_json_url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
response_static = requests.get(static_json_url)
print(response_static.content)
response_static.status_code





xf = pd.json_normalize(response_static.json())


data = xf.copy()


# Lets take a subset of our dataframe keeping only the features we want and the flight number, and date_utc.
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
data = data[data['cores'].map(len)==1]
data = data[data['payloads'].map(len)==1]

# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
data['cores'] = data['cores'].map(lambda x : x[0])
data['payloads'] = data['payloads'].map(lambda x : x[0])

# We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Using the date we will restrict the dates of the launches
data = data[data['date'] <= datetime.date(2020, 11, 13)]






#Global variables 
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []


# Call getBoosterVersion
getBoosterVersion(data)
print(BoosterVersion[0:5])




getLaunchSite(data)
print(LaunchSite[0:5])


# Call getPayloadData
getPayloadData(data)
print(PayloadMass[0:5])

# Call getCoreData
getCoreData(data)





launch_dict = {'FlightNumber': list(data['flight_number']),
                'Date': list(data['date']),
                'BoosterVersion':BoosterVersion,
                'PayloadMass':PayloadMass,
                'Orbit':Orbit,
                'LaunchSite':LaunchSite,
                'Outcome':Outcome,
                'Flights':Flights,
                'GridFins':GridFins,
                'Reused':Reused,
                'Legs':Legs,
                'LandingPad':LandingPad,
                'Block':Block,
                'ReusedCount':ReusedCount,
                'Serial':Serial,
                'Longitude': Longitude,
                'Latitude': Latitude
                }
                


launch_df = pd.DataFrame(launch_dict)   





#launch_df.describe(include='all')     
launch_df.describe()     

# Hint data['BoosterVersion']!='Falcon 1'

data_Falcon9= launch_df[launch_df['BoosterVersion']!='Falcon 1']
data_Falcon9



data_Falcon9.isnull().sum()




# Calculate the mean value of PayloadMass column
PayloadMass_mean = data_Falcon9['PayloadMass'].mean()


# Replace the np.nan values with its mean value
data_Falcon9['PayloadMass'].replace(np.nan, PayloadMass_mean, inplace=True)


data_Falcon9.to_csv('dataset_part_1.csv', index=False)




















