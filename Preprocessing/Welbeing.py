#!/usr/bin/env python
# coding: utf-8

# In[ ]:


####preprocessing tables
###data entry
query = syn.tableQuery("SELECT * FROM syn16782066")
welbeing_survey = query.asDataFrame()
###drop non useful rows
welbeing_survey=welbeing_survey.drop(labels=['recordId','appVersion','phoneInfo','createdOn'], axis=1)
#diet_survey.reset_index(inplace = True, drop = True)
welbeing_survey.reset_index(inplace=True)
welbeing_survey.duplicated(subset='healthCode').sum()
df2 = welbeing_survey[welbeing_survey.duplicated('healthCode', keep = False)].groupby('healthCode')['index'].apply(list).reset_index()

###finding outliers
X = welbeing_survey.drop(['healthCode','index'], axis=1)
X = X.fillna(0)
LOF = LocalOutlierFactor(n_neighbors=10)
p = LOF.fit_predict(X)
X['LOF'] = p
X.head(1)
X[X.LOF==-1]

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

