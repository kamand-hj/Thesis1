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

###finding outliers
X = heart_age.drop(['healthCode','index','smokingHistory','heartAgeDataHypertension','heartAgeDataEthnicity',
                   'heartAgeDataGender','heartAgeDataDiabetes'], axis=1)
X = X.fillna(0)
LOF = LocalOutlierFactor(n_neighbors=10)
p = LOF.fit_predict(X)
X['LOF'] = p
X.head(1)
X[X.LOF==-1]

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

