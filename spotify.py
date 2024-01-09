import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Sample dataset (replace with your own dataset)
data = {
    'song': ['Song1', 'Song2', 'Song3', 'Song4', 'Song5'],
    'lyrics': ['happy lyrics', 'sad lyrics', 'happy song', 'sad song', 'upbeat lyrics'],
    'mood': ['happy', 'sad', 'happy', 'sad', 'happy']
}

df = pd.DataFrame(data)

# Split the data into training and testing sets
train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

# Encode the mood labels
le = LabelEncoder()
train_data['encoded_mood'] = le.fit_transform(train_data['mood'])
test_data['encoded_mood'] = le.transform(test_data['mood'])

# Define and train the model (using lyrics as features)
model = make_pipeline(CountVectorizer(), RandomForestClassifier())
model.fit(train_data['lyrics'], train_data['encoded_mood'])

# Predict the mood for a new song
new_song_lyrics = ['energetic beats', 'calm melody', 'uplifting lyrics']
new_song_prediction = model.predict(new_song_lyrics)
predicted_new_song_mood = le.inverse_transform(new_song_prediction)

print(f"Predicted mood for the new song: {predicted_new_song_mood[0]}")

# Set up Spotify API authentication
SPOTIPY_CLIENT_ID = 'e49c1214df8148858517de9bf4c7e230'
SPOTIPY_CLIENT_SECRET = 'edbdaa10bdbf4782a37d62bc92a54e53'
SPOTIPY_REDIRECT_URI = 'spotify.com'

# Set up Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-modify-public"))

# Create a playlist on Spotify based on the predicted mood
playlist_name = f"{predicted_new_song_mood[0]} Playlist"
playlist_description = f"Automatically generated playlist for {predicted_new_song_mood[0]} songs."

# Get Spotify user ID
user_id = sp.me()['id']

# Create a new playlist
playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=playlist_description)

# Search for tracks on Spotify based on the predicted mood
search_query = f"mood:{predicted_new_song_mood[0]}"
tracks = sp.search(q=search_query, type='track', limit=10)['tracks']['items']

# Add tracks to the playlist
track_uris = [track['uri'] for track in tracks]
sp.playlist_add_items(playlist['id'], track_uris)

print(f"Playlist '{playlist_name}' created on Spotify with {len(track_uris)} tracks.")
