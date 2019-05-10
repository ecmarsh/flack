from flask import request
from datetime import datetime


def now_stamp():
    """ Creates string formatted timestamp """
    now = datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    return timestamp


def getcookie():
    """ Gets display name from cookie """
    try:
        name = request.cookies.get('displayName')
    except ValueError:
        name = None
    return name
