from config import get_logger


log = get_logger(__file__)


class AlreadyConnectedError(Exception):
    def __init__(self, ip_address: tuple[str, int]):
        self.ip_address = ip_address
        self.status_code = 400
        self.message = f'{self.status_code}: Client {self.ip_address} already connected.'

        super().__init__()

    def __str__(self):
        log.warning(self.message)

        return self.message
