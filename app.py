from flask import Flask, render_template, request, redirect, url_for, session, Response, jsonify
import os
import bcrypt
import json
from databaseCalls import *

app = Flask(__name__)
app.secret_key = "super secret key"


def is_valid_album_review(data):
    print(data)
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
    return render_template('index.html', title='Album Review', content='Hello, Flask!',Albums = Albums)

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
            session['user'] = account
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
    songs = get_songs_by_albumID(album)
    artist = get_artist_by_albumID(album)
    print(artist)
    
    SongLen = len(songs)
    print(SongLen)
    return render_template('AlbumReviewPage.html', 
                           albums = albums,
                           songs = songs, 
                           artist = artist,
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
    print(artist)

    return render_template('AlbumPage.html', 
                           albums = albums, 
                           album_details = album_details, 
                           artist = artist,
                           comments =comments)

if __name__ == '__main__':
    app.run(debug=True)