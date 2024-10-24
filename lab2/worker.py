import socket
import os
import time

from stoppable import StoppableThread
from timer import TimeCounterThread

PACKET_SIZE = 8192 * 4


class Worker(StoppableThread):
    def __init__(self,
                 sock: socket.socket = None,
                 host: str = '0.0.0.0',
                 port: str = '5123',
                 path: str = './uploads',
                 delay: int = 0.0001
                 ):
        super().__init__()
        self.socket = sock
        self.host = host
        self.port = port
        self.path = path
        self.delay = delay
        self.is_last_received = False
        self.file_size = 0
        self.file_name = None
        self.file_path = ''
        self.fd = None
        self.bytes_read = 0
        self.timer = None

    def init_fd(self):
        self.file_path = os.path.join(self.path, self.file_name)
        self.fd = open(self.file_path, "wb")

    def close_fd(self):
        print(f'file_size = {self.file_size}\nbytes received = {self.bytes_read}')
        self.fd.close()

    def send_message(self):
        try:
            byte_to_send = b'\x00'
            if self.file_size == self.bytes_read:
                byte_to_send = b'\x01'
            self.socket.send(byte_to_send)
            return
        except socket.timeout:
            ########
            return

    def receive_message(self):
        try:
            data = self.socket.recv(PACKET_SIZE)
            if not data:
                self.close()
                return

            is_last = int(data[0])
            length = int.from_bytes(data[1:5], "big")
            message = data[5:5 + length]
            # print(data[0:5])
            # print(is_last)

            self.fd.write(message)
            self.bytes_read += length
            # print(length)
            # print(data)
            self.timer.update(time.time_ns(), length)
            if is_last:
                self.is_last_received = True
                # self.close()

        except socket.timeout:
            #################
            return

    def receive_info(self):
        try:
            size_info = self.socket.recv(4)
            info_size_decoded = int.from_bytes(size_info[0:4], "big")
            print(f'info message size = {info_size_decoded}')

            data = self.socket.recv(info_size_decoded)
            if not data:
                self.close()
                return

            packet_size = int.from_bytes(data[0:4], "big")
            self.file_size = int.from_bytes(data[4:12], "big")
            self.file_name = data[12:packet_size].decode()
        except socket.timeout:
            ####################
            self.close()
            ####################
            return

    def run(self) -> None:
        self.receive_info()

        if self.is_stopped:
            self.socket.close()
            return

        self.timer = TimeCounterThread(3, file_size=self.file_size)
        self.timer.start()
        self.timer.update(time.time_ns(), 0)

        self.init_fd()

        # i = 0
        while not self.is_last_received and not self._stop_event.wait(self.delay):
            # print(i)
            self.receive_message()
            # i += 1
        # print(123123123)
        self.timer.close()

        if self.is_stopped:
            self.close_fd()
            self.socket.close()
            return

        self.send_message()

        self.close_fd()
        self.socket.close()
        #################################
        self.close()
