#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import the necessary libraries needed to perform the analysis

import pandas as pd
import numpy as np
import seaborn as sns
import seaborn as sn
from matplotlib import pyplot as plt
pd.set_option('display.max_rows', 2000) # used to expand the number of visible rows within Jupiter 

#assign a name to the data sets and import them into a dataframe
athletes = 'athletes.csv' 
countries = 'countries.csv'

#read in the athletes csv
athletes = pd.read_csv('athletes.csv',encoding='ISO-8859-1')
athletes.head()


# In[2]:


#read in the countries csv and view the first five results
countries = pd.read_csv('countries.csv',encoding='ISO-8859-1')
countries.head()


# In[3]:


# show the data types in order to determine if any changes are needed
athletes.dtypes


# In[4]:


# another way to view the data types
athletes.info()


# In[5]:


# what are the basis statistics of the data
athletes.describe()


# In[6]:


#Data Cleaning

# Check the entire df for NAs
athletes.isnull().values.any()


# In[7]:


# since there NAs we need to check each column to see where they are

dob_na= athletes['dob'].isnull().sum()
print('There are', dob_na, 'dob NAs')

name_na= athletes['name'].isnull().sum()
print('There are', name_na, 'name NAs')

nationality_na= athletes['nationality'].isnull().sum()
print('There are', nationality_na, 'nationality NAs')

sex_na= athletes['sex'].isnull().sum()
print('There are',sex_na, "sex NAs")

height_na= athletes['height'].isnull().sum()
print('There are', height_na, 'height NAs')

weight_na= athletes['weight'].isnull().sum()
print('There are', weight_na, 'weight NAs')

sport_na= athletes['sport'].isnull().sum()
print('There are', sport_na, 'sport NAs')

gold_na= athletes['gold'].isnull().sum()
print('There are',gold_na, 'gold medal NAs')

silver_na= athletes['silver'].isnull().sum()
print('There are', silver_na, 'silver medal NAs')

bronze_na= athletes['bronze'].isnull().sum()
print('There are',bronze_na, 'bronze medal NAs')

age_na= athletes['age'].isnull().sum()
print('There are',age_na, 'age NAs')


# In[8]:


#Since the dob column has only 1 NA, we will delete that value from the dataframe
# removing all of the NA rows would delete almost 8% of the data
# we will replace each columns NAs with the mean value of the column

athletes= athletes.dropna(subset =['dob'])


# In[9]:


# recheck the dob column to see if NAs were removed
dob_na= athletes['dob'].isnull().sum()
print('There are', dob_na, 'dob NAs')


# In[10]:


# using info we see that only one row was removed from the original dataset
athletes.info()


# In[11]:


# replace NAs in the height and weight columns with their respective column means

athletes['height'].fillna(value=athletes['height'].mean(), inplace=True)
athletes['weight'].fillna(value=athletes['weight'].mean(), inplace=True)


# In[12]:


# Check the entire df for NAs

athletes.isnull().values.any()


# In[14]:


#add a column that addes the gold, silver and broze columns together
athletes['Total Medals'] = athletes['gold']+athletes['silver']+athletes['bronze']
athletes.head()


# In[15]:


#Sort total medals from highest to lowest
athletes.sort_values(by=['Total Medals'], inplace=True, ascending=False)
athletes


# In[16]:


# convert the weight column from kilograms to to lbs by multiplying weight by 2.2

athletes['Weight in Lbs'] = athletes['weight']*2.2
athletes.head()

# convert the height column from meters to feet by multiplying height by 3.28084
athletes['Height in Feet'] = athletes['height']*3.28084
athletes.head()


# In[17]:


#convert the 'nationality' column name to 'code' in order to merge with gdp dataset
athletes = athletes.rename(columns={'nationality':'code'}, inplace = False)
athletes.head()


# In[18]:


#Now using the left merge function we combine the athletes and countries files based on the country code
# The left function was used because I wanted to keep any un-matched values

athletes_gdp = pd.merge(athletes,countries, on='code',how='left')
athletes_gdp.head()


# In[19]:


#drop the 'id','weight' and 'height' columns since not needed
athletes_gdp = athletes_gdp.drop(['id'], axis =1)
athletes_gdp = athletes_gdp.drop(['weight'], axis =1)
athletes_gdp = athletes_gdp.drop(['height'], axis =1)

#round the gdp column to two decimals
athletes_gdp = athletes_gdp.round(decimals=2)
athletes_gdp.head()


# In[20]:


population_na= athletes_gdp['population'].isnull().sum()
print('There are', population_na, 'population NAs')

gdp_per_capita_na= athletes_gdp['gdp_per_capita'].isnull().sum()
print('There are', gdp_per_capita_na, 'gdp_per_capita NAs')


# In[21]:


#Data Analytics

#Correlation Dataframe
#create a new dataframe with specific columns used to run a correlation matrix
selected_columns = athletes_gdp[['code','sex','sport','Total Medals','Weight in Lbs','Height in Feet','population','gdp_per_capita']]

corr_df = selected_columns.copy()

corr_df.head(5)


# In[22]:


#Run a correlation matric

corrMatrix = corr_df.corr()
sn.heatmap(corrMatrix, annot=True)
plt.show()


# In[23]:


#Research Questions

#use the group function to sum the total medals by country and sort from highest to lowest
grouped_country_sum = athletes_gdp.groupby(['country'])['Total Medals'].sum().reset_index() #reset_index converts back to df
sorted_country_sum = grouped_country_sum.sort_values('Total Medals', ascending = False)

print(sorted_country_sum)


# In[24]:


#Create a bar chart
sorted_country_sum.head(5).plot(kind='bar', x='country', figsize=(15,8), title ="Top 5 Countries with Most Medals")


# In[25]:


#use the group function to sum the total medals by sport and sort from highest to lowest
grouped_sport_sum = athletes_gdp.groupby(['sport'])['Total Medals'].sum().reset_index() #reset_index converts back to df
sorted_sport_sum = grouped_sport_sum.sort_values('Total Medals', ascending = False)

print(sorted_sport_sum)


# In[26]:


#create a  bar chart of the results
sorted_sport_sum.head(5).plot(kind='bar', x='sport', figsize=(15,8), title ="Top 5 Sports with Most Medals")


# In[42]:


#use the group function to sum the total medals by sex and sort from highest to lowest
grouped_name = athletes_gdp.groupby(['sport'])['name'].count().reset_index() #reset_index converts back to df
sorted_name = grouped_name.sort_values('name', ascending = False)

print(sorted_name)


# In[27]:


#use the group function to sum the total medals by sex and sort from highest to lowest
grouped_sex = athletes_gdp.groupby(['sex'])['Total Medals'].sum().reset_index() #reset_index converts back to df
sorted_sex = grouped_sex.sort_values('Total Medals', ascending = False)

print(sorted_sex)


# In[28]:


#show the country by sex and total medals won
grouped_country_sex = athletes_gdp.groupby(['country','sex'])['Total Medals'].sum().reset_index() #reset_index converts back to df
sorted_country_sex = grouped_country_sex.sort_values('Total Medals', ascending = False)

print(sorted_country_sex)


# In[29]:


#show country and medals won by sport
grouped_country_sport = athletes_gdp.groupby(['country','sport'])['Total Medals'].sum().reset_index() #reset_index converts back to df
sorted_country_sport = grouped_country_sport.sort_values('Total Medals', ascending = False)

print(sorted_country_sport)


# In[30]:


grouped_country_gdp = athletes_gdp.groupby(['country','gdp_per_capita'])['Total Medals'].sum().reset_index() #reset_index converts back to df
sorted_country_gdp = grouped_country_gdp.sort_values('gdp_per_capita', ascending = False)

print(sorted_country_gdp)


# In[31]:


# using the groupby function we group the GDP metric with total Medals and graph it

plt.figure(figsize=(12,5))
plt.scatter('gdp_per_capita','Total Medals',data=sorted_country_gdp,s=15)

plt.title('Country GDP vs Total Medals Won')


# In[32]:


#group and sort the country population from highest to lowest to view total medals won
grouped_country_pop = athletes_gdp.groupby(['country','population'])['Total Medals'].sum().reset_index() #reset_index converts back to df
sorted_country_pop = grouped_country_pop.sort_values('population', ascending = False)

print(sorted_country_pop)


# In[33]:


#create a scatter plot of the country population and total medals won

plt.figure(figsize=(12,5))
plt.scatter('population','Total Medals',data=sorted_country_pop,s=15)

plt.title('Country Population vs Total Medals Won')


# In[34]:


#Lets look at Age and gold medals to see any correlations

grouped_age = athletes_gdp.groupby(['age'])['Total Medals'].sum().reset_index() #reset_index converts back to df
sorted_age = grouped_age.sort_values('Total Medals', ascending = False)

print(sorted_age)


# In[35]:


#Plot the age and total medals won by age
athletes_gdp.groupby(['age'])['Total Medals'].sum().plot(kind='bar', figsize=(15,8), title="Total Medals by Age")


# In[36]:


athletes_gdp.head(5)


# In[37]:


#Per the bar chart, some athletes are over the age of 50 and still win. How many over 50 won a medal
athletes_gdp['name'][athletes_gdp['age']>50].count()


# In[38]:


#what sport do the athletes over 50 compete in?
#create a df for athletes over 50

Over_50 = athletes_gdp['sport'][athletes_gdp['age']>50]

plt.figure(figsize=(10,8))
plt.tight_layout()
sns.countplot(Over_50)
plt.title("Sport Played for Athletes Over 50 that Won a Medal")


# In[39]:


#per the correlation matric above, the height and weight are the strongest correlated. 
#Create a scatter plot to visually view the relationship

plt.figure(figsize=(12, 10))
plt.scatter('Height in Feet','Weight in Lbs',data=athletes_gdp,s=10)

plt.title('Height vs Weight of Olympic Medalists')

