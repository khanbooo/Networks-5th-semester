import socket
import ntpath

from stoppable import StoppableThread
from worker import Worker


class Acceptor(StoppableThread):
    def __init__(self,
                 port: str = '5123',
                 host: str = '0.0.0.0',
                 path: str = "./uploads",
                 max_clients: int = 5,
                 delay: float = 0.0001,
                 timeout: int = 2
                 ):
        super().__init__()
        self.port = int(port)
        self.host = host
        self.path = path
        self.workers = []
        self.max_clients = max_clients
        self.delay = delay
        self.timeout = timeout
        self.socket = None

    def __setup_socket(self):
        data = socket.getaddrinfo(self.host, None)[0]
        socket_family = data[0]
        self.socket = socket.socket(
            family=socket_family,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )
        self.socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            True
        )
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.settimeout(self.timeout)

    def __join_all(self):
        for worker in self.workers:
            worker.close()
            worker.join()

    def accept(self):
        try:
            connection = self.socket.accept()
            cl_host, cl_port = connection[1]
            self.workers.append(Worker(connection[0], cl_host, cl_port, self.path))
            self.workers[-1].start()
            print(" connection accepted.\n client hostname:", cl_host, "\n client port:", cl_port)
        except socket.timeout:
            return

    def run(self) -> None:
        self.__setup_socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.max_clients)

        while not self._stop_event.wait(self.delay):
            print("waiting for connections...")
            self.accept()
        self.__join_all()
