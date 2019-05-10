import os
import requests
import uuid


from flask import Flask, flash, jsonify, make_response, session, redirect, render_template, request, url_for
from flask_scss import Scss
from flask_assets import Environment, Bundle
from flask_socketio import SocketIO, emit, namespace, send, join_room, leave_room

from helper import getcookie, now_stamp


# __Init__
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# Setup socketIO
socketio = SocketIO(app)

# Compile sass to css sheet
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle(
    'sass/main.scss',
    filters='pyscss',
    depends=('**/*.scss'),
    output='styles.css')
assets.register('scss_all', scss)


# Globals
messages = [{'text': 'Booting system', 'name': 'Bot', 'stamp': 'x'},
            {'text': 'Chat now live!', 'name': 'Anon', 'stamp': 'x'}]
users = {}
rooms = ['General']


@app.route("/")
def index():
    """Show chat app"""
    return render_template('index.html')


#
# Socket built-in events
#
@socketio.on('connect', namespace='/test')
def makeConnection():
    print('connected')


@socketio.on('join', namespace='/test')
def on_join(room):
    print('joining room ' + room)
    join_room(room)


@socketio.on('leave', namespace='/test')
def on_leave(room):
    print('leaving room ' + room)
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
    socketio.emit('roster', names, namespace='/test')


def updateRooms():
    """
    Send active channels to UI
    """
    socketio.emit('rooms', rooms, namespace='/test')


@socketio.on('identify', namespace='/test')
def on_identify(message):
    """ Handle setting display name """
    # If session already active
    # Just change the display name
    if 'uuid' in session:
        print('identify ' + message)
        users[session['uuid']] = {'username': message}
        updateRoster()
        socketio.emit('message', message + ' changed display name')
    else:
        # Create a new session and set name
        print('sending information')
        session['uuid'] = uuid.uuid1()
        session['username'] = message
        users[session['uuid']] = {'username': session['username']}
        # Sync globals for new user
        updateRoster()
        updateRooms()
        for message in messages:
            emit('message', message)


@socketio.on('message', namespace='/test')
def new_message(message):
    """
    Broadcast message to current room
    """
    room = message['room']
    # Default to general room
    if room is None:
        room = 'General'

    # Tmp message obj
    tmp = {'text': message['text'],
           'name': users[session['uuid']]['username'],
           'stamp': now_stamp()}
    print(tmp)

    # Add to list of messages
    messages.append(tmp)

    # Broadcast to current room
    emit('message', tmp, room=room, broadcast=True)


@app.route('/new_room', methods=['POST'])
def new_room():
    """
    Handle POST request from contoller
    Create a new channel and add to rooms
    """

    # Add created room to list
    rooms.append(request.get_json()['name'])
    print('updating rooms...')

    # Broadcast the new rooms to users
    updateRooms()

    # We goood 👍
    return jsonify(status=200, statusText='OK')


if __name__ == '__main___':
    socketio.run(app)
