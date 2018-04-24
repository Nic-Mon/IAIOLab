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

print('editing playlist name with id ' + str(playlist_id))
models.db_modify_playlist(
    playlist_id,
    'jams',
    ['songid1', 'songid2']
    )
print(models.db_fetch_playlists('mbayley'))

print('deleting playlist')
models.db_delete_playlist(playlist_id)

print('adding mp3 path')
models.db_mp3_path_add('songid1', 'www.fake.path/file.mp3')

print('looking up mp3 path')
print(models.db_mp3_path_lookup('songid1'))
