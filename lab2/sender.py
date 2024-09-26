import socket
import uuid
import struct
import os
import platform

from stoppable import StoppableThread


class Sender(StoppableThread):
    def __init__(self,
                 port: int = 5123,
                 # uuid: uuid = None,
                 hostname: str = '',
                 path: str = './client',
                 file_name: str = 'client',
                 timeout: int = 2):

        self.port = port
        # self.uuid = uuid
        self.hostname = hostname
        self.path = path
        self.file_size = os.path.getsize(self.path)
        self.file_name = file_name
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.is_connected = False
        super(Sender, self).__init__()

    def connect(self):
        if not self.is_connected:
            try:
                self.sock.connect((self.hostname, self.port))
                self.is_connected = True
            except ConnectionError as err:
                raise err

    def send_message(self):
        self.sock.sendto(self.uuid.bytes, (self.mcast_group, self.port))

    def send_info(self):
        data = bytes(0)
        self.sock.sendto(data, (self.hostname, self.port))
