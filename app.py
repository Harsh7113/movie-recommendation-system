import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=600702cd5a00af6d60467540689bad79&language=en-US".format(movie_id) 
    data = requests.get(url)
    data = data.json()
    return data

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        movie_data = fetch_poster(movie_id)
        credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=600702cd5a00af6d60467540689bad79"
        credits_data = requests.get(credits_url).json()

        cast = ", ".join(actor['name'] for actor in credits_data.get('cast', [])[:5])
        cast = cast + " ..." if len(credits_data.get('cast', [])) > 5 else cast
        crew = ", ".join(crew_member['name'] for crew_member in credits_data.get('crew', []) if crew_member['job'] == "Director")
        movie_data['cast'] = cast
        movie_data['crew'] = crew
        recommended_movies.append(movie_data)
    return recommended_movies



st.header('Movie Recommender System')
movies = pickle.load(open('C:/Users/Harshvardhan/Desktop/Important/movie_list.pkl','rb'))
similarity = pickle.load(open('C:/Users/Harshvardhan/Desktop/Important/similarity.pkl','rb'))


movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movies = recommend(selected_movie)
    for movie_data in recommended_movies:
        col1, col2 = st.columns([1, 3])
        with col1:
            poster_image = "https://image.tmdb.org/t/p/w500/" + movie_data['poster_path']
            st.image(poster_image, use_column_width=True)
        with col2:
            expander = st.expander(movie_data['title'])
            with expander:
                st.write("**Release Date:**", movie_data['release_date'])
                st.write("**Overview:**", movie_data['overview'])
                st.write("**Genres:**", ', '.join(genre['name'] for genre in movie_data['genres']))
                st.write("**Cast:**", movie_data['cast'])
                st.write("**Crew:**", movie_data['crew'])
