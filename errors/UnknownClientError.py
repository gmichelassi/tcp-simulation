class UnknownClientError(Exception):
    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        self.status_code = 401

        super().__init__()

    def __str__(self):
        return f'{self.status_code}: Unknown client {self.ip_address}.'
