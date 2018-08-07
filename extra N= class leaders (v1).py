# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import savReaderWriter 
from savReaderWriter import *

#read spss.sav file
with SavReader('L:\OMIZ\Omi final_weights_v4_R.sav',ioUtf8=True,returnHeader=True) as reader:
    records=reader.all()

#read in meta data
with SavHeaderReader('L:\OMIZ\Omi final_weights_v4_R.sav',ioUtf8=True) as header:
   metadata = header.all()

#get the info for value labels
value_labels=metadata[2]

#use the columns of the dataframe as the first item of records list
columns=records[0]
#delete that item as it is the column names
del records[0]
#create dataframe
df=pd.DataFrame(records)
#rename columns
df.columns=columns
#read in log files




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
    openended_all_counts={}
    for i in list(value_labels[questionID].keys()):
        p_senior_leaders=0
        p_class_leaders=0
        p_all=0
        s_senior_leaders=0
        s_class_leaders=0
        s_all=0  
        a_senior_leaders=0
        a_class_leaders=0
        a_all=0 
        answer_df=df[df[questionID] == i]
        for index,j in enumerate(answer_df[questionID]):
            school=answer_df['Z1'].iloc[index]
            seniority=answer_df['seniority'].iloc[index]
            #primary academy teacher
            if school == 1.0:
                #every primary academy senior leader teacher
                if seniority == 1.0:
                    p_senior_leaders+=(answer_df['weightpri'].iloc[index]/n_p_senior_leaders)*100
                #every primary academy classroom leader 
                if seniority == 2.0:
                    p_class_leaders+=(answer_df['weightpri'].iloc[index]/n_p_class_leaders)*100
                #every primary, classroom and senior leader 
                if (seniority == 1.0) or (seniority == 2.0):
                    p_all+=(answer_df['weightpri'].iloc[index]/n_p_all)*100
            #every secondary academy teacher
            if school == 2.0:
                #every senior leader secondary academy teacher
                if seniority == 1.0:
                    s_senior_leaders+=(answer_df['weightsec'].iloc[index]/n_s_senior_leaders)*100
                #every classroom leader secondary academy teacher
                if seniority == 2.0:
                    s_class_leaders+=(answer_df['weightsec'].iloc[index]/n_s_class_leaders)*100
                #every secondary, classroom and senior leader 
                if (seniority == 1.0) or (seniority == 2.0):
                    s_all+=(answer_df['weightpri'].iloc[index]/n_s_all)*100
            if (school == 1.0) or (school == 2.0):
                #every primary and secondary, senior leader 
                if seniority == 1.0:
                    a_senior_leaders+=(answer_df['weightall'].iloc[index]/n_s_class_leaders)*100
                #every primary and secondary, classroom leader 
                if seniority == 2.0:
                    a_senior_leaders+=(answer_df['weightall'].iloc[index]/n_s_class_leaders)*100
                #every primary and secondary, classroom and senior leader 
                if (seniority == 1.0) or (seniority == 2.0):
                    a_all+=(answer_df['weightpri'].iloc[index]/n_a_all)*100
                    
        openended_all_counts[value_labels[questionID][i]]=[p_senior_leaders,p_class_leaders,p_all,s_senior_leaders,
              s_class_leaders,s_all,a_senior_leaders,a_class_leaders,a_all]
    
    openended_all_counts.update({'N':[n_p_senior_leaders,n_p_class_leaders,n_p_all,n_s_senior_leaders,
                        n_s_class_leaders,n_s_all,n_a_senior_leaders,n_a_class_leaders,n_a_all]})
    return(openended_all_counts)

openended_all('U1')
    
def closeended_all (questionID):
    closeended_all_counts={}
    for i in list(value_labels[questionID].keys()):
        p_senior_leaders=0
        p_class_leaders=0
        p_all=0
        s_senior_leaders=0
        s_class_leaders=0
        s_all=0  
        a_senior_leaders=0
        a_class_leaders=0
        a_all=0 
        df2=df[df[questionID] == i]
        for index,j in enumerate(df2[questionID]):
            school=df2['Z1'].iloc[index]
            seniority=df2['seniority'].iloc[index]
            #primary academy teacher
            if school == 1.0:
                #every primary academy senior leader teacher
                if seniority == 1.0:
                    p_senior_leaders+=1
                #every primary academy classroom leader 
                if seniority == 2.0:
                    p_class_leaders+=1
                #every primary, classroom and senior leader 
                if (seniority == 1.0) or (seniority == 2.0):
                    p_all+=1
            #every secondary academy teacher
            if school == 2.0:
                #every senior leader secondary academy teacher
                if seniority == 1.0:
                    s_senior_leaders+=1
                #every classroom leader secondary academy teacher
                if seniority == 2.0:
                    s_class_leaders+=1
                #every secondary, classroom and senior leader 
                if (seniority == 1.0) or (seniority == 2.0):
                    s_all+=1
            if (school == 1.0) or (school == 2.0):
                a_all+=1
                if seniority == 1.0:
                    a_senior_leaders+=1
                if seniority == 2.0:
                    a_senior_leaders+=1
                #every primary and secondary, classroom and senior leader 
                if (seniority == 1.0) or (seniority == 2.0):
                    a_all+=1
                    
        closeended_all_counts[value_labels[questionID][i]]=[p_senior_leaders,p_class_leaders,p_all,s_senior_leaders,
              s_class_leaders,s_all,a_senior_leaders,a_class_leaders,a_all]
    
    closeended_all_counts.update({'N':[n_p_senior_leaders,n_p_class_leaders,n_p_all,n_s_senior_leaders,
                        n_s_class_leaders,n_s_all,n_a_senior_leaders,n_a_class_leaders,n_a_all]})


def closeended_acad (questionID):
    closeended_acad_counts={}
    for i in list(value_labels[questionID].keys()):
        a_p_senior_leaders=0
        a_p_class_leaders=0
        a_p_all=0
        a_s_senior_leaders=0
        a_s_class_leaders=0
        a_s_all=0
        a_a_senior_leaders=0
        a_a_class_leaders=0
        a_a_all=0
        na_p_senior_leaders=0
        na_p_class_leaders=0
        na_p_all=0
        na_s_senior_leaders=0
        na_s_class_leaders=0
        na_s_all=0
        na_a_senior_leaders=0
        na_a_class_leaders=0
        na_a_all=0
        df2=df[df[questionID] == i]
        for index,j in enumerate(df2[questionID]):
            academy=df2['type'].iloc[index]
            school=df2['Z1'].iloc[index]
            seniority=df2['seniority'].iloc[index]
            if academy == 22.0:
                if school == 1.0:
                #every primary academy senior leader teacher
                    if seniority == 1.0:
                        a_p_senior_leaders+=1
                    #every primary academy classroom leader 
                    if seniority == 2.0:
                        a_p_class_leaders+=1
                    #every primary, classroom and senior leader 
                    if (seniority == 1.0) or (seniority == 2.0):
                        a_p_all+=1
            #every secondary academy teacher
            if school == 2.0:
                #every senior leader secondary academy teacher
                if seniority == 1.0:
                    a_s_senior_leaders+=1
                #every classroom leader secondary academy teacher
                if seniority == 2.0:
                    a_s_class_leaders+=1
                #every secondary, classroom and senior leader 
                if (seniority == 1.0) or (seniority == 2.0):
                    a_s_all+=1
            if (school == 1.0) or (school == 2.0):
                a_a_all+=1
                if seniority == 1.0:
                    a_a_senior_leaders+=1
                if seniority == 2.0:
                    a_a_senior_leaders+=1
                #every primary and secondary, classroom and senior leader 
                if (seniority == 1.0) or (seniority == 2.0):
                    a_a_all+=1
            if academy != 22.0:
                #every person who answered in a non-academy
                na_a_all+=1
                #every senior leader in a non-academy
                if seniority == 1.0:
                    na_a_senior_leaders+=1
                #every classroom leader in a non-academy
                if seniority == 2.0:
                    na_a_class_leaders+=1    
                if school == 1.0:
                    #every primary non-academy teacher
                    na_p_all+=1
                    #every primary non-academy senior leader teacher
                    if seniority == 1.0:
                        na_p_senior_leaders+=1
                        #every primary non-academy classroom leader 
                    if seniority == 2.0:
                        na_p_class_leaders+=1
                if school == 2.0:
                    #every secondary non-academy teacher
                    na_s_all+=1
                    if seniority == 1.0:
                        #every senior leader secondary non-academy teacher
                        na_s_senior_leaders+=1
                        #every classroom leader secondary non-academy teacher
                    if seniority == 2.0:
                        na_s_class_leaders+=1
                    
        closeended_acad_counts[value_labels[questionID][i]]=[a_p_senior_leaders,a_p_class_leaders,a_p_all,a_s_senior_leaders,a_s_class_leaders,
           a_s_all,a_a_senior_leaders,a_a_class_leaders,a_a_all,na_p_senior_leaders,na_p_class_leaders,
           na_p_all,na_s_senior_leaders,na_s_class_leaders,na_s_all,na_a_senior_leaders,na_a_class_leaders,
           na_a_all]

