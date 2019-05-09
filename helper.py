from flask import request


def getcookie():
    """ Gets display name from cookie """
    try:
        name = request.cookies.get('user')
    except ValueError:
        name = None
    return name
