# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""
import pandas as pd
import numpy as np
from savReaderWriter import *

#read spss.sav file
with SavReader(r'X:\OMIZ2\June_2018\Data_Cleaning\All_Surveys\Omi final_weights_v3_R.sav',ioUtf8=True,returnHeader=True) as reader:
    records=reader.all()

#read in meta data
with SavHeaderReader(r'X:\OMIZ2\June_2018\Data_Cleaning\All_Surveys\Omi final_weights_v3_R.sav',ioUtf8=True) as header:
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


def openended_all (questionID):
    n_p_senior_leaders=int(len(df[(df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionID] >=0)]))
    n_p_class_leaders=int(len(df[(df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionID] >=0)]))
    n_p_all= n_p_class_leaders + n_p_senior_leaders
    n_s_senior_leaders=int(len(df[(df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionID] >=0)]))
    n_s_class_leaders=int(len(df[(df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionID] >=0)]))
    n_s_all= n_s_senior_leaders + n_s_class_leaders
    n_a_senior_leaders=n_p_senior_leaders + n_s_senior_leaders
    n_a_class_leaders=n_p_class_leaders + n_s_class_leaders
    n_a_all= n_a_senior_leaders + n_a_class_leaders
    global oa_exceldf
    openended_all_counts={}
    for i in list(value_labels[questionID].keys()):
        if i >0:
            answer_df=df[df[questionID] == i]
            p_senior_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1)]))
            #every primary classroom leader 
            p_class_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2)]))
            #every primary, classroom and senior leader 
            p_all=len((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]))
            #every senior leader secondary  teacher
            s_senior_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1)]))
            #every classroom leader secondary  teacher
            s_class_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2)]))
            #every secondary, classroom and senior leader 
            s_all=len((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]))
            #every primary and secondary, senior leader 
            a_senior_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1)]))
            #every primary and secondary, classroom leader 
            a_class_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2)]))
            #every primary and secondary, classroom and senior leader 
            a_all=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]))
            
            openended_all_counts[value_labels[questionID][i]]=[round(p_senior_leaders,2),
                         round(p_class_leaders,2),round(p_all,2),round(s_senior_leaders,2),
                         round(s_class_leaders,2),round(s_all,2),round(a_senior_leaders,2),
                         round(a_class_leaders,2),round(a_all,2)]
            
    openended_all_counts.update({'N':[n_p_senior_leaders,n_p_class_leaders,n_p_all,n_s_senior_leaders,
                        n_s_class_leaders,n_s_all,n_a_senior_leaders,n_a_class_leaders,n_a_all]})
    oa_exceldf=pd.DataFrame(openended_all_counts).T
    oa_exceldf.columns=all_columns
    oa_exceldf = pd.concat([oa_exceldf.drop('N', axis=0), oa_exceldf.loc[['N'], :]], axis=0)
    oa_exceldf=oa_exceldf.drop(oa_exceldf.T[oa_exceldf.T['N']==0].index,axis=1)

    
#openended_all('A5')    

def openended_all_many(questionIDs):
    n_p_senior_leaders=int(len(df[(df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
    n_p_class_leaders=int(len(df[(df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
    n_p_all= n_p_class_leaders + n_p_senior_leaders
    n_s_senior_leaders=int(len(df[(df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
    n_s_class_leaders=int(len(df[(df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
    n_s_all= n_s_senior_leaders + n_s_class_leaders
    n_a_senior_leaders=n_p_senior_leaders + n_s_senior_leaders
    n_a_class_leaders=n_p_class_leaders + n_s_class_leaders
    n_a_all= n_a_senior_leaders + n_a_class_leaders
    global oam_exceldf
    openended_all_many_counts={}
    for num,questionID in enumerate(questionIDs):
        for i in list(value_labels[questionID].keys()):
            if i >0:
                answer_df=df[df[questionID] == i]
                p_senior_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1)]))
                #every primary classroom leader 
                p_class_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2)]))
                #every primary, classroom and senior leader 
                p_all=len((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]))
                #every senior leader secondary  teacher
                s_senior_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1)])['weightsec'])
                #every classroom leader secondary  teacher
                s_class_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2)])['weightsec'])
                #every secondary, classroom and senior leader 
                s_all=len((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]))
                #every primary and secondary, senior leader 
                a_senior_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1)]))
                #every primary and secondary, classroom leader 
                a_class_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2)]))
                #every primary and secondary, classroom and senior leader 
                a_all=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))])['weightall'])
                
                
                question_name=questions[questionID].split('?')[1]  
                openended_all_many_counts[question_name]=[round(p_senior_leaders,2),
                                 round(p_class_leaders,2),round(p_all,2),round(s_senior_leaders,2),
                                 round(s_class_leaders,2),round(s_all,2),round(a_senior_leaders,2),
                                 round(a_class_leaders,2),round(a_all,2)]
                
        openended_all_many_counts.update({'N':[n_p_senior_leaders,n_p_class_leaders,n_p_all,n_s_senior_leaders,
                            n_s_class_leaders,n_s_all,n_a_senior_leaders,n_a_class_leaders,n_a_all]})    
    oam_exceldf=pd.DataFrame(openended_all_many_counts).T
    oam_exceldf.columns=all_columns
    oam_exceldf = pd.concat([oam_exceldf.drop('N', axis=0), oam_exceldf.loc[['N'], :]], axis=0)
    oam_exceldf=oam_exceldf.drop(oam_exceldf.T[oam_exceldf.T['N']==0].index,axis=1)
    
#openended_all_many(['A2_1','A2_2','A2_3','A2_4','A2_5','A2_6','A2_7'])

def openended_all_responses (questionIDs):
    n_p_senior_leaders=int(len(df[(df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
    n_p_class_leaders=int(len(df[(df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
    n_p_all= n_p_class_leaders + n_p_senior_leaders
    n_s_senior_leaders=int(len(df[(df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
    n_s_class_leaders=int(len(df[(df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
    n_s_all= n_s_senior_leaders + n_s_class_leaders
    n_a_senior_leaders=n_p_senior_leaders + n_s_senior_leaders
    n_a_class_leaders=n_p_class_leaders + n_s_class_leaders
    n_a_all= n_a_senior_leaders + n_a_class_leaders
    global oar_exceldf
    openended_all_responses_counts={}
    openended_all_responses_updates={}
    
    for num,questionID in enumerate(questionIDs):
        for i in list(value_labels[questionID].keys()):
            if i>0:
                answer_df=df[df[questionID] == i]
                p_senior_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1)]))
                #every primary classroom leader 
                p_class_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2)]))
                #every primary, classroom and senior leader 
                p_all=len((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]))
                #every senior leader secondary  teacher
                s_senior_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1)]))
                #every classroom leader secondary  teacher
                s_class_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2)]))
                #every secondary, classroom and senior leader 
                s_all=len((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]))
                #every primary and secondary, senior leader 
                a_senior_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1)]))
                #every primary and secondary, classroom leader 
                a_class_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2)]))
                #every primary and secondary, classroom and senior leader 
                a_all=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]))
                if num ==0:
                    openended_all_responses_counts[value_labels[questionID][i]]=[round(p_senior_leaders,2),
                                     round(p_class_leaders,2),round(p_all,2),round(s_senior_leaders,2),
                                     round(s_class_leaders,2),round(s_all,2),round(a_senior_leaders,2),
                                     round(a_class_leaders,2),round(a_all,2)]
                    #c.update(closeended_all_many_counts)
                else:
                    openended_all_responses_updates[value_labels[questionID][i]]=[round(p_senior_leaders,2),
                                     round(p_class_leaders,2),round(p_all,2),round(s_senior_leaders,2),
                                     round(s_class_leaders,2),round(s_all,2),round(a_senior_leaders,2),
                                     round(a_class_leaders,2),round(a_all,2)]
                    #print(closeended_all_many_counts['PE Mark '][0],closeended_all_many_updates['PE Mark '][0])
                    #c.update(closeended_all_many_updates)
        if num==0:
            openended_all_responses_df=pd.DataFrame(openended_all_responses_counts).T
            openended_all_responses_df.columns=all_columns
        else:
            d=pd.DataFrame(openended_all_responses_updates).T
            d.columns=all_columns
            openended_all_responses_df=openended_all_responses_df.add(d)
            
    openended_all_responses_df=openended_all_responses_df.append({'N':[n_p_senior_leaders,n_p_class_leaders,n_p_all,n_s_senior_leaders,
                         n_s_class_leaders,n_s_all,n_a_senior_leaders,n_a_class_leaders,n_a_all]}).T
    oar_exceldf.columns=all_columns
    oar_exceldf = pd.concat([oar_exceldf.drop('N', axis=0), oar_exceldf.loc[['N'], :]], axis=0)
    oar_exceldf=oar_exceldf.drop(oar_exceldf.T[oar_exceldf.T['N']==0].index,axis=1)
    
#openended_all_responses(['A4_Other_Code1','A4_Other_Code2','A4_Other_Code3','A4_Other_Code4','A4_Other_Code5'])
    
def closeended_all (questionID):
    n_p_senior_leaders=int(len(df[(df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionID] >=0)]))
    n_p_class_leaders=int(len(df[(df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionID] >=0)]))
    n_p_all= n_p_class_leaders + n_p_senior_leaders
    n_s_senior_leaders=int(len(df[(df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionID] >=0)]))
    n_s_class_leaders=int(len(df[(df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionID] >=0)]))
    n_s_all= n_s_senior_leaders + n_s_class_leaders
    n_a_senior_leaders=n_p_senior_leaders + n_s_senior_leaders
    n_a_class_leaders=n_p_class_leaders + n_s_class_leaders
    n_a_all= n_a_senior_leaders + n_a_class_leaders
    global ca_exceldf
    closeended_all_counts={}
    for i in list(value_labels[questionID].keys()):
        if i >0:
            answer_df=df[df[questionID] == i]
            #every primary senior leader teacher
            p_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1)])['weightpri']),n_p_senior_leaders)*100)
            #every primary classroom leader 
            p_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2)])['weightpri']),n_p_class_leaders)*100)
            #every primary, classroom and senior leader 
            p_all=(np.divide(sum((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))])['weightpri']),n_p_all)*100)
            #every senior leader secondary  teacher
            s_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1)])['weightsec']),n_s_senior_leaders)*100)
            #every classroom leader secondary  teacher
            s_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2)])['weightsec']),n_s_class_leaders)*100)
            #every secondary, classroom and senior leader 
            s_all=(np.divide(sum((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))])['weightsec']),n_s_all)*100)
            #every primary and secondary, senior leader 
            a_senior_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1)])['weightall']),n_a_senior_leaders)*100)
            #every primary and secondary, classroom leader 
            a_class_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2)])['weightall']),n_a_class_leaders)*100)
            #every primary and secondary, classroom and senior leader 
            a_all=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))])['weightall']),n_a_all)*100)
    
                        
            closeended_all_counts[value_labels[questionID][i]]=[round(p_senior_leaders,2),
                                 round(p_class_leaders,2),round(p_all,2),round(s_senior_leaders,2),
                                 round(s_class_leaders,2),round(s_all,2),round(a_senior_leaders,2),
                                 round(a_class_leaders,2),round(a_all,2)]
    
    closeended_all_counts.update({'N':[n_p_senior_leaders,n_p_class_leaders,n_p_all,n_s_senior_leaders,
                        n_s_class_leaders,n_s_all,n_a_senior_leaders,n_a_class_leaders,n_a_all]})
    ca_exceldf=pd.DataFrame(closeended_all_counts).T
    ca_exceldf.columns=all_columns
    ca_exceldf = pd.concat([ca_exceldf.drop('N', axis=0), ca_exceldf.loc[['N'], :]], axis=0)
    ca_exceldf=ca_exceldf.drop(ca_exceldf.T[ca_exceldf.T['N']==0].index,axis=1)
    if (n_p_senior_leaders ==0 and n_p_class_leaders==0 and  n_p_all==0):
        ca_exceldf=ca_exceldf.drop(['All senior leaders','All class teachers','All all'],axis=1)

#closeended_all('A1') 
#closeended_all('A4')    

def closeended_all_many (questionIDs):
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
                p_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1)]))['weightpri'],n_p_senior_leaders)/100)
                #every primary classroom leader 
                p_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2)]))['weightpri'],n_p_class_leaders)/100)
                #every primary, classroom and senior leader 
                p_all=(np.divide(sum((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]))['weightpri'],n_p_all)/100)
                #every senior leader secondary  teacher
                s_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1)]))['weightsec'],n_p_senior_leaders)/100)
                #every classroom leader secondary  teacher
                s_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2)]))['weightsec'],n_p_class_leaders)/100)
                #every secondary, classroom and senior leader 
                s_all=(np.divide(sum((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]))['weightsec'],n_p_all)/100)
                #every primary and secondary, senior leader 
                a_senior_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1)]))['weightall'],n_p_senior_leaders)/100)
                #every primary and secondary, classroom leader 
                a_class_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2)]))['weightall'],n_p_class_leaders)/100)
                #every primary and secondary, classroom and senior leader 
                a_all=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))]))['weightall'],n_p_all)/100)
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
            
    cam_exceldf=cam_exceldf.append({'N':[n_p_senior_leaders,n_p_class_leaders,n_p_all,n_s_senior_leaders,
                         n_s_class_leaders,n_s_all,n_a_senior_leaders,n_a_class_leaders,n_a_all]}).T
    
    cam_exceldf.columns=all_columns
    cam_exceldf = pd.concat([cam_exceldf.drop('N', axis=0), cam_exceldf.loc[['N'], :]], axis=0)
    cam_exceldf=cam_exceldf.drop(cam_exceldf.T[cam_exceldf.T['N']==0].index,axis=1)
    if (n_p_senior_leaders ==0 and n_p_class_leaders==0 and  n_p_all==0):
        cam_exceldf=cam_exceldf.drop(['All senior leaders','All class teachers','All all'],axis=1)

#closeended_all_many(['A3_1','A3_2','A3_3','A3_4','A3_5','A3_6','A3_7'])   
#closeended_all_many(['S4_1','S4_2','S4_3','S4_4','S4_5','S4_6','S4_7','S4_8','S4_9_OtherResponse'])

def openended_acad (questionID):
    n_acad_p_senior_leaders=int(len(df[(df['type']==22) & (df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionID] >=0)]))
    n_acad_p_class_leaders=int(len(df[(df['type']==22) & (df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionID] >=0)]))
    n_acad_p_all= n_acad_p_class_leaders + n_acad_p_senior_leaders
    n_acad_s_senior_leaders=int(len(df[(df['type']==22) & (df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionID] >=0)]))
    n_acad_s_class_leaders=int(len(df[(df['type']==22) & (df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionID] >=0)]))
    n_acad_s_all= n_acad_s_senior_leaders + n_acad_s_class_leaders
    n_acad_a_senior_leaders=n_acad_p_senior_leaders + n_acad_s_senior_leaders
    n_acad_a_class_leaders=n_acad_p_class_leaders + n_acad_s_class_leaders
    n_acad_a_all= n_acad_a_senior_leaders + n_acad_a_class_leaders
    n_nonacad_p_senior_leaders=int(len(df[(df['type']!=22) & (df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionID] >=0)]))
    n_nonacad_p_class_leaders=int(len(df[(df['type']!=22) & (df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionID] >=0)]))
    n_nonacad_p_all= n_nonacad_p_class_leaders + n_nonacad_p_senior_leaders
    n_nonacad_s_senior_leaders=int(len(df[(df['type']!=22) & (df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionID] >=0)]))
    n_nonacad_s_class_leaders=int(len(df[(df['type']!=22) & (df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionID] >=0)]))
    n_nonacad_s_all= n_nonacad_s_senior_leaders + n_nonacad_s_class_leaders
    n_nonacad_a_senior_leaders=n_nonacad_p_senior_leaders + n_nonacad_s_senior_leaders
    n_nonacad_a_class_leaders=n_nonacad_p_class_leaders + n_nonacad_s_class_leaders
    n_nonacad_a_all= n_nonacad_a_senior_leaders + n_nonacad_a_class_leaders
    global oacad_exceldf
    openended_acad_counts={}
    for i in list(value_labels[questionID].keys()):
        if i >0:
            answer_df=df[df[questionID] == i]
            a_p_senior_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1) & (answer_df['type']==22)]))
            #every primary classroom leader 
            a_p_class_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2) & (answer_df['type']==22)]))
            #every primary, classroom and senior leader 
            a_p_all=len((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']==22)]))
            #every senior leader secondary  teacher
            a_s_senior_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1) & (answer_df['type']==22)]))
            #every classroom leader secondary  teacher
            a_s_class_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2) & (answer_df['type']==22)]))
            #every secondary, classroom and senior leader 
            a_s_all=len((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']==22)]))
            #every primary and secondary, senior leader 
            a_a_senior_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1) & (answer_df['type']==22)]))
            #every primary and secondary, classroom leader 
            a_a_class_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2) & (answer_df['type']==22)]))
            #every primary and secondary, classroom and senior leader 
            a_a_all=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']==22)]))
                
            na_p_senior_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1) & (answer_df['type']!=22)]))
            #every primary classroom leader 
            na_p_class_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2) & (answer_df['type']!=22)]))
            #every primary, classroom and senior leader 
            na_p_all=len((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']!=22)]))
            #every senior leader secondary  teacher
            na_s_senior_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1) & (answer_df['type']!=22)]))
            #every classroom leader secondary  teacher
            na_s_class_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2) & (answer_df['type']!=22)]))
            #every secondary, classroom and senior leader 
            na_s_all=len((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']!=22)]))
            #every primary and secondary, senior leader 
            na_a_senior_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1) & (answer_df['type']!=22)]))
            #every primary and secondary, classroom leader 
            na_a_class_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2) & (answer_df['type']!=22)]))
            #every primary and secondary, classroom and senior leader 
            na_a_all=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']!=22)]))
           
                        
            openended_acad_counts[value_labels[questionID][i]]=[round(a_p_senior_leaders,2),
                             round(a_p_class_leaders,2),round(a_p_all,2),round(a_s_senior_leaders,2),
                             round(a_s_class_leaders,2),round(a_s_all,2),round(a_a_senior_leaders,2),
                             round(a_a_class_leaders,2),round(a_a_all,2),round(na_p_senior_leaders,2),
                             round(na_p_class_leaders,2),round(na_p_all,2),round(na_s_senior_leaders,2),
                             round(na_s_class_leaders,2),round(na_s_all,2),round(na_a_senior_leaders,2),
                             round(na_a_class_leaders,2),round(na_a_all,2)]
    
    openended_acad_counts.update({'N':[n_acad_p_senior_leaders,n_acad_p_class_leaders,n_acad_p_all,n_acad_s_senior_leaders,
                        n_acad_s_class_leaders,n_acad_s_all,n_acad_a_senior_leaders,n_acad_a_class_leaders,n_acad_a_all,
                        n_nonacad_p_senior_leaders,n_nonacad_p_class_leaders,n_nonacad_p_all,n_nonacad_s_senior_leaders,
                        n_nonacad_s_class_leaders,n_nonacad_s_all,n_nonacad_a_senior_leaders,n_nonacad_a_class_leaders,
                        n_nonacad_a_all]})
    oacad_exceldf=pd.DataFrame(openended_acad_counts).T
    oacad_exceldf.columns=acad_columns
    oacad_exceldf = pd.concat([oacad_exceldf.drop('N', axis=0), oacad_exceldf.loc[['N'], :]], axis=0)
    oacad_exceldf=oacad_exceldf.drop(oacad_exceldf.T[oacad_exceldf.T['N']==0].index,axis=1)

def openended_acad_many(questionIDs):
    n_acad_p_senior_leaders=int(len(df[(df['type']==22) & (df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
    n_acad_p_class_leaders=int(len(df[(df['type']==22) & (df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
    n_acad_p_all= n_acad_p_class_leaders + n_acad_p_senior_leaders
    n_acad_s_senior_leaders=int(len(df[(df['type']==22) & (df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
    n_acad_s_class_leaders=int(len(df[(df['type']==22) & (df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
    n_acad_s_all= n_acad_s_senior_leaders + n_acad_s_class_leaders
    n_acad_a_senior_leaders=n_acad_p_senior_leaders + n_acad_s_senior_leaders
    n_acad_a_class_leaders=n_acad_p_class_leaders + n_acad_s_class_leaders
    n_acad_a_all= n_acad_a_senior_leaders + n_acad_a_class_leaders
    n_nonacad_p_senior_leaders=int(len(df[(df['type']!=22) & (df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
    n_nonacad_p_class_leaders=int(len(df[(df['type']!=22) & (df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
    n_nonacad_p_all= n_nonacad_p_class_leaders + n_nonacad_p_senior_leaders
    n_nonacad_s_senior_leaders=int(len(df[(df['type']!=22) & (df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
    n_nonacad_s_class_leaders=int(len(df[(df['type']!=22) & (df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
    n_nonacad_s_all= n_nonacad_s_senior_leaders + n_nonacad_s_class_leaders
    n_nonacad_a_senior_leaders=n_nonacad_p_senior_leaders + n_nonacad_s_senior_leaders
    n_nonacad_a_class_leaders=n_nonacad_p_class_leaders + n_nonacad_s_class_leaders
    n_nonacad_a_all= n_nonacad_a_senior_leaders + n_nonacad_a_class_leaders
    global oacadm_exceldf
    openended_acad_many_counts={}
    for num,questionID in enumerate(questionIDs):
        for i in list(value_labels[questionID].keys()):
            if i >0:
                answer_df=df[df[questionID] == i]
                a_p_senior_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1) & (answer_df['type']==22)]))
                #every primary classroom leader 
                a_p_class_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2) & (answer_df['type']==22)]))
                #every primary, classroom and senior leader 
                a_p_all=len((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']==22)]))
                #every senior leader secondary  teacher
                a_s_senior_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1) & (answer_df['type']==22)]))
                #every classroom leader secondary  teacher
                a_s_class_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2) & (answer_df['type']==22)]))
                #every secondary, classroom and senior leader 
                a_s_all=len((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']==22)]))
                #every primary and secondary, senior leader 
                a_a_senior_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1) & (answer_df['type']==22)]))
                #every primary and secondary, classroom leader 
                a_a_class_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2) & (answer_df['type']==22)]))
                #every primary and secondary, classroom and senior leader 
                a_a_all=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2))])['weightall'])
                
                na_p_senior_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1) & (answer_df['type']!=22)]))
                #every primary classroom leader 
                na_p_class_leaders=len((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2) & (answer_df['type']!=22)]))
                #every primary, classroom and senior leader 
                na_p_all=len((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']!=22)]))
                #every senior leader secondary  teacher
                na_s_senior_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1) & (answer_df['type']!=22)]))
                #every classroom leader secondary  teacher
                na_s_class_leaders=len((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2) & (answer_df['type']!=22)]))
                #every secondary, classroom and senior leader 
                na_s_all=len((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']!=22)]))
                #every primary and secondary, senior leader 
                na_a_senior_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1) & (answer_df['type']!=22)]))
                #every primary and secondary, classroom leader 
                na_a_class_leaders=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2) & (answer_df['type']!=22)]))
                #every primary and secondary, classroom and senior leader 
                na_a_all=len((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']!=22)]))
           
                
                
                question_name=questions[questionID].split('?')[1]  
                openended_acad_many_counts[question_name]=[round(a_p_senior_leaders,2),
                         round(a_p_class_leaders,2),round(a_p_all,2),round(a_s_senior_leaders,2),
                         round(a_s_class_leaders,2),round(a_s_all,2),round(a_a_senior_leaders,2),
                         round(a_a_class_leaders,2),round(a_a_all,2),round(na_p_senior_leaders,2),
                         round(na_p_class_leaders,2),round(na_p_all,2),round(na_s_senior_leaders,2),
                         round(na_s_class_leaders,2),round(na_s_all,2),round(na_a_senior_leaders,2),
                         round(na_a_class_leaders,2),round(na_a_all,2)]
        
                
        openended_acad_many_counts.update({'N':[n_acad_p_senior_leaders,n_acad_p_class_leaders,n_acad_p_all,n_acad_s_senior_leaders,
                        n_acad_s_class_leaders,n_acad_s_all,n_acad_a_senior_leaders,n_acad_a_class_leaders,n_acad_a_all,
                        n_nonacad_p_senior_leaders,n_nonacad_p_class_leaders,n_nonacad_p_all,n_nonacad_s_senior_leaders,
                        n_nonacad_s_class_leaders,n_nonacad_s_all,n_nonacad_a_senior_leaders,n_nonacad_a_class_leaders,
                        n_nonacad_a_all]})  
    oacadm_exceldf=pd.DataFrame(openended_acad_many_counts).T
    oacadm_exceldf.columns=acad_columns
    oacadm_exceldf = pd.concat([oacadm_exceldf.drop('N', axis=0), oacadm_exceldf.loc[['N'], :]], axis=0)
    oacadm_exceldf=oacadm_exceldf.drop(oacadm_exceldf.T[oacadm_exceldf.T['N']==0].index,axis=1)
    
#openended_acad_many(['S7_1','S7_2','S7_3','S7_4','S7_5','S7_6'])

def closeended_acad (questionID):
    n_acad_p_senior_leaders=int(len(df[(df['type']==22) & (df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionID] >=0)]))
    n_acad_p_class_leaders=int(len(df[(df['type']==22) & (df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionID] >=0)]))
    n_acad_p_all= n_acad_p_class_leaders + n_acad_p_senior_leaders
    n_acad_s_senior_leaders=int(len(df[(df['type']==22) & (df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionID] >=0)]))
    n_acad_s_class_leaders=int(len(df[(df['type']==22) & (df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionID] >=0)]))
    n_acad_s_all= n_acad_s_senior_leaders + n_acad_s_class_leaders
    n_acad_a_senior_leaders=n_acad_p_senior_leaders + n_acad_s_senior_leaders
    n_acad_a_class_leaders=n_acad_p_class_leaders + n_acad_s_class_leaders
    n_acad_a_all= n_acad_a_senior_leaders + n_acad_a_class_leaders
    n_nonacad_p_senior_leaders=int(len(df[(df['type']!=22) & (df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionID] >=0)]))
    n_nonacad_p_class_leaders=int(len(df[(df['type']!=22) & (df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionID] >=0)]))
    n_nonacad_p_all= n_nonacad_p_class_leaders + n_nonacad_p_senior_leaders
    n_nonacad_s_senior_leaders=int(len(df[(df['type']!=22) & (df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionID] >=0)]))
    n_nonacad_s_class_leaders=int(len(df[(df['type']!=22) & (df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionID] >=0)]))
    n_nonacad_s_all= n_nonacad_s_senior_leaders + n_nonacad_s_class_leaders
    n_nonacad_a_senior_leaders=n_nonacad_p_senior_leaders + n_nonacad_s_senior_leaders
    n_nonacad_a_class_leaders=n_nonacad_p_class_leaders + n_nonacad_s_class_leaders
    n_nonacad_a_all= n_nonacad_a_senior_leaders + n_nonacad_a_class_leaders
    global cacad_exceldf
    closeended_acad_counts={}
    for i in list(value_labels[questionID].keys()):
        if i>0:
            answer_df=df[df[questionID] == i]
            #ACADEMIES
            #every primary senior leader teacher
            a_p_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1) & (answer_df['type']==22)])['weightpri'])/n_acad_p_senior_leaders)*100)
            #every primary classroom leader 
            a_p_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2) & (answer_df['type']==22)])['weightpri'])/n_acad_p_class_leaders)*100)
            #every primary, classroom and senior leader 
            a_p_all=(np.divide(sum((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']==22)])['weightpri'])/n_acad_p_all)*100)
            #every senior leader secondary  teacher
            a_s_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1) & (answer_df['type']==22)])['weightsec'])/n_acad_s_senior_leaders)*100)
            #every classroom leader secondary  teacher
            a_s_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2) & (answer_df['type']==22)])['weightsec'])/n_acad_s_class_leaders)*100)
            #every secondary, classroom and senior leader 
            a_s_all=(np.divide(sum((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']==22)])['weightsec'])/n_acad_s_all)*100)
            #every primary and secondary, senior leader 
            a_a_senior_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1) & (answer_df['type']==22)])['weightall'])/n_acad_a_senior_leaders)*100)
            #every primary and secondary, classroom leader 
            a_a_class_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2) & (answer_df['type']==22)])['weightall'])/n_acad_a_class_leaders)*100)
            #every primary and secondary, classroom and senior leader 
            a_a_all=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']==22)])['weightall'])/n_acad_a_all)*100)
            #NON-ACADEMIES
            #every primary senior leader teacher
            na_p_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1) & (answer_df['type']!=22)])['weightpri'])/n_nonacad_p_senior_leaders)*100)
            #every primary classroom leader 
            na_p_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2) & (answer_df['type']!=22)])['weightpri'])/n_nonacad_p_class_leaders)*100)
            #every primary, classroom and senior leader 
            na_p_all=(np.divide(sum((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']!=22)])['weightpri'])/n_nonacad_p_all)*100)
            #every senior leader secondary  teacher
            na_s_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1) & (answer_df['type']!=22)])['weightsec'])/n_nonacad_s_senior_leaders)*100)
            #every classroom leader secondary  teacher
            na_s_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2) & (answer_df['type']!=22)])['weightsec'])/n_nonacad_s_class_leaders)*100)
            #every secondary, classroom and senior leader 
            na_s_all=(np.divide(sum((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']!=22)])['weightsec'])/n_nonacad_s_all)*100)
            #every primary and secondary, senior leader 
            na_a_senior_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1) & (answer_df['type']!=22)])['weightall'])/n_nonacad_a_senior_leaders)*100)
            #every primary and secondary, classroom leader 
            na_a_class_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2) & (answer_df['type']!=22)])['weightall'])/n_nonacad_a_class_leaders)*100)
            #every primary and secondary, classroom and senior leader 
            na_a_all=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']!=22)])['weightall'])/n_nonacad_a_all)*100)
            
                    
            closeended_acad_counts[value_labels[questionID][i]]=[round(a_p_senior_leaders,2),
                         round(a_p_class_leaders,2),round(a_p_all,2),round(a_s_senior_leaders,2),
                         round(a_s_class_leaders,2),round(a_s_all,2),round(a_a_senior_leaders,2),
                         round(a_a_class_leaders,2),round(a_a_all,2),round(na_p_senior_leaders,2),
                         round(na_p_class_leaders,2),round(na_p_all,2),round(na_s_senior_leaders,2),
                         round(na_s_class_leaders,2),round(na_s_all,2),round(na_a_senior_leaders,2),
                         round(na_a_class_leaders,2),round(na_a_all,2)]
        
    closeended_acad_counts.update({'N':[n_acad_p_senior_leaders,n_acad_p_class_leaders,n_acad_p_all,n_acad_s_senior_leaders,
                        n_acad_s_class_leaders,n_acad_s_all,n_acad_a_senior_leaders,n_acad_a_class_leaders,n_acad_a_all,
                        n_nonacad_p_senior_leaders,n_nonacad_p_class_leaders,n_nonacad_p_all,n_nonacad_s_senior_leaders,
                        n_nonacad_s_class_leaders,n_nonacad_s_all,n_nonacad_a_senior_leaders,n_nonacad_a_class_leaders,
                        n_nonacad_a_all]})
    cacad_exceldf=pd.DataFrame(closeended_acad_counts).T
    cacad_exceldf.columns=acad_columns
    cacad_exceldf = pd.concat([cacad_exceldf.drop('N', axis=0), cacad_exceldf.loc[['N'], :]], axis=0)
    cacad_exceldf=cacad_exceldf.drop(cacad_exceldf.T[ca_exceldf.T['N']==0].index,axis=1)
    if (n_acad_p_senior_leaders ==0 and n_acad_p_class_leaders==0 and  n_acad_p_all==0):
        cacad_exceldf=cacad_exceldf.drop(['Acad All senior leaders','Acad All class teachers','Acad All all'],axis=1)
    if (n_nonacad_p_senior_leaders ==0 and n_nonacad_p_class_leaders==0 and  n_nonacad_p_all==0):
        cacad_exceldf=cacad_exceldf.drop(['Non-Acad All senior leaders','Non-Acad All class teachers','Non-Acad All all'],axis=1)
    
    

#closeended_acad('S1')
#closeended_acad('S3a')

    
def closeended_acad_many (questionIDs):
    n_acad_p_senior_leaders=int(len(df[(df['type']==22) & (df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
    n_acad_p_class_leaders=int(len(df[(df['type']==22) & (df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
    n_acad_p_all= n_acad_p_class_leaders + n_acad_p_senior_leaders
    n_acad_s_senior_leaders=int(len(df[(df['type']==22) & (df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
    n_acad_s_class_leaders=int(len(df[(df['type']==22) & (df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
    n_acad_s_all= n_acad_s_senior_leaders + n_acad_s_class_leaders
    n_acad_a_senior_leaders=n_acad_p_senior_leaders + n_acad_s_senior_leaders
    n_acad_a_class_leaders=n_acad_p_class_leaders + n_acad_s_class_leaders
    n_acad_a_all= n_acad_a_senior_leaders + n_acad_a_class_leaders
    n_nonacad_p_senior_leaders=int(len(df[(df['type']!=22) & (df['seniority']==1.0) & (df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
    n_nonacad_p_class_leaders=int(len(df[(df['type']!=22) & (df['seniority']==2.0)&(df['Z1']==1.0) & (df[questionIDs[0]] >=0)]))
    n_nonacad_p_all= n_nonacad_p_class_leaders + n_nonacad_p_senior_leaders
    n_nonacad_s_senior_leaders=int(len(df[(df['type']!=22) & (df['seniority']==1.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
    n_nonacad_s_class_leaders=int(len(df[(df['type']!=22) & (df['seniority']==2.0)&(df['Z1']==2.0) & (df[questionIDs[0]] >=0)]))
    n_nonacad_s_all= n_nonacad_s_senior_leaders + n_nonacad_s_class_leaders
    n_nonacad_a_senior_leaders=n_nonacad_p_senior_leaders + n_nonacad_s_senior_leaders
    n_nonacad_a_class_leaders=n_nonacad_p_class_leaders + n_nonacad_s_class_leaders
    n_nonacad_a_all= n_nonacad_a_senior_leaders + n_nonacad_a_class_leaders
    global cacadm_exceldf
    closeended_acad_many_counts={}
    for num,questionID in enumerate(questionIDs):
        for i in list(value_labels[questionID].keys()):
            if value_labels[questionID][i] == 'quoted':
                answer_df=df[df[questionID] == i]
                #ACADEMIES
                #every primary senior leader teacher
                a_p_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1) & (answer_df['type']==22)])['weightpri'])/n_acad_p_senior_leaders)*100)
                #every primary classroom leader 
                a_p_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2) & (answer_df['type']==22)])['weightpri'])/n_acad_p_class_leaders)*100)
                #every primary, classroom and senior leader 
                a_p_all=(np.divide(sum((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']==22)])['weightpri'])/n_acad_p_all)*100)
                #every senior leader secondary  teacher
                a_s_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1) & (answer_df['type']==22)])['weightsec'])/n_acad_s_senior_leaders)*100)
                #every classroom leader secondary  teacher
                a_s_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2) & (answer_df['type']==22)])['weightsec'])/n_acad_s_class_leaders)*100)
                #every secondary, classroom and senior leader 
                a_s_all=(np.divide(sum((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']==22)])['weightsec'])/n_acad_s_all)*100)
                #every primary and secondary, senior leader 
                a_a_senior_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1) & (answer_df['type']==22)])['weightall'])/n_acad_a_senior_leaders)*100)
                #every primary and secondary, classroom leader 
                a_a_class_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2) & (answer_df['type']==22)])['weightall'])/n_acad_a_class_leaders)*100)
                #every primary and secondary, classroom and senior leader 
                a_a_all=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']==22)])['weightall'])/n_acad_a_all)*100)
                #NON-ACADEMIES
                #every primary senior leader teacher
                na_p_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==1) & (answer_df['type']!=22)])['weightpri'])/n_nonacad_p_senior_leaders)*100)
                #every primary classroom leader 
                na_p_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==1) & (answer_df['seniority']==2) & (answer_df['type']!=22)])['weightpri'])/n_nonacad_p_class_leaders)*100)
                #every primary, classroom and senior leader 
                na_p_all=(np.divide(sum((answer_df[(answer_df['Z1']==1) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']!=22)])['weightpri'])/n_nonacad_p_all)*100)
                #every senior leader secondary  teacher
                na_s_senior_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==1) & (answer_df['type']!=22)])['weightsec'])/n_nonacad_s_senior_leaders)*100)
                #every classroom leader secondary  teacher
                na_s_class_leaders=(np.divide(sum((answer_df[(answer_df['Z1']==2) & (answer_df['seniority']==2) & (answer_df['type']!=22)])['weightsec'])/n_nonacad_s_class_leaders)*100)
                #every secondary, classroom and senior leader 
                na_s_all=(np.divide(sum((answer_df[(answer_df['Z1']==2) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']!=22)])['weightsec'])/n_nonacad_s_all)*100)
                #every primary and secondary, senior leader 
                na_a_senior_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==1) & (answer_df['type']!=22)])['weightall'])/n_nonacad_a_senior_leaders)*100)
                #every primary and secondary, classroom leader 
                na_a_class_leaders=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & (answer_df['seniority']==2) & (answer_df['type']!=22)])['weightall'])/n_nonacad_a_class_leaders)*100)
                #every primary and secondary, classroom and senior leader 
                na_a_all=(np.divide(sum((answer_df[((answer_df['Z1']==1)|(answer_df['Z1']==2)) & ((answer_df['seniority']==1) | (answer_df['seniority']==2)) & (answer_df['type']!=22)])['weightall'])/n_nonacad_a_all)*100)

                question_name=questions[questionID].split('?')[1]        
                closeended_acad_many_counts[question_name]=[round(a_p_senior_leaders,2),
                             round(a_p_class_leaders,2),round(a_p_all,2),round(a_s_senior_leaders,2),
                             round(a_s_class_leaders,2),round(a_s_all,2),round(a_a_senior_leaders,2),
                             round(a_a_class_leaders,2),round(a_a_all,2),round(na_p_senior_leaders,2),
                             round(na_p_class_leaders,2),round(na_p_all,2),round(na_s_senior_leaders,2),
                             round(na_s_class_leaders,2),round(na_s_all,2),round(na_a_senior_leaders,2),
                             round(na_a_class_leaders,2),round(na_a_all,2)]
    
    closeended_acad_many_counts.update({'N':[n_acad_p_senior_leaders,n_acad_p_class_leaders,n_acad_p_all,n_acad_s_senior_leaders,
                        n_acad_s_class_leaders,n_acad_s_all,n_acad_a_senior_leaders,n_acad_a_class_leaders,n_acad_a_all,
                        n_nonacad_p_senior_leaders,n_nonacad_p_class_leaders,n_nonacad_p_all,n_nonacad_s_senior_leaders,
                        n_nonacad_s_class_leaders,n_nonacad_s_all,n_nonacad_a_senior_leaders,n_nonacad_a_class_leaders,
                        n_nonacad_a_all]})
    cacadm_exceldf=pd.DataFrame(closeended_acad_many_counts).T
    cacadm_exceldf.columns=acad_columns
    cacadm_exceldf = pd.concat([cacadm_exceldf.drop('N', axis=0), cacadm_exceldf.loc[['N'], :]], axis=0)
    cacadm_exceldf=cacadm_exceldf.drop(cacadm_exceldf.T[cacadm_exceldf.T['N']==0].index,axis=1)
    if (n_acad_p_senior_leaders ==0 and n_acad_p_class_leaders==0 and  n_acad_p_all==0):
        cacadm_exceldf=cacadm_exceldf.drop(['Acad All senior leaders','Acad All class teachers','Acad All all'],axis=1)
    if (n_nonacad_p_senior_leaders ==0 and n_nonacad_p_class_leaders==0 and  n_nonacad_p_all==0):
        cacadm_exceldf=cacadm_exceldf.drop(['Non-Acad All senior leaders','Non-Acad All class teachers','Non-Acad All all'],axis=1)
    
#closeended_acad_many(['S4_1','S4_2','S4_3','S4_4','S4_5','S4_6','S4_7','S4_8','S4_9_OtherResponse'])
#closeended_acad_many(['S7_1','S7_2','S7_3','S7_4','S7_5','S7_6'])



while True:
    x=int(input('1) Are you creating tables for All(1) or Academies(2) ? '))
    if x == 1:
        y=int(input('2) Is the question(s) openended(1) or closeended(2)? '))
        if y == 1:
            z=int(input('3) Does this table contain more than one question e.g A2_1, A2_2, A2_3...  Yes(1) or No (2) ? '))
            if z==1:
                a=int(input('3a) Is this table showing the other responses answer for a previous question? Yes(1) or No (2): '))
                if a== 1:
                    qID=list(input("Please type the Question IDs for this openended other responses table inside '', seperated with a comma e.g 'A2_1','A2_2',A2_3'...: "))
                    openended_all_responses(qID)
                    break
                if a==2:
                    qID=list(input("Please type the Question IDs for this openended multi question table inside '', seperated with a comma e.g 'A2_1','A2_2',A2_3'...: "))
                    openended_all_many(qID)
                    break
            if z==2:
                qID=str(input('Please type the Question ID for this openended single question table for all types of schools: '))
                openended_all(qID)
                break
        if y==2:
            z=int(input('3) Does this table contain more than one question e.g A2_1, A2_2, A2_3...  Yes(1) or No (2) ? '))
            if z==1:
                qID=list(input("Please type the Question IDs for this closeended multi question table inside '', seperated with a comma e.g 'A2_1','A2_2',A2_3'...: "))
                closeended_all_many(qID)
                break
            if z==2:
                qID=str(input('Please type the Question ID for this closeended single question table for all types of schools: '))
                closeended_all(qID)
                break












