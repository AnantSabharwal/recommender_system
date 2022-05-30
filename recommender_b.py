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

#### concidering user based similarity based on other movies liked by the users who watched a given movie
df_pivot = ratings.pivot(index ='movieId',columns='userId',values='rating')
df_pivot = df_pivot.dropna(thresh = 10, axis = 0)
df_pivot.fillna(0,inplace = True)

# counting rated movies and users who have rated movies
users_rated = ratings.groupby('movieId')['rating'].agg('count')
movies_rated = ratings.groupby('userId')['rating'].agg('count')

#concidering users which have rated more than 10 movies only
df_pivot = df_pivot.loc[:, movies_rated[movies_rated > 10].index]

#importing the libraries
#creating a compressed matrix aka spare matrix
#scipy is an opensource library for mathemnatics, science and engineering
from scipy.sparse import csr_matrix
from sklearn.neighbors import KNeighborsClassifier,NearestNeighbors

rating_movieid_matrix = csr_matrix(df_pivot.values)
df_pivot.reset_index(inplace = True)
knn_model = NearestNeighbors(n_neighbors=10,metric ='cosine',algorithm = 'auto',n_jobs=-1)
knn_model.fit(rating_movieid_matrix) 

def get_movie_recommendation(movie_name):
    n = 10
    movie_list = movie[movie['title'].str.contains(movie_name,case = False)]  
    if len(movie_list):        
        movie_idx= movie_list.iloc[0]['movieId']
        movie_idx = df_pivot[df_pivot['movieId'] == movie_idx].index[0]
        distances , indices = knn_model.kneighbors(rating_movieid_matrix[movie_idx],n_neighbors=n+1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = df_pivot.iloc[val[0]]['movieId']
            idx = movie[movie['movieId'] == movie_idx].index
            recommend_frame.append({'Title':movie.iloc[idx]['title'].values[0],'Distance':val[1]})
        df = pd.DataFrame(recommend_frame,index=range(1,n+1))
        return df
    else:
        return "No movie found :( Check input" 

# print(get_movie_recommendation('Avatar'));