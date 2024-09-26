import threading
import uuid
import socket
from datetime import datetime, timedelta
from stoppable import StoppableThread
from socketsetupper import SocketSetupper

uids = set()
mp = dict()
timeout = 3


def map_lookup():
    time = datetime.now()
    uids_to_discard = set()
    for uid in uids:
        if time - mp[uid] > timedelta(seconds=3):
            print(uid, "died at", time.isoformat())
            uids_to_discard.add(uid)

    for uid in uids_to_discard:
        if uid in uids:
            uids.discard(uid)


class Receiver(StoppableThread, SocketSetupper):
    def __init__(self,
                 port: int = 5123,
                 mcast_group: str = '224.0.0.224',
                 ttl: int = 1,
                 group: str = 'IPv4',
                 uuid: uuid = None,
                 reusable_address_opt: bool = True,
                 loop_message_opt: bool = True,
                 delay: int = 0.1):

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
        self.sock.settimeout(self.delay)
        self._stop_event = threading.Event()
        super(Receiver, self).__init__(target=self.receive_message())

    def receive_message(self):
        try:
            data, address = self.sock.recvfrom(1024)
            uid = uuid.UUID(bytes=data)
            if uid == self.uuid:
                return

            time = datetime.now()
            if uid not in uids:
                uids.add(uid)
                print(uid, "was found by", self.uuid, 'at', time.isoformat())

            mp[uid] = time
        except socket.timeout:
            return

    def run(self):
        while not self._stop_event.wait(self.delay):
            self.receive_message()
            map_lookup()
        self.sock.close()
