import sys

from time import sleep
from parser import Parser
from client import Client

default_settings = {
    'port': '5123',
    'ip': '0.0.0.0',
    'path': './input.txt',
    'hostname': ''
}


class ClientApp:
    def __init__(self, args):
        Parser.parse(args=' '.join(*args), default_settings=default_settings)
        for key, value in default_settings.items():
            print(key + ': ', value)
        self.client = Client(default_settings)

    def join(self):
        self.client.join()

    def start(self):
        self.client.start()

    def close(self):
        self.client.close()

    @property
    def is_closed(self):
        return self.client.is_stopped


def main(*args):
    client_app = ClientApp(args=args)

    try:
        client_app.start()
        while not client_app.is_closed:
            sleep(0.5)
    except KeyboardInterrupt:
        print("interrupted")
        client_app.close()
        sys.exit(0)
    client_app.join()
    sys.exit(0)


if __name__ == '__main__':
    print("bruh")
    main(sys.argv)
