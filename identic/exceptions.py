class ArgumentError(Exception):
    """Raised to indicate invalid user input.
    """
    def __init__(self, message):
        self.message = message
