#!/usr/bin/env python
# coding: utf-8

# In[ ]:


df_data = pd.read_csv('healthkit_data.csv')

####drawing box cart for continues variables
# Import libraries
import matplotlib.pyplot as plt
import numpy as np

# Creating dataset
###converting columns to arrays
duration_ar = np.array(df_data['distance'])
morning_time_ar = np.array(df_data['morning_distance'])
noon_time_ar = np.array(df_data['noon_distance'])
afternoon_time_ar = np.array(df_data['afternoon_distance'])
evening_time_ar = np.array(df_data['evening_distance'])

data = [duration_ar,morning_time_ar,noon_time_ar,afternoon_time_ar,evening_time_ar]

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)

# Creating axes instance
###showfliers equal to false makes it not to show the outliers
bp = ax.boxplot(data, patch_artist = True,notch ='True', vert = 0,showfliers=False)
#bp = ax.boxplot(data,vert = 0)

colors = ['#0000FF', '#00FF00',
        '#FFFF00', '#FF00FF','#FF8C00']

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
ax.set_yticklabels(['Distance', 'Morning Activity Distance','Noon Activity Distance','Afternoon Activity Distance',
                   'Evening Activity Distance', 'Night Activity Distnace'])

# Adding title
plt.title("Distance in HealthKit Data")

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
duration_ar = np.array(df_data['energy'])
morning_time_ar = np.array(df_data['morning_energy'])
noon_time_ar = np.array(df_data['noon_energy'])
afternoon_time_ar = np.array(df_data['afternoon_energy'])
evening_time_ar = np.array(df_data['evening_energy'])

data = [duration_ar,morning_time_ar,noon_time_ar,afternoon_time_ar,evening_time_ar]

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)

# Creating axes instance
###showfliers equal to false makes it not to show the outliers
bp = ax.boxplot(data, patch_artist = True,notch ='True', vert = 0,showfliers=False)
#bp = ax.boxplot(data,vert = 0)

colors = ['#0000FF', '#00FF00',
        '#FFFF00', '#FF00FF','#FF8C00']

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
ax.set_yticklabels(['Energy', 'Morning Activity Energy','Noon Activity Energy','Afternoon Activity Energy',
                   'Evening Activity Energy', 'Night Activity Energy'])

# Adding title
plt.title("Energy")

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
duration_ar = np.array(df_data['duration'])
morning_time_ar = np.array(df_data['morning_time'])
noon_time_ar = np.array(df_data['noon_time'])
afternoon_time_ar = np.array(df_data['afternoon_time'])
evening_time_ar = np.array(df_data['evening_time'])

data = [duration_ar,morning_time_ar,noon_time_ar,afternoon_time_ar,evening_time_ar]

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)

# Creating axes instance
###showfliers equal to false makes it not to show the outliers
bp = ax.boxplot(data, patch_artist = True,notch ='True', vert = 0,showfliers=False)
#bp = ax.boxplot(data,vert = 0)

colors = ['#0000FF', '#00FF00',
        '#FFFF00', '#FF00FF','#FF8C00']

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
ax.set_yticklabels(['Duration', 'Morning Activity Duration ','Noon Activity Duration','Afternoon Activity Duration',
                   'Evening Activity Duration', 'Night Activity Duration'])

# Adding title
plt.title("Duration")

# Removing top axes and right axes
# ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# show plot
plt.show()

###ethnicity pie chart
###riskfactor1 pie chart
import matplotlib.pyplot as plt

values = np.array(df_data['day_part'].value_counts())
colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple']
labels = ['Morning','Night','Afternoon','Evening','Noon']
explode = (0.2, 0,0,0,0)
plt.pie(values, colors=colors, 
explode=explode, autopct='%1.1f%%',
counterclock=False, shadow=True)
plt.title('Day Parts')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

