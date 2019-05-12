from flask import request
from datetime import datetime


def cObj(val):
    """ Generate style objects """
    return {'color': str(val)}


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


def add_seconds(strtime, seconds=2):
    """ Space time for bot message """
    s = int(strtime[6:]) + seconds % 60
    if len((str(s))) < 2:
        s = f'{0}' + s
    return strtime[:(len(strtime)-2)] + f'{s}'
