import mysql.connector
from datetime import datetime
from api_requests import *
import os

def remove_special_characters(input_string):
    """
    Remove single and double quotes from the input string.

    Parameters:
    - input_string (str): The input string.

    Returns:
    - str: The string with single and double quotes removed.
    """
    return input_string.replace("'", "").replace('"', '')


config = {
    'user': os.getenv("USER"),
    'password': os.getenv("PASSWORD"),
    'host': 'localhost',
    'port': 3306,
    'database': 'musicDatabase',
}

connection = mysql.connector.connect(**config)

cursor = connection.cursor(buffered=True)

related = get_related_artists("5INjqkS1o8h1imAzPqGZBb",token)
related_artists = related_artist_ids(related)


"""
Loop to add artist, albums and songs to the database.
Iterates Per Related Artist
"""
for artists in related_artists:
    sql_select = f"SELECT ArtistID FROM Artist WHERE ArtistID = '{artists['ArtistId']}'"
     # Execute the SQL statement
    cursor.execute(sql_select)
    # Fetch the result
    result = cursor.fetchone()
    print(result)
    if result == None:
        """ 
        Iterates through artists and inserts them into the database
        """
        artist_albums = get_artist_albums(token,artists['ArtistId'])

        albums_list = forge_album_tracklist(artist_albums, token)
        sql_insert = "INSERT INTO Artist (ArtistID, ArtistName, Genre) VALUES (%s, %s, %s)"
        s = ''.join(str(x) for x in artists['genres'])
        cursor.execute(sql_insert, (artists['ArtistsId'], artists['ArtistName'], s))
        for albums in albums_list:
            """
            Iterates through albums and inserts them into the database
            """
            albums_list = forge_album_tracklist(artist_albums, token)
            artists['albums'].append(albums_list)
            print(albums)
            sql_insert = "INSERT INTO Album (Title, ReleaseDate, CoverImage,ArtistID) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_insert, ((remove_special_characters(albums['album_name'])),(albums['release_date']),albums['images'],artists['ArtistsId']))
            tracks = albums['tracks']
            for songs in tracks:
                """"
                Iterates through songs and inserts them into the database
                """
                album_name = albums['album_name']
                # Your SQL SELECT statement
                sql_select = f"SELECT AlbumID FROM Album WHERE Title = '{remove_special_characters(album_name)}'"
                # Execute the SQL statement
                cursor.execute(sql_select)
                # Fetch the result
                result = cursor.fetchone()
                if result:
                    album_id = result[0]
                    print(f"Album ID for '{album_name}': {album_id}")
                    print(songs['track_title'])
                    sql_insert = "INSERT INTO Song (Title,AlbumID) VALUES (%s, %s)"
                    cursor.execute(sql_insert, (songs['track_title'],album_id))
                else:
                    print(f"No album found with the title '{album_name}'")
    else:
        """
        If artist data is already collected.
        """
        pass
        
    connection.commit()
    time.sleep(15)
   
