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
        con.commit()
        return True

def db_delete_playlist(id):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        val = cur.execute("DELETE FROM playlists WHERE id=?", [id])
        con.commit()
        return val

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

def db_rename_playlist(id, name):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        sqltext = "UPDATE playlists SET name=? WHERE (id=?)"
        cur.execute(sqltext, (name, id))

def db_fetch_playlist_songs(playlist_id):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        sqltext = ("SELECT id, playlist_id, song_order, song_id, "
            "mp3_path, img_path "
            "FROM playlist_songs "
            "WHERE (playlist_id=?)")
        response = []
        for rowlist in cur.execute(sqltext, [playlist_id]):
            row = {}
            row['id'] = rowlist[0]
            row['playlist_id'] = rowlist[1]
            row['song_order'] = rowlist[2]
            row['song_id'] = rowlist[3]
            row['mp3_path'] = rowlist[4]
            row['img_path'] = rowlist[5]
            response.append(row)
        return response

def db_song_add(playlist_id, song_id, mp3_path, img_path):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        sqltext = ("SELECT COUNT(*) FROM playlist_songs "
            "WHERE (playlist_id=?)")
        cur.execute(sqltext, [playlist_id])
        song_order = cur.fetchone()[0] + 1
        sqltext = ("INSERT INTO playlist_songs "
            "(playlist_id, song_order, song_id, mp3_path, img_path) "
            "VALUES (?, ?, ?, ?, ?)")
        cur.execute(sqltext, 
            (playlist_id, song_order, song_id, mp3_path, img_path))
    return

def db_song_delete(playlist_song_id):
    with sql.connect(dbname) as con:
        cur = con.cursor()
        sqltext = "DELETE FROM playlist_songs WHERE (id=?)"
        cur.execute(sqltext, [playlist_song_id])
    return

def db_song_earlier(playlist_song_id):
    return

def db_song_later(playlist_song_id):
    return
