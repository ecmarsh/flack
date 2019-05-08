import os
import requests

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_scss import Scss
from flask_assets import Environment, Bundle
from flask_socketio import SocketIO, emit, send


# __Init__
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# Setup socketIO
socketio = SocketIO(app)

# Scss --> css
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle(
    'sass/main.scss',
    filters='pyscss',
    depends=('**/*.scss'),
    output='styles.css')
assets.register('scss_all', scss)

# Channels
channels = ('channel')
messages = dict([
    {'channel', '', 'user': '', 'message': ''}
])


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/channel/<channel_name>")
def channel():
    if not channel_name:
        return render_template('channel.html')


@socketio.on('connect')
def indicate_connected():
    print('Connected')


@socketio.on('disconnect')
def disconnected():
    print('Connection terminated')


@socketio.on('create channel')
def create_channel(data):
    emit('create channel', {'channel': data['channel']}, broadcast=True)


@socketio.on('name set')
def start_channel():
    return redirect(url_for('channel'))


@socketio.on('register display name')
def create_display_name(data):
    displayName = data['display_name']
    emit('show display name', {
         'displayName': displayName
         }, broadcast=True)


if __name__ == '__main___':
    socketio.run(app)
