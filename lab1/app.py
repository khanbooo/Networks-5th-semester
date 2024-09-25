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
    def __init__(self, args: list):
        Parser.parse(args=' '.join(*args), default_settings=default_settings)
        for key, value in default_settings.items():
            print(key + ': ', value)

        self.sender = Sender(
            port=int(default_settings['port']),

            mcast_group=default_settings['mcast4']
            if default_settings['group'] == 'IPv4' else default_settings['mcast6'],

            ttl=int(default_settings['ttl']),
            group=default_settings['group']
        )

        self.receiver = Receiver(
            port=int(default_settings['port']),

            mcast_group=default_settings['mcast4']
            if default_settings['group'] == 'IPv4' else default_settings['mcast6'],

            ttl=int(default_settings['ttl']),
            group=default_settings['group']
        )

    def start(self):
        self.sender.start()
        self.receiver.start()

    def close(self):
        self.sender.close()
        self.sender.join()
        self.receiver.close()
        self.receiver.join()

    @staticmethod
    def __parse(args=None):

        for key, value in default_settings.items():
            print(f'{key}: {value}')
