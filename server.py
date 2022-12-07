from config import BUFFER_SIZE, SERVER_PORT, SERVER_IP
from socket import socket
from socket import AF_INET, SOCK_DGRAM

message = "Hello, this is a UDP server!"
encoded_message = str.encode(message)


def run_server():
    udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
    udp_socket.bind((SERVER_IP, SERVER_PORT))

    print("UDP server up and listening")

    while True:
        received_message, address = udp_socket.recvfrom(BUFFER_SIZE)

        print(f"Client's message: {received_message}")
        print(f"Client's IP Address: {address}")

        udp_socket.sendto(encoded_message, address)


if __name__ == '__main__':
    run_server()
