from config import get_logger


log = get_logger(__file__)


class BaseError(Exception):
    def __init__(self, ip_address: tuple[str, int], message: str, status_code: int):
        self.ip_address = ip_address
        self.status_code = status_code
        self.message = message

        super().__init__()

    def __str__(self):
        log.error(self.message)

        return self.message
