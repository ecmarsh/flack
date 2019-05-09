from flask_socketio import Namespace, emit


class CustomNamespace(Namespace):
    def __init__(self, name, messages):
        self.name = name
        self.messages = messages

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_my_event(self, data):
        emit('my_response', data)


# socketio.on_namespace(CustomNamespace('/test'))
