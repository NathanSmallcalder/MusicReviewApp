import mysql.connector
import os
from datetime import datetime, timezone

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

def filter_albums(selected_rating, selected_year):
    # Establish a connection to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    '''
    QUERY FOR SELECTED YEAR,RAITING
    '''
    query = """
        SELECT
            Album.AlbumID,
            Album.Title,
            Album.ReleaseDate,
            Album.CoverImage,
            Album.ArtistID,
            AVG(Review.Rating) AS AvgRating
        FROM
            Album
        JOIN
            Review ON Album.AlbumID = Review.AlbumID
    """

    conditions = []
    params = []

    # Add conditions based on the selected rating
    if selected_rating and selected_rating != 'Any':
        conditions.append("Review.Rating = %s")
        params.append(selected_rating)

    # Add conditions based on the selected year
    if selected_year and selected_year != 'Any':
        conditions.append("YEAR(Album.ReleaseDate) = %s")
        params.append(selected_year)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Move the GROUP BY clause outside the WHERE clause
    query += " GROUP BY Album.AlbumID, Album.Title, Album.ReleaseDate, Album.CoverImage, Album.ArtistID"

    print(query)

    cursor.execute(query, params)
    filtered_albums = cursor.fetchall()
  
    return filtered_albums



# For queryAlbumPage
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
        sql_select = "SELECT * FROM User WHERE Username = %s"
        cursor.execute(sql_select, (username,))
        result = cursor.fetchone()
    except Exception as e:
        # Handle exceptions, log errors, or raise them as needed
        print(f"Error: {e}")
        return None
    finally:
        close_connection(connection, cursor)
        return result
    
#Gets Account
def get_account_db(username):
    try:
        connection, cursor = get_cursor()
        cursor.execute("SELECT * FROM User WHERE Username = %s", (username,))
        user = cursor.fetchall()
        close_connection(connection,cursor)
    except Exception as e:
        # Handle exceptions, log errors, or raise them as needed
        print(f"Error: {e}")
        return None
    finally:
        close_connection(connection, cursor)
        return user
    

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
        print(f"Error: {e}")
        return None
    finally:
        close_connection(connection, cursor)


#Inserts Album Review into the database
def insert_rating_album(album_review):
    connection, cursor = get_cursor()
    
    # Convert 'DatePosted' to MySQL datetime format
    dt_object = datetime.fromisoformat(album_review['DatePosted'][:-1])
    mysql_datetime = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if the review already exists
    sql_check = "SELECT * FROM Review WHERE UserID = %s AND AlbumID = %s"
    cursor.execute(sql_check, (album_review['UserId'], album_review['AlbumId']))
    existing_review = cursor.fetchone()
    
    if existing_review:
        # Update the existing review
        sql_update = "UPDATE Review SET Rating = %s, Comment = %s, DatePosted = %s WHERE UserID = %s AND AlbumID = %s"
        cursor.execute(sql_update, (album_review['Rating'], album_review['Comment'], mysql_datetime, album_review['UserId'], album_review['AlbumId']))
    else:
        # Insert a new review
        sql_insert = "INSERT INTO Review (UserID, AlbumID, Rating, Comment, DatePosted) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql_insert, (album_review['UserId'], album_review['AlbumId'], album_review['Rating'], album_review['Comment'], mysql_datetime))

    connection.commit()
    close_connection(connection, cursor)

### Inserts Song Review into the Database
def insert_raiting_songs(song_review):
    connection, cursor = get_cursor()
    for songs in song_review:
        sql_check = "SELECT * FROM SongReview WHERE UserID = %s AND SongID = %s"
        cursor.execute(sql_check, (songs['UserId'], songs['SongId']))
        existing_review = cursor.fetchone()

        if existing_review:
            # Update the existing review
            sql_update = "UPDATE SongReview SET Rating = %s WHERE UserID = %s AND SongID = %s"
            cursor.execute(sql_update, (songs['Rating'], songs['UserId'], songs['SongId']))
        else:
            # Insert a new review
            sql_insert = "INSERT INTO SongReview (UserID, SongID, Rating) VALUES (%s, %s, %s)"
            cursor.execute(sql_insert, (songs['UserId'], songs['SongId'], songs['Rating']))
        connection.commit()


    close_connection(connection, cursor)


def get_album_details(album_id):
    try:
        # Create a cursor object to execute SQL queries
        connection, cursor = get_cursor()

        # SQL query to retrieve album details
        query = """
            SELECT
                A.Title AS AlbumName,
                S.SongID,
                GROUP_CONCAT(DISTINCT S.Title ORDER BY S.Title) AS SongTitles,
                AVG(R.Rating) AS AverageAlbumRating,
                AVG(SR.Rating) AS AverageSongRating,
                SpotifyID,
                TrackURL
            FROM
                Album A
            LEFT JOIN Song S ON A.AlbumID = S.AlbumID
            LEFT JOIN Review R ON A.AlbumID = R.AlbumID
            LEFT JOIN SongReview SR ON S.SongID = SR.SongID
            WHERE
                A.AlbumID = %s
            GROUP BY
                A.Title, S.SongID;
        """

        # Execute the query with the specified AlbumID
        cursor.execute(query, (album_id,))

        # Fetch all the results
        result = cursor.fetchall()
        return result

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()


def get_album_comments(album_id):
    try:
        # Create a cursor object to execute SQL queries
        connection, cursor = get_cursor()

        # Your SQL query
        sql_query = """
            SELECT
                Review.Comment,
                Review.DatePosted,
                User.Username
            FROM
                Review
            JOIN
                User ON Review.UserID = User.UserID
            WHERE
                Review.AlbumID = %s;
        """

        cursor.execute(sql_query, (album_id,))
        comments = cursor.fetchall()

        cursor.close()
        connection.close()

        return comments
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()


def get_search(search_term):
    try:
        connection, cursor = get_cursor()
        query = f""" SELECT * FROM Album WHERE Title LIKE '%{search_term}%' """
        cursor.execute(query)
        search_results = cursor.fetchall()
        return search_results

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
            
def get_user_reviews(userId):
    try:
        connection, cursor = get_cursor()
        query = """SELECT Album.AlbumID, Album.Title,Album.CoverImage, Review.Rating, Review.Comment, Review.DatePosted
                    FROM Album
                    JOIN Review ON Album.AlbumID = Review.AlbumID
                    WHERE UserID = %s;"""
        cursor.execute(query, (userId,))
        search_results = cursor.fetchall()
        return search_results

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

import mysql.connector

def removeUserReview(userID, albumID):
    try:
        connection, cursor = get_cursor()

        # Delete SongReviews for the specified User and Album
        delete_song_reviews_query = "DELETE FROM SongReview WHERE UserID = %s AND AlbumID = %s"
        cursor.execute(delete_song_reviews_query, (userID, albumID))

        # Delete the reviews associated with the given user and album
        delete_reviews_query = "DELETE FROM Review WHERE UserID = %s AND AlbumID = %s"
        cursor.execute(delete_reviews_query, (userID, albumID))

        # Commit the changes to the database
        connection.commit()

        print("Deletion successful!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

def insertUserList(data, user_id):
    connection, cursor = get_cursor()  # Assuming you have a function named get_cursor

    # Insert into UserAlbumList
    insert_user_album_list_query = "INSERT INTO UserAlbumList (UserID, ListName, Description, CreatedDate) VALUES (%s, %s, %s, %s)"
    description = "Some description"
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_album_list_data = (user_id, data.get('listName', ''), description, created_date)
    cursor.execute(insert_user_album_list_query, user_album_list_data)
    user_list_id = cursor.lastrowid

    # Insert into List
    insert_list_query = "INSERT INTO List (UserListID, AlbumID) VALUES (%s, %s)"
    for ids in data['albumIds']:
        list_data = (user_list_id, ids)
        cursor.execute(insert_list_query, list_data)

    # Commit the changes to the database
    connection.commit()

 