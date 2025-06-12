from src.singleton import Singleton
from src.cypher import AESCypher

from typing import Any
import requests
import json

class HTTPService(Singleton):
    def initialize(self, url: str, key: bytes, nonce: str) -> None:
        self.__url = url
        self.__nonce = nonce
        self.__cypher = AESCypher(key)
        self.__session = requests.session()

    def send_request(self, request: dict[str, Any]) -> str:
        # Add nonce and encrypt the request
        request['nonce'] = self.__nonce
        jsonBody = json.dumps(request)
        encrypted_request = self.__cypher.encrypt(jsonBody)

        # Send the request
        response = self.__session.post(self.__url, json = {
            'body': encrypted_request['body'],
            'iv': encrypted_request['iv'],
        }).json()

        # Extract the nonce and body
        response = json.loads(
                self.__cypher.decrypt(response['body'].encode(), response['iv'].encode())
        )

        # Update the nonce
        self.__nonce = response.pop('nonce')

        return response
