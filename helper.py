from flask import request


def getcookie():
    """ Gets display name from cookie """
    try:
        name = request.cookies.get('user')
        return name
    except ValueError:
        name = None
        return False
