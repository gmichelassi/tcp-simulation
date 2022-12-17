from config import get_logger


log = get_logger(__file__)


class PacketLostError(Exception):
    def __init__(self, ip_address: tuple[str, int]):
        self.ip_address = ip_address
        self.status_code = 500
        self.message = f'{self.status_code}: Packet lost.'

        super().__init__()

    def __str__(self):
        log.error(self.message)

        return self.message
