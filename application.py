import os
import requests
import uuid
import time


from datetime import date
from flask import Flask, flash, jsonify, make_response, session, redirect, render_template, request, url_for
from flask_scss import Scss
from flask_assets import Environment, Bundle
from flask_socketio import SocketIO, emit, namespace, send, join_room, leave_room
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helper import getcookie, now_stamp


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


# Globals
messages = [{'text': 'Booting system', 'name': 'Bot', 'stamp': 'x'},
            {'text': 'Chat now live!', 'name': 'Anon', 'stamp': 'x'}]
users = {}
rooms = ['General']


@socketio.on('join', namespace='/test')
def on_join(room):
    print('joining room ' + room)
    join_room(room)


@socketio.on('leave', namespace='/test')
def on_leave(room):
    print('leaving room ' + room)
    leave_room(room)


def updateRoster():
    names = []
    for user_id in users:
        username = users[user_id]['username']
        if len(username) == 0:
            names.append('Anonymous')
        else:
            names.append(username)
    socketio.emit('roster', names, namespace='/test')


def updateRooms():
    socketio.emit('rooms', rooms, namespace='/test')


@socketio.on('connect', namespace='/test')
def makeConnection():
    print('connected')


@socketio.on('identify', namespace='/test')
def on_identify(message):
    if 'uuid' in session:
        print('identify ' + message)
        users[session['uuid']] = {'username': message}
        updateRoster()
        socketio.emit('message', message + ' changed display name')
    else:
        print('sending information')
        session['uuid'] = uuid.uuid1()
        session['username'] = message
        users[session['uuid']] = {'username': session['username']}
        updateRoster()
        updateRooms()
        for message in messages:
            emit('message', message)


@socketio.on('message', namespace='/test')
def new_message(message):
    room = message['room']
    tmp = {'text': message['text'], 'name': users[session['uuid']]
           ['username'], 'stamp': now_stamp()}
    print(tmp)
    messages.append(tmp)
    emit('message', tmp, room=room, broadcast=True)


@socketio.on('disconnect')
def on_disconnect():
    if session['uuid'] in users:
        del users[session['uuid']]
        updateRoster()


@app.route('/new_room', methods=['POST'])
def new_room():
    rooms.append(request.get_json()['name'])
    print('updating rooms...')
    updateRooms()

    return jsonify(status=200, statusText='OK')


# def get_channel(name):
#     fallback_data = {
#         'name': 'Channel Undefined',
#         'messages': [],
#     }
#     for channel in channels:
#         if channel['name'] == name:
#             channel_data = channel
#             return channel_data
#     return fallback_data


# def add_message(name, message):
#     for channel in channels:
#         if channel['name'] == name:
#             channel['messages'].append(message)
#             return channel
#     return False


@app.route("/")
def index():
    """
    If first time, show name form,
    else proceed to channels
    """
    return render_template('index.html')


# def getcookie():
#     """ Gets display name from cookie """
#     try:
#         name = request.cookies.get('user')
#     except ValueError:
#         name = None
#     return name


# @app.route('/setcookie', methods=['POST', 'GET'])
# def setcookie():
#     """
#     Sets cookie with users chosen display name
#     """
#     error = None
#     if request.method == 'POST':
#         try:
#             user = request.form["display-name"]
#         except ValueError:
#             error = 'Must choose a display name'

#         # Drop cookie with next view
#         res = make_response(redirect(url_for('channel', error=error)))
#         res.set_cookie('user', user)
#         return res

#     # Method is GET
#     return redirect(url_for('index', error=error))


# @app.route("/channel", methods=['POST', 'GET'])
# def channel():
#     return render_template('channel.html', channels=channels, user=getcookie())


# @app.route("/chat/<channel_name>")
# def chat(channel_name):
#     channel_data = get_channel(channel_name)
#     return render_template('chat.html', channel=channel_data, user=getcookie())


# @socketio.on('connect')
# def indicate_connected():
#     print('Connected')


# @socketio.on('disconnect')
# def disconnected():
#     print('Connection terminated')


# @socketio.on('newmessage')
# def on_message(data):
#     user = getcookie()
#     channel = data['channel']
#     message = data['message']
#     new_data = {
#         'user': user,
#         'text': message,
#         'stamp': 'x'
#     }
#     new_messages = add_message(channel, new_data)
#     emit('received', new_messages['messages'])


# @socketio.on('create channel')
# def create_channel(data):
#     emit('create channel', {'channel': data['channel']}, broadcast=True)


# @socketio.on('incoming')
# def create_message(data):
#     name = data['name']
#     new_data = {
#         'user': data['user'],
#         'text': data['text'],
#         'stamp': data['stamp']
#     }
#     add_message(name, new_data)
#     emit('new message', new_data, namespace='/' + name, broadcast=True)


if __name__ == '__main___':
    socketio.run(app)
