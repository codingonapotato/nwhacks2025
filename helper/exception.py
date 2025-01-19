class RequestError(Exception):
    pass

class HTTPError(RequestError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ConnectionError(RequestError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class TimeoutError(RequestError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class RequestException(RequestError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
