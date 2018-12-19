# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 12:56:25 2018

@author: mattr
"""
import os
import pandas as pd


filenames_03=[]
for filename in os.listdir(r'K:\PSUK\RO\Main Study 2018\Portal\pupil data\11103'):
    if '.xlsx' in filename:
        filenames_03.append(filename.split('-')[1])

'''
filenames_04=[]
for filename in os.listdir(r'K:\PSUK\RO\Main Study 2018\Portal\pupil data\11104'):
    filenames_04.append(filename.split('-')[1])


    
    
df_03_05=
df_06_09=

'''    
df_03_05=pd.read_excel(r'K:\PSUK\RO\Main Study 2018\Recruitment\11103-5-2a.xlsx')
03_agreed=df_03_05[(df_03_04['SampleNo']==11103)&(df_03_05['Agreed (Y/R/W/IN/LA)']=='Y')]




missing=[]

for i in df['NFER_No']:
    if str(i) in filenames_09:
        continue
    else:
        missing.append(i)
        
missing.sort()
        