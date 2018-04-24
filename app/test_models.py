import models

print('-- creating user --')
print(models.db_create_user('mbayley', '1111'))

print('-- logging in --')
print(models.db_login('mbayley', '1111'))

print('-- creating playlist --')
playlist_id = models.db_create_playlist('mbayley', 'my_playlist')
print('playlist id = ' + str(playlist_id))

print('-- fetching playlists --')
print(models.db_fetch_playlists('mbayley'))

print('-- editing playlist name with id ' + str(playlist_id) + ' --')
models.db_modify_playlist(
    playlist_id,
    'jams',
    ['songid1', 'songid2']
    )
print(models.db_fetch_playlists('mbayley'))

print('-- deleting playlist --')
models.db_delete_playlist(playlist_id)

print('-- looking up mp3 path --')
mp3_path = models.db_mp3_path_lookup('songid1')
print(mp3_path)

if mp3_path:
    print('-- deleting mp3 path --')
    models.db_mp3_path_delete('songid1')

print('-- adding mp3 path --')
models.db_mp3_path_add('songid1', 'www.fake.path/file.mp3')

