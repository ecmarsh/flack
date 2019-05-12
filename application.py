import os
import requests
import uuid

from flask import Flask, flash, jsonify, make_response, session, redirect, render_template, request, url_for
from flask_scss import Scss
from flask_assets import Environment, Bundle
from flask_socketio import SocketIO, emit, namespace, send, join_room, leave_room

from channels import Channels
from helper import add_seconds, cObj, get_cookie, now_stamp


# App Init
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Compile scss
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle(
    'sass/main.scss',
    filters='pyscss',
    depends=('**/*.scss'),
    output='styles.css')
assets.register('scss_all', scss)


# Globals
users = {}
rooms = Channels()

# Initalize channels
rooms.add_channel('general')
msg = {'text': 'Welcome to channel #general',
       'name': 'FlackBot', 'stamp': now_stamp(), 'color': cObj('#888888')}
rooms.add_message('general', msg)


@app.route("/")
def index():
    """Show chat app"""
    return render_template('index.html')


@app.route('/new_room', methods=['POST'])
def new_room():
    """
    Handle POST request from contoller
    Create a new channel and add to rooms
    """

    # Save channel
    channel = request.get_json()['name'].lower()
    create_channel(channel)

    # Broadcast the new rooms to users
    updateRooms()

    # We goood 👍
    return jsonify(status=200, statusText='OK')


@socketio.on('connect', namespace='/chat')
def makeConnection():
    print('Connected')


@socketio.on('disconnect')
def on_disconnect():
    """ Remove from online users """
    if session['uuid'] in users:
        del users[session['uuid']]
        updateRoster()


@socketio.on('join', namespace='/chat')
def on_join(room):
    join_room(room)
    updateMessages(room)  # Sync UI


@socketio.on('leave', namespace='/chat')
def on_leave(room):
    leave_room(room)


@socketio.on('identify', namespace='/chat')
def on_identify(displayName):
    """ Handle session / username creation """
    # If session already active
    # Just change the display name
    if 'uuid' in session:
        print('Identifying ' + displayName)
        users[session['uuid']] = {'username': displayName}
        updateRoster()
    else:
        # Create a new session and set name
        print('Setting new user...')
        session['uuid'] = uuid.uuid1()
        users[session['uuid']] = {'username': displayName}

        # Sync globals for new user
        updateRoster()
        updateRooms()
        channel = get_cookie('activeChannel')
        updateMessages(channel)


@socketio.on('message', namespace='/chat')
def on_message(message):
    """
    Broadcast message to current room
    """

    room = message['room']
    # Default to general room
    if room is None:
        room = 'general'

    # Message color
    col = message['color']
    if col is None:
        col = '#888888'

    # Tmp message obj
    msg = {'text': message['text'],
           'name': users[session['uuid']]['username'],
           'stamp': now_stamp(),
           'color': cObj(col)}

    # Save message to room
    rooms.add_message(room, msg)

    # Broadcast to current room
    emit('message', msg, room=room, broadcast=True)


def create_channel(channel):
    """ Setup a new channel """
    rooms.add_channel(channel)
    # Add booting messages
    tmp1 = {'text': 'Booting channel...',
            'name': 'FlackBot',
            'stamp': now_stamp(),
            'color': cObj('#888888')}
    tmp2 = {'text': f'Channel #{channel} is active!',
            'name': 'FlackBot',
            'stamp': add_seconds(tmp1['stamp']),
            'color': cObj('#888888')}
    rooms.add_message(channel, tmp1)
    rooms.add_message(channel, tmp2)


def updateRoster():
    """
    Sync online users with socket's active sids
    """
    names = ['FlackBot']

    # Fill roster with current sessions
    for _uuid in users:
        username = users[_uuid]['username']
        if len(username) == 0:
            names.append('Anonymous')
        else:
            names.append(username)

    # Send to client for UI update
    socketio.emit('roster', names, namespace='/chat')


def updateMessages(channel='general'):
    """ Update session UI with current room """
    messages = rooms.get_messages(channel)
    emit('localUpdate', messages, broadcast=False, namespace='/chat')


def updateRooms():
    """ Send active channels to UI """
    socketio.emit('rooms', rooms.all_channels(), namespace='/chat')


if __name__ == '__main___':
    socketio.run(app)
