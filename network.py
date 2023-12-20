from server import server

class Network:
    def __init__(self) -> None:
        self.server = None

    def connect(self) -> dict:
        self.server = server
        return self.server.connect()

    def send_data(self, data) -> dict:
        response = server.recieve(data)
        return response
