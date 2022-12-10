from config import BUFFER_SIZE, SERVER_PORT, SERVER_IP, COMMANDS
from config import (
    CONNECTION_FINISHED,
    CONNECTION_REQUEST,
    REQUEST_TO_SEND,
    SEND_FILE
)
from config import get_logger
from errors import (
    AlreadyConnectedError,
    InvalidCommandError,
    UnauthorizedClientError,
    UnknownClientError,
)
from socket import socket
from socket import AF_INET, SOCK_DGRAM

log = get_logger(__file__)


class Server:
    def __init__(self):
        self.udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.udp_socket.bind((SERVER_IP, SERVER_PORT))

        self.clients = []
        self.authorized_clients = []

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
                UnknownClientError,
                UnauthorizedClientError,
                NotImplementedError
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

        ip_address: tuple[str, int] = kwargs['ip_address']

        if message == CONNECTION_REQUEST:
            return self.establish_connection(ip_address=ip_address)

        if message == CONNECTION_FINISHED:
            return self.finish_connection(ip_address=ip_address)

        if message == REQUEST_TO_SEND:
            return self.request_to_send(ip_address=ip_address)

        if message == SEND_FILE:
            return self.receive_file(ip_address=ip_address)

    def establish_connection(self, ip_address: tuple[str, int]) -> str:
        if ip_address in self.clients:
            raise AlreadyConnectedError(ip_address=ip_address)

        self.clients.append(ip_address)

        message = f"200: Connection between {ip_address} and server established."

        log.info(message)
        log.info(f'Connected clients: {self.clients}')

        return message

    def finish_connection(self, ip_address: tuple[str, int]) -> str:
        if ip_address not in self.clients:
            raise UnknownClientError(ip_address=ip_address)

        self.clients.remove(ip_address)

        message = f"200: Connection between {ip_address} and server finished."

        log.info(message)
        log.info(f'Connected clients: {self.clients}')

        return message

    def request_to_send(self, ip_address: tuple[str, int]):
        if ip_address not in self.clients:
            raise UnknownClientError(ip_address=ip_address)

        self.authorized_clients.append(ip_address)

        message = f"200: Request from {ip_address} accepted."

        log.info(message)
        log.info(f'Authorized clients: {self.clients}')

        return message

    def receive_file(self, ip_address: tuple[str, int]):
        if ip_address not in self.authorized_clients:
            raise UnauthorizedClientError(ip_address=ip_address)

        raise NotImplementedError('Function yet to be implemented')

    def send_message(self, message: str, ip_address: tuple[str, int]):
        self.udp_socket.sendto(str.encode(message), ip_address)


if __name__ == '__main__':
    server = Server()

    server.run_server()
