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
query = syn.tableQuery("SELECT * FROM syn16782069")
activity = query.asDataFrame()
###drop non useful rows
activity=activity.drop(labels=['recordId','appVersion','phoneInfo','createdOn',
                                              ], axis=1)
activity.reset_index(inplace=True)

df2 = activity[activity.duplicated('healthCode', keep = False)].groupby('healthCode')['index'].apply(list).reset_index()
#print (df2)

activity['atwork'] = activity['atwork'].apply (str)
activity['phys_activity'] = activity['phys_activity'].apply (str)

for i in range(len(df2)):
    filtered_df = activity.loc[activity['healthCode'] == df2['healthCode'][i]]
    filtered_df = filtered_df.reset_index(drop = True)
    #filtered_df.drop(labels=['index'], axis=1)
    atwork = filtered_df['atwork'].unique()
    atwork = ','.join(str(x) for x in atwork)
    phys_activity = filtered_df['phys_activity'].unique()
    phys_activity = ','.join(str(x) for x in phys_activity)
    activity.loc[filtered_df['index'][0], 'atwork'] = atwork
    activity.loc[filtered_df['index'][0], 'phys_activity'] = phys_activity
    activity.loc[filtered_df['index'][0], 'moderate_act'] = np.nanmean(filtered_df['moderate_act'])
    activity.loc[filtered_df['index'][0], 'sleep_time'] = np.nanmean(filtered_df['sleep_time'])
    activity.loc[filtered_df['index'][0], 'sleep_time1'] = np.nanmean(filtered_df['sleep_time1'])
    activity.loc[filtered_df['index'][0], 'vigorous_act'] = np.nanmean(filtered_df['vigorous_act'])
activity = activity.drop_duplicates(subset = ['healthCode'], keep = 'first').reset_index(drop = True)  

activity['mostly_sit_stand'] = activity.atwork.str.contains('1.0')
activity['mostly_walk'] = activity.atwork.str.contains('2.0')
activity['mostly_lift'] = activity.atwork.str.contains('3.0')
activity['hard_physical_activity'] = activity.atwork.str.contains('4.0')

activity['not_much_physical_activity'] = activity.phys_activity.str.contains('1.0')
activity['once_or_twice_physical_activity'] = activity.phys_activity.str.contains('2.0')
activity['three_times_physical_activity'] = activity.phys_activity.str.contains('3.0')
activity['daily_physical_activity'] = activity.phys_activity.str.contains('4.0')
activity['three_times_vigorous_activity'] = activity.phys_activity.str.contains('5.0')
activity['daily_vigorous_activity'] = activity.phys_activity.str.contains('6.0')
activity = activity.replace(to_replace='nan', value=None, regex=False)

activity = activity[activity['vigorous_act']<4200]
activity = activity[activity['moderate_act']<4200]

activity=activity.drop(labels=['index'], axis=1)

activity = activity[(activity.sleep_time <=15) & (activity.sleep_time1 <= 15)]

activity = activity[:-1]

