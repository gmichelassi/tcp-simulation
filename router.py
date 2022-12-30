from config import BUFFER_SIZE, SERVER_PORT, LOCALHOST, ROUTER_PORT
from config import get_logger
from socket import socket
from socket import AF_INET, SOCK_DGRAM
from threading import Thread

import argparse
import re
import time


log = get_logger(__file__)

SERVER_HEADER = r'.*[1-5]00-(#)?([0-9])*-([0-9])*.*'


class Router:
    def __init__(self, queue_max_size: int, simulate_message_processing_delay: bool, message_processing_delay: int):
        self.udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.udp_socket.bind((LOCALHOST, ROUTER_PORT))

        self.message_queue = []

        self.queue_max_size = queue_max_size
        self.simulate_message_processing_delay = simulate_message_processing_delay
        self.message_processing_delay = message_processing_delay

    def run_router(self):
        log.info("Router up and listening")

        listen_thread = Thread(target=self.listen)
        forward_thread = Thread(target=self.forward)

        listen_thread.start()
        forward_thread.start()

        listen_thread.join()
        forward_thread.join()

    def listen(self):
        while True:
            received_data = self.receive_message()

            if received_data is None:
                continue

    def forward(self):
        while True:
            if len(self.message_queue) == 0:
                continue

            if self.simulate_message_processing_delay:
                time.sleep(self.message_processing_delay)

            current_message = self.message_queue[0]

            if self.message_from_server(current_message.decode()):
                address = self.get_address_from_message(current_message)
            else:
                address = (LOCALHOST, SERVER_PORT)

            self.send_message(current_message, address)

    def receive_message(self) -> tuple[bytes, tuple[str, int]] | None:
        received_message, ip_address = self.udp_socket.recvfrom(BUFFER_SIZE)

        if len(self.message_queue) == self.queue_max_size:
            log.debug('Queue full. Ignoring message.')
            return None

        self.message_queue.append(received_message)

        log.debug(received_message.decode())
        log.debug(f'Queue size: {len(self.message_queue)}')

        return received_message, ip_address

    def send_message(self, message: bytes, address: tuple[str, int]):
        self.message_queue.pop(0)

        log.debug(f'Message from server? {self.message_from_server(message.decode())}')
        log.debug(f'Forwarding {message.decode()}')
        log.debug(f'Queue size: {len(self.message_queue)}')

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
    parser = argparse.ArgumentParser(description='Router Simulation')

    parser.add_argument('-s', '--simulatedelay', help='simulate delay when forward message (boolean)', default=False, type=bool)
    parser.add_argument('-d', '--delay', help='the delay to forward message (int)', default=1, type=int)
    parser.add_argument('-q', '--queuemaxsize', help='the maximum size of the router queue (int)', default=5, type=int)

    args = parser.parse_args()

    queue_max_size, simulate_message_processing_delay, message_processing_delay = \
        args.queuemaxsize, args.simulatedelay, args.delay

    router = Router(
        queue_max_size=queue_max_size,
        simulate_message_processing_delay=simulate_message_processing_delay,
        message_processing_delay=message_processing_delay
    )

    router.run_router()
