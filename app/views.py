from flask import render_template, redirect, request, session
from app import app, models
from .models import *
import requests
import random
import numpy as np
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
gb_path = os.path.join(SITE_ROOT, 'static', 'georgeblood_ids.npy')
georgeblood_ids = np.load(gb_path).tolist()

#hit IA api
def get_mp3_filename(identifier):
	url = 'http://archive.org/metadata/{}'.format(identifier)
	r = requests.get(url)
	json = r.json()

	files = json['files']

	mp3s = []
	for file in files:
		name = file['name']
		if '.mp3' in name:
			mp3s.append(name)
	#remove results that start with 78 or _78
	clean_mp3s = [m for m in mp3s if not m.startswith('78') and not m.startswith('_78')]
	# only return first one
	return clean_mp3s[0]

@app.route('/')
def index():
	song_ids = random.sample(georgeblood_ids, 12)
	records = []
	url = 'http://archive.org/download/'

	for identifier in song_ids:
		song_mp3 = get_mp3_filename(identifier)
		song_name = song_mp3[:-4]
		mp3_url = url + identifier + '/' + song_mp3
		img_url = url + identifier + '/' + identifier + '_itemimage.jpg'

		records.append( (identifier, song_name, mp3_url, img_url) )

	return render_template('index.html', records=records)



@app.route("/save_playlist", methods=['GET','POST'])
def save_playlist():

	if not request.json:
		return "no json received"
	else:
		mydata = request.json # will be

	## Get user and songs
	user = 'peter' # TESTING
	song_id_list = mydata['song_id_list']
	playlist_name = mydata['playlist_name']
	# playlist_id = mydata['playlist_id']

    ## if playlist_id is null, create new playlist and get id from function
	if mydata['playlist_id']:
		playlist_id = mydata['playlist_id']
	else:
		playlist_id = models.db_create_playlist(user, playlist_name)

    ## write songs to playlist
	models.db_modify_playlist(playlist_id, playlist_name, song_id_list)

	## convert return value to str and return
	return_id = str(playlist_id)
	return return_id


# @app.route('/new_user', methods=['GET', 'POST'])
# def new_user():
#     form = UserForm()
#     if form.validate_on_submit():
#         # Get data from the form
#         # Send data from form to Database
#         username = form.username.data
#         password = form.password.data

#         success = insert_user(username, password)
#         if success:
#             session['username'] = username
#             return redirect('/trips')
#         else:
#             return redirect('/new_user')
#     return render_template('signup.html', form=form)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = UserForm()
#     if form.validate_on_submit():
#         # Get data from the form
#         # Send data from form to Database
#         username = form.username.data
#         password = form.password.data

#         success = db_login(username, password)
#         if success:
#             session['username'] = username
#             return redirect('/trips')
#         else:
#             return redirect('/login')
#     return render_template('login.html', form=form)

# @app.route('/trips')
# def display_user():
#     # Retreive data from database to display
#     if 'username' not in session:
#         return redirect('/login')
#     else:
#         username = session['username']
#         trips = fetch_trips(username)
#         return render_template('trips.html', username=username, trips=trips)

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/')

# @app.route('/create_trip', methods=['GET', 'POST'])
# def create_trip():
#     form = TripForm()
#     username = session['username']
#     users = fetch_other_users(username)

#     if form.validate_on_submit():
#         # Get data from the form
#         # Send data from form to Database
#         name = form.name.data
#         destination = form.destination.data
#         user1 = username
#         user2 = form.user2.data
#         db_create_trip(name, destination, user1, user2)
#         return redirect('/trips')
#     return render_template('create_trip.html', form=form, username=username, users=users)

# @app.route('/delete_trip/<value>')
# def delete_trip(value):
#     db_delete_trip(value)
#     return redirect('/trips')
