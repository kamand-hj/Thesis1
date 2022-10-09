#!/usr/bin/env python
# coding: utf-8

# In[ ]:


####preprocessing tables
###data entry
query = syn.tableQuery("SELECT * FROM syn16782068")
risk_survey = query.asDataFrame()

risk_survey=risk_survey.drop(labels=['recordId','appVersion','phoneInfo','createdOn'], axis=1)

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
risk_survey.to_csv("risk_survey.csv")

