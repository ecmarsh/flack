import os
import requests
import uuid


from flask import Flask, flash, jsonify, make_response, session, redirect, render_template, request, url_for
from flask_scss import Scss
from flask_assets import Environment, Bundle
from flask_socketio import SocketIO, emit, namespace, send, join_room, leave_room

from channels import Channels
from helper import get_cookie, now_stamp


# __Init__
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

# Initalize channels
rooms = Channels()
rooms.add_channel('general')
msg = {'text': 'Booting system', 'name': 'Bot', 'stamp': now_stamp()}
rooms.add_message('general', msg)


@app.route("/")
def index():
    """Show chat app"""
    return render_template('index.html')


#
# Socket built-in events
#
@socketio.on('connect', namespace='/chat')
def makeConnection():
    print('connected')


@socketio.on('join', namespace='/chat')
def on_join(room):
    print('Joining room ' + room)
    join_room(room)
    updateMessages(room)  # Sync UI


@socketio.on('leave', namespace='/chat')
def on_leave(room):
    print('Leaving room ' + room)
    leave_room(room)


@socketio.on('disconnect')
def on_disconnect():
    """ Remove from online users """
    if session['uuid'] in users:
        del users[session['uuid']]
        updateRoster()


#
# Custom events
#

def updateRoster():
    """
    Sync online users with socket's active sids
    """
    names = []
    for _uuid in users:
        username = users[_uuid]['username']
        if len(username) == 0:
            names.append('Anonymous')
        else:
            names.append(username)
    # Send to client for UI update
    socketio.emit('roster', names, namespace='/chat')


def updateRooms():
    """ Send active channels to UI """
    socketio.emit('rooms', rooms.all_channels(), namespace='/chat')


@socketio.on('identify', namespace='/chat')
def on_identify(displayName):
    """ Handle setting display name """
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


def updateMessages(channel='general'):
    messages = rooms.get_messages(channel)
    print(messages)
    print('Should be updating room ' + channel)
    for message in messages:
        emit('message', message, room="channel", broadcast=False)


@socketio.on('message', namespace='/chat')
def new_message(message):
    """
    Broadcast message to current room
    """
    room = message['room']
    # Default to general room
    if room is None:
        room = 'general'

    # Tmp message obj
    tmp = {'text': message['text'],
           'name': users[session['uuid']]['username'],
           'stamp': now_stamp()}

    # Save message to room
    rooms.add_message(room, tmp)
    print(room+":")
    print(rooms._msgs[room])
    # Broadcast to current room
    emit('message', tmp, room=room, broadcast=True)


@app.route('/new_room', methods=['POST'])
def new_room():
    """
    Handle POST request from contoller
    Create a new channel and add to rooms
    """

    channel = request.get_json()['name'].lower()

    # Save channel
    create_channel(channel)
    print('Updating rooms...')

    # Broadcast the new rooms to users
    updateRooms()

    # We goood 👍
    return jsonify(status=200, statusText='OK')


def create_channel(channel):
    """ Setup a new channel """
    rooms.add_channel(channel)
    # Tmp message obj
    tmp1 = {'text': 'Booting channel...',
            'name': 'Bot',
            'stamp': now_stamp()}
    rooms.add_message(channel, tmp1)
    tmp2 = tmp1
    tmp2['text'] = 'Chat in ' + channel + ' live!'
    rooms.add_message(channel, tmp2)


if __name__ == '__main___':
    socketio.run(app)
