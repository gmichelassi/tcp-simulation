from config import BUFFER_SIZE, COMMANDS, SERVER_PORT, SERVER_IP
from config import get_logger
from socket import socket
from socket import AF_INET, SOCK_DGRAM
from random import randint

log = get_logger(__file__)

server_response = '[Server response]'


class Client:
    def __init__(self):
        self.udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.udp_socket.connect((SERVER_IP, SERVER_PORT))

        self.id = f'#{randint(0, 10000)}'

        log.info(f'Client {self.id} communicating with server {SERVER_IP}:{SERVER_PORT}')

    def run_client(self):
        while True:
            command = self.handle_command_input()
            response = self.receive_response()

    def handle_command_input(self):
        log.info(f'Available commands: {COMMANDS}')
        command = input('Server command: ')

        self.udp_socket.send(str.encode(command))

        return command

    def receive_response(self):
        response, _ = self.udp_socket.recvfrom(BUFFER_SIZE)

        log.info(f'{server_response} {response.decode()}')

        return response


if __name__ == '__main__':
    client = Client()

    client.run_client()
