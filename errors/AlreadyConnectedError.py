from errors.BaseError import BaseError


class AlreadyConnectedError(BaseError):
    def __init__(self, ip_address: tuple[str, int]):
        self.ip_address = ip_address
        self.status_code = 400
        self.message = f'Client {self.ip_address} already connected.'

        super().__init__(
            ip_address=self.ip_address,
            status_code=self.status_code,
            message=self.message
        )
