#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
#print (df2)

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

demographic1 = demographic.dropna()

####drawing box cart for continues variables
# Import libraries
import matplotlib.pyplot as plt
import numpy as np

# Creating dataset
###converting columns to arrays
Weight_ar = np.array(demographic1['patientWeightPounds'])
Height_ar = np.array(demographic1['patientHeightInches'])
Age_ar = np.array(demographic1['patientCurrentAge'])

data = [Weight_ar, Height_ar,Age_ar]

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
ax.set_yticklabels(['Weight', 'Height','Age'])

# Adding title
plt.title("Continues Features of Demographic Table")

# Removing top axes and right axes
# ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# show plot
plt.show()

####barchart for wake up time
import matplotlib.pyplot as plt

#su1 = demographic['patientWakeUpTime'].value_counts().index.tolist()
su1 = ['21:30','23:30','22:30','23:00','00:30','00:00','22:00','01:30','01:00','02:30']
plt.bar(su1[0:10],demographic['patientWakeUpTime'].value_counts()[0:10])
plt.title('Most popular wakeing up times')
plt.xlabel('Time')
plt.ylabel('Count')
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
fig = plt.figure(figsize=(8,7))
sns.heatmap(demographic.corr(), annot=True)

###ethnicity pie chart
###riskfactor1 pie chart
import matplotlib.pyplot as plt

values = np.array(demographic1['patientBiologicalSex'].value_counts())
colors = ['tab:blue','tab:orange']
labels = ['Male','Female']
explode = (0.2, 0)
plt.pie(values, colors=colors, 
explode=explode, autopct='%1.1f%%',
counterclock=False, shadow=True)
plt.title('Gender')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

