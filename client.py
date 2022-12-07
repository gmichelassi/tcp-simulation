from config import BUFFER_SIZE, SERVER_PORT, SERVER_IP
from socket import socket
from socket import AF_INET, SOCK_DGRAM


def run_client():
    udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)

    while True:
        message = str.encode(input('Type something: '))
        udp_socket.sendto(message, (SERVER_IP, SERVER_PORT))

        response, _ = udp_socket.recvfrom(BUFFER_SIZE)
        print(f"Server Response: {response}")


if __name__ == '__main__':
    run_client()
