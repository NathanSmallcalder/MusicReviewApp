from flask import Flask, render_template, request, redirect, url_for, session, Response
import os
import bcrypt
import json
from databaseCalls import *

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/')
def index():
    Albums = get_albums_db()
    return render_template('index.html', title='Album Review', content='Hello, Flask!',Albums = Albums)

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_account_db(username)
    
        if user and bcrypt.checkpw(password.encode('utf8'), user[0][3].encode('utf-8')):
            session['user'] = username 
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"
        
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/albumReview', methods=['GET','POST'])
def getAlbumReview():
    album = request.args.get('album')

    albums = get_album_by_albumID(album)
    songs = get_songs_by_albumID(album)
    artist = get_artist_by_albumID(album)
    
    SongLen = len(songs)
    print(SongLen)
    return render_template('AlbumReviewPage.html', 
                           albums = albums,
                           songs = songs, 
                           artist = artist,
                           SongLen = SongLen,
                           UserId = session['user'])


@app.route('/albumReviewSend', methods=['POST'])
def PostAlbumReview():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = json.loads(request.data)
        print(data)
    return Response(status = 200)



@app.route('/album', methods=['GET','POST'])
def getAlbum():
    album = request.args.get('album')

    albums = get_album_by_albumID(album)
    songs = get_songs_by_albumID(album)
    artist = get_artist_by_albumID(album)

    return render_template('AlbumPage.html', 
                           albums = albums,
                           songs = songs, 
                           artist = artist)

if __name__ == '__main__':
    app.run(debug=True)