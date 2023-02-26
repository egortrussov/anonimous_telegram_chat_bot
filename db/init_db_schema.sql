DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS connections;
DROP TABLE IF EXISTS messages;

CREATE TABLE users (
    user_id TEXT NOT NULL, 
    username TEXT NOT NULL,
    current_room_id TEXT
); 

CREATE TABLE rooms (
    room_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE connections (
    connection_id TEXT NOT NULL,
    room_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    last_login DATETIME
);

CREATE TABLE messages (
    message_id TEXT UNIQUE NOT NULL,
    room_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    text TEXT NOT NULL,
    time DATETIME NOT NULL
); 

