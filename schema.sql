-- sqlite3 database schema;

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

drop view if exists playlist_song_paths;
drop table if exists playlist_songs;
create table playlist_songs (
    playlist_id integer,
    song_order integer,
    song_id text,
    PRIMARY KEY(playlist_id, song_order),
    FOREIGN KEY(playlist_id) REFERENCES playlists(id)
);

drop table if exists mp3_paths;
create table mp3_paths (
    song_id text PRIMARY KEY,
    mp3_path text
);

create view playlist_song_paths AS
    SELECT * FROM playlist_songs
        LEFT JOIN mp3_paths 
            ON playlist_songs.song_id=mp3_paths.song_id;

-- temporarily hard code an account for Peter;
insert into users (username, password)
    values ('test', 'password');

