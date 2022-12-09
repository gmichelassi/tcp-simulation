from config import BUFFER_SIZE, SERVER_PORT, SERVER_IP, COMMANDS
from config import (
    CONNECTION_REQUEST,
    REQUEST_TO_SEND
)
from config import get_logger
from errors import AlreadyConnectedError, InvalidCommandError, UnknownClientError
from socket import socket
from socket import AF_INET, SOCK_DGRAM

log = get_logger(__file__)


class Server:
    def __init__(self):
        self.udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.udp_socket.bind((SERVER_IP, SERVER_PORT))

        self.clients = []

    def run_server(self):
        log.info("UDP server up and listening")

        ip_address = None

        while True:
            try:
                decoded_message, ip_address = self.receive_message()

                response = self.handle_request(
                    message=decoded_message,
                    ip_address=ip_address
                )

                self.send_message(response, ip_address)
            except (
                AlreadyConnectedError,
                InvalidCommandError,
                UnknownClientError
            ) as error:
                if ip_address is not None:
                    self.send_message(str(error), ip_address)

    def receive_message(self):
        received_message, address = self.udp_socket.recvfrom(BUFFER_SIZE)
        decoded_message = received_message.decode()

        log.info(f"Received message '{decoded_message}' from {address}")

        return decoded_message, address

    def handle_request(self, message: str, **kwargs) -> str:
        if message not in COMMANDS:
            raise InvalidCommandError(command=message)

        ip_address: str = kwargs['ip_address']

        if message == CONNECTION_REQUEST:
            return self.establish_connection(ip_address=ip_address)

        if message == REQUEST_TO_SEND:
            return self.request_to_send(ip_address=ip_address)

    def establish_connection(self, ip_address: str) -> str:
        if ip_address in self.clients:
            raise AlreadyConnectedError(ip_address=ip_address)

        self.clients.append(ip_address)

        message = f"200: Connection between {ip_address} and server established."

        log.info(message)
        log.info(f'Connected clients: {self.clients}')

        return message

    def request_to_send(self, ip_address: str):
        if ip_address not in self.clients:
            raise UnknownClientError(ip_address=ip_address)

        message = f"200: Request from {ip_address} accepted."

        self.send_message(message, ip_address)
        log.info(message)

        return message

    def send_message(self, message: str, address: str):
        self.udp_socket.sendto(str.encode(message), address)


if __name__ == '__main__':
    server = Server()

    server.run_server()
