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

activity=activity.drop(labels=['index'], axis=1)
activity = activity[(activity.sleep_time <=15) & (activity.sleep_time1 <= 15)]

activity = activity[:-1]

####drawing box cart for continues variables
# Import libraries
import matplotlib.pyplot as plt
import numpy as np
# Creating dataset
###converting columns to arrays
moderate_act_ar = np.array(activity1['moderate_act'])
vigorous_act_ar = np.array(activity1['vigorous_act'])


data = [moderate_act_ar,vigorous_act_ar]

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)

# Creating axes instance
###showfliers equal to false makes it not to show the outliers
bp = ax.boxplot(data, patch_artist = True,notch ='True', vert = 0,showfliers=False)
#bp = ax.boxplot(data,vert = 0)

colors = ['#0000FF', '#00FF00',
        '#FFFF00', '#FF00FF']

for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

# changing color and linewidth of
# whiskers
for whisker in bp['whiskers']:
    whisker.set(color ='#8B008B',
                linewidth = 1.5,
                linestyle =":")

# changing color and linewidth of
# caps
for cap in bp['caps']:
    cap.set(color ='#8B008B',
            linewidth = 2)

# changing color and linewidth of
# medians
for median in bp['medians']:
    median.set(color ='red',
            linewidth = 3)

# changing style of fliers
for flier in bp['fliers']:
    flier.set(marker ='D',
            color ='#e7298a',
            alpha = 0.5)
    
# x-axis labels
ax.set_yticklabels(['Minutes of moderate activity', 'Minutes of vigorous activity'])

# Adding title
plt.title("Activity")

# Removing top axes and right axes
# ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# show plot
plt.show()


####drawing box cart for continues variables
# Import libraries
import matplotlib.pyplot as plt
import numpy as np

# Creating dataset
###converting columns to arrays

sleep_time_ar = np.array(activity['sleep_time'])
sleep_time1_ar = np.array(activity['sleep_time1'])


data = [sleep_time_ar,sleep_time1_ar]

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)

# Creating axes instance
###showfliers equal to false makes it not to show the outliers
bp = ax.boxplot(data, patch_artist = True,notch ='True', vert = 0,showfliers=False)
#bp = ax.boxplot(data,vert = 0)

colors = ['#0000FF', '#00FF00',
        '#FFFF00', '#FF00FF']

for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

# changing color and linewidth of
# whiskers
for whisker in bp['whiskers']:
    whisker.set(color ='#8B008B',
                linewidth = 1.5,
                linestyle =":")

# changing color and linewidth of
# caps
for cap in bp['caps']:
    cap.set(color ='#8B008B',
            linewidth = 2)

# changing color and linewidth of
# medians
for median in bp['medians']:
    median.set(color ='red',
            linewidth = 3)

# changing style of fliers
for flier in bp['fliers']:
    flier.set(marker ='D',
            color ='#e7298a',
            alpha = 0.5)
    
# x-axis labels
ax.set_yticklabels(['Weekday sleep time', 'Sleep needed to be rested'])

# Adding title
plt.title("Sleep Time")

# Removing top axes and right axes
# ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# show plot
plt.show()


####barchart for wake up time
import matplotlib.pyplot as plt
fig = plt.subplots(figsize =(12, 8))
plt.bar(['False','True'],activity['sleep_diagnosis1'].value_counts())
#plt.title('Diagnosed with sleep disorder')
plt.xlabel('Diagnosed with sleep disorder',fontweight ='bold', fontsize = 15)
plt.ylabel('Count',fontweight ='bold', fontsize = 15)
plt.show()

###ethnicity pie chart
###riskfactor1 pie chart
import matplotlib.pyplot as plt
activity['atwork'] = activity['atwork'].dropna()
values = np.array(activity['atwork'].value_counts())
colors = ['tab:blue','tab:orange','tab:green','tab:red']
labels = ['sitting or standing most of the day','walking or using hands and arms in work',
          'lifting or carrying heavy objects', 'doing hard physical labor'
         ]
explode = (0.2, 0, 0, 0)
plt.pie(values, colors=colors, autopct='%1.1f%%',
explode=explode, 
counterclock=False, shadow=True)
plt.title('at work activity')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

###ethnicity pie chart
###riskfactor1 pie chart
import matplotlib.pyplot as plt
activity['phys_activity']=activity['phys_activity'].dropna()
values = np.array(activity['phys_activity'].value_counts())
colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:pink']
labels = ['do not do that much physical activity', 'Once or twice a week,light activities',
          'three times a week, moderate activities','Almost daily, moderate activities', 
          'About three times a week, vigorous activities','Almost daily, vigorous activities'
         ]
explode = (0.2, 0, 0, 0,0,0)
plt.pie(values, colors=colors, autopct='%1.1f%%',
explode=explode, 
counterclock=False, shadow=True)
plt.title('physical activity')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
fig = plt.figure(figsize=(8,7))
sns.heatmap(activity.corr(), annot=True)

