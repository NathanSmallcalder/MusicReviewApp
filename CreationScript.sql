USE musicDatabase;


-- Create User table
CREATE TABLE User (
    UserID INT PRIMARY KEY,
    Username VARCHAR(255),
    Email VARCHAR(255),
    Password VARCHAR(255)
);

-- Create Album table
CREATE TABLE Album (
    AlbumID INT PRIMARY KEY,
    Title VARCHAR(255),
    Artist VARCHAR(255),
    ReleaseDate DATE,
    Genre VARCHAR(255),
    CoverImage VARCHAR(255)
);

-- Create Review table
CREATE TABLE Review (
    ReviewID INT PRIMARY KEY,
    UserID INT,
    AlbumID INT,
    Rating INT,
    Comment TEXT,
    DatePosted DATE,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID)
);

-- Create Song table
CREATE TABLE Song (
    SongID INT PRIMARY KEY,
    Title VARCHAR(255),
    Artist VARCHAR(255),
    AlbumID INT,
    Duration INT,
    ReleaseDate DATE,
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID)
);

-- Create UserAlbumList table
CREATE TABLE UserAlbumList (
    ListID INT PRIMARY KEY,
    UserID INT,
    ListName VARCHAR(255),
    Description TEXT,
    CreatedDate DATE,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Create UserAlbumListDetail table
CREATE TABLE UserAlbumListDetail (
    DetailID INT PRIMARY KEY,
    ListID INT,
    AlbumID INT,
    OrderIndex INT,
    FOREIGN KEY (ListID) REFERENCES UserAlbumList(ListID),
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID)
);

-- Create SongReview table
CREATE TABLE SongReview (
    SongReviewID INT PRIMARY KEY,
    UserID INT,
    SongID INT,
    Rating INT,
    Comment TEXT,
    DatePosted DATE,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (SongID) REFERENCES Song(SongID)
);

-- Create Follower table
CREATE TABLE Follower (
    FollowerID INT PRIMARY KEY,
    FollowerUserID INT,
    FollowedUserID INT,
    DateFollowed DATE,
    FOREIGN KEY (FollowerUserID) REFERENCES User(UserID),
    FOREIGN KEY (FollowedUserID) REFERENCES User(UserID)
);
