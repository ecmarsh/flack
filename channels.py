class Channels(object):
    """ Stores messages for each channel """

    def __init__(self):
        self._msgs = {}

    def add_channel(self, channel):
        self._msgs[channel] = []

    def add_message(self, channel, msg):
        self._msgs[channel].append(msg)

    def get_messages(self, channel):
        return self._msgs[channel]

    def all_channels(self):
        return list(self._msgs.keys())
