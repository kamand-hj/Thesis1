#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import synapseclient
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from missingpy import MissForest
import datetime
#from datetime import datetime, date
from datetime import timedelta
syn = synapseclient.Synapse()

syn.login('Kamand', 'Kamand13579-')

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

