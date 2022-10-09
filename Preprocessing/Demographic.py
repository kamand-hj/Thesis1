#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import synapseclient
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from missingpy import MissForest
import datetime
#from datetime import datetime, date
from datetime import timedelta
syn = synapseclient.Synapse()

syn.login('Kamand', 'Kamand13579-')

####preprocessing tables
###data entry
query = syn.tableQuery("SELECT * FROM syn16782063")
demographic = query.asDataFrame()
###drop non useful rows
demographic=demographic.drop(labels=['recordId','appVersion','phoneInfo','createdOn',
                                              ], axis=1)
demographic.reset_index(inplace=True)

demographic['patientWakeUpTime'] = pd.to_datetime(demographic['patientWakeUpTime'],format= '%H:%M' ).dt.time
demographic['patientGoSleepTime'] = pd.to_datetime(demographic['patientGoSleepTime'],format= '%H:%M' ).dt.time
demographic['patientWeightPounds'] = demographic['patientWeightPounds']*0.45359237
demographic['patientHeightInches'] = demographic['patientHeightInches']*2.54

demographic = demographic.dropna(axis=0, thresh=2,subset=['patientWeightPounds', 'patientBiologicalSex', 'patientHeightInches','patientWakeUpTime','patientCurrentAge','patientGoSleepTime'] ).reset_index(drop = True)
df2 = demographic[demographic.duplicated('healthCode', keep = False)].groupby('healthCode')['index'].apply(list).reset_index()

###dropping duplicates
for i in range(len(df2)):
    filtered_df = demographic.loc[demographic['healthCode'] == df2['healthCode'][i]]
    filtered_df = filtered_df.reset_index(drop = True)
    #filtered_df.drop(labels=['index'], axis=1)
    hour_wake = 0
    mins_wake = 0
    hour_sleep = 0
    mins_sleep = 0
    for j in range(len(filtered_df['patientWakeUpTime'])):
        if pd.isnull(filtered_df['patientWakeUpTime'][j]):
            j = j+1
        else:
            hour_wake = (hour_wake + filtered_df['patientWakeUpTime'][j].hour)
            mins_wake = mins_wake + filtered_df['patientWakeUpTime'][j].minute
            
    if mins_wake>=60:
        hour_wake = (hour_wake+ (mins_wake//60))
        mins_wake = (mins_wake%60) 
    hour_wake= hour_wake/(len(filtered_df['patientWakeUpTime']))
    mins_wake = (mins_wake/(len(filtered_df['patientWakeUpTime']))) + ((hour_wake%1)*60)
    if   mins_wake >= 60: 
             hour_wake = int(hour_wake+ (mins_wake//60))
             mins_wake = int(mins_wake%60) 
    else: 
        hour_wake = int(hour_wake)
        mins_wake = int(mins_wake)                 
        
    
    for k in range(len(filtered_df['patientGoSleepTime'])):
        if pd.isnull(filtered_df['patientGoSleepTime'][k]):
            k = k+1
        else:
            hour_sleep = hour_sleep + filtered_df['patientGoSleepTime'][k].hour
            mins_sleep = mins_sleep + filtered_df['patientGoSleepTime'][k].minute     
    if mins_sleep>=60:
        hour_sleep = (hour_sleep+ (mins_sleep//60))
        mins_sleep = (mins_sleep%60)
    hour_sleep= hour_sleep/(len(filtered_df['patientGoSleepTime']))
    mins_sleep = (mins_sleep/(len(filtered_df['patientGoSleepTime']))) + ((hour_sleep%1)*60)
    if   mins_sleep >= 60: 
             hour_wake = int(hour_wake+ (mins_sleep//60))
             mins_sleep = int(mins_sleep%60) 
    else:
        hour_sleep= int(hour_sleep)
        mins_sleep =  int(mins_sleep)   
    
    if all(pd.isnull(filtered_df['patientGoSleepTime'])) == False:
        demographic.loc[filtered_df['index'][0], 'patientGoSleepTime'] = datetime.time(hour_sleep, mins_sleep)
    if all(pd.isnull(filtered_df['patientWakeUpTime'])) == False:    
        demographic.loc[filtered_df['index'][0], 'patientWakeUpTime'] = datetime.time(hour_wake, mins_wake)
        
    
    
    demographic.loc[filtered_df['index'][0], 'patientWeightPounds'] = np.nanmean(filtered_df['patientWeightPounds'])
    demographic.loc[filtered_df['index'][0], 'patientHeightInches'] = np.nanmean(filtered_df['patientHeightInches'])
    
demographic = demographic.drop_duplicates(subset = ['healthCode'], keep = 'first').reset_index(drop = True)  
demographic = demographic[:-1]

demographic=demographic.drop(labels=['index'], axis=1)

