import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_assets import Environment, Bundle
from flask_socketio import SocketIO, send, emit

# __Init__
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
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


@app.route("/")
def index():
    return render_template('index.html')


@socketio.on("create channel")
def create_channel(data):
    channel = data["channel"]
    emit("create channel", {"channel": channel}, broadcast=True)


@socketio.on("register display name")
def register_display_name(data):
    display_name = data["display_name"]
    emit("display name", {"display_name": display_name}, broadcast=True)


if __name__ == '__main___':
    socketio.run(app)
