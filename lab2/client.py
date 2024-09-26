import sys
import ntpath
import threading

from time import sleep
from sender import Sender
from parser import Parser


default_settings = {
    'port': '5123',
    'IPv4': '224.0.0.224',
    'IPv6': 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173',
    'path': './client.py',
    'hostname': ''
}


class Client:
    def __init__(self):
        # self.uuid = uuid.uuid4()
        self.sender = Sender(port=int(default_settings['port']),
                             # uuid=self.uuid,
                             hostname=default_settings['hostname'] if self.is_host_name_given
                             else default_settings[default_settings['group']],
                             path=default_settings['path'],
                             file_name=ntpath.basename(default_settings['path'])
                             )

    def receive_answer(self):
        data, address = self.sender.sock.recv(1024)
        if data[0] == 1:
            print("File transmitted successfully")
        print("File transmitted successfully")

    def run(self):
        try:
            self.sender.connect()
            t1 = threading.Thread(target=self.receive_answer())
            self.sender.send_info()
            t1.join()
        except ConnectionError:
            raise ConnectionError

    def start(self):
        self.run()

    @property
    def is_ipv4(self):
        return default_settings['group'] == "IPv4"

    @property
    def is_host_name_given(self):
        return default_settings['hostname'] != ''


def main(*args):
    Parser.parse(args=' '.join(*args), default_settings=default_settings)
    for key, value in default_settings.items():
        print(key + ': ', value)

    client = Client()
    client.start()


if __name__ == '__main__':
    main(sys.argv)
