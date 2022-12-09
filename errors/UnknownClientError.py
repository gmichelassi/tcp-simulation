from config import get_logger


log = get_logger(__file__)


class UnknownClientError(Exception):
    def __init__(self, ip_address: tuple[str, int]):
        self.ip_address = ip_address
        self.status_code = 401
        self.message = f'{self.status_code}: Unknown client {self.ip_address}.'

        super().__init__()

    def __str__(self):
        log.error(self.message)

        return self.message
