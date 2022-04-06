import select
import socket
import struct
from socketserver import StreamRequestHandler, ThreadingTCPServer
from proxy.enums import Reply, AddressType, Command, Method
from proxy.utils import encrypt, decrypt
import threading
from queue import SimpleQueue

from loguru import logger

from string import digits

SOCKS_VERSION = 0x05

queue = SimpleQueue()


def start_proxy(host, port):
    server = ThreadingTCPServer((host, port), Socks5Proxy)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info(f"Listening on port: {host}:{port}")
    # wait_for_input(server.socket)
    # wait_for_input()


def wait_for_input():
    while True:
        data = input("[Input]: ")
        queue.put(data)


class Socks5Proxy(StreamRequestHandler):
    def handle(self) -> None:
        self.on_connected()

        # get version identifier and method selection from client
        version, nmethods = struct.unpack("!BB", self.receive(2))
        if version != SOCKS_VERSION or nmethods <= 0:
            self.connection.close()
            return

        # get available method selection from client
        methods = self.get_available_methods(nmethods)
        if Method.NO_AUTHENTICATION_REQUIRED not in set(methods):
            self.connection.close()
            return

        # sends a method selection message to client
        self.send(struct.pack("!BB", SOCKS_VERSION, Method.NO_AUTHENTICATION_REQUIRED))

        # the method-dependent subnegotiation has completed
        version, cmd, rsv, address_type = struct.unpack("!BBBB", self.receive(4))

        match address_type:
            case AddressType.IPv4:
                remote_address = socket.inet_ntoa(self.receive(4))
            case AddressType.IPv6:
                remote_address = socket.inet_ntop(socket.AF_INET6, self.receive(16))
            case AddressType.DOMAIN_NAME:
                domain_length = self.receive(1)[0]
                domain_name = self.receive(domain_length).decode("utf-8")
                remote_address = socket.gethostbyname(domain_name)
            case _:
                self.connection.close()
                return
        remote_port = struct.unpack("!H", self.receive(2))[0]

        match cmd:
            case Command.CONNECT:
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    remote.connect((remote_address, remote_port))
                except Exception as e:
                    print(e)
                    reply = self.generate_failed_reply(address_type, Reply.CONNECTION_REFUSED)
                    self.send(reply)
                else:
                    logger.info("Connected to {} {}".format(remote_address, remote_port))
                    bind_address, bind_port = remote.getsockname()
                    bind_address = struct.unpack("!I", socket.inet_aton("127.0.0.1"))[0]
                    reply = struct.pack(
                        "!BBBBIH",
                        SOCKS_VERSION,
                        Reply.SUCCEEDED,
                        rsv,
                        AddressType.IPv4,
                        bind_address,
                        bind_port,
                    )
                    self.send(reply)
                    # start exchange loop
                    self.exchange_loop(remote)

    def exchange_loop(self, remote):
        while True:
            # wait until client or remote is available for read
            readable, writeable, exceptional = select.select([self.connection, remote], [], [])

            # get data from client, transmit to server
            if self.connection in readable:
                data = self.connection.recv(4096)
                logger.debug(f"client: {decrypt(data, key=0x00)}")
                if remote.send(data) <= 0:
                    break

            # get data from server, transmit to client
            if remote in readable:
                data = remote.recv(4096)
                logger.debug(f"server: {decrypt(data, key=0x00)}")
                if self.connection.send(data) <= 0:
                    break

    def get_available_methods(self, nmethods: int) -> list[int]:
        return [method for method in self.receive(nmethods)]

    @staticmethod
    def generate_failed_reply(address_type, error_number):
        return struct.pack("!BBBBIH", SOCKS_VERSION, error_number, 0, address_type, 0, 0)

    def on_connected(self) -> None:
        logger.info(f"Accepting connection from {self.client_address[0]}:{self.client_address[1]}")

    def receive(self, size: int) -> bytes:
        return self.connection.recv(size)

    def send(self, data: bytes) -> None:
        self.connection.sendall(data)
