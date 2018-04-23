import models

print('creating user')
print(models.db_create_user('mbayley', '1111'))

print('logging in')
print(models.db_login('mbayley', '1111'))

print('creating playlist')
print(models.db_create_playlist('mbayley', 'my_playlist'))

print('fetching playlists')
pl = models.db_fetch_playlists('mbayley')
print(pl)
playlist_id = pl[0]['id']
print('id=' + str(playlist_id))

print('changing playlist name with id ' + str(playlist_id))
models.db_rename_playlist(playlist_id, 'jams')
print(models.db_fetch_playlists('mbayley'))

print('deleting playlist')
models.db_delete_playlist(playlist_id)

print('adding a song')
models.db_create_playlist('mbayley', 'my_playlist2')
pl = models.db_fetch_playlists('mbayley')
playlist_id = pl[0]['id']
models.db_song_add(playlist_id, 1, 'mp3_path', 'img_path')

print('deleting a song')
playlist_song_id = models.db_fetch_playlist_songs(playlist_id)[0]['id']
models.db_song_delete(playlist_song_id)

