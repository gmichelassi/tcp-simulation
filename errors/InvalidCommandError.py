from config import get_logger


log = get_logger(__file__)


class InvalidCommandError(Exception):
    def __init__(self, command: str):
        self.command = command
        self.status_code = 500
        self.message = f"{self.status_code}: Unknown command '{self.command}'."

        super().__init__()

    def __str__(self):
        log.error(self.message)

        return self.message
