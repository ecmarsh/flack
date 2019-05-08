import os
import requests

from flask import Flask, flash, jsonify, make_response, redirect, render_template, request, url_for
from flask_scss import Scss
from flask_assets import Environment, Bundle
from flask_socketio import SocketIO, emit, namespace, send, join_room, leave_room
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


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
channels = [{'name': 'test', 'messages': [
    {'user': 'ethan', 'text': 'sup', 'stamp': 'Wed May 08 2019 00: 39: 14 GMT-0700'}]}]


def get_channel(name):
    fallback_data = {
        'name': 'Channel Undefined',
        'messages': [],
    }
    for channel in channels:
        if channel['name'] == name:
            channel_data = channel
            return channel_data
    return fallback_data


def add_message(name, message):
    for channel in channels:
        if channel['name'] == name:
            channel['messages'].append(message)
            return channel
    return False


@app.route("/")
def index():
    """
    If first time, show name form,
    else proceed to channels
    """
    name = getcookie()
    if name is None:
        return render_template('index.html')
    return render_template('channel.html', channels=channels)


def getcookie():
    """ Gets display name from cookie """
    try:
        name = request.cookies.get('user')
    except ValueError:
        name = None
    return name


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    """
    Sets cookie with users chosen display name
    """
    error = None
    if request.method == 'POST':
        try:
            user = request.form["display-name"]
        except ValueError:
            error = 'Must choose a display name'

        # Drop cookie with next view
        res = make_response(redirect(url_for('channel', error=error)))
        res.set_cookie('user', user)
        return res

    # Method is GET
    return redirect(url_for('index', error=error))


@app.route("/channel", methods=['POST', 'GET'])
def channel():
    return render_template('channel.html', channels=channels, user=getcookie())


@app.route("/chat/<channel_name>")
def chat(channel_name):
    channel_data = get_channel(channel_name)
    return render_template('chat.html', channel=channel_data)


@socketio.on('connect')
def indicate_connected():
    print('Connected')


@socketio.on('disconnect')
def disconnected():
    print('Connection terminated')


@socketio.on('newmessage')
def on_message(data):
    user = getcookie()
    channel = data['channel']
    message = data['message']
    new_data = {
        'user': user,
        'text': message,
        'stamp': 'x'
    }
    new_messages = add_message(channel, new_data)
    emit('received', new_messages['messages'])


@socketio.on('create channel')
def create_channel(data):
    emit('create channel', {'channel': data['channel']}, broadcast=True)


@socketio.on('incoming')
def create_message(data):
    name = data['name']
    new_data = {
        'user': data['user'],
        'text': data['text'],
        'stamp': data['stamp']
    }
    add_message(name, new_data)
    emit('new message', new_data, namespace='/' + name, broadcast=True)


if __name__ == '__main___':
    socketio.run(app)
