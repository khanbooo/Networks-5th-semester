import threading
from stoppable import StoppableThread


class Sender(StoppableThread):
    def __init__(self,
                 port: int = 5123,
                 mcast_group: str = '224.0.0.224',
                 ttl: int = 1,
                 group: str = 'IPv4',
                 delay: int = 0.5):
        self.port = port
        self.mcast_group = mcast_group
        self.ttl = ttl
        self.group = group
        self.delay = delay
        self.sock = self.setup_socket()
        self._stop_event = threading.Event()
        super(Sender, self).__init__(target=self.send_message())

    def setup_socket(self):
        return 1

    def send_message(self):
        # pass
        print(self._stop_event.is_set())
            # addr_info = socket.getaddrinfo(group, None)[0]
            # sock = socket.socket(addr_info[0], SOCK_DGRAM)

    def run(self):
        while not self._stop_event.wait(self.delay):
            self.send_message()

    # def close(self) -> None:
    #     # self.send_packet(
    #     #     Packet(
    #     #         program_uuid=self.uuid,
    #     #         secret=self.secret,
    #     #         alive=False
    #     #     )
    #     # )
    #     self.stop()
    #     # pass