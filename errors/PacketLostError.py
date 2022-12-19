from errors.BaseError import BaseError


class PacketLostError(BaseError):
    def __init__(self, ip_address: tuple[str, int]):
        self.ip_address = ip_address
        self.status_code = 500
        self.message = f'Packet lost.'

        super().__init__(
            ip_address=self.ip_address,
            status_code=self.status_code,
            message=self.message
        )
