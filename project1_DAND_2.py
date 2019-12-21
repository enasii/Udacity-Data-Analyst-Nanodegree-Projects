#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigate a Dataset (TMDb movie data analysis)
# # By Enas Alshamrani
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# For Project 2 i use TMDb movie data set . This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue.
# 
# 

# ## Questions to be Answered
# General questions about the dataset.
# <ul>
# <li><a href="#q1">What the Average Runtime Of Movies each Year?</a></li>
# <li><a href="#q2">How much movie Released by year?</a></li>
# </ul>
# What are the similar characteristics does the most seccussful movie have :
# <ul>
# <li><a href="#q3">What is The Top 7 Movie Genre With Highest Release?</a></li>
# <li><a href="#q6">What is Average Budget of the movies?</a></li>
# <li><a href="#q4">What is The Top 7 directors With the highest Number of movie they direct?</a></li>
# <li><a href="#q5">What is The Most Frequent Cast?</a></li>   
# </ul>

# In[54]:


# Use this cell to set up import statements for all of the packages that i need
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# 
# ### General Properties

# In[55]:


#reading tmdb csv file and storing that to a variable
df = pd.read_csv('tmdb-movies.csv')
type(df)


# In[56]:


df.head()


# In[57]:


df.shape


# In[58]:


df.info()


# In[59]:


df.describe()


# ## we can see from the data set that:
#  * The columns ('budget', 'revenue', 'budget_adj', 'revenue_adj')has no currency so i assume it is dollars.
#  * many movies has budget or revenue of '0' value
#  * many duplication in the rows in the dataset
#  * the Format Of 'Release Date' colmn should be in a Datetime Format
#  * many colmn that not useful in the data analysist so it should be remove 

# 
# 
# ## Data Cleaning

# ### The duplication

# In[60]:


#count the duplicate 
sum(df.duplicated())


# In[61]:


#removing duplicate value
df.drop_duplicates(inplace = True)
print("Afetr Removing Duplicate Values (Rows,Columns) : ",df.shape)


# ###  Changing Format Of Release Date Into Datetime Format

# In[62]:


df['release_date'] = pd.to_datetime(df['release_date'])
df['release_date'].head()


# ### Remove colmn that not useful

# In[63]:


df.drop(['overview','imdb_id','homepage','tagline'],axis =1,inplace = True)
print("Afetr Remove colmn that not useful (Rows,Columns) : ",df.shape)


# In[64]:


#giving list of column names that needs to be checked
check_row = ['budget', 'revenue']

#this will replace the value of '0' to NaN of columns given in the list
df[check_row] = df[check_row].replace(0, np.NaN)

#now we will drop any row which has NaN values in any of the column of the list (check_row) 
df.dropna(subset = check_row, inplace = True)


# In[65]:


df.shape


# Since now we have the columns, rows and format of the dataset in right way, its time to investigate the data for the questions asked.

# <a id='eda'></a>
# ## Exploratory Data Analysis

# <a id='q1'></a>
# ### Research Question 1  (Average Runtime Of Movies each Year?)

# In[67]:


#how the runtime of the movies differ year to year.

#make the group of the data according to their release_year and find the mean  related to this and plot.
df.groupby('release_year').mean()['runtime'].plot(xticks = np.arange(1960,2016,5))

#setup the figure size.
sns.set(rc={'figure.figsize':(10,5)})

#setup the title of the figure
plt.title("Runtime Vs Year",fontsize = 14)

#setup the x-label and y-label of the plot.
plt.xlabel('Year',fontsize = 13)
plt.ylabel('Runtime',fontsize = 13)
sns.set_style('ticks')


# In[68]:



print('Year 1965 have the highest Average Runtime , in geranale the Average Runtime decreases as time progresses.')


# In[69]:


calculat_avg = df['runtime'].mean()
print('And the Average Runtime',calculat_avg)


# <a id='q2'></a>
# ### Research Question 2  (How much movie Released by year?)

# In[70]:


# make group for each year and count the number of movies in each year 
data=df.groupby('release_year').count()['id']
print(data.tail())

#make group of the data according to their release year and count the total number of movies in each year and pot.
df.groupby('release_year').count()['id'].plot(xticks = np.arange(1960,2016,5))

#set the figure size and labels
sns.set(rc={'figure.figsize':(10,5)})
plt.title("Year Vs Number Of Movies",fontsize = 14)
plt.xlabel('Release year',fontsize = 13)
plt.ylabel('Number Of Movies',fontsize = 13)
#set the style sheet
sns.set_style("whitegrid")


# In[71]:


print ('Maximum Number Of Movies Release In year 2011.')


# <a id='q3'></a>
# ### Research Question 3  (Top 7 Genre With Highest Release?)

# In[73]:


#function which will take any column as argument from which data is need to be extracted and keep track of count
def extract_data(column_name):
    #will take a column, and separate the string by '|'
    all_data = df[column_name].str.cat(sep = '|')
    
    #giving pandas series and storing the values separately
    all_data = pd.Series(all_data.split('|'))
    
    #this will us value in descending order
    count = all_data.value_counts(ascending = False)
    
    return count


# In[74]:



#call the function for counting the movies of each genre.
total_genre_movies = extract_data('genres')
#plot a 'barh' plot using plot function for 'genre vs number of movies'.
total_genre_movies.iloc[:7].plot(kind='barh',figsize = (13,6),fontsize=12,colormap='tab20c')

#setup the title and the labels of the plot.
plt.title("Top 7 Genre With Highest Release",fontsize=15)
plt.xlabel('Number Of Movies',fontsize=13)
plt.ylabel("Genres",fontsize= 13)
sns.set_style()


# In[75]:


print('Drame, Comedy, Thriller and Action are four most-made genres.')


# <a id='q6'></a>
# ### Research Question 4  ( Average Budget of the movies?)

# In[81]:


calculat_avg = df['budget'].mean()
calculat_avg


# <a id='q4'></a>
# ### Research Question 5  (Top 7 director With Number of movie they direct?)

# In[77]:


count_director_movies = extract_data('director')

#plot a barh graph
count_director_movies.iloc[:7].plot(kind='bar',figsize=(13,6),fontsize=12)

#setup the title and the labels 
plt.title("Director Vs Number Of Movies",fontsize=15)
plt.xticks(rotation=70)
plt.ylabel("Number Of Movies",fontsize= 13)
sns.set_style("whitegrid")


# In[78]:


print('Robert De Niro has the hiegest number of movie that he direct then Bruce Willis and Samuel L. Jackson')


# <a id='q5'></a>
# ### Research Question 6  (Most Frequent Cast?)

# In[80]:


count_c = extract_data('cast')
#printing top 5 values
count_c.head()


# <a id='conclusions'></a>
# ## Conclusions
# 

# We came out with some very interesting facts about movies. After this analysis we can conclude following:
# 
# For a Movie to be in successful criteria
# 
# Average Budget must be around 37 millon dollar
# Average duration of the movie must be 109 minutes
# Any one of these should be in the cast :Robert De Niro, Bruce Willis , Samuel L. Jackson 
# Genre must be : Drame, Comedy, Thriller , Action
# 
# By doing all this will Give the movie a chance to become one of the best .
# 

# ### Limitations
# 
# It's not 100 percent guaranteed solution that this formula is gonna work, But this suggestion can increase the probability of a movie to become a great movie. However, I am not sure if the data provided to me is completely correct and up-to-date.
# 
# During the data cleaning process, I split the data seperated by '|' into lists for easy parsing during the exploration phase. This increases the time taken in calculating the result.
# Dropping rows with missing values also affect the overall analysis.
# Also, columns like ('budget', 'revenue') has no currency so I assume it is dollars but it depend on the country that moveis made in.
