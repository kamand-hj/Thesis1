#!/usr/bin/env python
# coding: utf-8

# In[ ]:


####preprocessing tables
###data entry
query = syn.tableQuery("SELECT * FROM syn16782065")
heart_age = query.asDataFrame()
###drop non useful rows
heart_age=heart_age.drop(labels=['recordId','appVersion','phoneInfo','createdOn','bloodPressureInstruction_unit',
                                             'heartAgeDataBloodGlucose_unit','heartAgeDataHdl_unit','heartAgeDataLdl_unit',
                                              'heartAgeDataSystolicBloodPressure_unit','heartAgeDataTotalCholesterol_unit'], axis=1)
#diet_survey.reset_index(inplace = True, drop = True)
heart_age.reset_index(inplace=True)
#heart_age.duplicated(subset='healthCode').sum()
df2 = heart_age[heart_age.duplicated('healthCode', keep = False)].groupby('healthCode')['index'].apply(list).reset_index()
print (df2)

heart_age1 = heart_age[(heart_age['heartAgeDataSystolicBloodPressure']>180) | (heart_age['heartAgeDataSystolicBloodPressure']<95) |
                      (heart_age['bloodPressureInstruction']<55) | (heart_age['bloodPressureInstruction']>120) | 
                      (heart_age['heartAgeDataBloodGlucose']<3) | (heart_age['heartAgeDataBloodGlucose']>15) |
                      (heart_age['heartAgeDataHdl']<0.8) | (heart_age['heartAgeDataHdl']>7) | (heart_age['heartAgeDataLdl']<1) |
                      (heart_age['heartAgeDataLdl']> 7)  | (heart_age['heartAgeDataTotalCholesterol']<2) | 
                       (heart_age['heartAgeDataTotalCholesterol']>12)]

###dropping duplicates
for i in range(len(df2)):
    filtered_df = heart_age.loc[heart_age['healthCode'] == df2['healthCode'][i]]
    filtered_df = filtered_df.reset_index(drop = True)
    #filtered_df.drop(labels=['index'], axis=1)
    diabete = filtered_df['heartAgeDataDiabetes'].sum()
    heart_age.loc[filtered_df['index'][0], 'heartAgeDataDiabetes'] = diabete
    
    hyper = filtered_df['heartAgeDataHypertension'].sum()
    heart_age.loc[filtered_df['index'][0], 'heartAgeDataHypertension'] = hyper
    
    smoke = filtered_df['smokingHistory'].sum()
    heart_age.loc[filtered_df['index'][0], 'smokingHistory'] = smoke
    
    heart_age.loc[filtered_df['index'][0], 'bloodPressureInstruction'] = np.nanmean(filtered_df['bloodPressureInstruction'])
    heart_age.loc[filtered_df['index'][0], 'heartAgeDataBloodGlucose'] = np.nanmean(filtered_df['heartAgeDataBloodGlucose'])
    heart_age.loc[filtered_df['index'][0], 'heartAgeDataHdl'] = np.nanmean(filtered_df['heartAgeDataHdl'])
    heart_age.loc[filtered_df['index'][0], 'heartAgeDataLdl'] = np.nanmean(filtered_df['heartAgeDataLdl'])
    heart_age.loc[filtered_df['index'][0], 'heartAgeDataSystolicBloodPressure'] = np.nanmean(filtered_df['heartAgeDataSystolicBloodPressure'])
    heart_age.loc[filtered_df['index'][0], 'heartAgeDataTotalCholesterol'] = np.nanmean(filtered_df['heartAgeDataTotalCholesterol'])
heart_age = heart_age.drop_duplicates(subset = ['healthCode'], keep = 'first').reset_index(drop = True)    

heart_age['heartAgeDataSystolicBloodPressure'] = np.where((heart_age['heartAgeDataSystolicBloodPressure']> 180) | (heart_age['heartAgeDataSystolicBloodPressure']<95) ,
    None, heart_age['heartAgeDataSystolicBloodPressure'])
heart_age['bloodPressureInstruction'] = np.where((heart_age['bloodPressureInstruction']> 120) | (heart_age['bloodPressureInstruction']<55) ,
    None, heart_age['bloodPressureInstruction'])
heart_age['heartAgeDataBloodGlucose'] = np.where((heart_age['heartAgeDataBloodGlucose']> 15) | (heart_age['heartAgeDataBloodGlucose']<3) ,
    None, heart_age['heartAgeDataBloodGlucose'])
heart_age['heartAgeDataHdl'] = np.where((heart_age['heartAgeDataHdl']> 7) | (heart_age['heartAgeDataHdl']<0.8) ,
    None, heart_age['heartAgeDataHdl'])
heart_age['heartAgeDataLdl'] = np.where((heart_age['heartAgeDataLdl']> 7) | (heart_age['heartAgeDataLdl']<1) ,
    None, heart_age['heartAgeDataLdl'])
heart_age['heartAgeDataTotalCholesterol'] = np.where((heart_age['heartAgeDataTotalCholesterol']> 12) | (heart_age['heartAgeDataTotalCholesterol']<2) ,
    None, heart_age['heartAgeDataTotalCholesterol'])

from missingpy import MissForest

# Make an instance and perform the imputation
imputer = MissForest()
X = heart_age.drop(['index','healthCode','heartAgeDataDiabetes','heartAgeDataGender','heartAgeDataHypertension',
                    'heartAgeDataEthnicity','smokingHistory',
                   'heartAgeDataAge'],axis=1)
X_imputed = imputer.fit_transform(X)

###replacing the columns
heart_age['bloodPressureInstruction'] = X_imputed[:, 0]
heart_age['heartAgeDataBloodGlucose'] = X_imputed[:, 1]
heart_age['heartAgeDataHdl'] = X_imputed[:, 2]
heart_age['heartAgeDataLdl'] = X_imputed[:, 3]
heart_age['heartAgeDataSystolicBloodPressure'] = X_imputed[:, 4]
heart_age['heartAgeDataTotalCholesterol'] = X_imputed[:, 5]

heart_age=heart_age.drop(labels=['index'], axis=1)
#heart_age

heart_age1 = heart_age.dropna()

####drawing box cart for continues variables
# Import libraries
import matplotlib.pyplot as plt
import numpy as np

# Creating dataset
###converting columns to arrays
blood_pressure_ar = np.array(heart_age1['bloodPressureInstruction'])
blood_glucose_ar = np.array(heart_age1['heartAgeDataBloodGlucose'])
HDI_ar = np.array(heart_age1['heartAgeDataHdl'])
LDI_ar = np.array(heart_age1['heartAgeDataLdl'])
blood_pressure_sys_ar = np.array(heart_age1['heartAgeDataSystolicBloodPressure'])
cholesterol_ar = np.array(heart_age1['heartAgeDataTotalCholesterol'])
heart_age_ar = np.array(heart_age1['heartAgeDataAge'])

data = [blood_pressure_ar, blood_glucose_ar,HDI_ar, LDI_ar,blood_pressure_sys_ar,cholesterol_ar,heart_age_ar]

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)

# Creating axes instance
###showfliers equal to false makes it not to show the outliers
bp = ax.boxplot(data, patch_artist = True,notch ='True', vert = 0,showfliers=False)
#bp = ax.boxplot(data,vert = 0)

colors = ['#0000FF', '#00FF00',
        '#FFFF00', '#FF00FF','#f97306', 'g', 'r', 'c', 'm']

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
ax.set_yticklabels(['Blood Pressure', 'Blood Glucose' ,'HDL','LDL','Systolic Blood Pressure','Cholesterol','Heart Age'])

# Adding title
plt.title("Heart Age Continues Variables Box Plot")

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
blood_pressure_ar = np.array(heart_age1['bloodPressureInstruction'])
blood_pressure_sys_ar = np.array(heart_age1['heartAgeDataSystolicBloodPressure'])
heart_age_ar = np.array(heart_age1['heartAgeDataAge'])

data = [blood_pressure_ar,blood_pressure_sys_ar,heart_age_ar]

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)

# Creating axes instance
###showfliers equal to false makes it not to show the outliers
bp = ax.boxplot(data, patch_artist = True,notch ='True', vert = 0,showfliers=False)
#bp = ax.boxplot(data,vert = 0)

colors = ['#0000FF', '#00FF00','#FFFF00']

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
ax.set_yticklabels(['Blood Pressure','Systolic Blood Pressure','Heart Age'])

# Adding title
plt.title("Heart Age Continues Variables Box Plot1")

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
blood_glucose_ar = np.array(heart_age1['heartAgeDataBloodGlucose'])
HDI_ar = np.array(heart_age1['heartAgeDataHdl'])
LDI_ar = np.array(heart_age1['heartAgeDataLdl'])
cholesterol_ar = np.array(heart_age1['heartAgeDataTotalCholesterol'])

data = [ blood_glucose_ar,HDI_ar, LDI_ar,cholesterol_ar]

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)

# Creating axes instance
###showfliers equal to false makes it not to show the outliers
bp = ax.boxplot(data, patch_artist = True,notch ='True', vert = 0,showfliers=False)
#bp = ax.boxplot(data,vert = 0)

colors = ['#0000FF', '#00FF00',
        '#FFFF00', '#FF00FF','#f97306', 'g', 'r', 'c', 'm']

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
ax.set_yticklabels(['Blood Glucose' ,'HDL','LDL','Cholesterol'])

# Adding title
plt.title("Heart Age Continues Variables Box Plot2")

# Removing top axes and right axes
# ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# show plot
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))

# set height of bar
true = [heart_age1['heartAgeDataDiabetes'].value_counts()[True],
        heart_age1['heartAgeDataHypertension'].value_counts()[True],
       heart_age1['smokingHistory'].value_counts()[True]]
false= [heart_age1['heartAgeDataDiabetes'].value_counts()[False],
        heart_age1['heartAgeDataHypertension'].value_counts()[False],
       heart_age1['smokingHistory'].value_counts()[False]]


# Set position of bar on X axis
br1 = np.arange(len(true))
br2 = [x + barWidth for x in br1]

# Make the plot
plt.bar(br1, true, color ='r', width = barWidth,
		edgecolor ='grey', label ='True')
plt.bar(br2, false, color ='g', width = barWidth,
		edgecolor ='grey', label ='False')


# Adding Xticks
plt.xlabel('Heart Age TRUE/FALSE Measures', fontweight ='bold', fontsize = 15)
plt.ylabel('Values', fontweight ='bold', fontsize = 15)
plt.xticks([r + 0.5*barWidth for r in range(len(true))],
		['Diabetes', 'Hypertension', 'Smoking History'])

plt.legend()
plt.show()

###ethnicity pie chart
###riskfactor1 pie chart
import matplotlib.pyplot as plt

values = np.array(heart_age1['heartAgeDataEthnicity'].value_counts())
colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:pink','tab:gray','tab:olive','tab:cyan']
labels = ['White','Asian','Hispanic','Black','Other','unknown','American Indian','Pacific Islander','Alaska Native']
explode = (0.2, 0, 0, 0, 0,0,0,0,0)
plt.pie(values, colors=colors, 
explode=explode, 
counterclock=False, shadow=True)
plt.title('Ethnicity')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

###ethnicity pie chart
###riskfactor1 pie chart
import matplotlib.pyplot as plt

values = np.array(heart_age1['heartAgeDataGender'].value_counts())
colors = ['tab:blue','tab:orange','tab:green']
labels = ['Male','Female','other']
explode = (0.2, 0,0)
plt.pie(values, colors=colors, 
explode=explode, autopct='%1.1f%%',
counterclock=False, shadow=True)
plt.title('Gender')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

