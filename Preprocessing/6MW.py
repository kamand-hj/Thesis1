#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import synapseclient
import pandas as pd
import numpy as np
import synapseclient
import json
from matplotlib import pyplot as plt
import os
import glob
import regex as re
import cmath

syn = synapseclient.Synapse()
syn.login('Kamand', 'Kamand13579-')
query = syn.tableQuery("SELECT * FROM syn16782058")
data = query.asDataFrame()
files_finding= data.groupby('healthCode')['UnknownFile_1.json.items'].apply(list)

###making an array of dataframes from json files
content = []
content_kit =[]
empty_data = []
for i in range (0,len(files_finding)):
    
    file_founded_length = len(files_finding[i])
    
    #df = pd.DataFrame([])A
    list_of_dfs = []
    #print(list_of_dfs)
    for k in range(0,file_founded_length):
        #df = pd.DataFrame([])
        
        #data_frame = pd.DataFrame()
        #content = []
        for j in range(0,999):
            path = 'C:/leiden/master nl/thesis/mathias/data/6mw/'+str(j)+'/'+str(files_finding[i][k])
            #print(path)
            #print(files)
            if os.path.exists(path) == True:
                files = glob.glob(path + "/*.tmp")
                with open(files[0]) as f:
                       data = json.load(f)
                #df1 = pd.read_csv(files[0], sep=';', header=None,index_col=None)
                #df1 = pd.read_csv(files[0], sep=',', header=None,index_col=None)
                #df1 = pd.read_csv(files[0],sep=',', usecols = ['startTime','endTime','type','value',
                                                               #'unit','source','sourceIdentifier'])
               
                #print(df1)
                if type(data) == dict:
                    data_list = {'displacement':[data['displacement']],'time':[data['timestamp']]}
                    df_displace=pd.DataFrame(data_list)
                    list_of_dfs.append(df_displace) 
                else:   
                    displacement_list=[]
                    time_list = []
                    for l in range(0,len(data)): 
                        displacement_list.append(data[l]['displacement'])
                        time_list.append(data[l]['timestamp'])
                    data_list = {'displacement':displacement_list,'time':time_list}
                    df_displace=pd.DataFrame(data_list)
                    list_of_dfs.append(df_displace) 
             
            else:
                j=j+1
      
            
    #print(i)    
    #print(j)
    #print(k)
    if len(list_of_dfs) == 0:
        empty_data.append(i)
        i = i+1
    else:
        b = pd.concat(list_of_dfs, ignore_index=True)            
        content.append(b)  
        content_kit.append(b)
        
valid_dis =[]
for i in range(0, len(content)):
    content[i] = content[i].replace(to_replace=re.escape('+01:00'), value=' ', regex=True)
    content[i] = content[i].replace(to_replace='T', value=' ', regex=True)
    content[i]['time'] = pd.to_datetime(content[i]['time'],utc=True,errors='coerce')
    if ((max(content[i]['time']) - min(content[i]['time']))/np.timedelta64(1, 'm')) >= 6:
        #last_day = max(content[i]['time']).day
        #last_month = max(content[i]['time']).month
        content[i]['day_date']=np.array(content[i]['time'].values, dtype='datetime64[D]')
        last_date = max(content[i]['day_date'])
        dis_new=0
        last_try =[]
        for j in range(len(content[i])):
            if  content[i]['day_date'][j]==last_date:
                last_try.append(content[i]['time'][j])
                dis_new=content[i]['displacement'][j] + dis_new
            else:
                j=j+1
        ###there are some dataframes with only one row, this line is for not considering them
        if ((max(last_try) - min(last_try))/np.timedelta64(1, 'm'))>=6 and ((max(last_try) - min(last_try))/np.timedelta64(1, 'm')) <=8:
            valid_dis.append(dis_new)
        else:
            valid_dis.append(None)
    else:
            valid_dis.append(None)
            
###deleting empty data frames
to_delet = []
for i in range(0,len(empty_data)):
    to_delet.append(files_finding.keys()[empty_data[i]])
    
###making a new data frame based on non empty ones
S = files_finding.drop(to_delet)
health_code=S.keys()

data_walk={'code':health_code, 'displacement':valid_dis}
# Create DataFrame
six_mw = pd.DataFrame(data_walk)

six_mw = six_mw.dropna()

