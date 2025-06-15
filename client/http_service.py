from client.singleton import Singleton
from client.cypher import AESCypher

from typing import Any
import requests
import json

class HTTPService(Singleton):
    def initialize(self, url: str, key: bytes, nonce: str) -> None:
        self.__url = url
        self.__nonce = nonce
        self.__cypher = AESCypher(key)
        self.__session = requests.session()

    def send_request(self, request: dict[str, Any]) -> dict[str, str]:
        # Add nonce and encrypt the request
        request['nonce'] = self.__nonce
        jsonBody = json.dumps(request)
        encrypted_request = self.__cypher.encrypt(jsonBody)

        # Send the request
        response = self.__session.post(self.__url, json = {
            'body': encrypted_request['body'],
            'iv': encrypted_request['iv'],
        })

        # Process response
        return self.__process_response(response)

    def __process_response(self, response: requests.Response) -> dict[str, str]:
        # Create an empty response
        processed_response = {}

        # Check if the response contains a body
        if len(response.text) > 0:
            # Extract the nonce and body
            response_body = response.json()
            processed_response = json.loads(
                    self.__cypher.decrypt(response_body['body'].encode(), response_body['iv'].encode())
            )

            # Extract the nonce from the response and update its value
            self.__nonce = processed_response.pop('nonce')
        else:
            processed_response = { 'output': '' }

        return processed_response
