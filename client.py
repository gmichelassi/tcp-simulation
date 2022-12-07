from socket import socket
from socket import AF_INET, SOCK_DGRAM


bufferSize = 1024


def run_client():
    udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)

    while True:
        message = str.encode(input('Type something: '))
        udp_socket.sendto(message, ("127.0.0.1", 20000))

        response, _ = udp_socket.recvfrom(bufferSize)
        print(f"Server Response: {response}")


if __name__ == '__main__':
    run_client()
