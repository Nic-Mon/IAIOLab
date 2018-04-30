import sqlite3 as sql
dbname = 'app.db'

def db_reset():
    with open('schema.sql', 'r') as myfile:
        schema=myfile.read()
    with sql.connect(dbname) as con:
        cur = con.cursor()
        cur.execute(schema)
        con.commit()

def db_create_user(username, password):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE username=?", [username])
        if cur.fetchone()[0]>0: return False
        result = cur.execute(
            "INSERT INTO users (username, password)"
            " VALUES (?,?)"
            , (username, password))
        con.commit()
        return True

def db_login(username, password):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        sqltext = "SELECT COUNT(*) FROM users WHERE (username=? AND password=?)"
        cur.execute(sqltext, (username, password))
        return (cur.fetchone()[0]>0)

def db_create_playlist(username, name):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        sqltext = ("INSERT INTO playlists (username, name)"
            " VALUES (?, ?)")
        cur.execute(sqltext, (username, name))
        id = cur.lastrowid
        con.commit()
        return id

def db_delete_playlist(id):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM playlists WHERE id=?", [id])
        con.commit()
        return

def db_fetch_playlists(username):
    response = []
    with sql.connect(dbname) as con:
        cur = con.cursor()
        sqltext = ("SELECT id, username, name "
            "FROM playlists "
            "WHERE (username=?)")
        for rowlist in cur.execute(sqltext, [username]):
            row = {}
            row['id'] = rowlist[0]
            row['username'] = rowlist[1]
            row['name'] = rowlist[2]
            response.append(row)
        return response

def db_fetch_playlist_songs(playlist_id):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        sqltext = ("SELECT playlist_id, song_order, song_id, mp3_path"
            "FROM playlist_song_paths "
            "WHERE (playlist_id=?)")
        response = []
        for rowlist in cur.execute(sqltext, [playlist_id]):
            row = {}
            row['playlist_id'] = rowlist[0]
            row['song_order'] = rowlist[1]
            row['song_id'] = rowlist[2]
            row['mp3_path'] = rowlist[3]
            response.append(row)
        return response

def db_modify_playlist(playlist_id, name, song_id_list):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        sqltext = "UPDATE playlists SET name=? WHERE (id=?)"
        cur.execute(sqltext, (name, playlist_id))
        sqltext = "DELETE FROM playlist_songs WHERE (playlist_id=?)"
        cur.execute(sqltext, [playlist_id])
        sqltext = ("INSERT INTO playlist_songs (playlist_id, "
            "song_order, song_id) "
            " VALUES (?, ?, ?)")
        song_order = 1
        for song_id in song_id_list:
            cur.execute(sqltext, (playlist_id, song_order, song_id))
            song_order += 1
        con.commit()

def db_mp3_path_add(song_id, mp3_path):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        sqltext = ("INSERT INTO mp3_paths (song_id, mp3_path) "
            "VALUES (?, ?)")
        cur.execute(sqltext, (song_id, mp3_path))
        con.commit()

def db_mp3_path_lookup(song_id):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        sqltext = ("SELECT mp3_path FROM mp3_paths "
            "WHERE (song_id=?)")
        cur.execute(sqltext, [song_id])
    return (cur.fetchone()[0])

def db_mp3_path_delete(song_id):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM mp3_paths WHERE song_id=?", [song_id])
        con.commit()
        return
