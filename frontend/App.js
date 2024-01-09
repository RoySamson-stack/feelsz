import React, { useEffect, useState } from 'react';
import { View, Text, Button } from 'react-native';
import { createPlaylist } from './SpotifyService';

export default function App() {
  const [mood, setMood] = useState('happy');
  const [tracks, setTracks] = useState([]);

  useEffect(() => {
    // Fetch tracks based on mood
    // Replace the following with your logic to fetch tracks
    const fetchTracks = async () => {
      try {
        // Fetch tracks based on mood
        // Replace the following with your logic to fetch tracks
        const response = await axios.get(
          'https://api.spotify.com/v1/search',
          {
            params: {
              q: `mood:${mood}`,
              type: 'track',
              limit: 10,
            },
            headers: {
              Authorization: `Bearer ${yourAccessToken}`, // You need to replace this with the actual access token
            },
          }
        );

        setTracks(response.data.tracks.items);
      } catch (error) {
        console.error('Error fetching tracks:', error);
      }
    };

    fetchTracks();
  }, [mood]);

  const handleCreatePlaylist = async () => {
    try {
      await createPlaylist(mood, tracks);
      console.log('Playlist created successfully!');
    } catch (error) {
      console.error('Error creating playlist:', error);
    }
  };

  return (
    <View>
      <Text>{`Predicted mood: ${mood}`}</Text>
      <Button title="Create Playlist" onPress={handleCreatePlaylist} />
    </View>
  );
}
