# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import libraries
import pandas as pd
import numpy as np
import os

path = r'C:\\Users\\npirt\\Documents\\Instacart basket analysis 03-2023'




#####1
df_prods = pd.read_csv(os.path.join(path, '02 Data', 'Original data', 'products.csv'))

#locate rows with NAs
df_prods.isnull().sum()
df_nan = df_prods[df_prods['product_name'].isnull() == True]


df_prods.shape #rows before cleaning

df_prods_clean = df_prods[df_prods['product_name'].isnull() == False] #removing rows with NAs
df_prods_clean.shape

#instead of subsetting, can drop all NAs from df: df_prods.dropna(inplace = True)
# of from a certain column: df_prods.dropna(subset = [‘column_name’], inplace = True)

#find rows that are duplicates
df_dups = df_prods_clean[df_prods_clean.duplicated()]

#drop duplicates
df_prods_clean_no_dups = df_prods_clean.drop_duplicates()
df_prods_clean_no_dups.shape





#####2
#determine whether anything about the data looks off or should be investigated further
df_ords = pd.read_csv(os.path.join(path, '02 Data', 'Prepared data', 'orders_wrangled.csv'))
df_ords.shape

df_ords.describe()
df_ords['order_id'] = df_ords['order_id'].astype('str')
df_ords['user_id'] = df_ords['user_id'].astype('str')
df_ords.dtypes

pd.set_option('display.max_columns', None)
df_ords.describe().apply(lambda s: s.apply('{0:.5f}'.format))

##All of the values in this dataframe's columns seem to have values that appear normal.




#####3
#check if any columns have mixed data
for col in df_ords.columns.tolist():
  weird = (df_ords[[col]].applymap(type) != df_ords[[col]].iloc[0].apply(type)).any(axis = 1)
  if len (df_ords[weird]) > 0:
    print (col)

##No columns were printed from this for loop function so no columns have mixed data.




#####5
#missing data in df_ords dataframe
df_ords.isnull().sum()

df_nan_ords = df_ords[df_ords['days_since_prior_order'].isnull() == True]

##Missing values in the days_since_prior_order column are because this is the first order for all 
##customers so there are no days since prior order

#####6
##I did not remove the NA values in this column because they mean something in this dataset:
##that these are each customers first orders.




#####7
#find rows that are duplicates in df_ords dataframe
df_dups_ords = df_ords[df_ords.duplicated()]

##The df_dups_ords dataframe has no rows, indicating there are no duplicate values.





#####8
##No duplicate values were found so no action was required to deal with them.




#####9
#export cleans csv files
df_prods_clean_no_dups.to_csv(os.path.join(path, '02 Data','Prepared data', 'products_checked.csv'))
df_ords.to_csv(os.path.join(path, '02 Data','Prepared data', 'orders_checked.csv'))
