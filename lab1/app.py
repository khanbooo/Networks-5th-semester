import threading
import socket
import uuid

from sender import Sender
from receiver import Receiver
from parser import Parser

default_settings = {
    'port': '5123',
    'mcast4': '224.0.0.224',
    'mcast6': 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173',
    'ttl': '1',
    'group': 'IPv4'
}


class App:
    def __init__(self, args):
        Parser.parse(args=' '.join(*args), default_settings=default_settings)
        for key, value in default_settings.items():
            print(key + ': ', value)

        self.uuid = uuid.uuid4()
        self.sender = Sender(
            port=int(default_settings['port']),

            mcast_group=default_settings['mcast4']
            if default_settings['group'] == 'IPv4' else default_settings['mcast6'],

            ttl=int(default_settings['ttl']),
            group=default_settings['group'],
            uuid=self.uuid
        )

        self.receiver = Receiver(
            port=int(default_settings['port']),

            mcast_group=default_settings['mcast4']
            if default_settings['group'] == 'IPv4' else default_settings['mcast6'],

            ttl=int(default_settings['ttl']),
            group=default_settings['group'],
            uuid=self.uuid
        )

    def start(self):
        self.sender.start()
        self.receiver.start()

    def close(self):
        print(123)
        self.sender.close()
        self.sender.join()
        self.receiver.close()
        self.receiver.join()
