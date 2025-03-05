import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials



def spotify_auth():
    scope = ["user-library-read", "playlist-modify-public"]
    # auth_manager = SpotifyClientCredentials()
    auth_manager = SpotifyOAuth(scope=scope)
    return spotipy.Spotify(auth_manager=auth_manager)
