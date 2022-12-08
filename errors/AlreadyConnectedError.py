class AlreadyConnectedError(Exception):
    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        self.status_code = 400

        super().__init__()

    def __str__(self):
        return f'{self.status_code}: Client {self.ip_address} already connected.'
