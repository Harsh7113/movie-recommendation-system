# movie-recommendation-system


# **Quick Start**

Download and extract the archive file.
you will get 2 csv files 

1.tmdb_5000_movies

2.tmdb_5000_credits


After downloading and extracting provide the file paths in Movie Recommendation System.py

movies=pd.read_csv("**PATH OF** tmdb_5000_movies.csv")
credits=pd.read_csv("**PATH OF** tmdb_5000_credits.csv")


run the Movie Recommendation System.py and 2 pkl files will be created.

1.movie_list.pkl

2.similarity.pkl

provide the path of these 2 files in app.py

movies = pickle.load(open('**PATH OF** movie_list.pkl','rb'))

similarity = pickle.load(open('**PATH OF** similarity.pkl','rb'))

**Now to Run the Program**


