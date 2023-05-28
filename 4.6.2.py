# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 09:27:28 2023

@author: npirt
"""

#import libraries, set path
import pandas as pd
import os

path = r'C:\\Users\\npirt\\Documents\\Instacart basket analysis 03-2023'

#####3
#import pickle file
orders_products_combined = pd.read_pickle(os.path.join(path, '02 Data', 'Prepared data', 
                                                    'orders_products_combined.pkl'))
pd.set_option('display.max_columns', None) #display all columns
orders_products_combined.head()




#####4
orders_products_combined.shape

##The dataframe has the same number of rows (32,434,489) and columns (12) as the exported file.




#####5
df_prods = pd.read_csv(os.path.join(path, '02 Data', 'Prepared data', 'products_checked.csv'))
df_prods.head()

##Both dataframes have the product_id column, which is what we will use as a common column on the join.

#getting error with indicator=True, cannot use existing column for indicator column
#use indicator='exists' as indicator instead, adds second indicator column = 'exists'
df_merged = orders_products_combined.merge(df_prods, on = 'product_id', indicator='exists')
df_merged.head()
df_merged.shape

##After the merge, the new df has 29,630 less columns. Maybe there were products that did not have 
## a code in the combined dataframe.



#####6
#check type of merge
df_merged['exists'].value_counts()

##All flags returned a both/inner join.




#####7
#save dataframe
df_merged.to_pickle(os.path.join(path, '02 Data', 'Prepared data', 'orders_products_combined_final.pkl'))
