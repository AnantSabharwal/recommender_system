#importing the basic libraries
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

#reading the dataset
movie = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
links = pd.read_csv("links.csv")
tags = pd.read_csv("tags.csv")

# general data perprocessing
ratings.drop(columns='timestamp',inplace=True)
tags.drop(columns='timestamp',inplace=True)
movie['Year'] = movie['title'].str.extract('.*\((.*)\).*',expand = False)
movie.replace('2006–2007','2007', inplace = True)

mean_rat = ratings.groupby('movieId').rating.mean()
num_users = ratings.groupby('movieId').userId.count()
mean_rat_movie_temp = pd.merge(mean_rat, movie, how='inner', on='movieId')
mean_rat_movie = pd.merge(mean_rat_movie_temp, num_users, how='inner', on='movieId')

mean_rat_movie.drop(columns='genres', inplace=True)
mean_rat_movie.rename(columns={'rating':'mean_ratings','userId':'num_users'}, inplace=True)
def hello():
    popular_movies = mean_rat_movie[mean_rat_movie["num_users"]>50].sort_values('mean_ratings',ascending=False)
    return popular_movies.head(10)["title"]
print(hello())