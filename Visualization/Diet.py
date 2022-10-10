#!/usr/bin/env python
# coding: utf-8

# In[ ]:


query = syn.tableQuery("SELECT * FROM syn16782067")
diet_survey = query.asDataFrame()
diet_survey=diet_survey.drop(labels=['recordId','appVersion','phoneInfo','createdOn'], axis=1)

#diet_survey.reset_index(inplace = True, drop = True)
diet_survey.reset_index(inplace=True)
diet_survey.duplicated(subset='healthCode').sum()
df2 = diet_survey[diet_survey.duplicated('healthCode', keep = False)].groupby('healthCode')['index'].apply(list).reset_index()
#print (df2)

for i in range(len(df2)):
    filtered_df = diet_survey.loc[diet_survey['healthCode'] == df2['healthCode'][i]]
    filtered_df = filtered_df.reset_index(drop = True)
    #filtered_df.drop(labels=['index'], axis=1)
    sod = filtered_df['sodium'].unique()
    sod = ','.join(str(x) for x in sod)
    diet_survey.loc[filtered_df['index'][0], 'sodium'] = sod
    diet_survey.loc[filtered_df['index'][0], 'fish'] = np.nanmean(filtered_df['fish'])
    diet_survey.loc[filtered_df['index'][0], 'fruit'] = np.nanmean(filtered_df['fruit'])
    diet_survey.loc[filtered_df['index'][0], 'grains'] = np.nanmean(filtered_df['grains'])
    diet_survey.loc[filtered_df['index'][0], 'sugar_drinks'] = np.nanmean(filtered_df['sugar_drinks'])
    diet_survey.loc[filtered_df['index'][0], 'vegetable'] = np.nanmean(filtered_df['vegetable'])
diet_survey = diet_survey.drop_duplicates(subset = ['healthCode'], keep = 'first').reset_index(drop = True)
diet_survey['avoid_pre_packed'] = diet_survey.sodium.str.contains('1')
diet_survey['avoid_eating_out'] = diet_survey.sodium.str.contains('2')
diet_survey['avoid_salt'] = diet_survey.sodium.str.contains('3')
diet_survey['not_avoiding'] = diet_survey.sodium.str.contains('4')
diet_survey=diet_survey.drop(labels=['index'], axis=1)

diet_survey.describe()

diet_survey['sodium']=diet_survey['sodium'].replace(['2,1','1,2,4'], '1,2')
diet_survey['sodium']=diet_survey['sodium'].replace(['3,1'], '1,3')
diet_survey['sodium']=diet_survey['sodium'].replace(['3,2,1','1,3,2','2,3,1','3,1,2','2,1,3'], '1,2,3')
diet_survey['sodium']=diet_survey['sodium'].replace(['1,4','4,1'], '1')
diet_survey['sodium']=diet_survey['sodium'].replace(['2,4'], '2')
diet_survey['sodium']=diet_survey['sodium'].replace(['3,4','4,3'], '3')
diet_survey['sodium']=diet_survey['sodium'].replace(['3,2'], '2,3')
print('value counts of sodium:\n', diet_survey['sodium'].value_counts())
print('relative value counts of sodium:\n', diet_survey['sodium'].value_counts(normalize=True))

diet_survey = diet_survey.dropna()

####drawing box cart for continues variables
# Import libraries
import matplotlib.pyplot as plt
import numpy as np
diet_survey['fish'] =diet_survey['fish'].dropna()
diet_survey['fruit'] = diet_survey['fruit'].dropna()
diet_survey['grains'] = diet_survey['grains'].dropna()
diet_survey['sugar_drinks'] = diet_survey['sugar_drinks'].dropna()
diet_survey['vegetable'] = diet_survey['vegetable'].dropna()
# Creating dataset
###converting columns to arrays
fish_ar = np.array(diet_survey['fish'])
fruit_ar = np.array(diet_survey['fruit'])
grains_ar = np.array(diet_survey['grains'])
sugar_drinks_ar = np.array(diet_survey['sugar_drinks'])
vegetable_ar = np.array(diet_survey['vegetable'])

data = [fish_ar, fruit_ar,grains_ar,sugar_drinks_ar,vegetable_ar]

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
ax.set_yticklabels(['fish', 'fruit','grains','sugar_drinks','vegetable'])

# Adding title
plt.title("Consumption of Different Ingredients")

# Removing top axes and right axes
# ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# show plot
plt.show()

###pie chart for soium
import matplotlib.pyplot as plt
diet_survey['sodium'] = diet_survey['sodium'].dropna()
values = np.array(diet_survey['sodium'].value_counts())
colors = ['b', 'g', 'r', 'c', 'm', 'y','springgreen','gray']
labels = ['no prepackaged foods ', 'no salt while cooking','none',
                            'no prepackaged foods & no salt while cooking', 'all','not eating out',
          'no prepackaged foods & not eating out','not eating out & no salt while cooking' ]
explode = (0.2, 0, 0, 0, 0, 0,0,0)
plt.pie(values, colors=colors, 
explode=explode, autopct='%1.1f%%',
counterclock=False, shadow=True)
plt.title('Sodium usuage')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

