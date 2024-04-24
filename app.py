from flask import Flask, render_template, request, redirect, url_for, session, Response, jsonify
import os
import bcrypt
import json
from databaseCalls import *

app = Flask(__name__)
app.secret_key = "super secret key"

from jinja2 import Environment

def jinja2_min(a, b):
    return min(a, b)

# Add the custom filter to Jinja's environment
env = Environment()
env.filters['min'] = jinja2_min

def is_valid_album_review(data):
    # Check if the required keys are present in the album review data
    required_keys = ['Album','Songs']
    
    # Check if all required keys are present and 'Rating' is an integer
    return (
        all(key in data for key in required_keys) 
    )

# Home page
@app.route('/')
def index():
    Albums = get_albums_db()
    return render_template('index.html', title='Album Review',Albums = Albums)

@app.route('/albums')
def albums():
    Albums = get_albums_db() 
    return render_template('index.html', title='Album Review', Albums=Albums)

@app.route('/queryAlbums')
def queryAlbums():
    # Get selected rating and year from the query parameters
    selected_rating = request.args.get('selectedRating', None) 
    selected_year = request.args.get('selectedYear', None)
    print(selected_year)
    Albums = filter_albums(selected_rating,selected_year)
    print(Albums)
    for albums in Albums:
        print(albums['CoverImage'])
    return render_template('queryAlbum.html', title='Album Review',Albums = Albums)
    

# Signup
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            # Hash Password
            # Adding the salt to password
            salt = bcrypt.gensalt()
            # Hashing the password
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Check credentials in the database
            account = sign_up_db(username,email,hashed)
            print(account)
            session['user'] = account[0]
            session['nickname'] = account[1]
            
            return redirect(url_for('index'))
        except:
            return "Invalid credentials. <a href='/login'>Try again</a>"

    return render_template('signup.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_account_db(username)
    
        if user and bcrypt.checkpw(password.encode('utf8'), user[0][3].encode('utf-8')):
            session['user'] = user[0][0]
            session['nickname'] = user[0][1]
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"
        
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# Album Review Page
@app.route('/albumReview', methods=['GET','POST'])
def getAlbumReview():
    album = request.args.get('album')

    albums = get_album_by_albumID(album)
    album_details = get_album_details(album)
    songs = get_songs_by_albumID(album)
    artist = get_artist_by_albumID(album)

    SongLen = len(songs)

    return render_template('AlbumReviewPage.html', 
                           albums = albums,
                           songs = songs, 
                           artist = artist,
                           albumDetails = album_details,
                           SongLen = SongLen,
                           UserId = session['user'])


## Endpoint for posting album review to database
@app.route('/albumReviewSend', methods=['POST'])
def PostAlbumReview():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        try:
            data = json.loads(request.data)
            print(data)
            if 'Album' in data and len(data['Album']) > 0 and is_valid_album_review(data):
                insert_rating_album(data['Album'][0])
                insert_raiting_songs(data['Songs'])
                return jsonify({'message': 'Album review posted successfully'}), 200
            else:
                return jsonify({'error': 'Invalid or missing "Album" property'}), 400
        except Exception as e:
            return jsonify({'error': f'Error processing JSON data: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid Content-Type'}), 400



### Album Page                                                
@app.route('/album', methods=['GET','POST'])
def getAlbum():
    album = request.args.get('album')

    albums = get_album_by_albumID(album)
    album_details = get_album_details(album)
    artist = get_artist_by_albumID(album)
    comments = get_album_comments(album)
    print(album_details)

    return render_template('AlbumPage.html', 
                           albums = albums, 
                           album_details = album_details, 
                           artist = artist,
                           comments =comments)



@app.route('/search', methods=['POST'])
def search():
    try:
        # Retrieve search term from the Ajax request
        search_term = request.form.get('searchTerm')

        # Perform the database query
        search_results = get_search(search_term)
        # Process the results and send back as JSON
        formatted_results = []
        for row in search_results:
            formatted_results.append({'id': row[0], 'name': row[1],'image_url':row[3]})
        print(formatted_results)
        return jsonify(formatted_results)

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/lists', methods=["GET",'POST'])
def userLists():
    Albums = get_albums_db()
    print(Albums)
    return render_template('ListPage.html',Albums = Albums)

@app.route('/userReview', methods=["GET",'POST'])
def userReviews():
    userReviews = get_user_reviews(session['user'])
    print(userReviews)
    return render_template('userReviews.html', userReviews = userReviews)

@app.route('/removeReview', methods=["GET", "POST"])
def removeReview():
    if request.method == 'POST':
        # Assuming you're using request.json.get for JSON data
        album_id = request.json.get('albumID')

        # Assuming you have a function like removeUserReview to handle the deletion
        removeUserReview(session['user'], album_id)

        # You might want to return a response indicating success or failure
        return {'status': 'success', 'message': 'Review removed successfully'}

    # Handle GET requests if needed
    return {'status': 'error', 'message': 'Invalid request method for /removeReview endpoint'}


@app.route('/addList', methods=['GET', "POST"])
def addList():
   content_type = request.headers.get('Content-Type')
   if (content_type == 'application/json'):
        try:
            data = request.get_json()
            list_name = data.get('listName')
            album_ids = data.get('albumIds')
            response_data = {'listName': list_name, 'albumIds': album_ids}
            insertUserList(response_data,session['user'])

            return jsonify(response_data), 200
            #Post to Database
        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)