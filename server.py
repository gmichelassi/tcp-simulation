from config import BUFFER_SIZE, SERVER_PORT, SERVER_IP, COMMANDS
from config import (
    CONNECTION_REQUEST
)
from errors import AlreadyConnectedError, InvalidCommandError, UnknownClientError
from socket import socket
from socket import AF_INET, SOCK_DGRAM


class Server:
    def __init__(self):
        self.udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.udp_socket.bind((SERVER_IP, SERVER_PORT))

        self.clients = []

    def run_server(self):
        print("UDP server up and listening")

        while True:
            received_message, address = self.udp_socket.recvfrom(BUFFER_SIZE)
            ip_address = f'{address[0]}:{address[1]}'

            try:
                response = self.handle_request(
                    message=received_message.decode(),
                    ip_address=ip_address
                )

                self.send_message(response, address)
            except (
                    AlreadyConnectedError,
                    InvalidCommandError,
                    UnknownClientError
            ) as error:
                self.send_message(str(error), address)

    def establish_connection(self, ip_address: str) -> str:
        if ip_address in self.clients:
            raise AlreadyConnectedError(ip_address=ip_address)

        self.clients.append(ip_address)

        return f"200: Connection between {ip_address} and server established."

    def handle_request(self, message: str, **kwargs) -> str:
        if message not in COMMANDS:
            raise InvalidCommandError(command=message)

        ip_address: str = kwargs['ip_address']

        if message == CONNECTION_REQUEST:
            return self.establish_connection(ip_address=ip_address)

        if ip_address not in self.clients:
            raise UnknownClientError(ip_address=ip_address)

    def send_message(self, message: str, address: str):
        self.udp_socket.sendto(str.encode(message), address)


if __name__ == '__main__':
    server = Server()

    server.run_server()
