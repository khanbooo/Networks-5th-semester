import socket
import struct
import platform


class SocketSetupper:
    def __init__(self,
                 port: int = 5123,
                 mcast_group: str = '224.0.0.224',
                 ttl: int = 1,
                 group: str = 'IPv4',
                 reusable_address_opt: bool = True,
                 loop_message_opt: bool = True,
                 delay: int = 0.1):

        self.port = port
        self.mcast_group = mcast_group
        self.ttl = ttl
        self.group = group
        self.reusable_address_opt = reusable_address_opt
        self.loop_message_opt = loop_message_opt
        self.delay = delay
        self.info = socket.getaddrinfo(self.mcast_group, None)[0]
        self.sock = self.setup_socket()

    def setup_socket(self):
        sock = socket.socket(family=self.info[0], type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)

        sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            self.reusable_address_opt
        )

        sock.setsockopt(
            socket.IPPROTO_IP if self.is_ipv4 else socket.IPPROTO_IPV6,
            socket.IP_MULTICAST_LOOP if self.is_ipv4 else socket.IPV6_MULTICAST_LOOP,
            self.loop_message_opt
        )

        sock.setsockopt(
            socket.IPPROTO_IP if self.is_ipv4 else socket.IPPROTO_IPV6,
            socket.IP_MULTICAST_TTL if self.is_ipv4 else socket.IPV6_MULTICAST_HOPS,
            struct.pack('@i', self.ttl)
        )

        group_bin = socket.inet_pton(self.info[0], self.info[4][0])
        sock.setsockopt(
            socket.IPPROTO_IP if self.is_ipv4 else socket.IPPROTO_IPV6,
            socket.IP_ADD_MEMBERSHIP if self.is_ipv4 else socket.IPV6_JOIN_GROUP,
            group_bin + struct.pack('=I', socket.INADDR_ANY) if self.is_ipv4 else
            group_bin + struct.pack('@I', 0)
        )

        if platform.system() == "Windows":
            if self.group == 'IPv4':
                any_addr = '0.0.0.0'
            else:
                any_addr = '0:0:0:0:0:0:0:0'
            sock.bind((any_addr, self.port))
        else:
            sock.bind((self.mcast_group, self.port))

        return sock

    @property
    def is_ipv4(self):
        return self.group == "IPv4"
