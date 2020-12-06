CREATE TABLE Users (
    user_id SERIAL NOT NULL,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    PRIMARY KEY(user_id)
);

CREATE TABLE Playlist (
    playlist_id SERIAL NOT NULL,
    name VARCHAR NOT NULL,
    owner_id SERIAL NOT NULL,
    FOREIGN KEY(owner_id) REFERENCES Users(user_id),
    songs VARCHAR[],
    PRIMARY KEY (playlist_id)
);