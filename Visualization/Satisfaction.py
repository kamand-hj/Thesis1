#!/usr/bin/env python
# coding: utf-8

# In[ ]:


####preprocessing tables
###data entry
query = syn.tableQuery("SELECT * FROM syn16782066")
welbeing_survey = query.asDataFrame()
###dropping duplicates
#welbeing_survey = welbeing_survey.drop_duplicates(
  #subset = ['healthCode'],
  #keep = 'last').reset_index(drop = True)
###drop non useful rows
welbeing_survey=welbeing_survey.drop(labels=['recordId','appVersion','phoneInfo','createdOn'], axis=1)
###droping null values
#welbeing_survey = welbeing_survey.dropna()

welbeing_survey.reset_index(inplace=True)
welbeing_survey.duplicated(subset='healthCode').sum()
df2 = welbeing_survey[welbeing_survey.duplicated('healthCode', keep = False)].groupby('healthCode')['index'].apply(list).reset_index()
print (df2)
for i in range(len(df2)):
    filtered_df = welbeing_survey.loc[welbeing_survey['healthCode'] == df2['healthCode'][i]]
    filtered_df = filtered_df.reset_index(drop = True)
    welbeing_survey.loc[filtered_df['index'][0], 'feel_worthwhile1'] = np.nanmean(filtered_df['feel_worthwhile1'])
    welbeing_survey.loc[filtered_df['index'][0], 'feel_worthwhile2'] = np.nanmean(filtered_df['feel_worthwhile2'])
    welbeing_survey.loc[filtered_df['index'][0], 'feel_worthwhile3'] = np.nanmean(filtered_df['feel_worthwhile3'])
    welbeing_survey.loc[filtered_df['index'][0], 'riskfactors1'] = np.nanmean(filtered_df['riskfactors1'])
    welbeing_survey.loc[filtered_df['index'][0], 'riskfactors2'] = np.nanmean(filtered_df['riskfactors2'])
    welbeing_survey.loc[filtered_df['index'][0], 'riskfactors3'] = np.nanmean(filtered_df['riskfactors3'])
    welbeing_survey.loc[filtered_df['index'][0], 'riskfactors4'] = np.nanmean(filtered_df['riskfactors4'])
    welbeing_survey.loc[filtered_df['index'][0], 'satisfiedwith_life'] = np.nanmean(filtered_df['satisfiedwith_life'])
welbeing_survey = welbeing_survey.drop_duplicates(subset = ['healthCode'], keep = 'first').reset_index(drop = True)
welbeing_survey=diet_survey.drop(labels=['index'], axis=1)

###columns descriptions
print('description of feel_worthwhile1 : \n', welbeing_survey['feel_worthwhile1'].describe())
print('description of feel_worthwhile2 : \n', welbeing_survey['feel_worthwhile2'].describe())
print('description of feel_worthwhile3 : \n', welbeing_survey['feel_worthwhile3'].describe())
print('description of feel_worthwhile4 : \n', welbeing_survey['feel_worthwhile4'].describe())
print('description of friskfactors1 : \n', welbeing_survey['riskfactors1'].describe())
print('description of friskfactors2 : \n', welbeing_survey['riskfactors2'].describe())
print('description of friskfactors3 : \n', welbeing_survey['riskfactors3'].describe())
print('description of friskfactors4 : \n', welbeing_survey['riskfactors4'].describe())
print('description of satisfiedwith_life : \n', welbeing_survey['satisfiedwith_life'].describe())
print('description of zip3 : \n', welbeing_survey['zip3'].describe())

print( welbeing_survey['riskfactors1'].value_counts()/welbeing_survey['riskfactors1'].count())
print( welbeing_survey['riskfactors2'].value_counts()/welbeing_survey['riskfactors1'].count())
print( welbeing_survey['riskfactors3'].value_counts()/welbeing_survey['riskfactors1'].count())
print( welbeing_survey['riskfactors4'].value_counts()/welbeing_survey['riskfactors1'].count())

welbeing_survey1 = welbeing_survey.dropna()

####drawing box cart for continues variables
# Import libraries
import matplotlib.pyplot as plt
import numpy as np

# Creating dataset
###converting columns to arrays
feel1_ar = np.array(welbeing_survey1['feel_worthwhile1'])
feel2_ar = np.array(welbeing_survey1['feel_worthwhile2'])
feel3_ar = np.array(welbeing_survey1['feel_worthwhile3'])
feel4_ar = np.array(welbeing_survey1['feel_worthwhile4'])
satisfied_ar = np.array(welbeing_survey1['satisfiedwith_life'])

data = [feel1_ar, feel2_ar,feel3_ar,feel4_ar,satisfied_ar ]

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)

# Creating axes instance
bp = ax.boxplot(data, patch_artist = True,
                notch ='True', vert = 0)

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
ax.set_yticklabels(['Being worthwhile', 'being happy','being worried','being depressed','satisfied'])

# Adding title
plt.title("Feeling Worth While and Satisfied with Life")

# Removing top axes and right axes
# ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# show plot
plt.show()

###riskfactor1 pie chart
import matplotlib.pyplot as plt
welbeing_survey['riskfactors1'] = welbeing_survey['riskfactors1'].dropna() 
values = np.array(welbeing_survey['riskfactors1'].value_counts())
colors = ['#f97306', 'g', 'r', 'c', 'm']
labels = ['Not at all','A little','Moderately' ,'A lot','Extremely']
explode = (0.2, 0, 0, 0, 0)
plt.pie(values, colors=colors, 
explode=explode, autopct='%1.1f%%',
counterclock=False, shadow=True)
plt.title('How likely do you think it is that you personally will have a heart attack,\n stroke, or die due to cardiovascular disease?')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

###riskfactor2 pie chart
import matplotlib.pyplot as plt
welbeing_survey['riskfactors2'] = welbeing_survey['riskfactors2'].dropna() 
values = np.array(welbeing_survey['riskfactors2'].value_counts())
colors = ['#f97306', 'g', 'r', 'c', 'm']
labels = ['Lower than average','Average','Much lower than average','Higher than average','Much higher than average']
explode = (0.2, 0, 0, 0, 0)
plt.pie(values, colors=colors, 
explode=explode, autopct='%1.1f%%',
counterclock=False, shadow=True)
plt.title('Over the next 10 years, compared to others your age and sex,\n how would you rate your risk of having a heart attack, stroke, or dying due to cardiovascular disease?')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

###riskfactor3 pie chart
import matplotlib.pyplot as plt
welbeing_survey['riskfactors3'] = welbeing_survey['riskfactors3'].dropna()
values = np.array(welbeing_survey['riskfactors3'].value_counts())
colors = ['#f97306', 'g', 'r', 'c', 'm']
labels = ['A little','Moderately','Not at all','A lot','Extremely']
explode = (0.2, 0, 0, 0, 0)
plt.pie(values, colors=colors, 
explode=explode, autopct='%1.1f%%',
counterclock=False, shadow=True)
plt.title('Over your lifetime how likely do you think it is \n that you personally will have a heart attack, stroke, or die due to cardiovascular disease?')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

###riskfactor4 pie chart
import matplotlib.pyplot as plt
welbeing_survey['riskfactors4'] = welbeing_survey['riskfactors4'].dropna() 
values = np.array(welbeing_survey['riskfactors4'].value_counts())
colors = ['#f97306', 'g', 'r', 'c', 'm']
labels = ['Average','Lower than average','Higher than average','Much lower than average ','Much higher than average']
explode = (0.2, 0, 0, 0, 0)
plt.pie(values, colors=colors, 
explode=explode, autopct='%1.1f%%',
counterclock=False, shadow=True)
plt.title('Over your lifetime, compared to others your age and sex, \n how would you rate your risk of having a heart attack, stroke, or dying \n due to cardiovascular disease?  ')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
fig = plt.figure(figsize=(8,7))
sns.heatmap(welbeing_survey.corr(), annot=True)

