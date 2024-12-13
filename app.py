import pickle
import streamlit as st
import requests
import base64
import os

# Fetch poster image from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Encode local image in Base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load background image from local file
background_image_path = 'image.jpeg'
if os.path.exists(background_image_path):
    try:
        base64_image = get_base64_of_bin_file(background_image_path)
        page_bg_img = f'''
        <style>
        body {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #FFFFFF;
            font-family: 'Trebuchet MS', sans-serif;
        }}
        .stButton>button {{
            background-color: #FF6347;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            padding: 12px 24px;
            margin-top: 20px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        }}
        .stSelectbox>div>div>div {{
            color: black;
            font-size: 16px;
            font-family: 'Trebuchet MS', sans-serif;
        }}
        h1 {{
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #FFD700;
        }}
        h5 {{
            text-align: center;
            color: #FFD700;
            font-style: italic;
        }}
        p {{
            font-size: 14px;
            text-align: center;
            color: #FFFFFF;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load background image: {e}")
else:
    st.warning("Background image not found. Please make sure 'image' is in the correct directory.")

# Streamlit app header
st.title('🎬 Movie Recommendation System')
st.markdown("<h5>Discover movies tailored to your taste!</h5>", unsafe_allow_html=True)

# Load movie data and similarity matrix
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("Select or search for a movie:", movie_list)

if st.button('Recommend'):  # On clicking 'Recommend'
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommendations in a grid layout
    st.subheader("Recommended Movies")
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[idx], use_container_width=True)
            st.markdown(f"<p>{recommended_movie_names[idx]}</p>", unsafe_allow_html=True)
