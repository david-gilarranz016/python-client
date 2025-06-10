from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import secrets

class AESCypher:
    # Class constants
    BLOCKSIZE = 16

    def __init__(self, key: bytes) -> None:
        self.__key = key

    def encrypt(self, plaintext: str) -> dict[str, str]:
        # Add padding to the plaintext
        padded_plaintext = self.__pad(plaintext).encode()

        # Generate a random initialization vector and create an AES cypher
        iv = secrets.token_bytes(16)
        cypher = AES.new(self.__key, AES.MODE_CBC, iv)

        # Encrypt the plaintext and return the base64 encoded string and iv
        cyphertext = cypher.encrypt(padded_plaintext)
        return {
            'body': b64encode(cyphertext).decode(),
            'iv': b64encode(iv).decode()
        }

    def decrypt(self, cyphertext: str, iv: str) -> str:
        # Decode the cyphertext and iv
        raw_cyphertext = b64decode(cyphertext)
        raw_iv = b64decode(iv)

        # Decrypt the message
        cypher = AES.new(self.__key, AES.MODE_CBC, raw_iv)
        plaintext = cypher.decrypt(raw_cyphertext)

        # Unpad and return the response
        return self.__unpad(plaintext).decode()

    def __pad(self, plaintext: str) -> str:
        # Adds PKCS#7 padding -> k - (l mod k) octects with value k - (l mod k)
        return plaintext + (16 - len(plaintext) % 16) * chr(16 - len(plaintext) % 16)

    def __unpad(self, plaintext: bytes) -> bytes:
        # Reverse the operation -> since the padding value is the number of added bytes,
        # slice the received plaintext up to the first padded byte
        return plaintext[:-ord(plaintext[len(plaintext) - 1:])]
