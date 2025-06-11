from src.singleton import Singleton

class HTTPService(Singleton):
    def initialize(self, key: bytes, iv: bytes, nonce: str) -> None:
        pass
