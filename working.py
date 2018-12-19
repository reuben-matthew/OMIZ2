# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""
import pandas as pd
import numpy as np
from savReaderWriter import *

#read spss.sav file
with SavReader(r'X:\OMIZ2\March_2018\Data_Cleaning\All_Surveys\Omi final_weights_v4_R.sav',ioUtf8=True,returnHeader=True) as reader:
    records=reader.all()

#read in meta data
with SavHeaderReader(r'X:\OMIZ2\March_2018\Data_Cleaning\All_Surveys\Omi final_weights_v4_R.sav',ioUtf8=True) as header:
   metadata = header.all()

#get the info for value labels
value_labels=metadata[2]
#queestion names
questions=metadata[3]

#use the columns of the dataframe as the first item of records list
columns=records[0]
#delete that item as it is the column names
del records[0]
#create dataframe
df=pd.DataFrame(records)
#rename columns
df.columns=columns

df=df[pd.notnull(df['weightpri'])]
df=df[pd.notnull(df['weightsec'])]
df=df[pd.notnull(df['weightall'])]
df=df.reset_index(drop=True)

all_columns=['Primary senior leaders','Primary class teachers','Primary all','Secondary senior leaders',
             'Secondary class teacher','Secondary all','All senior leaders','All class teachers','All all']

acad_columns=['Acad Primary senior leaders','Acad Primary class teachers','Acad Primary all','Acad Secondary senior leaders',
             'Acad Secondary class teacher','Acad Secondary all','Acad All senior leaders','Acad All class teachers','Acad All all',
             'Non-Acad Primary senior leaders','Non-Acad Primary class teachers','Non-Acad Primary all','Non-Acad Secondary senior leaders',
             'Non-Acad Secondary class teacher','Non-Acad Secondary all','Non-Acad All senior leaders','Non-Acad All class teachers',
             'Non-Acad All all']



questionIDs=['A3_1','A3_2','A3_3','A3_4','A3_5','A3_6','A3_7']

n_p_senior_leaders=int(len(df[(df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
n_p_class_leaders=int(len(df[(df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
n_p_all= n_p_class_leaders + n_p_senior_leaders
n_s_senior_leaders=int(len(df[(df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
n_s_class_leaders=int(len(df[(df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
n_s_all= n_s_senior_leaders + n_s_class_leaders
n_a_senior_leaders=n_p_senior_leaders + n_s_senior_leaders
n_a_class_leaders=n_p_class_leaders + n_s_class_leaders
n_a_all= n_a_senior_leaders + n_a_class_leaders
global cam_exceldf
closeended_all_many_counts={}
closeended_all_many_updates={}

for num,questionID in enumerate(questionIDs):
    for i in list(value_labels[questionID].keys()):
        if i>0:
            answer_df=df[df[questionID] == i]
            p_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1)]['weightpri'])),n_p_senior_leaders)/100)
            #every primary classroom leader 
            p_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2)]['weightpri'])),n_p_class_leaders)/100)
            #every primary, classroom and senior leader 
            p_all=(np.divide(sum((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]['weightpri'])),n_p_all)/100)
            #every senior leader secondary  teacher
            s_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1)]['weightsec'])),n_p_senior_leaders)/100)
            #every classroom leader secondary  teacher
            s_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2)]['weightsec'])),n_p_class_leaders)/100)
            #every secondary, classroom and senior leader 
            s_all=(np.divide(sum((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]['weightsec'])),n_p_all)/100)
            #every primary and secondary, senior leader 
            a_senior_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1)]['weightall'])),n_p_senior_leaders)/100)
            #every primary and secondary, classroom leader 
            a_class_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2)]['weightall'])),n_p_class_leaders)/100)
            #every primary and secondary, classroom and senior leader 
            a_all=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]['weightall'])),n_p_all)/100)
            
            
            '''
            if num ==0:
                closeended_all_many_counts[value_labels[questionID][i]]=[round(p_senior_leaders,2),
                                 round(p_class_leaders,2),round(p_all,2),round(s_senior_leaders,2),
                                 round(s_class_leaders,2),round(s_all,2),round(a_senior_leaders,2),
                                 round(a_class_leaders,2),round(a_all,2)]
                #c.update(closeended_all_many_counts)
            else:
                closeended_all_many_updates[value_labels[questionID][i]]=[round(p_senior_leaders,2),
                                 round(p_class_leaders,2),round(p_all,2),round(s_senior_leaders,2),
                                 round(s_class_leaders,2),round(s_all,2),round(a_senior_leaders,2),
                                 round(a_class_leaders,2),round(a_all,2)]
                #print(closeended_all_many_counts['PE Mark '][0],closeended_all_many_updates['PE Mark '][0])
                #c.update(closeended_all_many_updates)
    if num==0:
        cam_exceldf=pd.DataFrame(closeended_all_many_counts).T
        cam_exceldf.columns=all_columns
    else:
        d=pd.DataFrame(closeended_all_many_updates).T
        d.columns=all_columns
        cam_exceldf=cam_exceldf.add(d)
        '''
            question_name=questions[questionID].split('?')[1]  
                
            closeended_all_many_counts[question_name]=[round(p_senior_leaders,2),
                                 round(p_class_leaders,2),round(p_all,2),round(s_senior_leaders,2),
                                 round(s_class_leaders,2),round(s_all,2),round(a_senior_leaders,2),
                                 round(a_class_leaders,2),round(a_all,2)]
#cam_exceldf=cam_exceldf.append({'N':[n_p_senior_leaders,n_p_class_leaders,n_p_all,n_s_senior_leaders,
                     #n_s_class_leaders,n_s_all,n_a_senior_leaders,n_a_class_leaders,n_a_all]}).T
            closeended_all_many_counts.update({'N':[n_p_senior_leaders,n_p_class_leaders,n_p_all,n_s_senior_leaders,
                     n_s_class_leaders,n_s_all,n_a_senior_leaders,n_a_class_leaders,n_a_all]})
cam_exceldf=pd.DataFrame(closeended_all_many_counts).T
cam_exceldf.columns=all_columns
cam_exceldf = pd.concat([cam_exceldf.drop('N', axis=0), cam_exceldf.loc[['N'], :]], axis=0)
cam_exceldf=cam_exceldf.drop(cam_exceldf.T[cam_exceldf.T['N']==0].index,axis=1)
if (n_p_senior_leaders ==0 and n_p_class_leaders==0 and  n_p_all==0):
    cam_exceldf=cam_exceldf.drop(['All senior leaders','All class teachers','All all'],axis=1)