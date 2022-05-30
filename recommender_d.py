import pandas as pd

movies = pd.read_csv('movies.csv')
tags_ = pd.read_csv('tags.csv')
ratings = pd.read_csv('ratings.csv')

user_rating_user = pd.merge(movies, ratings, on='movieId').drop('timestamp', axis=1)

user_pivot_table = user_rating_user.pivot_table(index='userId', columns='movieId', values='rating')

user_pivot_norm = user_pivot_table.subtract(user_pivot_table.mean(axis=1), axis = 'rows')

user_sim_corr = user_pivot_norm.T.corr()

def get_similar_user(pick_user_id,n):
    user_similarity_threshold = 0.3
    similar_users = user_sim_corr[user_sim_corr[pick_user_id]>user_similarity_threshold][pick_user_id].sort_values(ascending=False)[:n]
    return similar_users

def user_based_recommend(user_id,m):
    n=10
    sim_users = get_similar_user(user_id,n)
    picked_userid_watched = user_pivot_norm[user_pivot_norm.index == user_id].dropna(axis=1, how='all')
    similar_user_movies = user_pivot_norm[user_pivot_norm.index.isin(sim_users.index)].dropna(axis=1, how='all')
    similar_user_movies.drop(picked_userid_watched.columns,axis=1, inplace=True, errors='ignore')
    item_score = {}
    for i in similar_user_movies.columns:
        movie_rating = similar_user_movies[i]
        total = 0
        count = 0
        for j in sim_users.index:
            if pd.isna(movie_rating[j]) == False:
                score = sim_users[j] * movie_rating[j]
                total += score
                count +=1
        item_score[i] = total / count
    item_score = pd.DataFrame(item_score.items(), columns=['movieId', 'movie_score'])

    ranked_item_score = item_score.sort_values(by='movie_score', ascending=False)
    ranked_item_score = pd.merge(ranked_item_score,movies, on='movieId').drop('genres',axis=1)
    return ranked_item_score.head(m)
