from socket import socket
from socket import AF_INET, SOCK_DGRAM

local_ip = '127.0.0.1'
server_port = 20000
buffer_size = 1024
message = "Hello, this is a UDP server!"
encoded_message = str.encode(message)


def run_server():
    udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
    udp_socket.bind((local_ip, server_port))

    print("UDP server up and listening")

    while True:
        received_message, address = udp_socket.recvfrom(buffer_size)

        print(f"Client's message: {received_message}")
        print(f"Client's IP Address: {address}")

        udp_socket.sendto(encoded_message, address)


if __name__ == '__main__':
    run_server()
