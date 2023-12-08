from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
import bcrypt

app = Flask(__name__)
app.secret_key = "super secret key"

db_config  = {
    'user': os.getenv("USER"),
    'password': os.getenv("PASSWORD"),
    'host': 'localhost',
    'port': 3306,
    'database': 'musicDatabase',
}

def connect_db():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    connection = connect_db()
    cursor = connection.cursor(buffered=True)

    sql_select = f"SELECT * FROM Album"
    cursor.execute(sql_select)
    Albums = cursor.fetchall()

    #sql_select = f"SELECT Genre FROM Artist"
    return render_template('index.html', title='Flask Template Example', content='Hello, Flask!',Albums = Albums)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash Password
        # Adding the salt to password
        salt = bcrypt.gensalt()
        # Hashing the password
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Check credentials in the database
        conn = connect_db()
        cursor = conn.cursor()
        sql_insert = "INSERT INTO User (Username, Email, PasswordHash) VALUES (%s, %s, %s)"
        cursor.execute(sql_insert, (username,email,hashed))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = user[1]  # Store the username in the session
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials in the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE Username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['PasswordHash']):
            session['user'] = user['Username']  # Store the username in the session
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"

    return render_template('login.html')
# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/album', methods=['GET','POST'])
def getAlbum():
    album = request.args.get('album')
    connection = connect_db()
    cursor = connection.cursor(buffered=True)

    sql_select = f"SELECT * FROM Album WHERE AlbumID = {album}"
    cursor.execute(sql_select)
    albums = cursor.fetchone()
    print(albums)

    sql_select = f"SELECT * FROM Song WHERE AlbumID = {album}"
    cursor.execute(sql_select)
    songs = cursor.fetchall()

    sql_select = f"SELECT * FROM Artist JOIN Album ON Artist.ArtistID = Album.ArtistID WHERE Album.AlbumID = {album};"
    cursor.execute(sql_select)
    artist = cursor.fetchone()
    print(songs)
    return render_template('AlbumPage.html', 
                           albums = albums,
                           songs = songs, 
                           artist = artist)

if __name__ == '__main__':
    app.run(debug=True)