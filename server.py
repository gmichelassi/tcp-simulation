from config import (
    BUFFER_SIZE,
    COMMANDS,
    CONNECTION_FINISHED,
    CONNECTION_REQUEST,
    REQUEST_TO_SEND,
    SERVER_IP,
    SERVER_PORT,
    get_logger
)
from errors import (
    AlreadyConnectedError,
    InvalidCommandError,
    MessageCorruptedError,
    PacketLostError,
    UnauthorizedClientError,
    UnknownClientError,
    RcvBufferCapacityError,
    MessageDuplicatedError
)
from random import randint
from socket import (
    AF_INET,
    SOCK_DGRAM,
    socket,
    SOL_SOCKET,
    SO_RCVBUF
)
from util import checksum, verify_checksum
import sys


log = get_logger(__file__)


class Server:
    def __init__(self):
        self.udp_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.udp_socket.bind((SERVER_IP, SERVER_PORT))

        self.clients = []
        self.authorized_clients = []

        self.simulate_packet_loss = False
        self.packet_loss_probabilty = 1

        self.last_message_id = None
        self.last_client_id = None

        self.simulate_overflow_buffer = False
        
        if self.simulate_overflow_buffer:
            self.udp_socket.setsockopt(SOL_SOCKET, SO_RCVBUF, 24)
            self.buffer_capacity = self.udp_socket.getsockopt(SOL_SOCKET, SO_RCVBUF)
        else:
            self.buffer_capacity = self.udp_socket.getsockopt(SOL_SOCKET, SO_RCVBUF)

    def run_server(self):
        log.info("UDP server up and listening")

        while True:
            self.listen()

    def listen(self):
        header = None
        ip_address = None
        response = None

        try:
            client_id, message_id, message_type, message_info, message, router_address, client_ip_address = \
                self.receive_message()

            ip_address = router_address

            response, status_code = self.handle_request(
                client_id=client_id,
                message_id=message_id,
                message_type=message_type,
                message_info=message_info,
                message=message,
                ip_address=client_ip_address,
            )

            header = self.make_response_header(
                status_code=status_code,
                message=response,
                client_id=client_id,
                message_id=message_id,
                rcv_buffer_capacity=self.buffer_capacity,
                client_ip_address=client_ip_address
            )
        except (
            AlreadyConnectedError,
            InvalidCommandError,
            MessageCorruptedError,
            PacketLostError,
            UnauthorizedClientError,
            UnknownClientError,
            RcvBufferCapacityError,
            MessageDuplicatedError
        ) as error:
            response = error.message
            ip_address = error.ip_address
            status_code = error.status_code

            header = self.make_response_header(status_code=status_code, message=response)

            str(error)
        finally:
            if ip_address is not None:
                self.send_message(header=header, message=response, ip_address=ip_address)

    def receive_message(self):
        received_message, router_address = self.udp_socket.recvfrom(BUFFER_SIZE)

        decoded_message = received_message.decode()

        header, command = decoded_message.split(": ")
     
        client_id, message_id, message_type, message_info, client_ip_address, message_checksum = header[1:-1].split("-")

        client_address, client_port = client_ip_address[1:-1].split(',')

        client_ip_address = (client_address[1:-1], int(client_port))

        if self.simulate_packet_loss and randint(0, 100) <= self.packet_loss_probabilty * 100:
            raise PacketLostError(ip_address=client_ip_address)

        verify_checksum(message=command, message_checksum=int(message_checksum), ip_address=client_ip_address)
      
        if self.simulate_overflow_buffer and self.buffer_capacity < sys.getsizeof(command):
            raise RcvBufferCapacityError(ip_address=client_ip_address)

        if message_id == self.last_message_id and client_id == self.last_client_id:
            log.warning("Duplicated message received... discarding")

            raise MessageDuplicatedError(ip_address=client_ip_address)
        else:
            self.last_message_id = message_id
            self.last_client_id = client_id
            log.info(
                f"Received message '{decoded_message}' from {client_ip_address} with checksum {message_checksum}"
            )

        return client_id, message_id, message_type, message_info, command, router_address, client_ip_address

    def handle_request(
        self,
        message_type,
        message_info,
        message,
        ip_address,
        **kwargs
    ) -> tuple[str, int]:
        if message_type == 'command' and message not in COMMANDS:
            raise InvalidCommandError(command=message, ip_address=ip_address)

        if message == CONNECTION_REQUEST:
            return self.establish_connection(ip_address=ip_address)

        if message == CONNECTION_FINISHED:
            return self.finish_connection(ip_address=ip_address)

        if message == REQUEST_TO_SEND:
            return self.request_to_send(ip_address=ip_address)

        if message_type == 'file':
            return self.receive_file(ip_address=ip_address, message=message, message_info=message_info)

    def establish_connection(self, ip_address: tuple[str, int]) -> tuple[str, int]:
        if ip_address in self.clients:
            raise AlreadyConnectedError(ip_address=ip_address)

        self.clients.append(ip_address)

        message = f"Connection between {ip_address} and server established."

        log.info(message)
        log.info(f'Connected clients: {self.clients}')

        return message, 200

    def finish_connection(self, ip_address: tuple[str, int]) -> tuple[str, int]:
        if ip_address not in self.clients:
            raise UnknownClientError(ip_address=ip_address)

        self.clients.remove(ip_address)

        message = f"Connection between {ip_address} and server finished."

        log.info(message)
        log.info(f'Connected clients: {self.clients}')

        return message, 200

    def request_to_send(self, ip_address: tuple[str, int]) -> tuple[str, int]:
        if ip_address not in self.clients:
            raise UnknownClientError(ip_address=ip_address)

        self.authorized_clients.append(ip_address)

        message = f"Request from {ip_address} accepted. You can now send your file."

        log.info(message)
        log.info(f'Authorized clients: {self.clients}')

        return message, 200

    def receive_file(self, ip_address: tuple[str, int], message: str, message_info: str) -> tuple[str, int]:
        if ip_address not in self.authorized_clients:
            raise UnauthorizedClientError(ip_address=ip_address)

        filename, current_packet, total_packet = message_info[1:-1].split(';')

        output_file = f'./files/server_{filename[-8:][:-4]}.txt'
        log.info(f"Receiving file from {ip_address}")

        with open(output_file, "w") as file:
            file.write(message)
            file.close()

        return f'Received packet {current_packet}/{total_packet} from {ip_address}', 200

    @staticmethod
    def make_response_header(
            status_code: int,
            message: str,
            client_id: int = 0,
            message_id: int = 0,
            rcv_buffer_capacity: int = 0,
            client_ip_address: tuple = ()
    ):
        return f'{status_code}-{client_id}-{message_id}-{rcv_buffer_capacity}-{client_ip_address}-{checksum(message)}'

    def send_message(self, header: str | None, message: str, ip_address: tuple[str, int]):
        print(ip_address)
        self.udp_socket.sendto(str.encode(f'[{header}]: {message}'), ip_address)


if __name__ == '__main__':
    server = Server()

    server.run_server()
