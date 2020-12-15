CREATE TABLE Users (
    id SERIAL NOT NULL,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE Playlist (
    id SERIAL NOT NULL,
    name VARCHAR NOT NULL,
    owner_id SERIAL NOT NULL,
    FOREIGN KEY(owner_id) REFERENCES Users(id),
    songs VARCHAR[],
    status VARCHAR NOT NULL,
    PRIMARY KEY (id)
);