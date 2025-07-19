import streamlit as st
import gdown
import os
import pickle
import requests
import time

movies_url = "https://drive.google.com/uc?id=1ZS5grgUSeobuI9E9MQPt3r5RHu86PCqR"
similarity_url = "https://drive.google.com/uc?id=1FfqvMfdufSxWrSvh5EPWrZOKNoo2-cM5"

if not os.path.exists('movies.pkl'):
    gdown.download(movies_url, 'movies.pkl', quiet=False)

if not os.path.exists('similarity.pkl'):
    gdown.download(similarity_url, 'similarity.pkl', quiet=False)

with open('movies.pkl', 'rb') as f:
    movies_df = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

API_KEY = "7f740fc310ed76697e23b3b545588c7a"
poster_cache = {}

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    if movie_id in poster_cache:
        return poster_cache[movie_id]

    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    retries = 3

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path', None)
                poster_url = (
                    "https://image.tmdb.org/t/p/w500/" + poster_path
                    if poster_path else
                    "https://via.placeholder.com/500x750?text=No+Image"
                )
                poster_cache[movie_id] = poster_url
                return poster_url
            time.sleep(2 ** attempt)
        except requests.exceptions.RequestException:
            time.sleep(2 ** attempt)

    poster_cache[movie_id] = "https://via.placeholder.com/500x750?text=Error"
    return poster_cache[movie_id]

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_posters = []

    for i in movie_indices:
        movie_data = movies_df.iloc[i[0]]
        title = movie_data.get('title', 'Unknown Title')
        movie_id = movie_data.get('movie_id')
        recommended_movies.append(title)
        time.sleep(0.5)  # avoid rate limits
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

st.markdown("<h1 style='text-align: center;'>🎥 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Choose a movie and get 10 similar recommendations based on ML.</p>", unsafe_allow_html=True)
st.markdown("---")

selected_movie = st.selectbox("🎬 Select a movie you like:", movies_df['title'].values)

if st.button("🔍 Show Recommendations"):
    with st.spinner("Fetching recommendations and posters..."):
        names, posters = recommend(selected_movie)

    st.markdown("### ⭐ Top 10 Recommendations")
    cols = st.columns(10)

    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.caption(f"🎞️ {names[idx]}")
else:
    st.info("👆 Choose a movie and click **Show Recommendations** to get started.")