# spotify_player.py
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
))

def play_song(song_name):
    results = sp.search(q=song_name, type='track', limit=1)
    if results["tracks"]["items"]:
        uri = results["tracks"]["items"][0]["uri"]
        sp.start_playback(uris=[uri])
        print(f"Playing: {song_name}")
    else:
        print("Song not found.")