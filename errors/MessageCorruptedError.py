from errors.BaseError import BaseError


class MessageCorruptedError(BaseError):
    def __init__(self, ip_address: tuple[str, int], message: str):
        self.ip_address = ip_address
        self.message = message
        self.status_code = 500
        self.message = f'Command {self.message} from {self.ip_address} corrupted.'

        super().__init__(
            ip_address=self.ip_address,
            status_code=self.status_code,
            message=self.message
        )
