from errors.BaseError import BaseError


class UnknownClientError(BaseError):
    def __init__(self, ip_address: tuple[str, int]):
        self.ip_address = ip_address
        self.status_code = 401
        self.message = f'Unknown client {self.ip_address}.'

        super().__init__(
            ip_address=self.ip_address,
            status_code=self.status_code,
            message=self.message
        )
