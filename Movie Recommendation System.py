import numpy as np
import pandas as pd
import ast
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


movies=pd.read_csv("C:/Users/Harshvardhan/Desktop/Datasets/tmdb_5000_movies.csv") #provide the path where you have downloaded the csv file
credits=pd.read_csv("C:/Users/Harshvardhan/Desktop/Datasets/tmdb_5000_credits.csv") #provide the path where you have downloaded the csv file

#merging movies and credits on the basis of title
movies=movies.merge(credits,on="title")

movies=movies[["movie_id","title","overview","genres","keywords","cast","crew"]]

movies.dropna(inplace=True)


def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i["name"])
    return L

#function to get first 5 names of cast

def convert5(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter != 5:
            L.append(i["name"])
            counter+=1
        else:
            break
    return L

#function to get directors name from crew

def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            L.append(i["name"])
            break
    return L

#calling functions 
movies["genres"]=movies["genres"].apply(convert)
movies["keywords"]=movies["keywords"].apply(convert)
movies["cast"]=movies["cast"].apply(convert5)
movies["crew"]=movies["crew"].apply(fetch_director)
movies["overview"]=movies["overview"].apply(lambda x:x.split())


#removing space between words and making it 1 entity so that the can be categorised
movies["genres"]=movies["genres"].apply(lambda x:[i.replace(" ","") for i in x])
movies["keywords"]=movies["keywords"].apply(lambda x:[i.replace(" ","") for i in x])
movies["cast"]=movies["cast"].apply(lambda x:[i.replace(" ","") for i in x])
movies["crew"]=movies["crew"].apply(lambda x:[i.replace(" ","") for i in x])


#creating a new column tag which contains overview genres keywords cast crew
movies["tag"]=movies["overview"]+movies["genres"]+movies["keywords"]+movies["cast"]+movies["crew"]


#removing the other columns
new_df=movies[["movie_id","title","tag"]]

#converting tag into string
new_df["tag"]=new_df["tag"].apply(lambda x:" ".join(x))

#converting into lowercase
new_df["tag"]=new_df["tag"].apply(lambda x:x.lower())


ps = PorterStemmer()

def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df["tag"]=new_df["tag"].apply(stem)

#removing stop words from tag
cv=CountVectorizer(max_features=5000,stop_words="english")

#converting tag into vectors so that model can classify and recommend movies
vectors = cv.fit_transform(new_df["tag"]).toarray()
cv.get_feature_names_out()

similarity=cosine_similarity(vectors)

def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new_df.iloc[i[0]].title)

#to create plk file 
pickle.dump(new_df,open('movie_list.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))


