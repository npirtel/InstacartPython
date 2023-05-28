# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 08:43:15 2023

@author: npirt
"""

#import libraries
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

#import combined dataset
path = r'C:\\Users\\npirt\\Documents\\Instacart basket analysis 03-2023'





######1
ords_prods_cust = pd.read_pickle(os.path.join(path, '02 Data', 'Prepared data', 'orders_products_customers.pkl'))
pd.set_option('display.max_columns', None) #display all columns in head
ords_prods_cust.head()






######2
#bar chart of number of orders per day of the week
bar = ords_prods_cust['order_day_of_week'].value_counts().plot.bar(color =['purple', 'red', 'pink', 'orange', 
                                                                     'yellow', 'green', 'blue'])

##The busiest day of week to order is Sunday and least busy is Thursday.

#to sort by day of week in order:
#ords_prods_cust['order_day_of_week'].value_counts().sort_index().plot.bar()
#sort_index() can also be used when printing value counts

#save bar chart as png file
bar.figure.savefig(os.path.join(path, '04 Analysis','Visualizations', 'bar_orders_dow.png'))



#histogram of prices of products
ords_prods_cust['prices'].plot.hist(bins=25)
ords_prods_cust['prices'].describe() #max value is very high

sns.scatterplot(x='prices', y='prices', data=ords_prods_cust)


#find all items with prices over $100, a realistic maximum price in a grocery store
ords_prods_cust.loc[ords_prods_cust['prices'] > 100]

#assign NAs to prices over $100
ords_prods_cust.loc[ords_prods_cust['prices'] > 100, 'prices'] = np.nan
ords_prods_cust['prices'].max() #check max value of column, is now $25


hist = ords_prods_cust['prices'].plot.hist(bins = 70)

##Most prices are between $0-$15.

#save histogram as png file
hist.figure.savefig(os.path.join(path, '04 Analysis','Visualizations', 'hist_prices.png'))




#line chart of how prices fluctuate over the week
#using the entire dataset would take up too much space, need to randomly subset

#set seed
np.random.seed(4)
dev = np.random.rand(len(ords_prods_cust)) <= 0.7

#split lists into 70 or 30 percent of data
big = ords_prods_cust[dev] #70% rows stored here
small = ords_prods_cust[~dev] #30% rows stored here

#make sure the number of columsn adds up to dataframe amount
len(ords_prods_cust) #30,629,741
len(big) + len(small) #30,629,741

#reduce samples to only columns necessary for chart: order dow and prices
df = small[['order_day_of_week', 'prices']]


line = sns.lineplot(data=df, x='order_day_of_week', y='prices')

#save line chart as png file
line.figure.savefig(os.path.join(path, '04 Analysis','Visualizations', 'line_order_dow_prices.png'))





######3
#descriptive findings of sales - histogram order hour of day
hist2 = ords_prods_cust['order_hour_of_day'].plot.hist(bins = 24)


##The histogram indicates that most sales/orders are being placed between the hours of about 9 AM
##to 4 PM (16:00, 16 in histogram) since these bars have the highest frequencies of orders.

#save histogram
hist2.figure.savefig(os.path.join(path, '04 Analysis','Visualizations', 'hist_order_hod.png'))





######4
#bar chart for loyalty flags
bar2 = ords_prods_cust['loyalty_flag'].value_counts().plot.bar()


##This bar chart indicates that a majority of customers are regular customers, meaning they placed
##between 11-40 orders.

#save bar chart
bar2.figure.savefig(os.path.join(path, '04 Analysis','Visualizations', 'bar_loyalty_status.png'))





######5
#prices depending on hour of day
#using small sample, reduce columns to those necessary for chart
df2 = small[['order_hour_of_day', 'prices']]


line2 = sns.lineplot(data=df2, x='order_hour_of_day', y='prices')

#save line chart
line2.figure.savefig(os.path.join(path, '04 Analysis','Visualizations', 'line_order_hod_prices.png'))




######6
#customer demographics - age and number of dependants
df3 = small[['age', 'n_dependants']]
line3 = sns.lineplot(data=df3, x='age', y='n_dependants')

##There is no clear relationship between age and the number of dependants the customers have.
##The line chart shows the number of dependants is up and down across age ranges, there are
##no ages that have significantly more or less dependants.

#save line chart
line3.figure.savefig(os.path.join(path, '04 Analysis','Visualizations', 'line_age_dependants.png'))




######7
#relationship between age and spending power/income
scatter = sns.scatterplot(data=ords_prods_cust, x='age', y='income')

##The scatterplot shows that there is also no relationship between age and income, although there are
##some higher incomes around the 40-80 age range that there aren't in the 20-40 age range. A majority
##of all people in the dataset have salaries between 0-$300k per year.

#save scatterplot
scatter.figure.savefig(os.path.join(path, '04 Analysis','Visualizations', 'scatter_age_income.png'))
