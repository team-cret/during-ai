
class ServerManager:
    def __init__(self) -> None:
        self.start()
        pass

    def start(self):
        self.services = [
            'sentiment_analysis',
        ]