# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 19:48:15 2023

@author: npirt
"""

######3
#import libraries
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

#import customer dataset
path = r'C:\\Users\\npirt\\Documents\\Instacart basket analysis 03-2023'

#read files
cust = pd.read_csv(os.path.join(path, '02 Data', 'Original data', 'customers.csv'))
pd.options.display.max_rows = None #no limit to rows displayed
pd.set_option('display.max_columns', None) #display all columns in head
cust.head(15)


######4 - wrangling
#rename columns to be consistent
cust.rename(columns = {'First Name': 'first_name',
                       'Surnam': 'last_name',
                       'Gender': 'gender',
                       'STATE': 'state',
                       'Age': 'age',
                       'fam_status': 'family_status'}, inplace=True)
cust.head(15)

##No columns will be removed yet, as we don't know what is or isn't important.





######5 - consistency checks
#missing values
cust.shape #206,209 rows in 10 columns
cust.describe() #values look within normal range
cust.isnull().sum() #first_name column has some null rows: 11,259
df_nan = cust[cust['first_name'].isnull() == True]
cust_clean = cust[cust['first_name'].isnull() == False] #removing rows with NAs

##I decided to remove rows with NA values because the customer wouldn't be
##able to be identified without a first name since many last names are repeated.
##These rows only make up 5% of the data as well so it doesn't affect the overall
##customer base much.


#duplicate values
cust_dups = cust_clean[cust.duplicated()]

##No duplicates found.


#Mixed data
#check if any columns have mixed data
for col in cust_clean.columns.tolist():
  weird = (cust_clean[[col]].applymap(type) != 
           cust_clean[[col]].iloc[0].apply(type)).any(axis = 1)
  if len (cust_clean[weird]) > 0:
    print (col)
    
##No mixed data found.




######6 - combine with products, orders combined dataframe
#save clean customer dataframe
cust_clean.to_csv(os.path.join(path, '02 Data', 'Prepared data', 'customers_clean.csv'))

#load prods, ords and customer data
cust_clean = pd.read_csv(os.path.join(path, '02 Data', 'Prepared data', 'customers_clean.csv'))
ords_prods = pd.read_pickle(os.path.join(path, '02 Data', 'Prepared data', 'orders_products_group_agg.pkl'))
ords_prods.head()

#merge ords_prods and cust_clean using user_id column
ords_prods_cust = ords_prods.merge(cust_clean, on = 'user_id', indicator=True)
ords_prods_cust.head()
ords_prods_cust['_merge'].value_counts() #all both merge types
del ords_prods_cust['_merge'] #delete merge column, not necessary for analyses
ords_prods_cust.head()

#save pickle file
ords_prods_cust.to_pickle(os.path.join(path, '02 Data', 'Prepared data', 'orders_products_customers.pkl'))
