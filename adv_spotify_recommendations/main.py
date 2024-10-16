from methods import *

user_id = input("What's your spotify username?\n>")

seed_artists = []
seed_genres = []
seed_tracks = []

print("\nWhich artists would you like to create a playlist with?(maximum of 5)\nType 'q' to quit.")
while len(seed_artists) < 5:
    answer = input("\n>")
    if answer == "q":
        continue_loop = False
        break
    artist = search_for_artist(token, answer)
    if artist:
        print(f"{artist['name']} added!")
        artist_id = artist["id"]
        artist_genres = artist["genres"]
        top_tracks = get_songs_by_artist(token, artist_id)
        if top_tracks:
            seed_tracks.append(top_tracks[0]["id"])

        seed_artists.append(artist_id)
        seed_genres.extend(artist_genres[:2])

# Ensure we only have up to 5 seed values in total
seed_artists = seed_artists[:5]
seed_genres = seed_genres[:5 - len(seed_artists)]
seed_tracks = seed_tracks[:5 - len(seed_artists) - len(seed_genres)]

while True:
    try:
        song_limit = int(input("\nHow many songs would you like for the playlist to have?(max 100)\n")) # make a failsafe check later
        if 0 < song_limit <= 100:
            break
        else:
            print("\nIncorrect range! Try again.\n")
    except ValueError:
        print("\nInvalid input! Please enter a number.")


# Optional parameters
optional_params = {}
params_list = [
    ("min_acousticness", "Enter min_acousticness (0-1) or press Enter to skip: ", float),
    ("max_acousticness", "Enter max_acousticness (0-1) or press Enter to skip: ", float),
    ("target_acousticness", "Enter target_acousticness (0-1) or press Enter to skip: ", float),
    ("min_danceability", "Enter min_danceability (0-1) or press Enter to skip: ", float),
    ("max_danceability", "Enter max_danceability (0-1) or press Enter to skip: ", float),
    ("target_danceability", "Enter target_danceability (0-1) or press Enter to skip: ", float),
    ("min_duration_ms", "Enter min_duration_ms or press Enter to skip: ", int),
    ("max_duration_ms", "Enter max_duration_ms or press Enter to skip: ", int),
    ("target_duration_ms", "Enter target_duration_ms or press Enter to skip: ", int),
    ("min_energy", "Enter min_energy (0-1) or press Enter to skip: ", float),
    ("max_energy", "Enter max_energy (0-1) or press Enter to skip: ", float),
    ("target_energy", "Enter target_energy (0-1) or press Enter to skip: ", float),
    ("min_instrumentalness", "Enter min_instrumentalness (0-1) or press Enter to skip: ", float),
    ("max_instrumentalness", "Enter max_instrumentalness (0-1) or press Enter to skip: ", float),
    ("target_instrumentalness", "Enter target_instrumentalness (0-1) or press Enter to skip: ", float),
    ("min_key", "Enter min_key (0-11) or press Enter to skip: ", int),
    ("max_key", "Enter max_key (0-11) or press Enter to skip: ", int),
    ("target_key", "Enter target_key (0-11) or press Enter to skip: ", int),
    ("min_liveness", "Enter min_liveness (0-1) or press Enter to skip: ", float),
    ("max_liveness", "Enter max_liveness (0-1) or press Enter to skip: ", float),
    ("target_liveness", "Enter target_liveness (0-1) or press Enter to skip: ", float),
    ("min_loudness", "Enter min_loudness or press Enter to skip: ", float),
    ("max_loudness", "Enter max_loudness or press Enter to skip: ", float),
    ("target_loudness", "Enter target_loudness or press Enter to skip: ", float),
    ("min_mode", "Enter min_mode (0-1) or press Enter to skip: ", int),
    ("max_mode", "Enter max_mode (0-1) or press Enter to skip: ", int),
    ("target_mode", "Enter target_mode (0-1) or press Enter to skip: ", int),
    ("min_popularity", "Enter min_popularity (0-100) or press Enter to skip: ", int),
    ("max_popularity", "Enter max_popularity (0-100) or press Enter to skip: ", int),
    ("target_popularity", "Enter target_popularity (0-100) or press Enter to skip: ", int),
    ("min_speechiness", "Enter min_speechiness (0-1) or press Enter to skip: ", float),
    ("max_speechiness", "Enter max_speechiness (0-1) or press Enter to skip: ", float),
    ("target_speechiness", "Enter target_speechiness (0-1) or press Enter to skip: ", float),
    ("min_tempo", "Enter min_tempo or press Enter to skip: ", float),
    ("max_tempo", "Enter max_tempo or press Enter to skip: ", float),
    ("target_tempo", "Enter target_tempo or press Enter to skip: ", float),
    ("min_time_signature", "Enter min_time_signature or press Enter to skip: ", int),
    ("max_time_signature", "Enter max_time_signature or press Enter to skip: ", int),
    ("target_time_signature", "Enter target_time_signature or press Enter to skip: ", int),
    ("min_valence", "Enter min_valence (0-1) or press Enter to skip: ", float),
    ("max_valence", "Enter max_valence (0-1) or press Enter to skip: ", float),
    ("target_valence", "Enter target_valence (0-1) or press Enter to skip: ", float),
]

for param, prompt, type_cast in params_list:
    value = get_user_input(prompt, type_cast)
    if value == "QUIT":
        break  # Exit the loop if the user inputs 'q'
    optional_params[param] = value

# Remove None values from optional_params
optional_params = {k: v for k, v in optional_params.items() if v is not None}

recommendations = get_recommendations(
    token,
    seed_artists,
    seed_genres,
    seed_tracks,
    song_limit,
    **optional_params
)

print("These are the tracks in your new playlist:\n")
track_uris = [track['uri'] for track in recommendations['tracks']]
for track in recommendations['tracks']:
    print(track['name'] + ' - ' + track['artists'][0]['name'])

name_of_playlist = input("\nWhat would you like to call your new playlist?\n>")

playlist_id = create_playlist(token, user_id, name_of_playlist)

# Adds songs to the newly created playlist
add_tracks_to_playlist(token, playlist_id, track_uris)