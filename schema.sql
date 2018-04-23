-- Insert code to create Database Schema
-- This will create your .db database file for use
drop table if exists users;
create table users (
    username text primary key,
    password text not null
);

drop table if exists playlists;
create table playlists (
    id integer primary key,
    username text not null,
    name text not null,
    FOREIGN KEY(username) REFERENCES users(username)
);

drop table if exists playlist_songs;
create table playlist_songs (
    id integer primary key,
    playlist_id integer,
    song_order integer,
    song_id text,
    mp3_path text,
    img_path text,
    FOREIGN KEY(playlist_id) REFERENCES playlists(id)
);
