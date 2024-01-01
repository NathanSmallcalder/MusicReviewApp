CREATE DATABASE IF NOT EXISTS musicDatabase;
USE musicDatabase;

-- Create User table
CREATE TABLE User (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    PasswordHash VARCHAR(64) NOT NULL
);

-- Create Artist table
CREATE TABLE Artist (
    ArtistID VARCHAR(255) PRIMARY KEY,
    ArtistName VARCHAR(255) NOT NULL,
    Genre VARCHAR(255) NOT NULL
);

-- Create Album table
CREATE TABLE Album (
    AlbumID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255) NOT NULL,
    ReleaseDate VARCHAR(25),
    CoverImage VARCHAR(255),
    ArtistID VARCHAR(255),
    FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID)
);

-- Create Review table
CREATE TABLE Review (
    ReviewID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    AlbumID INT,
    Rating INT,
    Comment TEXT,
    DatePosted DATETIME,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID)
);

-- Create Song table
CREATE TABLE Song (
    SongID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255) NOT NULL,
    AlbumID INT,
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID)
);

-- Create UserAlbumList table
CREATE TABLE UserAlbumList (
    ListID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    ListName VARCHAR(255),
    Description TEXT,
    CreatedDate DATETIME,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Create SongReview table for individual song reviews
CREATE TABLE SongReview (
    SongReviewID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    SongID INT,
    Rating INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (SongID) REFERENCES Song(SongID)
);


-- Create Following table
CREATE TABLE Following (
    FollowingID INT PRIMARY KEY AUTO_INCREMENT,
    FollowerUserID INT,
    FollowedUserID INT,
    DateFollowed DATETIME,
    FOREIGN KEY (FollowerUserID) REFERENCES User(UserID),
    FOREIGN KEY (FollowedUserID) REFERENCES User(UserID)
);
