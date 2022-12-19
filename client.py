from config import BUFFER_SIZE, COMMANDS, SERVER_PORT, SERVER_IP, MAX_TRIES
from config import FILES
from config import SEND_FILE
from config import get_logger
from errors import NoResponseError
from socket import socket
from socket import AF_INET, SOCK_DGRAM
from random import randint
from util import checksum, verify_checksum

log = get_logger(__file__)

server_response = '[Server response]'


class Client:
    def __init__(self):
        self.udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.udp_socket.connect((SERVER_IP, SERVER_PORT))

        self.id = f'#{randint(0, 10000)}'
        self.message_id = 0

        log.info(f'Client {self.id} communicating with server {SERVER_IP}:{SERVER_PORT}')

    def run_client(self):
        while True:
            try:
                message = self.get_user_input()
                self.send_message_and_wait_for_response(message)
            except NoResponseError as error:
                log.error(str(error))
                continue

    @staticmethod
    def get_user_input() -> str:
        log.info(f'\nAvailable commands: {COMMANDS}')
        command = input('Input your command: ')

        return command

    def send_message_and_wait_for_response(self, message: str):
        self.message_id += 1

        if message == SEND_FILE:
            return self.send_file()

        return self.send_message(message)

    def send_file(self):
        filename, size = self.get_file()
        total_packets = size / (BUFFER_SIZE / 2)

        log.info(f'Sending {filename} ({total_packets} packets).')

        with open(filename, 'rb') as file:
            current_packet = 1
            while current_packet <= total_packets:
                bytes_read: bytes = file.read(int(BUFFER_SIZE / 2))

                if not bytes_read:
                    break

                text_read = bytes_read.decode()
                message_info = f'[{filename};{current_packet};{total_packets}]'
                header = self.make_request_header(text_read, message_type='file', message_info=message_info)
                formatted_message = self.build_message(header, text_read)

                self.udp_socket.sendall(formatted_message.encode())
                self.receive_response(formatted_message)
                current_packet += 1

            file.close()
            return

    @staticmethod
    def get_file():
        selected_file = FILES[randint(0, len(FILES) - 1)]

        return selected_file['name'], selected_file['size']

    def send_message(
        self,
        message: str,
        message_type: str = 'command',
        message_info: str = '{}'
    ):
        header = self.make_request_header(message, message_type, message_info)
        formatted_message = self.build_message(header, message)
        self.udp_socket.send(str.encode(formatted_message))

        return self.receive_response(message)

    def make_request_header(
        self,
        message: str,
        message_type: str = 'command',
        message_info: str = '{}'
    ) -> str:
        return f'{self.id}-{self.message_id}-{message_type}-{message_info}-{checksum(message)}'

    @staticmethod
    def build_message(header: str, message: str):
        return f'[{header}]: {message}'

    def receive_response(self, message: str, current_try: int = 0) -> str:
        response, _ = self.udp_socket.recvfrom(BUFFER_SIZE)

        if current_try >= 1:
            log.info(f"Re-try '{message}': #{current_try}")

        if current_try == MAX_TRIES:
            raise NoResponseError()

        header, command = response.decode().split(": ")
        status_code, client_id, message_id, response_checksum = header.split("-")

        verify_checksum(
            message=command, message_checksum=int(response_checksum[:-1]), ip_address=(SERVER_IP, SERVER_PORT)
        )

        if command == 'Packet lost.':
            log.warning('No response from server... trying again')
            self.udp_socket.send(str.encode(message))
            self.receive_response(message, current_try + 1)

        log.info(f'{server_response} {status_code[1:]} - {command}')

        return response.decode()


if __name__ == '__main__':
    client = Client()

    client.run_client()
