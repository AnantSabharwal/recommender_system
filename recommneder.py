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

#creating copies of the datasets and working on the copies
movie1 = movie.copy()
tag1 = tags.copy()

tag1.drop('userId', inplace = True, axis = 1)
tag1.drop_duplicates(inplace = True)

#preprocessing on tags
tag1['tag'] = tag1['tag'].apply(lambda x : x.replace(' ', ''))
tag1['tag'] = tag1['tag'].apply(lambda x : x.lower())

temp_tag = pd.DataFrame(tag1.groupby('movieId')['tag'].apply(lambda x: "%s" % ' '.join(x)))

movie1['genres'] = movie1['genres'].apply(lambda x: x.split('|'))
movie1['genres'] = movie1['genres'].apply(lambda x: ' '.join(x))
movie1['genres'] = movie1['genres'].apply(lambda x: x.lower())

df = pd.merge(movie1,temp_tag,on = 'movieId')
df['Year'] = df['Year'].replace(np.nan,'0')

df['keywords'] = df['genres'] +" "+ df['Year'] + " "+df['tag']

#creating the final dataframe that we will be working on for item to item based
final_df = df[['movieId','title','keywords']]

#importing the libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
cv = CountVectorizer()
vectors = cv.fit_transform(final_df['keywords']).toarray()
similarity = cosine_similarity(vectors)

#function to recommend the movies
def recommend(movie):
    movie_index = final_df[final_df['title'] == movie].index[0]
#     print(movie_index)
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True, key = lambda x:x[1])[1:11]
    mlist = []
    for i in movies_list:
        mlist.append(final_df.iloc[i[0]].title)
        #print(final_df.iloc[i[0]].title)
    return mlist

    
# print(recommend("Toy Story (1995)"))