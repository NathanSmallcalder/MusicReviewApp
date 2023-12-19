import mysql.connector
import os

#Config DB settings
db_config = {
    'user': os.getenv("USER"),
    'password': os.getenv("PASSWORD"),
    'host': 'localhost',
    'port': 3306,
    'database': 'musicDatabase',
}

#Connect to database
def connect_db():
    return mysql.connector.connect(**db_config)

# Get cursor
def get_cursor():
    connection = connect_db()
    cursor = connection.cursor(buffered=True)
    return connection, cursor

#Close DB connections
def close_connection(connection, cursor):
    cursor.close()
    connection.close()

# Gets All Albums
# For index page
def get_albums_db():
    try:
        connection, cursor = get_cursor()
        sql_select = "SELECT * FROM Album"
        cursor.execute(sql_select)
        albums = cursor.fetchall()
        return albums
    except Exception as e:
        # Handle exceptions, log errors, or raise them as needed
        print(f"Error: {e}")
        return None
    finally:
        close_connection(connection, cursor)

# Inserts user into database
def sign_up_db(username,email,hashed):
    try:
        connection, cursor = get_cursor()
        sql_insert = "INSERT INTO User (Username, Email, PasswordHash) VALUES (%s, %s, %s)"
        cursor.execute(sql_insert, (username,email,hashed))
        connection.commit()
    except Exception as e:
        # Handle exceptions, log errors, or raise them as needed
        print(f"Error: {e}")
        return None
    finally:
        close_connection(connection, cursor)

# Gets Album by album ID
def get_album_by_albumID(album_id):
    try:
        connection, cursor = get_cursor()
        sql_select = f"SELECT * FROM Album WHERE AlbumID = {album_id}"
        cursor.execute(sql_select)
        albums = cursor.fetchone()
        return albums
    except Exception as e:
        # Handle exceptions, log errors, or raise them as needed
        print(f"Error: {e}")
        return None
    finally:
        close_connection(connection, cursor)
  
# Gets songs by album ID
# Gets all songs within album
def get_songs_by_albumID(album_id):
    try:
        connection, cursor = get_cursor()
        sql_select = f"SELECT * FROM Song WHERE AlbumID = {album_id}"
        cursor.execute(sql_select)
        songs = cursor.fetchall()
        return songs
    except Exception as e:
        # Handle exceptions, log errors, or raise them as needed
        print(f"Error: {e}")
        return None
    finally:
        close_connection(connection, cursor)

#Gets the artist from an album id
def get_artist_by_albumID(album_id):
    try:
        connection, cursor = get_cursor()
        sql_select = f"SELECT * FROM Artist JOIN Album ON Artist.ArtistID = Album.ArtistID WHERE Album.AlbumID = {album_id};"
        cursor.execute(sql_select)
        artist = cursor.fetchone()
        return artist
    except Exception as e:
        # Handle exceptions, log errors, or raise them as needed
        print(f"Error: {e}")
        return None
    finally:
        close_connection(connection, cursor)

#Gets Account
def get_account_db(username):
        connection, cursor = get_cursor()
        cursor.execute("SELECT * FROM User WHERE Username = %s", (username,))
        user = cursor.fetchall()
        close_connection(connection,cursor)
        return user