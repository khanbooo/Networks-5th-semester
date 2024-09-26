import threading
import socket
import uuid
from stoppable import StoppableThread
from socketsetupper import SocketSetupper


class Sender(StoppableThread, SocketSetupper):
    def __init__(self,
                 port: int = 5123,
                 mcast_group: str = '224.0.0.224',
                 ttl: int = 1,
                 group: str = 'IPv4',
                 uuid: uuid = None,
                 reusable_address_opt: bool = True,
                 loop_message_opt: bool = True,
                 delay: int = 2):

        self.port = port
        self.mcast_group = mcast_group
        self.ttl = ttl
        self.group = group
        self.uuid = uuid
        self.reusable_address_opt = reusable_address_opt
        self.loop_message_opt = loop_message_opt
        self.delay = delay
        self.info = socket.getaddrinfo(self.mcast_group, None)[0]
        self.sock = self.setup_socket()
        self._stop_event = threading.Event()
        super(Sender, self).__init__(target=self.send_message())

    def send_message(self):
        self.sock.sendto(self.uuid.bytes, (self.mcast_group, self.port))

    def run(self):
        while not self._stop_event.wait(self.delay):
            self.send_message()
        self.sock.close()
