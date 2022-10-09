#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import synapseclient
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import os
import glob
import pandas as pd
import regex as re
syn = synapseclient.Synapse()

syn.login('Kamand', 'Kamand13579-')

query = syn.tableQuery("SELECT * FROM syn16782062")
data = query.asDataFrame()
files_finding= data.groupby('healthCode')['data.csv'].apply(list)

###making an array of dataframes from csv files
content = []
content_kit =[]
for i in range (0,len(files_finding)):
    
    if i!= 2708:
    
        file_founded_length = len(files_finding[i])
    
    #df = pd.DataFrame([])A
        list_of_dfs = []
    #print(list_of_dfs)
        for k in range(0,file_founded_length):
        #df = pd.DataFrame([])
        
        #data_frame = pd.DataFrame()
        #content = []
            for j in range(0,999):
                path = 'C:/leiden/master nl/thesis/mathias/data/healthkit data/'+str(j)+'/'+str(files_finding[i][k])
            #print(path)
            #print(files)
                if os.path.exists(path) == True:
                    if files_finding[i][k]==31036799:
                        k=k+1
                    else:
                        files = glob.glob(path + "/*.csv")
                #df1 = pd.read_csv(files[0], sep=';', header=None,index_col=None)
                #df1 = pd.read_csv(files[0], sep=',', header=None,index_col=None)
                        df1 = pd.read_csv(files[0],sep=',', usecols = ['startTime','endTime','type','value',
                                                               'unit','source','sourceIdentifier'])
               
                #print(df1)
                        list_of_dfs.append(df1) 
             
                else:
                    j=j+1
        else: 
            i = i+1
            
    #print(i)        
    b = pd.concat(list_of_dfs, ignore_index=True)            
    content.append(b)  
    content_kit.append(b)
    
###########considering unknown start and end time and omit those data
###preprocessing all the dataframes to get the mean and mode
distance_mean =[]
energy_mean = []
steps_mean = []
heart_rate=[]
duration_mean = []
day_part_most=[]
frequency = []
empty_data = []
number_of_time = 0
number_of_days = []
morning_steps = []
noon_steps = []
afternoon_steps = []
evening_steps= []
night_steps=[]
morning_count = []
noon_count = []
afternoon_count = []       
evening_count = []
night_count=[]
morning_time =[]
noon_time = []
afternoon_time =[]
evening_time = []
night_time = []
        
morning_energy =[]
noon_energy = []
afternoon_energy = []
evening_energy =[]
night_energy = []

morning_distance = []
noon_distance = []
afternoon_distance =[]
evening_distance =[]
night_distance =[]

morning_heart = []
noon_heart = []
afternoon_heart = []
evening_heart = []
night_heart = []
for i in range(0, len(content)):

    ###in some files the start time is equal to zero so I droped them
    content[i] = content[i][content[i]['startTime'] != 0]
    ###in some of them it is equal to HKWorkoutTypeIdentifier so I also droped them
    content[i] = content[i][content[i]['startTime'] != 'HKWorkoutTypeIdentifier']
    if content[i].empty == True:
        empty_data.append(i)
        
    else:
        #content[i].reset_index(inplace = True, drop = True)
        content[i].reset_index(inplace = True, drop = True)
    ###bc of these conditions we might have some empty dataframes, so I will change the index

        content[i].reset_index(inplace = True, drop = True)
    
    ###droping +1:00
        content[i] = content[i].replace(to_replace=re.escape('+01:00'), value=' ', regex=True)
    
    ###replace T with ' '
        content[i] = content[i].replace(to_replace='T', value=' ', regex=True)
    #convert start time to date_time
        content[i]['startTime'] = pd.to_datetime(content[i]['startTime'],utc=True,errors='coerce')
    #convert end time to data time
        content[i]['endTime'] = pd.to_datetime(content[i]['endTime'],utc=True,errors='coerce')
        content[i] = content[i].sort_values(['startTime'], ascending=[True])
        content[i].reset_index(inplace = True, drop = True)
    ###duration calculation
        content[i]['Duration'] = (content[i]['endTime']-content[i]['startTime'])/np.timedelta64(1,'m')
    
        content[i]= content[i][content[i]['Duration']>=0]
        content[i].reset_index(inplace = True, drop = True)
    ###only save the hour
        list_of_hours =[]
        list_of_steps = []
        list_of_heart_rate = []
        list_of_energy = []
        list_of_distance = []
        list_of_days =[]
        list_exc = []
        for j in range(0,len(content[i])):
            day = content[i]['startTime'][j].day
            list_of_days.append(day)
            if content[i]['unit'][j] == 'count' and content[i]['Duration'][j]>15:
                list_exc.append(1)
            else:
                list_exc.append(0)
            hour = content[i]['startTime'][j].hour
            list_of_hours.append(hour)
            if content[i]['unit'][j] == 'count':
                steps = content[i]['value'][j]
                list_of_steps.append(steps)
                list_of_heart_rate.append(0)
                list_of_energy.append(0)
                list_of_distance.append(0)
            elif content[i]['unit'][j] == 'count/s':
                heart = content[i]['value'][j]
                list_of_steps.append(0)
                list_of_heart_rate.append(heart)
                list_of_energy.append(0)
                list_of_distance.append(0)
            elif content[i]['unit'][j] == 'm':
                distance = content[i]['value'][j]
                list_of_steps.append(0)
                list_of_heart_rate.append(0)
                list_of_energy.append(0)
                list_of_distance.append(distance)
            else: 
                energy = content[i]['value'][j]
                list_of_steps.append(0)
                list_of_heart_rate.append(0)
                list_of_energy.append(energy)
                list_of_distance.append(0)
        content[i]['day_date']=np.array(content[i]['startTime'].values, dtype='datetime64[D]')
    #content[i]['day_date']=list_of_days
        content[i]['freq'] = list_exc
        df=content[i].groupby(["day_date"]).sum().sort_values(["freq"], ascending=False).reset_index()
        content[i]['Hour']=list_of_hours
        content[i]['Steps'] = list_of_steps
        content[i]['Heart'] = list_of_heart_rate
        content[i]['Distance'] = list_of_distance
        content[i]['Energy'] = list_of_energy
        day_section_list =[]
        for k in range(0,len(content[i])):
            if content[i]['Hour'][k] < 11:
                day_section_list.append('morning')
            elif (content[i]['Hour'][k]>=11 and content[i]['Hour'][k]<13):
                day_section_list.append('noon')
            elif (content[i]['Hour'][k]>=13 and content[i]['Hour'][k]<17):
                day_section_list.append('afternoon')
            elif (content[i]['Hour'][k]>=17 and content[i]['Hour'][k]<19):
                day_section_list.append('evening')
            else:
                day_section_list.append('night')
        content[i]['day_part']=day_section_list
    #print(i)
    
        if content[i]['Distance'].dtype == object:
            content[i]['Distance'] = content[i]['Distance'].replace(to_replace=['other','m','distance','5.0000005.00000010.00000010.00000016.00000016.0000005.0000005.00000010.0000008.00000010.0000005.0000008.0000005.00000012.00000012.00000027.000000'],
                                                                value=0)
        #content[i] = content[i][content[i]['Distance'].str.contains('other') == False]
        #content[i] = content[i][content[i]['Distance'].str.contains('m') == False]
        #content[i] = content[i][content[i]['Distance'].str.contains('distance') == False]
        #content[i] = content[i][content[i]['Distance'].str.contains('5.0000005.00000010.00000010.00000016.00000016.0000005.0000005.00000010.0000008.00000010.0000005.0000008.0000005.00000012.00000012.00000027.000000') == False]
        content[i]['Distance'] = pd.to_numeric(content[i]['Distance'], downcast="float")
    
    
        if content[i]['Energy'].dtype == object:
            content[i]['Energy'] = content[i]['Energy'].replace(to_replace=["other","m","cal","kg","value","count/s","count",
                                                                        "RHY HM+","iPhone 6","mmHg","(null)"], value=0)
            content[i]['Energy']=content[i]['Energy'].replace(to_replace='FLAVIO*', value=0, regex=True)
            content[i]['Energy']=content[i]['Energy'].replace(to_replace='Robert*', value=0, regex=True)
        #content[i] = content[i][content[i]['Energy'].str.contains('other','m') == False]
        #content[i] = content[i][content[i]['Energy'].str.contains('m') == False]
        #content[i] = content[i][content[i]['Energy'].str.contains('cal') == False]
        #content[i] = content[i][content[i]['Energy'].str.contains('value') == False]
        content[i]['Energy'] = pd.to_numeric(content[i]['Energy'], downcast="float")
        content[i]['Heart'] = pd.to_numeric(content[i]['Heart'], downcast="float")
        content[i]['Steps'] = pd.to_numeric(content[i]['Steps'], downcast="float")
        if content[i].empty == True:
            empty_data.append(i)
        else:
    
            content[i].reset_index(inplace = True, drop = True)
            morning_count.append(len(content[i][(content[i]['day_part'] == 'morning')]))
            noon_count.append(len(content[i][(content[i]['day_part'] == 'noon')]))
            afternoon_count.append(len(content[i][(content[i]['day_part'] == 'afternoon')]))       
            evening_count.append(len(content[i][(content[i]['day_part'] == 'evening')]))
            night_count.append(len(content[i][(content[i]['day_part'] == 'night')]))
    ###day part active time sum
            morning_time.append(content[i][(content[i]['day_part'] == 'morning')]['Duration'].sum())
            noon_time.append(content[i][(content[i]['day_part'] == 'noon')]['Duration'].sum())
            afternoon_time.append(content[i][(content[i]['day_part'] == 'afternoon')]['Duration'].sum())
            evening_time.append(content[i][(content[i]['day_part'] == 'evening') ]['Duration'].sum())
            night_time.append(content[i][(content[i]['day_part'] == 'night')]['Duration'].sum())
        
            morning_energy.append(content[i][(content[i]['day_part'] == 'morning')]['Energy'].sum())
            noon_energy.append(content[i][(content[i]['day_part'] == 'noon')]['Energy'].sum())
            afternoon_energy.append(content[i][(content[i]['day_part'] == 'afternoon')]['Energy'].sum())
            evening_energy.append(content[i][(content[i]['day_part'] == 'evening')]['Energy'].sum())
            night_energy.append(content[i][(content[i]['day_part'] == 'night')]['Energy'].sum())

            morning_distance.append(content[i][(content[i]['day_part'] == 'morning')]['Distance'].sum())
            noon_distance.append(content[i][(content[i]['day_part'] == 'noon')]['Distance'].sum())
            afternoon_distance.append(content[i][(content[i]['day_part'] == 'afternoon')]['Distance'].sum())
            evening_distance.append(content[i][(content[i]['day_part'] == 'evening')]['Distance'].sum())
            night_distance.append(content[i][(content[i]['day_part'] == 'night')]['Distance'].sum())
    
            morning_steps.append(content[i][(content[i]['day_part'] == 'morning')]['Steps'].sum())
            noon_steps.append(content[i][(content[i]['day_part'] == 'noon')]['Steps'].sum())
            afternoon_steps.append(content[i][(content[i]['day_part'] == 'afternoon')]['Steps'].sum())
            evening_steps.append(content[i][(content[i]['day_part'] == 'evening')]['Steps'].sum())
            night_steps.append(content[i][(content[i]['day_part'] == 'night')]['Steps'].sum())
    
            morning_heart.append(content[i][(content[i]['day_part'] == 'morning')]['Heart'].sum())
            noon_heart.append(content[i][(content[i]['day_part'] == 'noon')]['Heart'].sum())
            afternoon_heart.append(content[i][(content[i]['day_part'] == 'afternoon')]['Heart'].sum())
            evening_heart.append(content[i][(content[i]['day_part'] == 'evening')]['Heart'].sum())
            night_heart.append(content[i][(content[i]['day_part'] == 'night')]['Heart'].sum())
            days = 0
            if len(content[i])>1:
                for m in range(len(content[i])-1):
                    if content[i]['startTime'][m].date !=  content[i]['startTime'][m+1].date:
                        days = days+1
            else:
                        days = days+1
            
            number_of_days.append(days)
            duration_mean.append(content[i]['Duration'].sum()/days)
            day_part_most.append(content[i]['day_part'].mode()[0])

            distance_mean.append(content[i]['Distance'].sum()/days)
            energy_mean.append(content[i]['Energy'].sum()/days)
            steps_mean.append(content[i]['Steps'].sum()/days)
            heart_rate.append(content[i]['Heart'].sum()/days)
            frequency.append(df['freq'].mean())
            
###deleting empty data frames
to_delet = []
for i in range(0,len(empty_data)):
    to_delet.append(files_finding.keys()[empty_data[i]])
    
###making a new data frame based on non empty ones
S = files_finding.drop(to_delet)
health_code=S.keys()
    
data={'code':health_code, 'duration':duration_mean, 'day_part':day_part_most, 'heart_rate':heart_rate, 'steps':steps_mean,
     'energy': energy_mean,'distance':distance_mean,'freq':frequency,'number_of_days':number_of_days,'night_heart':night_heart,
      'evening_heart':evening_heart,
     'afternoon_heart':afternoon_heart,'noon_heart':noon_heart,'morning_heart':morning_heart,'night_steps':night_steps,
     'evening_steps':evening_steps,'afternoon_steps':afternoon_steps,'noon_steps':noon_steps,'morning_steps':morning_steps,
      'night_distance':night_distance,'evening_distance':evening_distance,'afternoon_distance':afternoon_distance,
      'noon_distance':noon_distance,'morning_distance':morning_distance,'night_energy':night_energy,'evening_energy':evening_energy,
      'afternoon_energy':afternoon_energy,'noon_energy':noon_energy,'morning_energy':morning_energy,'night_time':night_time,
      'evening_time':evening_time,'afternoon_time':afternoon_time,'noon_time':noon_time,'morning_time':morning_time,
      'night_count':night_count,'evening_count':evening_count,'afternoon_count':afternoon_count,'noon_count':noon_count,
      'morning_count':morning_count
     }
# Create DataFrame
df1 = pd.DataFrame(data)

df1.to_csv("healthkit_data.csv")

