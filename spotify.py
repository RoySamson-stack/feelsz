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
# ...

# Spotify API credentials
SPOTIPY_CLIENT_ID = 'your_client_id'
SPOTIPY_CLIENT_SECRET = 'your_client_secret'
SPOTIPY_REDIRECT_URI = 'your_redirect_uri'

# Set up Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-modify-public"))

# ...

# Predict the mood for a new song
new_song_lyrics = ['energetic beats', 'calm melody', 'uplifting lyrics']
new_song_prediction = model.predict(new_song_lyrics)
predicted_new_song_mood = le.inverse_transform(new_song_prediction)

print(f"Predicted mood for the new song: {predicted_new_song_mood[0]}")

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
