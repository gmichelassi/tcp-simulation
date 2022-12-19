from config import get_logger


log = get_logger(__file__)


class NoResponseError(Exception):
    def __init__(self):
        self.status_code = 500
        self.message = f'Server did not respond.'

        super().__init__()

    def __str__(self):
        log.error(self.message)

        return self.message
