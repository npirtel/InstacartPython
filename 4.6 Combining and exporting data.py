# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 09:04:39 2023

@author: npirt
"""

#import libraries, set path
import pandas as pd
import os

path = r'C:\\Users\\npirt\\Documents\\Instacart basket analysis 03-2023'




#####1
#read files
df_ords_prior = pd.read_csv(os.path.join(path, '02 Data', 'Original data', 'order_products_prior.csv'))
df_ords = pd.read_csv(os.path.join(path, '02 Data', 'Prepared data', 'orders_checked.csv'))



#consistency checks for ords_prior df
df_ords_prior.isnull().sum() #no NA values
df_dups = df_ords_prior[df_ords_prior.duplicated()] #no duplicate rows
for col in df_ords.columns.tolist():
  weird = (df_ords[[col]].applymap(type) != df_ords[[col]].iloc[0].apply(type)).any(axis = 1)
  if len (df_ords[weird]) > 0:
    print (col) #no mixed data columns

#check data shape
df_ords_prior.shape
df_ords.shape

#merge dataframes using order_id column
df_merged_large = df_ords.merge(df_ords_prior, on = 'order_id', indicator=True)

pd.set_option('display.max_columns', None) #display all columns
df_merged_large.head()

#check type of merge
df_merged_large['_merge'].value_counts()





#####2
#export data to pkl file
df_merged_large.to_pickle(os.path.join(path, '02 Data', 'Prepared data', 'orders_products_combined.pkl'))
