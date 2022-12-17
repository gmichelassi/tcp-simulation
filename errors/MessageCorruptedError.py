from config import get_logger


log = get_logger(__file__)


class MessageCorruptedError(Exception):
    def __init__(self, ip_address: tuple[str, int], message: str):
        self.ip_address = ip_address
        self.message = message
        self.status_code = 500
        self.message = f'{self.status_code}: Command {self.message} from {self.ip_address} corrupted.'

        super().__init__()

    def __str__(self):
        log.warning(self.message)

        return self.message
