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
query = syn.tableQuery("SELECT * FROM syn16782060")
work_out = query.asDataFrame()
files_finding= work_out.groupby('healthCode')['data.csv'].apply(list)

###making an array of dataframes from csv files
content = []
content1 =[]
content2 = []
for i in range (0,len(files_finding)):
    
    file_founded_length = len(files_finding[i])
    
    #df = pd.DataFrame([])
    list_of_dfs = []
    #print(list_of_dfs)
    for k in range(0,file_founded_length):
        #df = pd.DataFrame([])
        
        #data_frame = pd.DataFrame()
        #content = []
        for j in range(0,999):
            path = 'C:/leiden/master nl/thesis/mathias/data/workout/'+str(j)+'/'+str(files_finding[i][k])
            #print(path)
            #print(files)
            if os.path.exists(path) == True:
                files = glob.glob(path + "/*.csv")
                #df1 = pd.read_csv(files[0], sep=';', header=None,index_col=None)
                #df1 = pd.read_csv(files[0], sep=',', header=None,index_col=None)
                df1 = pd.read_csv(files[0],sep=',', usecols = ['startTime', 'endTime', 'type',
                                                           'workoutType','total.distance','unit','energy.consumed',
                                                           'unit.1','source','sourceIdentifier'])
               
                #print(df1)
                list_of_dfs.append(df1) 
                
            else:
                j=j+1
            
    #print(i)       
    b = pd.concat(list_of_dfs, ignore_index=True)            
    content.append(b)  
    content1.append(b)
    content2.append(b)
    
###########considering unknown start and end time and omit those data
###preprocessing all the dataframes to get the mean and mode
distance_mean =[]
energy_mean = []
duration_mean = []
day_part_most=[]
frequency = []
empty_data = []

archery_duration = []
archery_count = []
bowling_duration = []
bowling_count = []
fencing_duration = []
fencing_count = []

gymnastics_duration = []
gymnastics_count = []

trackAndField_duration = []
trackAndField_count = []

americanFootball_duration = []
americanFootball_count = []

americanFootball_duration = []
americanFootball_count = []

australianFootball_duration = []
australianFootball_count = []

baseball_duration = []
baseball_count = []

baseball_duration = []
baseball_count = []

basketball_duration = []
basketball_count = []

cricket_duration = []
cricket_count = []

discSports_duration = []
discSports_count = []

handball_duration = []
handball_count = []

hockey_duration = []
hockey_count = []

lacrosse_duration = []
lacrosse_count = []

rugby_duration = []
rugby_count = []

soccer_duration = []
soccer_count = []

softball_duration = []
softball_count = []

volleyball_duration = []
volleyball_count = []

preparationAndRecovery_duration = []
preparationAndRecovery_count = []

flexibility_duration = []
flexibility_count = []

cooldown_duration = []
cooldown_count = []

walking_duration = []
walking_count = []

running_duration = []
running_count = []

wheelchairWalkPace_duration = []
wheelchairWalkPace_count = []

wheelchairRunPace_duration = []
wheelchairRunPace_count = []

cycling_duration = []
cycling_count = []

handCycling_duration = []
handCycling_count = []

coreTraining_duration = []
coreTraining_count = []

elliptical_duration = []
elliptical_count = []

functionalStrengthTraining_duration = []
functionalStrengthTraining_count = []

traditionalStrengthTraining_duration = []
traditionalStrengthTraining_count = []

crossTraining_duration = []
crossTraining_count = []

mixedCardio_duration = []
mixedCardio_count = []

highIntensityIntervalTraining_duration = []
highIntensityIntervalTraining_count = []

jumpRope_duration = []
jumpRope_count = []

stairClimbing_duration = []
stairClimbing_count = []

stairs_duration = []
stairs_count = []

stepTraining_duration = []
stepTraining_count = []

fitnessGaming_duration = []
fitnessGaming_count = []

barre_duration = []
barre_count = []

cardioDance_duration = []
cardioDance_count = []

socialDance_duration = []
socialDance_count = []

yoga_duration = []
yoga_count = []

mindAndBody_duration = []
mindAndBody_count = []

pilates_duration = []
pilates_count = []

badminton_duration = []
badminton_count = []

pickleball_duration = []
pickleball_count = []

racquetball_duration = []
racquetball_count = []

squash_duration = []
squash_count = []

tableTennis_duration = []
tableTennis_count = []

tennis_duration = []
tennis_count = []

climbing_duration = []
climbing_count = []

equestrianSports_duration = []
equestrianSports_count = []

fishing_duration = []
fishing_count = []

golf_duration = []
golf_count = []

hiking_duration = []
hiking_count = []

hunting_duration = []
hunting_count = []

play_duration = []
play_count = []

crossCountrySkiing_duration = []
crossCountrySkiing_count = []

curling_duration = []
curling_count = []

downhillSkiing_duration = []
downhillSkiing_count = []

snowSports_duration = []
snowSports_count = []

snowboarding_duration = []
snowboarding_count = []

skatingSports_duration = []
skatingSports_count = []

paddleSports_duration = []
paddleSports_count = []

rowing_duration = []
rowing_count = []

sailing_duration = []
sailing_count = []

surfingSports_duration = []
surfingSports_count = []

swimming_duration = []
swimming_count = []

waterFitness_duration = []
waterFitness_count = []

waterPolo_duration = []
waterPolo_count = []

waterSports_duration = []
waterSports_count = []

boxing_duration = []
boxing_count = []

kickboxing_duration = []
kickboxing_count = []

martialArts_duration = []
martialArts_count = []

taiChi_duration = []
taiChi_count = []

wrestling_duration = []
wrestling_count = []

other_duration = []
other_count = []

dance_duration = []
dance_count = []

danceInspiredTraining_duration = []
danceInspiredTraining_count = []

mixedMetabolicCardioTraining_duration = []
mixedMetabolicCardioTraining_count = []

swimBikeRun_duration = []
swimBikeRun_count = []

transition_duration = []
transition_count = []


morning_time = []
noon_time = []
afternoon_time = []
evening_time = []
night_time = []

morning_count = []
noon_count = []
afternoon_count = []
evening_count = []
night_count = []

morning_energy = []
noon_energy = []
afternoon_energy = []
evening_energy = []
night_energy = []

morning_distance = []
noon_distance = []
afternoon_distance = []
evening_distance = []
night_distance = []

number_of_days = []
for i in range(0, len(content)):

    ###in some files the start time is equal to zero so I droped them
    content[i] = content[i][content[i]['startTime'] != 0]
    ###in some of them it is equal to HKWorkoutTypeIdentifier so I also droped them
    content[i] = content[i][content[i]['startTime'] != 'HKWorkoutTypeIdentifier']
    ###bc of these conditions we might have some empty dataframes, so I will change the index
    if content[i].empty == True:
        empty_data.append(i)
        
    else:
        #content[i].reset_index(inplace = True, drop = True)
        content[i].reset_index(inplace = True, drop = True)
    
    ###droping +1:00
        content[i] = content[i].replace(to_replace=re.escape('+01:00'), value=' ', regex=True)
    ###replace T with ' '
        content[i]['startTime'] = content[i]['startTime'].replace(to_replace='T', value=' ', regex=True)
        content[i]['endTime'] = content[i]['endTime'].replace(to_replace='T', value=' ', regex=True)
    #convert start time to date_time
        content[i]['startTime'] = pd.to_datetime(content[i]['startTime'],utc=True,errors='coerce')
    #convert end time to data time
        content[i]['endTime'] = pd.to_datetime(content[i]['endTime'],utc=True,errors='coerce')
    ###make it ascending based on date for not having negative time values
        content[i] = content[i].sort_values(['startTime'], ascending=[True])
        content[i].reset_index(inplace = True, drop = True)
    ###duration calculation
        content[i]['Duration'] = (content[i]['endTime']-content[i]['startTime'])/np.timedelta64(1,'m')
    #if i == 31 or i==37 or i==83 or i==84:
        #if type(content[i]['total.distance'][0])==str:
            #content[i]['Duration'] = None
            #content[i]['energy.consumed'] = content[i]['unit']
            #content[i]['total.distance'] = content[i]['workoutType']
            #content[i]['workoutType'] = content[i]['type']
        for l in range(len(content[i])):
            if type(content[i]['total.distance'].iloc[l])==str:
                content[i]['Duration'].iloc[l] = None
                content[i]['energy.consumed'].iloc[l] = content[i]['unit'].iloc[l]
                content[i]['total.distance'].iloc[l] = content[i]['workoutType'].iloc[l]
                content[i]['workoutType'].iloc[l] = content[i]['type'].iloc[l]
        content[i]=content[i].dropna(axis=0, subset=['startTime'])
    
    ###only save the hour
        list_of_hours =[]
        #list_of_days =[]
        list_exc = []
        
        for j in range(0,len(content[i])):
            
            #day = content[i]['startTime'][j].day
            #day = content[i]['startTime'][j].date
            #list_of_days.append(day)
            if all(pd.isnull(content[i]['Duration'])) != True:
                if content[i]['Duration'][j]>15:
                    list_exc.append(1)
                else:
                    list_exc.append(0)
            else:
                list_exc.append(None)
            hour = content[i]['startTime'][j].hour
            list_of_hours.append(hour)
        content[i]['Hour']=list_of_hours
        day_section_list =[]
        #content[i]['day_date']=list_of_days
        content[i]['day_date']=np.array(content[i]['startTime'].values, dtype='datetime64[D]')
        content[i]['freq'] = list_exc
        if all(pd.isnull(content[i]['Duration'])) != True:
            df=content[i].groupby(["day_date"]).sum().sort_values(["freq"], ascending=False).reset_index()
    #print('after if all', i,content[i])
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
    #print('after day part',i,content[i])
    #print(i)

    #print('after day part sum',i,content[i])
        #print(i)
        #if (pd.isnull(content[i]['startTime'][-1]))==True:
            #content[i]['startTime'] = content[i]['startTime'][:-1]
        #
    ###apparently in distance there was some 'other' as value which I drop the related rows. not sure whether it is ok or not
        #if content[i]['total.distance'].dtype == object:
        if content[i]['total.distance'].dtype == str:
            content[i] = content[i][content[i]['total.distance'].str.contains('other') == False]
            content[i] = content[i][content[i]['total.distance'].str.contains('m') == False]
            content[i] = content[i][content[i]['total.distance'].str.contains('total distance') == False]
            content[i] = content[i][content[i]['total.distance'].str.contains('kcal') == False]
            #content[i] = content[i][content[i]['total.distance'].str.contains('HKWorkoutActivityTypeMixedMetabolicCardioTraining') == False]
        #content[i] = content[i][content[i]['total.distance'].str.contains('HKWorkoutActivityTypeOther') == False]
            content[i] = content[i][content[i]['total.distance'].str.contains('5.0000005.00000010.00000010.00000016.00000016.0000005.0000005.00000010.0000008.00000010.0000005.0000008.0000005.00000012.00000012.00000027.000000') == False]
        elif content[i]['total.distance'].dtype == object:
            content[i] = content[i][content[i]['total.distance'].astype(str).str.contains('kcal') == False]
            content[i] = content[i][content[i]['total.distance'].astype(str).str.contains('HKWorkoutActivityTypeCycling') == False]
            content[i] = content[i][content[i]['total.distance'].astype(str).str.contains('HKWorkoutActivityTypeMixedMetabolicCardioTraining') == False]
            content[i] = content[i][content[i]['total.distance'].astype(str).str.contains('HKWorkoutActivityTypeWalking') == False]  
        content[i]['total.distance'] = pd.to_numeric(content[i]['total.distance'], downcast="float")
        #if content[i]['energy.consumed'].dtype == object:
        if content[i]['energy.consumed'].dtype == str:
            content[i] = content[i][content[i]['energy.consumed'].str.contains('other','m') == False]
        content[i]['energy.consumed'] = pd.to_numeric(content[i]['energy.consumed'], downcast="float")
    

        
        if content[i].empty == True:
            empty_data.append(i)
        
        else:
            content[i].reset_index(inplace = True, drop = True)
            days = 0
            if len(content[i])>1:
                for m in range(len(content[i])-1):
                    if content[i]['startTime'][m].date !=  content[i]['startTime'][m+1].date:
                        days = days+1
            else:
                    days = days+1
            
            number_of_days.append(days)
            
            ####counting the number of activities
            transition_count.append((content[i].workoutType.astype(str).str.contains('Transition')).sum())
            swimBikeRun_count.append((content[i].workoutType.astype(str).str.contains('SwimBikeRun')).sum())
            mixedMetabolicCardioTraining_count.append((content[i].workoutType.astype(str).str.contains('MixedMetabolicCardioTraining')).sum())
            danceInspiredTraining_count.append((content[i].workoutType.astype(str).str.contains('DanceInspiredTraining')).sum())
            dance_count.append((content[i].workoutType.astype(str).str.contains('Dance')).sum())
            other_count.append((content[i].workoutType.astype(str).str.contains('Other')).sum())
            wrestling_count.append((content[i].workoutType.astype(str).str.contains('Wrestling')).sum())
            taiChi_count.append((content[i].workoutType.astype(str).str.contains('TaiChi')).sum())
            martialArts_count.append((content[i].workoutType.astype(str).str.contains('MartialArts')).sum())
            kickboxing_count.append((content[i].workoutType.astype(str).str.contains('Kickboxing')).sum())
            boxing_count.append((content[i].workoutType.astype(str).str.contains('Boxing')).sum())
            waterSports_count.append((content[i].workoutType.astype(str).str.contains('WaterSports')).sum())
            waterPolo_count.append((content[i].workoutType.astype(str).str.contains('WaterPolo')).sum())
            waterFitness_count.append((content[i].workoutType.astype(str).str.contains('WaterFitness')).sum())
            swimming_count.append((content[i].workoutType.astype(str).str.contains('Swimming')).sum())
            surfingSports_count.append((content[i].workoutType.astype(str).str.contains('SurfingSports')).sum())
            sailing_count.append((content[i].workoutType.astype(str).str.contains('Sailing')).sum())
            rowing_count.append((content[i].workoutType.astype(str).str.contains('Rowing')).sum())
            paddleSports_count.append((content[i].workoutType.astype(str).str.contains('PaddleSports')).sum())
            skatingSports_count.append((content[i].workoutType.astype(str).str.contains('SkatingSports')).sum())
            snowboarding_count.append((content[i].workoutType.astype(str).str.contains('Snowboarding')).sum())
            snowSports_count.append((content[i].workoutType.astype(str).str.contains('SnowSports')).sum())
            downhillSkiing_count.append((content[i].workoutType.astype(str).str.contains('DownhillSkiing')).sum())
            curling_count.append((content[i].workoutType.astype(str).str.contains('Curling')).sum())
            crossCountrySkiing_count.append((content[i].workoutType.astype(str).str.contains('CrossCountrySkiing')).sum())
            play_count.append((content[i].workoutType.astype(str).str.contains('Play')).sum())
            hunting_count.append((content[i].workoutType.astype(str).str.contains('Hunting')).sum())
            hiking_count.append((content[i].workoutType.astype(str).str.contains('Hiking')).sum())
            golf_count.append((content[i].workoutType.astype(str).str.contains('Golf')).sum())
            fishing_count.append((content[i].workoutType.astype(str).str.contains('Fishing')).sum())
            equestrianSports_count.append((content[i].workoutType.astype(str).str.contains('EquestrianSports')).sum())
            climbing_count.append((content[i].workoutType.astype(str).str.contains('Climbing')).sum())
            tennis_count.append((content[i].workoutType.astype(str).str.contains('Tennis')).sum())
            tableTennis_count.append((content[i].workoutType.astype(str).str.contains('TableTennis')).sum())
            squash_count.append((content[i].workoutType.astype(str).str.contains('Squash')).sum())
            racquetball_count.append((content[i].workoutType.astype(str).str.contains('Racquetball')).sum())
            pickleball_count.append((content[i].workoutType.astype(str).str.contains('Pickleball')).sum())
            badminton_count.append((content[i].workoutType.astype(str).str.contains('Badminton')).sum())
            pilates_count.append((content[i].workoutType.astype(str).str.contains('Pilates')).sum())
            mindAndBody_count.append((content[i].workoutType.astype(str).str.contains('MindAndBody')).sum())
            yoga_count.append((content[i].workoutType.astype(str).str.contains('Yoga')).sum())
            socialDance_count.append((content[i].workoutType.astype(str).str.contains('SocialDance')).sum())
            cardioDance_count.append((content[i].workoutType.astype(str).str.contains('CardioDance')).sum())
            barre_count.append((content[i].workoutType.astype(str).str.contains('Barre')).sum())
            fitnessGaming_count.append((content[i].workoutType.astype(str).str.contains('FitnessGaming')).sum())
            stepTraining_count.append((content[i].workoutType.astype(str).str.contains('StepTraining')).sum())
            stairs_count.append((content[i].workoutType.astype(str).str.contains('Stairs')).sum())
            stairClimbing_count.append((content[i].workoutType.astype(str).str.contains('StairClimbing')).sum())
            jumpRope_count.append((content[i].workoutType.astype(str).str.contains('JumpRope')).sum())
            highIntensityIntervalTraining_count.append((content[i].workoutType.astype(str).str.contains('HighIntensityIntervalTraining')).sum())
            mixedCardio_count.append((content[i].workoutType.astype(str).str.contains('MixedCardio')).sum())
            crossTraining_count.append((content[i].workoutType.astype(str).str.contains('CrossTraining')).sum())
            traditionalStrengthTraining_count.append((content[i].workoutType.astype(str).str.contains('TraditionalStrengthTraining')).sum())
            archery_count.append((content[i].workoutType.astype(str).str.contains('Walking')).sum())
            bowling_count.append((content[i].workoutType.astype(str).str.contains('Bowling')).sum())
            fencing_count.append((content[i].workoutType.astype(str).str.contains('Fencing')).sum())
            gymnastics_count.append((content[i].workoutType.astype(str).str.contains('Gymnastics')).sum())
            trackAndField_count.append((content[i].workoutType.astype(str).str.contains('TrackAndField')).sum())
            americanFootball_count.append((content[i].workoutType.astype(str).str.contains('AmericanFootball')).sum())
            australianFootball_count.append((content[i].workoutType.astype(str).str.contains('AustralianFootball')).sum())
            baseball_count.append((content[i].workoutType.astype(str).str.contains('Baseball')).sum())
            basketball_count.append((content[i].workoutType.astype(str).str.contains('Basketball')).sum())
            cricket_count.append((content[i].workoutType.astype(str).str.contains('Cricket')).sum())
            discSports_count.append((content[i].workoutType.astype(str).str.contains('DiscSports')).sum())
            handball_count.append((content[i].workoutType.astype(str).str.contains('Handball')).sum())
            hockey_count.append((content[i].workoutType.astype(str).str.contains('Hockey')).sum())
            lacrosse_count.append((content[i].workoutType.astype(str).str.contains('Lacrosse')).sum())
            rugby_count.append((content[i].workoutType.astype(str).str.contains('Rugby')).sum())
            soccer_count.append((content[i].workoutType.astype(str).str.contains('Soccer')).sum())
            softball_count.append((content[i].workoutType.astype(str).str.contains('Softball')).sum())
            volleyball_count.append((content[i].workoutType.astype(str).str.contains('Volleyball')).sum())
            preparationAndRecovery_count.append((content[i].workoutType.astype(str).str.contains('PreparationAndRecovery')).sum())
            flexibility_count.append((content[i].workoutType.astype(str).str.contains('Flexibility')).sum())
            cooldown_count.append((content[i].workoutType.astype(str).str.contains('Cooldown')).sum())
            walking_count.append((content[i].workoutType.astype(str).str.contains('Walking')).sum())
            running_count.append((content[i].workoutType.astype(str).str.contains('Running')).sum())
            wheelchairWalkPace_count.append((content[i].workoutType.astype(str).str.contains('WheelchairWalkPace')).sum())
            wheelchairRunPace_count.append((content[i].workoutType.astype(str).str.contains('WheelchairRunPace')).sum())
            cycling_count.append((content[i].workoutType.astype(str).str.contains('Cycling')).sum())
            handCycling_count.append((content[i].workoutType.astype(str).str.contains('HandCycling')).sum())
            coreTraining_count.append((content[i].workoutType.astype(str).str.contains('CoreTraining')).sum())
            elliptical_count.append((content[i].workoutType.astype(str).str.contains('Elliptical')).sum())
            functionalStrengthTraining_count.append((content[i].workoutType.astype(str).str.contains('FunctionalStrengthTraining')).sum())
        
    
                 ###counting different day part
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
        
            morning_energy.append(content[i][(content[i]['day_part'] == 'morning')]['energy.consumed'].sum())
            noon_energy.append(content[i][(content[i]['day_part'] == 'noon')]['energy.consumed'].sum())
            afternoon_energy.append(content[i][(content[i]['day_part'] == 'afternoon')]['energy.consumed'].sum())
            evening_energy.append(content[i][(content[i]['day_part'] == 'evening')]['energy.consumed'].sum())
            night_energy.append(content[i][(content[i]['day_part'] == 'night')]['energy.consumed'].sum())

            morning_distance.append(content[i][(content[i]['day_part'] == 'morning')]['total.distance'].sum())
            noon_distance.append(content[i][(content[i]['day_part'] == 'noon')]['total.distance'].sum())
            afternoon_distance.append(content[i][(content[i]['day_part'] == 'afternoon')]['total.distance'].sum())
            evening_distance.append(content[i][(content[i]['day_part'] == 'evening')]['total.distance'].sum())
            night_distance.append(content[i][(content[i]['day_part'] == 'night')]['total.distance'].sum())

    ###CALCULATING THE DURATION  
            transition_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Transition') == True)]['Duration'].sum())
            swimBikeRun_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('SwimBikeRun') == True)]['Duration'].sum())
            mixedMetabolicCardioTraining_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('MixedMetabolicCardioTraining') == True)]['Duration'].sum())
            danceInspiredTraining_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('DanceInspiredTraining') == True)]['Duration'].sum())
            dance_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Dance') == True)]['Duration'].sum())
            other_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Other') == True)]['Duration'].sum())
            wrestling_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Wrestling') == True)]['Duration'].sum())
            taiChi_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('TaiChi') == True)]['Duration'].sum())
            martialArts_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('AartialArts') == True)]['Duration'].sum())
            kickboxing_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Kickboxing') == True)]['Duration'].sum())
            boxing_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Boxing') == True)]['Duration'].sum())
            waterSports_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('WaterSports') == True)]['Duration'].sum())
            waterPolo_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('WaterPolo') == True)]['Duration'].sum())
            waterFitness_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('WaterFitness') == True)]['Duration'].sum())
            swimming_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Swimming') == True)]['Duration'].sum())
            surfingSports_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('SurfingSports') == True)]['Duration'].sum())
            sailing_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Sailing') == True)]['Duration'].sum())
            rowing_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Sowing') == True)]['Duration'].sum())
            paddleSports_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('PaddleSports') == True)]['Duration'].sum())
            skatingSports_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('SkatingSports') == True)]['Duration'].sum())
            snowboarding_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Snowboarding') == True)]['Duration'].sum())
            snowSports_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('SnowSports') == True)]['Duration'].sum())
            downhillSkiing_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('DownhillSkiing') == True)]['Duration'].sum())
            curling_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Curling') == True)]['Duration'].sum())
            crossCountrySkiing_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('CrossCountrySkiing') == True)]['Duration'].sum())
            play_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Play') == True)]['Duration'].sum())
            hunting_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Hunting') == True)]['Duration'].sum())
            hiking_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Hiking') == True)]['Duration'].sum())
            golf_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Golf') == True)]['Duration'].sum())
            fishing_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Fishing') == True)]['Duration'].sum())
            equestrianSports_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('EquestrianSports') == True)]['Duration'].sum())
            climbing_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Climbing') == True)]['Duration'].sum())
            tennis_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Tennis') == True)]['Duration'].sum())
            tableTennis_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('TableTennis') == True)]['Duration'].sum())
            squash_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Squash') == True)]['Duration'].sum())
            racquetball_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Racquetball') == True)]['Duration'].sum())
            pickleball_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Pickleball') == True)]['Duration'].sum())
            badminton_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Badminton') == True)]['Duration'].sum())
            pilates_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Pilates') == True)]['Duration'].sum())
            mindAndBody_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('MindAndBody') == True)]['Duration'].sum())
            yoga_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Yoga') == True)]['Duration'].sum())
            socialDance_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('SocialDance') == True)]['Duration'].sum())
            cardioDance_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('CardioDance') == True)]['Duration'].sum())
            barre_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Barre') == True)]['Duration'].sum())
            fitnessGaming_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('FitnessGaming') == True)]['Duration'].sum())
            stepTraining_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('StepTraining') == True)]['Duration'].sum())
            stairs_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Stairs') == True)]['Duration'].sum())
            stairClimbing_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('StairClimbing') == True)]['Duration'].sum())
            jumpRope_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('JumpRope') == True)]['Duration'].sum())
            highIntensityIntervalTraining_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('HighIntensityIntervalTraining') == True)]['Duration'].sum())
            mixedCardio_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('MixedCardio') == True)]['Duration'].sum())
            crossTraining_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('CrossTraining') == True)]['Duration'].sum())
            traditionalStrengthTraining_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('TraditionalStrengthTraining') == True)]['Duration'].sum())
            functionalStrengthTraining_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('FunctionalStrengthTraining') == True)]['Duration'].sum())
            elliptical_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Elliptical') == True)]['Duration'].sum())
            coreTraining_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('CoreTraining') == True)]['Duration'].sum())
            handCycling_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('HandCycling') == True)]['Duration'].sum())
            cycling_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Cycling') == True)]['Duration'].sum())
            wheelchairRunPace_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('WheelchairRunPace') == True)]['Duration'].sum())
            wheelchairWalkPace_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('WheelchairWalkPace') == True)]['Duration'].sum())
            running_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Running') == True)]['Duration'].sum())
            walking_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Walking') == True)]['Duration'].sum())
            cooldown_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Cooldown') == True)]['Duration'].sum())
            flexibility_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Flexibility') == True)]['Duration'].sum())
            preparationAndRecovery_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('PreparationAndRecovery') == True)]['Duration'].sum())
            volleyball_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Volleyball') == True)]['Duration'].sum())
            softball_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Softball') == True)]['Duration'].sum())
            soccer_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Soccer') == True)]['Duration'].sum())
            rugby_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Rugby') == True)]['Duration'].sum())
            lacrosse_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Lacrosse') == True)]['Duration'].sum())
            hockey_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Hockey') == True)]['Duration'].sum())
            handball_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Handball') == True)]['Duration'].sum())
            discSports_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('DiscSports') == True)]['Duration'].sum())
            cricket_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Cricket') == True)]['Duration'].sum())
            basketball_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Basketball') == True)]['Duration'].sum())
            baseball_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Baseball') == True)]['Duration'].sum())
            australianFootball_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('AustralianFootball') == True)]['Duration'].sum())
            americanFootball_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('AmericanFootball') == True)]['Duration'].sum())
            trackAndField_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('TrackAndField') == True)]['Duration'].sum())
            gymnastics_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Gymnastics') == True)]['Duration'].sum())
            fencing_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Fencing') == True)]['Duration'].sum())
            bowling_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Bowling') == True)]['Duration'].sum())
            archery_duration.append(content[i][(content[i].workoutType.astype(str).str.contains('Archery') == True)]['Duration'].sum())
        
            duration_mean.append(content[i]['Duration'].sum()/days)
            day_part_most.append(content[i]['day_part'].mode()[0])
            distance_mean.append(content[i]['total.distance'].sum()/days)
            energy_mean.append(content[i]['energy.consumed'].sum()/days)
            if all(pd.isnull(content[i]['Duration'])) == True:
                frequency.append(None)
            else:
                frequency.append(df['freq'].mean())
                
###deleting empty data frames
to_delet = []
for i in range(0,len(empty_data)):
    to_delet.append(files_finding.keys()[empty_data[i]])
    
###making a new data frame based on non empty ones
S = files_finding.drop(to_delet)
health_code=S.keys()

data={'code':health_code,'duration':duration_mean, 'day_part':day_part_most,'energy':energy_mean,'distance':distance_mean,'freq':frequency,
     'archery_duration': archery_duration,'archery_count':archery_count,'bowling_duration':bowling_duration,
     'bowling_count':bowling_count,'fencing_duration':fencing_duration,'fencing_count':fencing_count,
      'gymnastics_duration':gymnastics_duration,'gymnastics_count':gymnastics_count,'trackAndField_duration':trackAndField_duration,
     'trackAndField_count':trackAndField_count,'americanFootball_duration':americanFootball_duration,
     'americanFootball_count':americanFootball_count,'americanFootball_duration':americanFootball_duration,
      'americanFootball_count':americanFootball_count,'australianFootball_duration':australianFootball_duration,
      'australianFootball_count':australianFootball_count,'baseball_duration':baseball_duration,
      'baseball_count':baseball_count,'baseball_duration':baseball_duration,'baseball_count':baseball_count,
      'basketball_duration':basketball_duration,'basketball_count':basketball_count,'cricket_duration':cricket_duration,
      'cricket_count':cricket_count,'discSports_duration':discSports_duration,'discSports_count':discSports_count,
      'handball_duration':handball_duration,'handball_count':handball_count,'hockey_duration':hockey_duration,
      'hockey_count':hockey_count,'lacrosse_duration':lacrosse_duration,'lacrosse_count':lacrosse_count,
      'rugby_duration':rugby_duration,'rugby_count':rugby_count,'soccer_duration':soccer_duration,'soccer_count':soccer_count,
      'softball_duration':softball_duration,'softball_count':softball_count,'volleyball_duration':volleyball_duration,
      'volleyball_count':volleyball_count,'preparationAndRecovery_duration':preparationAndRecovery_duration,
      'preparationAndRecovery_count':preparationAndRecovery_count, 'flexibility_duration':flexibility_duration,
      'flexibility_count':flexibility_count,'cooldown_duration':cooldown_duration,'cooldown_count':cooldown_count,
      'walking_duration':walking_duration,'walking_count':walking_count,'running_duration':running_duration,
      'running_count':running_count,'wheelchairWalkPace_duration':wheelchairWalkPace_duration,
      'wheelchairWalkPace_count':wheelchairWalkPace_count,'wheelchairRunPace_duration':wheelchairRunPace_duration,
      'wheelchairRunPace_count':wheelchairRunPace_count,'cycling_duration':cycling_duration,'cycling_count':cycling_count,
      'handCycling_duration':handCycling_duration,'handCycling_count':handCycling_count,
      'coreTraining_duration':coreTraining_duration, 'coreTraining_count':coreTraining_count,'elliptical_duration':elliptical_duration,
      'elliptical_count':elliptical_count,'functionalStrengthTraining_duration':functionalStrengthTraining_duration,
      'functionalStrengthTraining_count':functionalStrengthTraining_count,'traditionalStrengthTraining_duration':traditionalStrengthTraining_duration,
      'traditionalStrengthTraining_count':traditionalStrengthTraining_count,'crossTraining_duration':crossTraining_duration,
      'crossTraining_count':crossTraining_count,'mixedCardio_duration':mixedCardio_duration,'mixedCardio_count':mixedCardio_count,
      'highIntensityIntervalTraining_duration':highIntensityIntervalTraining_duration,'highIntensityIntervalTraining_count':highIntensityIntervalTraining_count,
      'jumpRope_duration':jumpRope_duration,'jumpRope_count':jumpRope_count,'stairClimbing_duration':stairClimbing_duration,
      'stairClimbing_count':stairClimbing_count,'stairs_duration':stairs_duration,'stairs_count':stairs_count,
      'stepTraining_duration':stepTraining_duration,'stepTraining_count':stepTraining_count,
      'fitnessGaming_duration':fitnessGaming_duration,'fitnessGaming_count':fitnessGaming_count,'barre_duration':barre_duration,
      'barre_count':barre_count,'cardioDance_duration':cardioDance_duration,'cardioDance_count':cardioDance_count,
      'socialDance_duration':socialDance_duration,'socialDance_count':socialDance_count,'yoga_duration':yoga_duration,
      'yoga_count':yoga_count,'mindAndBody_duration':mindAndBody_duration,'mindAndBody_count':mindAndBody_count,
      'pilates_duration':pilates_duration,'pilates_count':pilates_count,'badminton_duration':badminton_duration,
      'badminton_count':badminton_count,'pickleball_duration':pickleball_duration,'pickleball_count':pickleball_count,
      'racquetball_duration':racquetball_duration,'racquetball_count':racquetball_count,'squash_duration':squash_duration,
      'squash_count':squash_count,'tableTennis_duration':tableTennis_duration,'tableTennis_count':tableTennis_count,
      'tennis_duration':tennis_duration,'tennis_count':tennis_count,'climbing_duration':climbing_duration,
      'climbing_count':climbing_count,'equestrianSports_duration':equestrianSports_duration,'equestrianSports_count':equestrianSports_count,
      'fishing_duration':fishing_duration,'fishing_count':fishing_count,'golf_duration':golf_duration,'golf_count':golf_count,
      'hiking_duration':hiking_duration,'hiking_count':hiking_count,'hunting_duration':hunting_duration,'hunting_count':hunting_count,
      'play_duration':play_duration,'play_count':play_count,'crossCountrySkiing_duration':crossCountrySkiing_duration,
      'crossCountrySkiing_count':crossCountrySkiing_count,'curling_duration':curling_duration,'curling_count':curling_count,
      'downhillSkiing_duration':downhillSkiing_duration,'downhillSkiing_count':downhillSkiing_count,
      'snowSports_duration':snowSports_duration,'snowSports_count':snowSports_count,'snowboarding_duration':snowboarding_duration,
      'snowboarding_count':snowboarding_count,'skatingSports_duration':skatingSports_duration,'skatingSports_count':skatingSports_count,
      'paddleSports_duration':paddleSports_duration,'paddleSports_count':paddleSports_count,'rowing_duration':rowing_duration,
      'rowing_count':rowing_count,'sailing_duration':sailing_duration,'sailing_count':sailing_count,
      'surfingSports_duration':surfingSports_duration,'surfingSports_count':surfingSports_count,'swimming_duration':swimming_count,
      'waterFitness_duration':waterFitness_duration,'waterFitness_count':waterFitness_count,'waterPolo_duration':waterPolo_duration,
      'waterPolo_count':waterPolo_count,'waterSports_duration':waterSports_duration,'waterSports_count':waterSports_count,
      'boxing_duration':boxing_duration,'boxing_count':boxing_count,'kickboxing_duration':kickboxing_duration,
      'kickboxing_count':kickboxing_count,'martialArts_duration':martialArts_duration,'martialArts_count':martialArts_count,
      'taiChi_duration':taiChi_duration,'taiChi_count':taiChi_count, 'wrestling_duration':wrestling_duration,
      'wrestling_count':wrestling_count,'other_duration':other_duration,'other_count':other_count,
      'dance_duration':dance_duration,'dance_count':dance_count,'danceInspiredTraining_duration':danceInspiredTraining_duration,
      'danceInspiredTraining_count':danceInspiredTraining_count,'mixedMetabolicCardioTraining_duration':mixedMetabolicCardioTraining_duration,
      'mixedMetabolicCardioTraining_count':mixedMetabolicCardioTraining_count,'swimBikeRun_duration':swimBikeRun_duration,
      'swimBikeRun_count':swimBikeRun_count,'transition_duration':transition_duration,'transition_count':transition_count,
      'morning_time':morning_time,
      'noon_time':noon_time,'afternoon_time':afternoon_time,'evening_time':evening_time,'night_time':night_time,
      'morning_count':morning_count,'noon_count':noon_count,'afternoon_count':afternoon_count,'evening_count':evening_count,
      'night_count':night_count,'morning_energy':morning_energy,'noon_energy':noon_energy,'afternoon_energy':afternoon_energy,
      'evening_energy':evening_energy,'night_energy':night_energy,'morning_distance':morning_distance,'noon_distance':noon_distance,
      'afternoon_distance':afternoon_distance,'evening_distance':evening_distance,'night_distance':night_distance,
      'number_of_days':number_of_days
      
     }


# Create DataFrame
df = pd.DataFrame(data)


df = df[df['duration']<=600]

