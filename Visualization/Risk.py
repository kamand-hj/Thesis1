#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import synapseclient
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
syn = synapseclient.Synapse()

syn.login('Kamand', 'Kamand13579-')

####preprocessing tables
###data entry
query = syn.tableQuery("SELECT * FROM syn16782068")
risk_survey = query.asDataFrame()
###dropping duplicates
#risk_no_dup = risk_survey.drop_duplicates(
  #subset = ['healthCode'],
  #keep = 'last').reset_index(drop = True)
###drop non useful rows
risk_survey=risk_survey.drop(labels=['recordId','appVersion','phoneInfo','createdOn'], axis=1)
###droping null values
#risk_no_dup = risk_no_dup.dropna()
###converting the more than one options to "more than one"
#risk_no_dup = risk_no_dup.replace(to_replace='.*,.*', value='more than one', regex=True)
risk_survey.reset_index(inplace=True)

df2 = risk_survey[risk_survey.duplicated('healthCode', keep = False)].groupby('healthCode')['index'].apply(list).reset_index()

for i in range(len(df2)):
    filtered_df = risk_survey.loc[risk_survey['healthCode'] == df2['healthCode'][i]]
    filtered_df = filtered_df.reset_index(drop = True)
    #filtered_df.drop(labels=['index'], axis=1)
    fam = filtered_df['family_history'].unique()
    fam = ','.join(str(x) for x in fam)
    heart = filtered_df['heart_disease'].unique()
    heart = ','.join(str(x) for x in heart)
    med = filtered_df['medications_to_treat'].unique()
    med = ','.join(str(x) for x in med)
    vas = filtered_df['vascular'].unique()
    vas = ','.join(str(x) for x in vas)
    risk_survey.loc[filtered_df['index'][0], 'family_history'] = fam
    risk_survey.loc[filtered_df['index'][0], 'heart_disease'] = heart
    risk_survey.loc[filtered_df['index'][0], 'medications_to_treat'] = med
    risk_survey.loc[filtered_df['index'][0], 'vascular'] = vas
risk_survey = risk_survey.drop_duplicates(subset = ['healthCode'], keep = 'first').reset_index(drop = True)
risk_survey['father_or_brother'] = risk_survey.family_history.str.contains('1')
risk_survey['mother_or_sister'] = risk_survey.family_history.str.contains('2')
###heart disease
risk_survey['Heart_Attack'] = risk_survey.heart_disease.str.contains('1')
risk_survey['Bypass_Surgery'] = risk_survey.heart_disease.str.contains('2')
risk_survey['Coronary_Blockage'] = risk_survey.heart_disease.str.contains('3')
risk_survey['Coronary_Stent'] = risk_survey.heart_disease.str.contains('4')
risk_survey['Angina'] = risk_survey.heart_disease.str.contains('5')
risk_survey['High_Coronary_Calcium_Score'] = risk_survey.heart_disease.str.contains('6')
risk_survey['Heart_Failure'] = risk_survey.heart_disease.str.contains('7')
risk_survey['Atrial_fibrillation'] = risk_survey.heart_disease.str.contains('8')
risk_survey['Congenital_Heart_Defect'] = risk_survey.heart_disease.str.contains('9')
###medication
risk_survey['lower_cholesterol_treatment'] = risk_survey.medications_to_treat.str.contains('1')
risk_survey['hypertension_lower_blood_pressure'] = risk_survey.medications_to_treat.str.contains('2')
risk_survey['diabetes'] = risk_survey.medications_to_treat.str.contains('3')
###vascular
risk_survey['stroke'] = risk_survey.vascular.str.contains('1')
risk_survey['TIA'] = risk_survey.vascular.str.contains('2')
risk_survey['Carotid_Artery_Blockage'] = risk_survey.vascular.str.contains('3')
risk_survey['Carotid_Artery_Surgery'] = risk_survey.vascular.str.contains('4')
risk_survey['Peripheral_Vascular_Disease'] = risk_survey.vascular.str.contains('5')
risk_survey['Abdominal_Aortic_Aneurysm'] = risk_survey.vascular.str.contains('6')
risk_survey=risk_survey.drop(labels=['index'], axis=1)

###converting the more than one options to "more than one"
risk_survey_replace = risk_survey.replace(to_replace='.*,.*', value='more than one', regex=True)

###pie chart for soium
import matplotlib.pyplot as plt
risk_survey_replace['family_history'] = risk_survey_replace['family_history'].dropna()
values = np.array(risk_survey_replace['family_history'].value_counts())
colors = ['y', 'g', 'r', 'c']
labels = ['None','Father or brother','Mother or sister',
                             'both' ]
explode = (0.2, 0, 0, 0)
plt.pie(values, colors=colors, 
explode=explode, autopct='%1.1f%%',
counterclock=False, shadow=True)
plt.title('Family History of Early Heart Disease')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

###family history pie chart

rvc_family_history = np.round(np.array(risk_survey_replace['family_history'].value_counts(normalize=True)*100),2)
rvc_family_history_labels = ['None','Father or brother','Mother or sister',
                             'both']
# Creating plot
fig = plt.figure(figsize =(10, 7))
plt.pie(rvc_family_history, labels = rvc_family_history_labels,autopct='%1.0f%%')
 
# show plot
plt.title("Family History of Early Heart Disease")
plt.show()

###pie chart for soium
import matplotlib.pyplot as plt
risk_survey_replace['heart_disease'] = risk_survey_replace['heart_disease'].dropna()
values = np.array(risk_survey_replace['heart_disease'].value_counts()[1:])
colors = ['#FFFF00', 'g', 'r', 'c', 'm', 'y','springgreen','gray','tab:olive','#f97306']
labels = ['more than one', 'Atrial fibrillation', 'Congenital Heart Defect',
                                  'Angina','Coronary Stent/Angioplasty','Heart Attack/Myocardial Infarction',
                                  'High Coronary Calcium Score','Heart Failure or Congestive Heart Failure',
                                 'Coronary Blockage/Stenosis', 'Heart Bypass Surgery' ]
explode = (0.2, 0, 0, 0,0,0,0,0,0,0)
plt.pie(values, colors=colors, 
explode=explode, autopct='%1.1f%%',
counterclock=False, shadow=True)
plt.title('Diagnosed Heart Disease')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

###pie chart for soium
import matplotlib.pyplot as plt
risk_survey_replace['medications_to_treat'] = risk_survey_replace['medications_to_treat'].dropna() 
values = np.array(risk_survey_replace['medications_to_treat'].value_counts()[1:])
colors = ['#069AF3', 'g', 'r', 'springgreen']
labels = ['more than one', 'hypertension and lower blood pressure','lower cholesterol ',
                                'diabetes/pre-diabetes and lower blood sugar']
explode = (0.2, 0, 0, 0)
plt.pie(values, colors=colors, 
explode=explode, autopct='%1.1f%%',
counterclock=False, shadow=True)
plt.title('Medications to treat')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

###pie chart for soium
import matplotlib.pyplot as plt
risk_survey_replace['vascular'] = risk_survey_replace['vascular'].dropna()  
values = np.array(risk_survey_replace['vascular'].value_counts()[1:])
colors = ['#FFFF00', 'g', 'r', 'c', 'm', 'y','springgreen']
labels = ['more than one','Carotid Artery Surgery or Stent',
                            'Peripheral Vascular Disease ','Stroke ' ,'Carotid Artery Blockage/Stenosis',
                             'Transient Ischemic Attack (TIA)','Abdominal Aortic Aneurysm' ]
explode = (0.2, 0, 0, 0,0,0,0)
plt.pie(values, colors=colors, 
explode=explode, autopct='%1.1f%%',
counterclock=False, shadow=True)
plt.title('Diagnosed vascular disease')
plt.legend(labels,bbox_to_anchor=(0.85,1.025),loc=2)
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(18, 8))

# set height of bar
true = [risk_survey['father_or_brother'].value_counts()[True],
       risk_survey['mother_or_sister'].value_counts()[True],
        risk_survey['Heart_Attack'].value_counts()[True],
       risk_survey['Bypass_Surgery'].value_counts()[True],
       risk_survey['Coronary_Blockage'].value_counts()[True],
       risk_survey['Coronary_Stent'].value_counts()[True],
       risk_survey['Angina'].value_counts()[True],
       risk_survey['High_Coronary_Calcium_Score'].value_counts()[True],
       risk_survey['Heart_Failure'].value_counts()[True],
       risk_survey['Atrial_fibrillation'].value_counts()[True],
       risk_survey['Congenital_Heart_Defect'].value_counts()[True],
       risk_survey['lower_cholesterol_treatment'].value_counts()[True],
       risk_survey['hypertension_lower_blood_pressure'].value_counts()[True],
       risk_survey['diabetes'].value_counts()[True],
       risk_survey['stroke'].value_counts()[True],
       risk_survey['TIA'].value_counts()[True],
       risk_survey['Carotid_Artery_Blockage'].value_counts()[True],
       risk_survey['Carotid_Artery_Surgery'].value_counts()[True],
       risk_survey['Peripheral_Vascular_Disease'].value_counts()[True],
       risk_survey['Abdominal_Aortic_Aneurysm'].value_counts()[True]]

false= [risk_survey['father_or_brother'].value_counts()[False],
        risk_survey['mother_or_sister'].value_counts()[False],
       risk_survey['Heart_Attack'].value_counts()[False],
       risk_survey['Bypass_Surgery'].value_counts()[False],
       risk_survey['Coronary_Blockage'].value_counts()[False],
       risk_survey['Coronary_Stent'].value_counts()[False],
       risk_survey['Angina'].value_counts()[False],
        risk_survey['High_Coronary_Calcium_Score'].value_counts()[False],
       risk_survey['Heart_Failure'].value_counts()[False],
       risk_survey['Atrial_fibrillation'].value_counts()[False],
       risk_survey['Congenital_Heart_Defect'].value_counts()[False],
       risk_survey['lower_cholesterol_treatment'].value_counts()[False],
       risk_survey['hypertension_lower_blood_pressure'].value_counts()[False],
       risk_survey['diabetes'].value_counts()[False],
       risk_survey['stroke'].value_counts()[False],
       risk_survey['TIA'].value_counts()[False],
       risk_survey['Carotid_Artery_Blockage'].value_counts()[False],
       risk_survey['Carotid_Artery_Surgery'].value_counts()[False],
       risk_survey['Peripheral_Vascular_Disease'].value_counts()[False],
       risk_survey['Abdominal_Aortic_Aneurysm'].value_counts()[False]]


# Set position of bar on X axis
br1 = np.arange(len(true))
br2 = [x + barWidth for x in br1]

# Make the plot
plt.bar(br1, true, color ='r', width = barWidth,
		edgecolor ='grey', label ='True')
plt.bar(br2, false, color ='g', width = barWidth,
		edgecolor ='grey', label ='False')


# Adding Xticks
plt.xlabel('Risk Factor Extracted Attributes', fontweight ='bold', fontsize = 11)
plt.ylabel('Values', fontweight ='bold', fontsize = 12)
#plt.xticks([r + 0.5*barWidth for r in range(len(true))],
		#['father \n or brother','mother \n or sister','Heart \n Attack','Bypass \n Surgery','Coronary \n Blockage','Coronary \n Stent',
        #'Angina','High Coronary \n Calcium \n Score','Heart \n Failure','Atrial \n fibrillation','Congenital\n Heart \n Defect','lower \n cholesterol \n treatment',
        #'hypertension \n lower \n blood \n pressure','diabetes','stroke','TIA','Carotid \n Artery \n Blockage',
        #'Carotid \n Artery \n Surgery','Peripheral \n Vascular \n Disease','Abdominal \n Aortic \n Aneurysm'],rotation=90)
plt.xticks([r + 0.5*barWidth for r in range(len(true))],
		['father or brother','mother or sister','Heart Attack','Bypass Surgery','Coronary Blockage','Coronary Stent',
        'Angina','High Coronary Calcium Score','Heart Failure','Atrial fibrillation','Congenital Heart Defect','lower cholesterol treatment',
        'hypertension lower blood pressure','diabetes','stroke','TIA','Carotid Artery Blockage',
        'Carotid Artery Surgery','Peripheral Vascular Disease','Abdominal Aortic Aneurysm'],rotation=90)
plt.legend()
plt.show()

