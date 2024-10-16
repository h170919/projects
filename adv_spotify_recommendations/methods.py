import os
import json
import base64
from requests import post, get
from dotenv import load_dotenv
import webbrowser

def get_token():
    auth_url = "https://accounts.spotify.com/authorize"
    auth_response_url = auth_url + f"?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    webbrowser.open(auth_response_url)
    auth_response = input("Enter the URL you were redirected to (after logging in): ")
    code = auth_response.split("code=")[1]

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)

    return json_result["access_token"]


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)

    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artists with this name exists")
        return None
    return json_result[0]


def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=NO"
    headers = get_auth_header(token)
    result = get(url, headers=headers)

    json_result = json.loads(result.content)["tracks"]

    return json_result

def get_user_input(prompt, type_cast):
    user_input = input(prompt)
    if user_input.strip().lower() == "q":
        return "QUIT"  # Return "QUIT" if the user inputs 'q'
    if user_input.strip() == "":
        return None
    try:
        return type_cast(user_input)
    except ValueError:
        print("Invalid input. Please try again.")
        return get_user_input(prompt, type_cast)
def get_recommendations(token, seed_artists, seed_genres, seed_tracks, song_limit, **kwargs):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)
    params = {
        "limit": song_limit,  # the amount of songs being recommended
        "seed_artists": ','.join(seed_artists),
        "seed_genres": ','.join(seed_genres),
        "seed_tracks": ','.join(seed_tracks),
    }

    # Add optional parameters if they are provided
    for key, value in kwargs.items():
        if value is not None:
            params[key] = value

    result = get(url, headers=headers, params=params)
    json_result = json.loads(result.content)
    return json_result



def add_tracks_to_playlist(token, playlist_id, track_uris):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    params = {
        "uris": track_uris
    }
    result = post(url, headers=headers, json=params)
    if result.status_code != 201:
        print("Failed to add tracks to playlist:", result.status_code, result.content)
        return None
    return json.loads(result.content)

def create_playlist(token, user_id, playlist_name):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = get_auth_header(token)
    params = {
        "name": playlist_name,
        "private": "false"
    }

    result = post(url, headers=headers, json=params)

    if result.status_code != 201:
        print("Failed to create a playlist:", result.status_code, result.content)
        return None
    return(json.loads(result.content)["id"])

load_dotenv()

client_secret = os.getenv("CLIENT_SECRET")
client_id = os.getenv("CLIENT_ID")
redirect_uri = os.getenv("REDIRECT_URI")
scope = "playlist-modify-public"

token = get_token()
