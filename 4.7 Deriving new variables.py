# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 15:46:05 2023

@author: npirt
"""

#import libraries, set path
import pandas as pd
import numpy as np
import os

path = r'C:\\Users\\npirt\\Documents\\Instacart basket analysis 03-2023'

#read files
ords_prods_merged = pd.read_pickle(os.path.join(path, '02 Data', 'Prepared data', 'orders_products_combined_final.pkl'))

#remove repeat columns
ords_prods_merged2 = ords_prods_merged[['order_id', 'user_id', 'order_number', 'order_dow', 'order_hour_of_day', 
                                        'days_since_prior_order', 'product_id', 'add_to_cart_order', 'reordered', 
                                        'product_name', 'aisle_id', 'department_id', 'prices', 'exists']]

pd.set_option('display.max_columns', None) #display all columns in head

#spell out order_dow (day of week) column
ords_prods_merged2.rename(columns = {'order_dow': 'order_day_of_week'}, inplace=True)
ords_prods_merged2.head()

#subset file up to row 1,000,000
df = ords_prods_merged2[:1000000]

#make new row for product price range
def price_label(row):
    
    if row['prices'] <= 5:
        return 'Low-range product'
    elif (row['prices'] > 5) and (row['prices'] <= 15):
        return 'Mid-range product'
    elif row['prices'] > 15:
        return 'High range'
    else: return 'Not enough data'


#assign above strings to values in price table in new column

df['price_range'] = df.apply(price_label, axis=1) #axis = 0 all columns, axis = 0 all rows

#freq of labels in price_range column and highest price: $14.80
df['price_range'].value_counts(dropna = False)
df['prices'].max()



#######1a
#alternative to above code using .loc function, better for whole dataframe
ords_prods_merged2.loc[ords_prods_merged2['prices'] > 15, 'price_range_loc'] = 'High-range product'
ords_prods_merged2.loc[(ords_prods_merged2['prices'] <= 15) & (ords_prods_merged2['prices'] > 5), 'price_range_loc'] = 'Mid-range product' 
ords_prods_merged2.loc[ords_prods_merged2['prices'] <= 5, 'price_range_loc'] = 'Low-range product'
ords_prods_merged2['price_range_loc'].value_counts(dropna = False)




#for loop to determine busiest day of week for orders
ords_prods_merged2['order_day_of_week'].value_counts(dropna = False)

result = []

for value in ords_prods_merged2['order_day_of_week']:
    if value == 0:
        result.append('Busiest day')
    elif value == 4:
        result.append('Least busy')
    else:
        result.append("Regularly busy")
        
result

######1b
#assign values of days of week in data frame to strings in result statement
ords_prods_merged2['busiest_day'] = result
ords_prods_merged2['busiest_day']. value_counts(dropna = False)
ords_prods_merged2.head()





######2
# include multiple days of week in least and most busy categories.
result = []

for value in ords_prods_merged2['order_day_of_week']:
    if value == 0 or value ==1:
        result.append('Busiest days')
    elif value == 3 or value == 4:
        result.append('Least busy days')
    else:
        result.append("Regularly busy")
        
        
#name column for for loop values
ords_prods_merged2['busiest_days'] = result
ords_prods_merged2['busiest_days']. value_counts(dropna = False)
ords_prods_merged2.head()




######3
##The two busiest days according to the value counts in the order_dow column, values 0 and 1 are the busiest
##and 3 and 4 are the least busy. Regularly busy: 12,916,111, Busiest days: 11,864,412, Least busy days: 7,624,336.
##When adding up the frequencies of the order_dow and busiest_day column values, the number of rows for each category 
##match. order_dow: 0+1 = 11,864,412; 3+4 = 7,624,336, and all other numbers = 12,916,111.


######4
ords_prods_merged2['order_hour_of_day'].value_counts(dropna = False)

##We will define the categories as follows: Fewest (most) orders = least (greatest) 6 frequent (lower/upper 25%) 
##order hod, average orders: middle 12 order hod. Most orders = 10,11,12,13,14,15 hod; fewest orders = 0,1,2,3,4,5.
##All else = average.

#for loop to determine most and least busy hour of the day for making orders
result_hod = []
for x in ords_prods_merged2['order_hour_of_day']:
    if all([x >= 10, x <=15]):
        result_hod.append('Most orders')
    elif all([x >= 0, x <=5]):
        result_hod.append('Fewest orders')
    else:
        result_hod.append("Average orders")


#name column for for loop values
ords_prods_merged2['busiest_period_of_day'] = result_hod
ords_prods_merged2.head()

##sum(10:15) = 16,128,666; sum(0:5) = 596,328; sum avg orders hod = 15,679,865





######5
ords_prods_merged2['busiest_period_of_day']. value_counts(dropna = False)

##The values that are produced from this function: 'Most orders': 16,128,666; 'Average orders': 15,679,865;
## and 'Fewest orders': 596,328. These frequencies match the ones above.






######7
ords_prods_merged2.to_pickle(os.path.join(path, '02 Data', 'Prepared data', 'orders_products_combine_stats.pkl'))
