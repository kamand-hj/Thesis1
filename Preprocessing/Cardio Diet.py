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
print (df2)

X = diet_survey.drop(['healthCode','sodium','index'], axis=1)
X = X.fillna(0)
LOF = LocalOutlierFactor(n_neighbors=10)
p = LOF.fit_predict(X)
X['LOF'] = p
X.head(1)
X[X.LOF==-1]

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

