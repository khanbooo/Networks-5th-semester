import sys
import socket
from os import path, makedirs

from time import sleep
from acceptor import Acceptor
from parser import Parser
from stoppable import StoppableThread


default_settings = {
    'port': '5123',
    'ip': '0.0.0.0',
    'path': './uploads',
    'hostname': '',
    'max_clients': '5'
}


class ServerApp(StoppableThread):
    def __init__(self, args):
        super().__init__()
        Parser.parse(args=' '.join(*args), default_settings=default_settings)
        for key, value in default_settings.items():
            print(key + ': ', value)

        print(socket.gethostname())
        self.port           = default_settings['port']
        self.ip             = default_settings['ip']
        self.path           = default_settings['path']
        self.max_clients    = int(default_settings['max_clients'])
        self.acceptor       = None

    def __create_directory(self):
        files_dir = path.join(path.curdir, self.path)
        makedirs(files_dir, exist_ok=True)

    def close_acceptor(self):
        self.acceptor.close()
        self.acceptor.join()

    def run(self):
        self.__create_directory()

        self.acceptor = Acceptor(self.port,
                                 self.ip,
                                 self.path,
                                 self.max_clients
                                 )

        self.acceptor.start()

        while not self.is_stopped:
            sleep(0.5)

        self.close_acceptor()


def main(*args):

    server_app = ServerApp(args=args)

    try:
        server_app.start()
        while True:
            sleep(0.5)
    except KeyboardInterrupt:
        print("interrupted")
        server_app.close()
        server_app.join()
        sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
