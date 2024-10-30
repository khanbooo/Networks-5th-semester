import socket
import ntpath
import os

from stoppable import StoppableThread

PACKET_SIZE = 8192 * 4


class Client(StoppableThread):
    def __init__(self,
                 default_settings,
                 delay: float = 0.0001,
                 timeout: int = 2):
        super().__init__()
        self.default_settings       = default_settings
        self.is_connected           = False
        self.is_completed           = False
        self.port                   = int(default_settings['port'])
        self.hostname               = default_settings['hostname'] if self.is_host_name_given else default_settings['ip']
        self.path                   = default_settings['path']
        self.file_name              = ntpath.basename(default_settings['path'])
        self.file_size              = os.path.getsize(self.path)
        self.bytes_left             = os.path.getsize(self.path)
        self.fd                     = None
        self.socket                 = None
        self.delay                  = delay
        self.timeout                = timeout

    def __setup_socket(self):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP
        )
        self.socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            True
        )
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.settimeout(self.timeout)

    def connect(self):
        if not self.is_connected:
            try:
                print(self.hostname, self.port)
                self.socket.connect((self.hostname, self.port))
                self.is_connected = True
            except ConnectionError as err:
                raise err

    def send_info(self):
        try:
            size = (int(self.file_size)).to_bytes(8, "big", signed=True)
            name = bytes(self.file_name.encode('utf-8'))
            packet_size = (int(len(size) + len(name) + 4)).to_bytes(4, "big", signed=True)
            data = packet_size + size + name

            size_info = (int(len(data))).to_bytes(4, "big", signed=True)
            self.socket.send(size_info)

            self.socket.send(data)
        except socket.timeout:

            self.close()
            return

    def send_message(self):
        try:
            useful_data_size = PACKET_SIZE - 5
            flag_byte = b'\x00'
            if self.bytes_left <= useful_data_size:
                useful_data_size = self.bytes_left
                flag_byte = b'\x01'

            current_length = useful_data_size.to_bytes(4, byteorder='big', signed=False)
            try:
                read_data = self.fd.read(useful_data_size)
            except ValueError:
                return
            data = flag_byte + current_length + read_data
            self.bytes_left -= len(read_data)
            self.socket.send(data)
            if flag_byte == b'\x01':
                self.is_completed = True
        except socket.timeout:
            self.close()
            return

    def receive_message(self):
        try:
            data = self.socket.recv(1)
            if int(data[0]) == 1:
                print("File transmitted successfully")
            else:
                print("File transmission failed")
        except socket.timeout:
            print("Did not receive ack byte. File transmission failed")
            return

    def run(self):
        self.__setup_socket()
        self.connect()
        self.send_info()

        if self.is_stopped:
            return

        self.fd = open(self.path, "rb")
        while not self.is_completed and not self._stop_event.wait(self.delay):
            self.send_message()

        self.fd.close()

        if self.is_stopped:
            return

        self.receive_message()

        self.close()

    @property
    def is_ipv4(self):
        return self.default_settings['group'] == "IPv4"

    @property
    def is_host_name_given(self):
        return self.default_settings['hostname'] != ''
