class InvalidCommandError(Exception):
    def __init__(self, command: str):
        self.command = command
        self.status_code = 500

        super().__init__()

    def __str__(self):
        return f'{self.status_code}: Unknown command {self.command}.'
