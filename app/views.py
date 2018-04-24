from flask import render_template, redirect, request, session
from app import app, models

# Access the models file to use SQL functions


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/save_playlist", methods=['GET','POST'])
def save_playlist():

    app.logger.debug("JSON received...")
    app.logger.debug(request.json)

    if request.json:
        mydata = request.json # will be
        app.logger.debug(mydata['a'])
        return "Data received"

    else:
        return "no json received"


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
