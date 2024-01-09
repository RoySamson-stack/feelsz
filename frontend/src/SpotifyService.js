import axios from 'axios';
import { SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI } from 'react-native-dotenv';

export const createPlaylist = async (mood, tracks) => {
  try {
    const response = await axios.post(
      'https://api.spotify.com/v1/me/playlists',
      {
        name: `${mood} Playlist`,
        description: `Automatically generated playlist for ${mood} songs.`,
        public: true,
      },
      {
        headers: {
          Authorization: `Bearer ${yourAccessToken}`, // You need to replace this with the actual access token
        },
      }
    );

    const playlistId = response.data.id;

    const uris = tracks.map((track) => track.uri);

    await axios.post(
      `https://api.spotify.com/v1/playlists/${playlistId}/tracks`,
      { uris },
      {
        headers: {
          Authorization: `Bearer ${yourAccessToken}`, // You need to replace this with the actual access token
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error('Error creating playlist:', error);
    throw error;
  }
};
