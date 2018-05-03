from flask import Flask

""" 1. Creating a flask application instance, the name argument is passed to flask
application constructor. It's used to determine the root path"""
app = Flask(__name__)
app.config.from_object('config')

from app import views, models
