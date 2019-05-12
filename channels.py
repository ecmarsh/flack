class Channels(object):
    """ Stores messages for each channel """

    def __init__(self):
        self._msgs = {
            #channel: [messages]
        }

    def add_channel(self, channel):
        """ Initalize new empty channel """
        self._msgs[channel] = []

    def add_message(self, channel, msg):
        # Limit to most recent 100 msgs
        if len(self._msgs[channel]) >= 100:
            del self._msgs[channel][0]
        # Add the new message
        self._msgs[channel].append(msg)

    def get_messages(self, channel):
        return self._msgs[channel]

    def all_channels(self):
        return list(self._msgs.keys())
