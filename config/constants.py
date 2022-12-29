LOCALHOST = '127.0.0.1'
SERVER_PORT = 20000
ROUTER_PORT = 10000
BUFFER_SIZE = 1024
MAX_TRIES = 3

CONNECTION_REQUEST = 'connection_request'
CONNECTION_FINISHED = 'connection_finished'
REQUEST_TO_SEND = 'request_to_send'
SEND_FILE = 'send_file'
OVERLOAD = 'overload'

COMMANDS = [
    CONNECTION_FINISHED,
    CONNECTION_REQUEST,
    REQUEST_TO_SEND,
    SEND_FILE,
    OVERLOAD
]

FILE_1024 = './files/lorem_ipsum_1024.txt'
FILE_2048 = './files/lorem_ipsum_2048.txt'
FILE_4096 = './files/lorem_ipsum_4096.txt'

FILES = [
    {'name': FILE_1024, 'size': 1024},
    {'name': FILE_2048, 'size': 2048},
    {'name': FILE_4096, 'size': 4096},
]
