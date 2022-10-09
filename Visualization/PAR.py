#!/usr/bin/env python
# coding: utf-8

# In[ ]:


####preprocessing tables
###data entry
query = syn.tableQuery("SELECT * FROM syn16782071")
PAR_survey = query.asDataFrame()
###dropping duplicates
PAR_no_dup = PAR_survey.drop_duplicates(
  subset = ['healthCode'],
  keep = 'last').reset_index(drop = True)
###drop non useful rows
PAR_no_dup=PAR_no_dup.drop(labels=['recordId','appVersion','phoneInfo','createdOn'], axis=1)
###droping null values
#PAR_no_dup = PAR_no_dup.dropna()

###relative value counts of each column
print('relative value counts of chestpain:\n', PAR_no_dup['chestPain'].value_counts(normalize=True))
print('relative value counts of chestPainInLastMonth:\n',PAR_no_dup['chestPainInLastMonth'].value_counts(normalize=True))
print('relative value counts of dizziness:\n',PAR_no_dup['dizziness'].value_counts(normalize=True))
print('relative value counts of heartCondition:\n',PAR_no_dup['heartCondition'].value_counts(normalize=True))
print('relative value counts of jointProblem:\n',PAR_no_dup['jointProblem'].value_counts(normalize=True))
print('relative value counts of physicallyCapable:\n',PAR_no_dup['physicallyCapable'].value_counts(normalize=True))
print('relative value counts of prescriptionDrugs:\n',PAR_no_dup['prescriptionDrugs'].value_counts(normalize=True))

###number of participants with more than one condition
details = PAR_no_dup.apply(lambda x : True
            if (x['chestPain'] == True and (x['chestPainInLastMonth'] == True or x['dizziness'] == True or
                                           x['heartCondition'] == True or x['jointProblem'] == True or
                                           x['physicallyCapable'] == True or x['prescriptionDrugs'] == True)) or
                      (x['chestPainInLastMonth'] == True and (x['chestPain'] == True or x['dizziness'] == True or
                                           x['heartCondition'] == True or x['jointProblem'] == True or
                                           x['physicallyCapable'] == True or x['prescriptionDrugs'] == True)) or
                      (x['dizziness'] == True and (x['chestPain'] == True or x['chestPainInLastMonth'] == True or
                                           x['heartCondition'] == True or x['jointProblem'] == True or
                                           x['physicallyCapable'] == True or x['prescriptionDrugs'] == True)) or
                      (x['heartCondition'] == True and (x['chestPain'] == True or x['chestPainInLastMonth'] == True or
                                           x['dizziness'] == True or x['jointProblem'] == True or
                                           x['physicallyCapable'] == True or x['prescriptionDrugs'] == True))   or
                      (x['jointProblem'] == True and (x['chestPain'] == True or x['chestPainInLastMonth'] == True or
                                           x['dizziness'] == True or x['heartCondition'] == True or
                                           x['physicallyCapable'] == True or x['prescriptionDrugs'] == True)) or 
                    (x['physicallyCapable'] == True and (x['chestPain'] == True or x['chestPainInLastMonth'] == True or
                                           x['dizziness'] == True or x['heartCondition'] == True or
                                           x['jointProblem'] == True or x['prescriptionDrugs'] == True)) or
                    (x['prescriptionDrugs'] == True and (x['chestPain'] == True or x['chestPainInLastMonth'] == True or
                                           x['dizziness'] == True or x['heartCondition'] == True or
                                           x['jointProblem'] == True or x['physicallyCapable'] == True))
                           
                                           else False, axis = 1)
num_rows = len(details[details == True].index)
print('Number of Rows in dataframe in which more than one issue : ',
      num_rows )

###number of participants with at least one issue
details = PAR_no_dup.apply(lambda x : True
            if x['chestPain'] == True or x['chestPainInLastMonth'] == True or x['dizziness'] == True or
                                           x['heartCondition'] == True or x['jointProblem'] == True or
                                           x['physicallyCapable'] == True or x['prescriptionDrugs'] == True

                           
                                             else False, axis = 1)

num_rows = len(details[details == True].index)
print('Number of participants with at least one issue : ',
      num_rows )

###number of participants with all the conditions
details = PAR_no_dup.apply(lambda x : True
            if x['chestPain'] == True and x['chestPainInLastMonth'] == True and x['dizziness'] == True and
                                           x['heartCondition'] == True and x['jointProblem'] == True and
                                           x['physicallyCapable'] == True and x['prescriptionDrugs'] == True

                           
                                             else False, axis = 1)

num_rows = len(details[details == True].index)
print('Number of participants with all issues : ',
      num_rows )

import numpy as np
import matplotlib.pyplot as plt

# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))

# set height of bar
true = [PAR_no_dup['chestPain'].value_counts()[True],PAR_no_dup['chestPainInLastMonth'].value_counts()[True],
       PAR_no_dup['dizziness'].value_counts()[True],PAR_no_dup['heartCondition'].value_counts()[True],
       PAR_no_dup['jointProblem'].value_counts()[True],PAR_no_dup['physicallyCapable'].value_counts()[True],
       PAR_no_dup['prescriptionDrugs'].value_counts()[True]]
false= [PAR_no_dup['chestPain'].value_counts()[False],PAR_no_dup['chestPainInLastMonth'].value_counts()[False],
       PAR_no_dup['dizziness'].value_counts()[False],PAR_no_dup['heartCondition'].value_counts()[False],
       PAR_no_dup['jointProblem'].value_counts()[False],PAR_no_dup['physicallyCapable'].value_counts()[False],
       PAR_no_dup['prescriptionDrugs'].value_counts()[False]]


# Set position of bar on X axis
br1 = np.arange(len(true))
br2 = [x + barWidth for x in br1]

# Make the plot
plt.bar(br1, true, color ='r', width = barWidth,
		edgecolor ='grey', label ='True')
plt.bar(br2, false, color ='g', width = barWidth,
		edgecolor ='grey', label ='False')


# Adding Xticks
plt.xlabel('PAR Attrivutes', fontweight ='bold', fontsize = 15)
plt.ylabel('Values', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(true))],
		['chestPain', 'chestPainInLastMonth', 'dizziness',
       'heartCondition', 'jointProblem', 'physicallyCapable',
       'prescriptionDrugs'])

plt.legend()
plt.show()

