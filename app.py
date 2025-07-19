import streamlit as st
import pickle
import requests
import time

# Load movie data and similarity matrix
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

API_KEY = "7f740fc310ed76697e23b3b545588c7a"

# Persistent cache for poster URLs (lives during app run)
poster_cache = {}

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    # Return from cache if available
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
                if poster_path:
                    poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path
                else:
                    poster_url = "https://via.placeholder.com/500x750?text=No+Image"
                poster_cache[movie_id] = poster_url
                return poster_url
            else:
                # Removed debug output for clean UI
                pass
        except requests.exceptions.RequestException:
            # Removed debug output for clean UI
            time.sleep(2 ** attempt)

    # After retries fail
    error_url = "https://via.placeholder.com/500x750?text=Error"
    poster_cache[movie_id] = error_url
    return error_url


def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_indices:
        movie_data = movies_df.iloc[i[0]]
        recommended_movies.append(movie_data['title'])
        # Delay to avoid rate limiting
        time.sleep(1)
        recommended_posters.append(fetch_poster(movie_data['movie_id']))

    return recommended_movies, recommended_posters


st.title('🎬 Movie Recommender System')

movie_titles = movies_df['title'].values
selected_movie = st.selectbox('Select a movie:', movie_titles)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    st.subheader("Recommended Movies:")
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])