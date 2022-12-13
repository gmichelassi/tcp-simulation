import re

from config import BUFFER_SIZE, COMMANDS, SERVER_PORT, SERVER_IP
from config import SEND_FILE
from config import get_logger
from socket import socket
from socket import AF_INET, SOCK_DGRAM
from random import randint
from tqdm import tqdm

log = get_logger(__file__)

server_response = '[Server response]'
success_response_regex = r"200:*"


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

            if self.send_file_command(command) and self.success_response(response):
                print('INICIAR PROCESSO DE ENVIAR ARQUIVO')
                filename = './files/lorem_ipsum_4096.txt'

                progress = tqdm(range(4096), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

                with open(filename, 'rb') as file:
                    while True:
                        bytes_read = file.read(BUFFER_SIZE)

                        if not bytes_read:
                            break

                        self.udp_socket.sendall(bytes_read)

                        progress.update(len(bytes_read))

    def handle_command_input(self) -> str:
        log.info(f'Available commands: {COMMANDS}')
        command = input('Server command: ')

        self.send_command(command)

        return command

    def receive_response(self) -> str:
        response, _ = self.udp_socket.recvfrom(BUFFER_SIZE)

        log.info(f'{server_response} {response.decode()}')

        return response.decode()

    def send_command(self, command: str):
        self.udp_socket.send(str.encode(command))

    @staticmethod
    def success_response(response: str) -> bool:
        return bool(re.match(success_response_regex, response))

    @staticmethod
    def send_file_command(command: str):
        return command == SEND_FILE


if __name__ == '__main__':
    client = Client()

    client.run_client()
