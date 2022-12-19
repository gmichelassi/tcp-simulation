from errors.BaseError import BaseError


class InvalidCommandError(BaseError):
    def __init__(self, ip_address: tuple[str, int], command: str):
        self.ip_address = ip_address
        self.command = command
        self.status_code = 500
        self.message = f"Unknown command '{self.command}'."

        super().__init__(
            ip_address=self.ip_address,
            status_code=self.status_code,
            message=self.message
        )
