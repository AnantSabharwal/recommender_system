import streamlit as st
import pandas as pd
import requests
import pickle
import ast

movies = pd.read_csv('movies.csv')
links = pd.read_csv('links.csv')


def home():
    try:
        st.title("Home")
        st.write("Top  movies based on average user rating")
        response = requests.get('http://127.0.0.1:8000/')
        data = ast.literal_eval(response.content.decode('UTF-8'))
        data = response.json()
        st.table(list(data.values()))
    except:
        st.error("API NOT RUNNING!")

def search():
    st.title("Search for a movie: ")
    movie_list = pickle.load(open('movie_list.pkl','rb'))
    movie_list = movie_list['title'].values
    movie_name = st.selectbox('Select a movie',movie_list)
    option = st.radio("Recommendation Type",("Movie to Movie",'Others also watched'))
    if(st.button("Recommend")):
        if option == "Movie to Movie":
            # try:
            response = requests.get('http://127.0.0.1:8000/movie_based?movie={}'.format(movie_name))
            data = ast.literal_eval(response.content.decode('UTF-8'))
            st.table(data)
            # except:
            #     st.error("API NOT RUNNING!")
        elif option == "Others also watched":
            try:
                #dis_mov = []
                response = requests.get('http://127.0.0.1:8000/movie_user_based?movie={}'.format(movie_name))
                data = ast.literal_eval(response.content.decode('UTF-8'))
                #for i in data:
                #   dis_mov.append(data[i])
                #st.table(dis_mov)
                st.table(data)
            except:
                pass

def search_user():
    st.title("Recommendation based on other users")
    user_id = st.number_input("Enter user id: ",1,610)
    number_rec = st.number_input("Enter the number of movies to be recommended:",1,15)
    if(st.button("Recommend")):
        #dis_mov = []
        response = requests.get('http://127.0.0.1:8000/user_based?u_id={}'.format(user_id)+'&num_rec={}'.format(number_rec))
        data = ast.literal_eval(response.content.decode('UTF-8'))
        #for i in data:
        #    dis_mov.append(data[i])
        st.table(data)


def main():
    st.title("Movie Recommender System")
    menu = ["Home","Search item based","Search user based"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == 'Home':
        home()
    elif choice == 'Search item based':
        search()
    elif choice == 'Search user based':
        search_user()

if __name__ == "__main__":
    main()

