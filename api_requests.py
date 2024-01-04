from dotenv import load_dotenv
import os
import base64
from requests import post, get 
import json
import requests
import base64
import random
import time

load_dotenv()

SPOTIFY_API_BASE = 'https://api.spotify.com/v1/'
SPOTIFY_API_RANDOM_ARTIST = 'browse/new-releases'
SPOTIFY_API_ARTIST = 'artists/{artist_id}'
SPOTIFY_API_ARTIST_ALBUMS = 'artists/{artist_id}/albums'
SPOTIFY_API_ALBUM_TRACKS = 'albums/{album_id}/tracks'

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}
    result = post(url,headers=headers,data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

token = get_token()
print(token)

def get_random_artist(token):
    headers = {
        'Authorization': f'Bearer {token}',
    }

    # Spotify API endpoint for new releases
    new_releases_url = f'{SPOTIFY_API_BASE}{SPOTIFY_API_RANDOM_ARTIST}'
    
    # Make the request to get new releases
    response = requests.get(new_releases_url, headers=headers)

    if response.status_code == 200:
        # Extract a random artist from the list of new releases
        artists = response.json().get('albums', {}).get('items', [])[0].get('artists', [])
        if artists:
            random_artist = random.choice(artists)
            return random_artist
    else:
        print(f'Error {response.status_code}: Unable to fetch new releases.')
        return None
    
# Function to get information about a specific artist by their ID
def get_artist_by_id(access_token, artist_id):
    # Spotify API endpoint for artist information
    artist_url = f'{SPOTIFY_API_BASE}{SPOTIFY_API_ARTIST.format(artist_id=artist_id)}'

    # Spotify API request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    # Make the request to get artist information
    response = requests.get(artist_url, headers=headers)

    if response.status_code == 200:
        # Extract and return artist information
        return response.json()
    else:
        print(f'Error {response.status_code}: Unable to fetch artist information.')
        return None

def get_artist_albums(access_token, artist_id):
    # Spotify API endpoint for artist's albums
    artist_albums_url = f'{SPOTIFY_API_BASE}{SPOTIFY_API_ARTIST_ALBUMS.format(artist_id=artist_id)}'

    # Spotify API request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    # Make the request to get artist's albums
    response = requests.get(artist_albums_url, headers=headers)

    if response.status_code == 200:
        # Extract and return the list of albums
        return response.json().get('items', [])
    else:
        print(f'Error {response.status_code}: Unable to fetch artist\'s albums.')
        return None

# Function to get a list of tracks in a specific album
def get_album_tracks(access_token, album_id):
    # Spotify API endpoint for album's tracks
    album_tracks_url = f'{SPOTIFY_API_BASE}{SPOTIFY_API_ALBUM_TRACKS.format(album_id=album_id)}'

    # Spotify API request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    # Make the request to get album's tracks
    response = requests.get(album_tracks_url, headers=headers)

    if response.status_code == 200:
        # Extract and return the list of tracks
        return response.json().get('items', [])
    else:
        print(f'Error {response.status_code}: Unable to fetch album\'s tracks.')
        return None

# Creates a dictionary out of the artists' albums
def forge_album_tracklist(artist_albums, token):
    albums_list = []
    for album in artist_albums:
        if album['album_group'] == 'album':
            album_id = album['id']
            album_name = album['name']
            release_date = album['release_date']
            album_data = {
                "album_name": album_name,
                "tracks": [],
                'release_date': release_date,
                'images':album['images'][0]['url']
            }

            album_tracks = get_album_tracks(token, album_id)
            for track in album_tracks:
           
                track_id = track['id']
                track_title = track['name']
                track_length_ms = track['duration_ms']
                track_url = track['preview_url']

                track_length_sec = track_length_ms / 1000 / 60
                
                # Add track information to the current album
                album_data['tracks'].append({
                    'track_id': track_id,
                    'track_title': track_title,
                    'track_length_sec': track_length_sec,
                    'preview_Link':track_url
                })

            # Add the album data to the list of albums
            albums_list.append(album_data)
        else:
            pass
    return albums_list

def get_related_artists(artist_id, access_token):
    # Spotify API endpoint for getting related artists
    endpoint = f'https://api.spotify.com/v1/artists/{artist_id}/related-artists'
    # Set up headers with the access token
    headers = {'Authorization': f'Bearer {access_token}'}
    # Make the request
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()  # Check for errors in the response
        related_artists = response.json()['artists']
        return related_artists
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

#Gets Related Artists
def related_artist_ids(related_artists):
    relatedArtists = []
    print(related_artists)
    for related in related_artists:
        related_temp = {
            "ArtistsId": related['id'],
            "ArtistName": related['name'],
            "albums": [],
            'ArtistId': related['id'],
            'genres':related['genres']
        }

        relatedArtists.append(related_temp)

    return relatedArtists




