# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 10:00:19 2023

@author: npirt
"""
######1
#import libraries, set path
import pandas as pd
import numpy as np
import os

path = r'C:\\Users\\npirt\\Documents\\Instacart basket analysis 03-2023'

#read files
ords_prods_merge = pd.read_pickle(os.path.join(path, '02 Data', 'Prepared data', 'orders_products_combine_stats.pkl'))

pd.options.display.max_rows = None #no limit to rows displayed
pd.set_option('display.max_columns', None) #display all columns in head
ords_prods_merge.head(15)




#subset file up to row 1,000,000
df = ords_prods_merge[:1000000]
df.head(10)

#group by department id of subset, aggregate by mean number of orders
df.groupby('department_id').agg({'order_number': ['mean']})

#alternative to above code: df.groupby('department_id')['order_number'].mean()

#group by department id of subset, aggregate by min, mean, max number of orders
df.groupby('department_id').agg({'order_number': ['mean', 'min', 'max']})





######2
#in entire dataframe, group by department id, aggregate by mean number of orders
ords_prods_merge.groupby('department_id').agg({'order_number': ['mean']})





######3
##These results differ from the subset because there are all of the departments included (21) vs only 8 in the subset.
##Also, in the subset, department 16 (dairy, eggs) had the highest mean orders while in the entire dataframe, department
##10 (bulk) had the highest mean orders (besides dept 21, which is 'missing'). As expected, aggregating columns in the
##entire dataframe gives us a more accurate picture of trends.




######4
#obtain maximum number of orders of every customer based on order_number column
ords_prods_merge['max_order'] = ords_prods_merge.groupby(['user_id'])['order_number'].transform(np.max)
ords_prods_merge.head(100)


#assign loyalty flag to all customers based on number of orders
ords_prods_merge.loc[ords_prods_merge['max_order'] > 40, 'loyalty_flag'] = 'Loyal customer'
ords_prods_merge.loc[(ords_prods_merge['max_order'] <= 40) & (ords_prods_merge['max_order'] > 10),
                     'loyalty_flag'] = 'Regular customer'
ords_prods_merge.loc[ords_prods_merge['max_order'] <= 10, 'loyalty_flag'] = 'New customer'

#check values of flags
ords_prods_merge['loyalty_flag'].value_counts(dropna = False)

#see if flags populated correctly
ords_prods_merge[['user_id', 'loyalty_flag', 'order_number']].head(60)




######5
#group by loyalty_flag and aggregate mean prices
ords_prods_merge.groupby('loyalty_flag').agg({'prices': ['mean']})

##The average price of products purchased by loyal customers is actually lowest compared to new and regular customers.
##On average, a loyal customer paid $10.39, regular customers $12.50 and new customers $13.29.





######6
#create column that averages customer order prices
ords_prods_merge['avg_order_cost'] = ords_prods_merge.groupby(['user_id'])['prices'].transform(np.mean)
ords_prods_merge.head(20)


#assign spender flag to all customers based on average order price
ords_prods_merge.loc[ords_prods_merge['avg_order_cost'] >= 10, 'spender_flag'] = 'High spender'
ords_prods_merge.loc[ords_prods_merge['avg_order_cost'] < 10, 'spender_flag'] = 'Low spender'

#check values of flags
ords_prods_merge['spender_flag'].value_counts(dropna = False)

#see if flags populated correctly
ords_prods_merge[['user_id', 'spender_flag', 'avg_order_cost']].head(60)





######7
#create column that describes median days since prior order for every customer
ords_prods_merge['median_days_since_order'] = ords_prods_merge.groupby(['user_id'])['days_since_prior_order'].transform(np.median)
ords_prods_merge.head(20)


#assign freq flag to all customers based on median days since prior order
ords_prods_merge.loc[ords_prods_merge['median_days_since_order'] <= 10, 'freq_flag'] = 'Frequent customer'
ords_prods_merge.loc[(ords_prods_merge['median_days_since_order'] <= 20) & 
                     (ords_prods_merge['median_days_since_order'] > 10), 'freq_flag'] = 'Regular customer'
ords_prods_merge.loc[ords_prods_merge['median_days_since_order'] > 20, 'freq_flag'] = 'Non-frequent customer'

#check values of flags
ords_prods_merge['freq_flag'].value_counts(dropna = False)

##There are 5 NA values present for this flag, maybe because they only placed 1 order.

#see if flags populated correctly
ords_prods_merge[['user_id', 'freq_flag', 'median_days_since_order']].head(60)




#remove outliers from prices column
ords_prods_merge['prices'].describe() #max value is very high


#find all items with prices over $100, a realistic maximum price in a grocery store
ords_prods_merge.loc[ords_prods_merge['prices'] > 100]

#assign NAs to prices over $100
ords_prods_merge.loc[ords_prods_merge['prices'] > 100, 'prices'] = np.nan
ords_prods_merge['prices'].max() #check max value of column, is now $25





######9
#export dataframe with new columns and aggregated variables
ords_prods_merge.to_pickle(os.path.join(path, '02 Data', 'Prepared data', 'orders_products_group_agg.pkl'))
