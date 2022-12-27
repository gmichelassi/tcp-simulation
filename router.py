from config import ROUTER_PORT
from config import BUFFER_SIZE, SERVER_PORT, SERVER_IP
from config import get_logger
from socket import socket
from socket import AF_INET, SOCK_DGRAM
import re


log = get_logger(__file__)

SERVER_HEADER = r'.[1-5]00-#([0-9])-([0-9]).'


class Router:
    def __init__(self):
        self.udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.udp_socket.bind((SERVER_IP, ROUTER_PORT))
        self.udp_socket.connect((SERVER_IP, SERVER_PORT))

        self.clients = []
        self.authorized_clients = []

    def run_router(self):
        log.info("Router up and listening")

        while True:
            message, ip_address = self.receive_message_from_client()
            self.send_message_to_server(message)
            self.message_from_server(message)

    def receive_message_from_client(self):
        received_message, ip_address = self.udp_socket.recvfrom(BUFFER_SIZE)

        return received_message, ip_address

    def send_message_to_server(self,message):
        self.udp_socket.send(message)

    @staticmethod
    def message_from_server(message):
        return bool(re.fullmatch(SERVER_HEADER, message))


if __name__ == '__main__':
    server = Router()
    

      
        
     




      


      
        






















