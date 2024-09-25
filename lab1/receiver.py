import threading
from stoppable import StoppableThread


class Receiver(StoppableThread):
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
        self._stop_event = threading.Event()
        self.sock = self.setup_socket()
        super(Receiver, self).__init__(target=self.receive_message())

    def setup_socket(self):
        return 1

    def receive_message(self):
        pass

    def run(self):
        self.receive_message()
        while not self._stop_event.wait(self.delay):
            self.receive_message()

    # def close(self) -> None:
    #     self.stop()
