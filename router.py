from config import BUFFER_SIZE, SERVER_PORT, LOCALHOST, ROUTER_PORT
from config import get_logger
from socket import socket
from socket import AF_INET, SOCK_DGRAM
import re


log = get_logger(__file__)

SERVER_HEADER = r'.*[1-5]00-(#)?([0-9])-([0-9]).*'


class Router:
    def __init__(self):
        self.udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.udp_socket.bind((LOCALHOST, ROUTER_PORT))

    def run_router(self):
        log.info("Router up and listening")

        while True:
            message, ip_address = self.receive_message()

            log.debug(message.decode())
            log.debug('Message from server?', self.message_from_server(message.decode()))

            if self.message_from_server(message.decode()):
                address = self.get_address_from_message(message)
            else:
                address = (LOCALHOST, SERVER_PORT)

            self.send_message(message, address)

    def receive_message(self) -> tuple[bytes, tuple[str, int]]:
        received_message, ip_address = self.udp_socket.recvfrom(BUFFER_SIZE)

        return received_message, ip_address

    def send_message(self, message: bytes, address: tuple[str, int]):
        self.udp_socket.sendto(message, address)

    @staticmethod
    def get_address_from_message(message: bytes):
        header, _ = message.decode().split(": ")
        _, _, _, _, client_ip_address, _ = header[1:-1].split("-")
        client_address, client_port = client_ip_address[1:-1].split(',')

        return client_address[1:-1], int(client_port)

    @staticmethod
    def message_from_server(message: str):
        return bool(re.fullmatch(SERVER_HEADER, message))


if __name__ == '__main__':
    router = Router()

    router.run_router()
