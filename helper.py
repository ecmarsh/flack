from flask import request
from datetime import datetime


def now_stamp():
    """ Timestamp generator """
    now = datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    return timestamp


def get_cookie(key):
    """ Get cookie value """
    try:
        return request.cookies.get(key)
    except ValueError:
        return None
