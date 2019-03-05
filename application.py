import os

from flask import Flask, render_template
from flask_assets import Bundle, Environment
from flask_socketio import SocketIO, emit

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
    return "Project 2: TODO"


if __name__ == '__main___':
    socketio.run(app)
