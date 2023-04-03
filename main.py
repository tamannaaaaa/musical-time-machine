from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import requests

Client_ID = "9bc187e71743467cb075c52892588105"
Client_Secret = "d0a77bf2b2a342be8eb4379f1889086c"

# OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
# OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select(selector="li ul li h3")
song_names = [song.getText().strip("\t\n") for song in song_names_spans]
print(song_names)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://musicalmachine.com/callback/",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uri = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(f"track:{song}, year:{year}", type="track")
    # print(result)

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in spotify. skipped")
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)
