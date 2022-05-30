import uvicorn
from fastapi import FastAPI,Path
from recommneder import recommend
from recommender_b import get_movie_recommendation
from recommend_c import hello
from recommender_d import  user_based_recommend
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI, Response, status
import ast
import requests

app = FastAPI(debug = True)

#to check if the server is up or not
@app.get('/status')
def health_check():
    return "Success!"

@app.get("/movie_based")
def read_name(movie: str):
    pred = recommend(movie)
    return pred 

@app.get("/")
def popular_movies_print():
    df = hello()
    return df

@app.get("/movie_user_based")
def read_name(movie: str):
    mov_list = []
    df = user_based_recommend(user_id=usr_id, m=num_rec)
    data = df.to_dict()
    for i in data['title']:
        mov_list.append(data['title'][i])
    return mov_list

@app.get("/user_based")
def read_id(u_id: int,num_rec:int):
    movie_list = []
    df = user_based_recommend(user_id = u_id ,m=num_rec)
    data = df.to_dict()
    for i in data['title']:
        movie_list.append(data['title'][i])
    return movie_list

@app.get('/images/{tmdbId}')
def grab_poster(tmdbId: int = Path(title="tmdbId for the movie")):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=621d3fee8614662e39e4cfea30a2a3ba&language=en-US'.format(tmdbId))
    data = response.content
    data = data.decode('UTF-8')
    data = data.replace('false','False')
    data = data.replace('null','""')
    data = ast.literal_eval(data)
    return 'https://image.tmdb.org/t/p/w500/{}'.format(data['poster_path'])

